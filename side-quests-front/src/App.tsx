import React from 'react';
import AppRouter from './Router';
import './index.css';

require('dotenv').config();

const App: React.FC = () => {
    return <AppRouter />;
};

export default App;