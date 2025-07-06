
import { useState } from 'react';
import './App.css';

function App() {
  const [response, setResponse] = useState(null);
  const [history, setHistory] = useState([]);

  const sendRequest = async () => {
    const res = await fetch('/quantum', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY_HERE'
      },
      body: JSON.stringify({
        intent: 'test',
        userId: 1,
        cacheKeys: [],
        requestedComponents: []
      })
    });
    const data = await res.json();
    setResponse(data);
    loadHistory();
  };

  const loadHistory = async () => {
    const res = await fetch('/quantum/history', {
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY_HERE'
      }
    });
    const data = await res.json();
    setHistory(data.history);
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>QuantumRequest Dashboard 🚀</h1>
      <button onClick={sendRequest}>Send Quantum Request</button>
      {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
      <h2>History</h2>
      <ul>
        {history.map(item => (
          <li key={item.id}>{item.intent} (User: {item.user_id}) at {item.created_at}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
