import { useState, useEffect } from 'react';
import { useDebounce } from '../hooks/useDebounce';

const DEBOUNCE_DELAY_MS = 300;

export default function UserSearch() {
  const [search, setSearch] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const debouncedSearch = useDebounce(search, DEBOUNCE_DELAY_MS);

  useEffect(() => {
    const query = debouncedSearch.trim();

    if (!query) {
      setUsers([]);
      setError(null);
      setLoading(false);
      return;
    }

    const controller = new AbortController();

    async function fetchUsers() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/users?search=${encodeURIComponent(query)}`,
          { signal: controller.signal }
        );

        if (!response.ok) {
          throw new Error('Something went wrong. Please try again.');
        }

        const data = await response.json();
        setUsers(data);
        setLoading(false);
      } catch (err) {
        if (err.name === 'AbortError') {
          return;
        }
        setError(err.message || 'Something went wrong. Please try again.');
        setLoading(false);
      }
    }

    fetchUsers();

    return () => {
      controller.abort();
    };
  }, [debouncedSearch]);

  const trimmedQuery = debouncedSearch.trim();

  return (
    <div style={{ maxWidth: '480px', margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>User Search</h2>
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="user-search-input">Search: </label>
        <input
          id="user-search-input"
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by name..."
          style={{ padding: '0.4rem', width: '250px' }}
        />
      </div>

      {loading && <p>Searching...</p>}

      {!loading && error && (
        <p role="alert" style={{ color: 'red' }}>
          {error}
        </p>
      )}

      {!loading && !error && trimmedQuery && users.length === 0 && (
        <p>No users found.</p>
      )}

      {!loading && !error && users.length > 0 && (
        <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
          {users.map((user) => (
            <li
              key={user.id}
              style={{
                padding: '0.5rem 0',
                borderBottom: '1px solid #eee',
              }}
            >
              <strong>{user.name}</strong>{' '}
              {user.email && <span style={{ color: '#666' }}>({user.email})</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
