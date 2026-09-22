import { useState } from 'react';
import UserList from './components/UserList';

const INITIAL_USERS = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Charlie' },
];

export default function App() {
  const [users, setUsers] = useState(INITIAL_USERS);
  const [selectedUser, setSelectedUser] = useState(null);

  const removeUser = (id) => {
    setUsers((prev) => prev.filter((u) => u.id !== id));
  };

  const removeSelected = () => {
    if (selectedUser) {
      removeUser(selectedUser.id);
    }
  };

  return (
    <div style={{ maxWidth: '420px', margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>User Directory</h2>
      <UserList users={users} onSelect={setSelectedUser} />

      <div style={{ marginTop: '1.5rem', borderTop: '1px solid #ddd', paddingTop: '1rem' }}>
        <h4 style={{ margin: '0 0 0.75rem 0' }}>Simulate Parent Actions:</h4>

        {/* Dynamic button to remove whichever user is currently selected */}
        {selectedUser ? (
          <div style={{ marginBottom: '10px' }}>
            <button
              type="button"
              onClick={removeSelected}
              style={{
                backgroundColor: '#dc2626',
                color: 'white',
                border: 'none',
                padding: '8px 14px',
                borderRadius: '4px',
                cursor: 'pointer',
                fontWeight: 'bold',
                width: '100%',
                marginBottom: '8px',
              }}
            >
              ✕ Remove Selected: {selectedUser.name} (ID {selectedUser.id})
            </button>
          </div>
        ) : (
          <p style={{ fontSize: '0.85rem', color: '#666', marginBottom: '8px' }}>
            (Click any user above to enable removing them)
          </p>
        )}

        {/* Remove buttons for each user currently present in the list */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
          {users.map((u) => (
            <button
              key={u.id}
              type="button"
              onClick={() => removeUser(u.id)}
              style={{
                padding: '4px 10px',
                border: '1px solid #ccc',
                backgroundColor: '#f9fafb',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '0.85rem',
              }}
            >
              Remove {u.name} (ID {u.id})
            </button>
          ))}
        </div>

        <div>
          <button
            type="button"
            onClick={() => setUsers(INITIAL_USERS)}
            style={{
              padding: '6px 14px',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Reset Users
          </button>
        </div>
      </div>
    </div>
  );
}
