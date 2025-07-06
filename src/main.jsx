import React from 'react';
import ReactDOM from 'react-dom/client';
import { sendQuantumRequest } from './QuantumRequestClient';

const App = () => {
  const handleClick = async () => {
    try {
      const result = await sendQuantumRequest();
      alert(JSON.stringify(result, null, 2));
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>QuantumRequest Client</h1>
      <button onClick={handleClick}>Send Quantum Request</button>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
