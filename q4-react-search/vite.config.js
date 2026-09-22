import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Mock user database for local development demonstration
const MOCK_USERS = [
  { id: 1, name: 'Sneha Bhatia',    email: 'sneha@example.com' },
  { id: 2, name: 'Rahul Sharma',    email: 'rahul@example.com' },
  { id: 3, name: 'Priya Mehta',     email: 'priya@example.com' },
  { id: 4, name: 'Amit Patel',      email: 'amit@example.com' },
  { id: 5, name: 'Neha Gupta',      email: 'neha@example.com' },
  { id: 6, name: 'Rohan Verma',     email: 'rohan@example.com' },
  { id: 7, name: 'Ananya Singh',    email: 'ananya@example.com' },
  { id: 8, name: 'Vikram Kumar',    email: 'vikram@example.com' },
  { id: 9, name: 'Pooja Joshi',     email: 'pooja@example.com' },
  { id: 10, name: 'Karan Malhotra', email: 'karan@example.com' },
];

export default defineConfig({
  plugins: [
    react(),
    {
      // Mock API middleware — intercepts GET /api/users?search=<query>
      name: 'mock-api',
      configureServer(server) {
        server.middlewares.use('/api/users', (req, res) => {
          const url = new URL(req.url, 'http://localhost');
          const query = (url.searchParams.get('search') || '').toLowerCase().trim();

          const results = query
            ? MOCK_USERS.filter(
                (u) =>
                  u.name.toLowerCase().includes(query) ||
                  u.email.toLowerCase().includes(query)
              )
            : [];

          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify(results));
        });
      },
    },
  ],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
  },
});
