import React from 'react';
import ReactDOM from 'react-dom/client';
import AppRouter from './Router'; // Import the router component

const container = document.getElementById('root');
if (!container) {
  throw new Error('No root element found');
}
const root = ReactDOM.createRoot(container);

root.render(
  <React.StrictMode>
    <AppRouter />
  </React.StrictMode>
);