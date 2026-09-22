import { useState, useEffect, useRef } from 'react';

export default function UserList({ users = [], onSelect }) {
  const [selectedUserId, setSelectedUserId] = useState(null);

  // Derived state: find the selected user from the current users array.
  // This automatically keeps the selected user fresh and resets to null
  // if the selected user is deleted from the users list, avoiding stale state.
  const selectedUser = users?.find((user) => user.id === selectedUserId) || null;

  const onSelectRef = useRef(onSelect);
  useEffect(() => {
    onSelectRef.current = onSelect;
  });

  // Corrected effect: include dependency array [selectedUser] so logging only
  // executes when the selected user actually changes, avoiding running on every render.
  useEffect(() => {
    console.log('Selected:', selectedUser);
    onSelectRef.current?.(selectedUser);
  }, [selectedUser]);

  const handleSelectUser = (id) => {
    setSelectedUserId(id);
  };

  const handleClear = () => {
    setSelectedUserId(null);
  };

  if (!users || users.length === 0) {
    return (
      <div>
        <p>No users available.</p>
        <button type="button" onClick={handleClear} disabled={selectedUserId === null}>
          Clear
        </button>
      </div>
    );
  }

  return (
    <div>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {users.map((user) => {
          const isSelected = selectedUser?.id === user.id;
          return (
            <li key={user.id} style={{ margin: '4px 0' }}>
              <button
                type="button"
                onClick={() => handleSelectUser(user.id)}
                aria-pressed={isSelected}
                style={{
                  fontWeight: isSelected ? 'bold' : 'normal',
                  backgroundColor: isSelected ? '#e0f2fe' : 'transparent',
                  border: '1px solid #ccc',
                  padding: '6px 12px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  width: '100%',
                  textAlign: 'left',
                }}
              >
                {user.name}
              </button>
            </li>
          );
        })}
      </ul>

      <div style={{ marginTop: '12px' }}>
        <button type="button" onClick={handleClear} disabled={selectedUserId === null}>
          Clear
        </button>
      </div>

      {selectedUser && (
        <p style={{ marginTop: '8px', color: '#0369a1' }}>
          Selected: <strong>{selectedUser.name}</strong>
        </p>
      )}
    </div>
  );
}
