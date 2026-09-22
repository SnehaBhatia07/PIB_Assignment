import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import UserList from './UserList';

describe('UserList Component', () => {
  const mockUsers = [
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' },
    { id: 3, name: 'Charlie' },
  ];

  let consoleSpy;

  beforeEach(() => {
    consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleSpy.mockRestore();
  });

  it('1. renders the list of users correctly', () => {
    render(<UserList users={mockUsers} />);

    expect(screen.getByRole('button', { name: 'Alice' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Bob' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Charlie' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Clear' })).toBeInTheDocument();
  });

  it('2. handles undefined or empty users prop gracefully', () => {
    const { rerender } = render(<UserList />);
    expect(screen.getByText('No users available.')).toBeInTheDocument();

    rerender(<UserList users={[]} />);
    expect(screen.getByText('No users available.')).toBeInTheDocument();
  });

  it('3. clicking a user updates the selected user', () => {
    render(<UserList users={mockUsers} />);

    const aliceBtn = screen.getByRole('button', { name: 'Alice' });
    fireEvent.click(aliceBtn);

    expect(aliceBtn).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: 'Bob' })).toHaveAttribute('aria-pressed', 'false');
  });

  it('4. displays selected user information and logs only on selection change', () => {
    const { rerender } = render(<UserList users={mockUsers} />);

    // Initially no user is selected
    expect(consoleSpy).toHaveBeenCalledWith('Selected:', null);
    consoleSpy.mockClear();

    // Select Alice
    fireEvent.click(screen.getByRole('button', { name: 'Alice' }));
    expect(screen.getByText(/Selected:/)).toHaveTextContent('Selected: Alice');
    expect(consoleSpy).toHaveBeenCalledWith('Selected:', { id: 1, name: 'Alice' });
    consoleSpy.mockClear();

    // Rerender with same props and state: effect should NOT fire again because dependency hasn't changed
    rerender(<UserList users={mockUsers} />);
    expect(consoleSpy).not.toHaveBeenCalled();
  });

  it('5. changing users data updates selected user without stale state', () => {
    const { rerender } = render(<UserList users={mockUsers} />);

    fireEvent.click(screen.getByRole('button', { name: 'Alice' }));
    expect(screen.getByText(/Selected:/)).toHaveTextContent('Selected: Alice');

    // Parent updates users list: Alice's name is updated to "Alice Smith"
    const updatedUsers = [
      { id: 1, name: 'Alice Smith' },
      { id: 2, name: 'Bob' },
      { id: 3, name: 'Charlie' },
    ];
    rerender(<UserList users={updatedUsers} />);

    // Selected user immediately reflects the updated name without stale closure/state
    expect(screen.getByText(/Selected:/)).toHaveTextContent('Selected: Alice Smith');
  });

  it('6. removing the selected user from users array resets selection cleanly', () => {
    const { rerender } = render(<UserList users={mockUsers} />);

    // Select Alice (ID 1)
    fireEvent.click(screen.getByRole('button', { name: 'Alice' }));
    expect(screen.getByText(/Selected:/)).toHaveTextContent('Selected: Alice');

    // Alice is deleted from the users array
    const usersWithoutAlice = [
      { id: 2, name: 'Bob' },
      { id: 3, name: 'Charlie' },
    ];
    rerender(<UserList users={usersWithoutAlice} />);

    // Selected user cleanly resets to null because derived state cannot find ID 1
    expect(screen.queryByText(/Selected: Alice/)).not.toBeInTheDocument();
    expect(consoleSpy).toHaveBeenLastCalledWith('Selected:', null);
  });

  it('7. clicking Clear button resets selection', () => {
    render(<UserList users={mockUsers} />);

    fireEvent.click(screen.getByRole('button', { name: 'Bob' }));
    expect(screen.getByText(/Selected:/)).toHaveTextContent('Selected: Bob');

    const clearBtn = screen.getByRole('button', { name: 'Clear' });
    fireEvent.click(clearBtn);

    expect(screen.queryByText(/Selected: Bob/)).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Bob' })).toHaveAttribute('aria-pressed', 'false');
  });

  it('8. does not trigger infinite render loop or memory leak', () => {
    // Render and click multiple users in succession
    render(<UserList users={mockUsers} />);

    fireEvent.click(screen.getByRole('button', { name: 'Alice' }));
    fireEvent.click(screen.getByRole('button', { name: 'Bob' }));
    fireEvent.click(screen.getByRole('button', { name: 'Charlie' }));
    fireEvent.click(screen.getByRole('button', { name: 'Clear' }));

    // Verify component rendered and stabilized cleanly
    expect(consoleSpy).toHaveBeenCalledTimes(5); // Initial (null) + Alice + Bob + Charlie + Clear (null)
  });
});
