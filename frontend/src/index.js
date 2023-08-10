import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  BrowserRouter as Router,
  Routes, Route
} from "react-router-dom";
import { StoreProvider } from 'easy-peasy';

import store from './store/store';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';
import App from './App';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <StoreProvider store={store}>
      <Router>
        <Routes>
          <Route path='/*' element={<App />} />
        </Routes>
      </Router>
    </StoreProvider>
  </React.StrictMode>
);

