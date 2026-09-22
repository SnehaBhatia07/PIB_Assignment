import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import UserSearch from './UserSearch';

describe('UserSearch Component', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it('1. renders the search input with label', () => {
    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);
    expect(input).toBeInTheDocument();
    expect(input).toHaveValue('');
  });

  it('2. updates input value on typing', () => {
    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);
    fireEvent.change(input, { target: { value: 'Alice' } });
    expect(input).toHaveValue('Alice');
  });

  it('3. does not call API immediately upon keystroke', () => {
    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'A' } });
    fireEvent.change(input, { target: { value: 'Al' } });
    fireEvent.change(input, { target: { value: 'Ali' } });

    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('4. calls API after debounce period of 300ms', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [{ id: 1, name: 'Alice', email: 'alice@example.com' }],
    });

    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'Alice' } });
    expect(global.fetch).not.toHaveBeenCalled();

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith(
      '/api/users?search=Alice',
      expect.objectContaining({ signal: expect.any(AbortSignal) })
    );
  });

  it('5. properly encodes special characters in search query', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'John & Jane Doe+Smith' } });

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(global.fetch).toHaveBeenCalledWith(
      `/api/users?search=${encodeURIComponent('John & Jane Doe+Smith')}`,
      expect.any(Object)
    );
  });

  it('6. displays loading state while request is in flight', async () => {
    let resolvePromise;
    global.fetch.mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          resolvePromise = resolve;
        })
    );

    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'Bob' } });

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(screen.getByText('Searching...')).toBeInTheDocument();

    await act(async () => {
      resolvePromise({
        ok: true,
        json: async () => [{ id: 2, name: 'Bob', email: 'bob@example.com' }],
      });
    });

    expect(screen.queryByText('Searching...')).not.toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
  });

  it('7. displays returned users on successful fetch', async () => {
    const mockUsers = [
      { id: 1, name: 'Alice Johnson', email: 'alice@example.com' },
      { id: 2, name: 'Bob Smith', email: 'bob@example.com' },
    ];
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers,
    });

    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'Johnson' } });

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(screen.getByText('Alice Johnson')).toBeInTheDocument();
    expect(screen.getByText('(alice@example.com)')).toBeInTheDocument();
    expect(screen.getByText('Bob Smith')).toBeInTheDocument();
  });

  it('8. shows "No users found." when API returns empty array', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'NonExistent' } });

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(screen.getByText('No users found.')).toBeInTheDocument();
  });

  it('9. shows error message when API responds with non-2xx status', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'ErrorQuery' } });

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(
      screen.getByText('Something went wrong. Please try again.')
    ).toBeInTheDocument();
    expect(screen.queryByText('Searching...')).not.toBeInTheDocument();
  });

  it('10. aborts previous outdated request when newer search starts', async () => {
    let firstAbortSignal;
    global.fetch.mockImplementationOnce((url, options) => {
      firstAbortSignal = options.signal;
      return new Promise(() => {}); // never resolves
    });

    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    // First search
    fireEvent.change(input, { target: { value: 'First' } });
    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(firstAbortSignal).toBeDefined();
    expect(firstAbortSignal.aborted).toBe(false);

    // Second search triggers cleanup of previous request
    fireEvent.change(input, { target: { value: 'Second' } });
    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(firstAbortSignal.aborted).toBe(true);
  });

  it('11. clearing or whitespace-only search does not call API and resets state', async () => {
    render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: '   ' } });

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(global.fetch).not.toHaveBeenCalled();
    expect(screen.queryByText('Searching...')).not.toBeInTheDocument();
    expect(screen.queryByText('No users found.')).not.toBeInTheDocument();
  });

  it('12. aborts active request when component unmounts', async () => {
    let capturedSignal;
    global.fetch.mockImplementationOnce((url, options) => {
      capturedSignal = options.signal;
      return new Promise(() => {});
    });

    const { unmount } = render(<UserSearch />);
    const input = screen.getByLabelText(/search:/i);

    fireEvent.change(input, { target: { value: 'UnmountTest' } });
    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(capturedSignal.aborted).toBe(false);

    unmount();

    expect(capturedSignal.aborted).toBe(true);
  });
});
