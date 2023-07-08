import React from 'react';
import ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client'; // Updated import statement

import App from './App';

createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
