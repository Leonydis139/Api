
import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [response, setResponse] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [intent, setIntent] = useState('test');
  const [userId, setUserId] = useState(1);
  const [cacheKeys, setCacheKeys] = useState('');
  const [requestedComponents, setRequestedComponents] = useState('');

  const apiKey = import.meta.env.VITE_QUANTUM_API_KEY;
  const apiUrl = import.meta.env.VITE_API_URL;

  const sendRequest = async () => {
    if (!apiKey || !apiUrl) {
      setError('Missing API key or API URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${apiUrl}/quantum`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          intent: intent.trim(),
          userId: parseInt(userId, 10),
          cacheKeys: cacheKeys.split(',').map(k => k.trim()).filter(Boolean),
          requestedComponents: requestedComponents.split(',').map(k => k.trim()).filter(Boolean),
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Request failed');
      }

      const data = await res.json();
      setResponse(data);
      loadHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    if (!apiKey || !apiUrl) return;

    try {
      const res = await fetch(`${apiUrl}/quantum/history`, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
        },
      });

      if (res.ok) {
        const data = await res.json();
        setHistory(data.history || []);
      }
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ color: '#0070f3' }}>⚛️ QuantumRequest Dashboard</h1>

      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Intent (e.g., refreshSession)"
          value={intent}
          onChange={(e) => setIntent(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <input
          type="number"
          placeholder="User ID (e.g., 1234)"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <input
          type="text"
          placeholder="Cache Keys (comma separated)"
          value={cacheKeys}
          onChange={(e) => setCacheKeys(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <input
          type="text"
          placeholder="Requested Components (comma separated)"
          value={requestedComponents}
          onChange={(e) => setRequestedComponents(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <button
          onClick={sendRequest}
          disabled={loading}
          style={{ padding: '10px 20px', backgroundColor: '#0070f3', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          {loading ? 'Sending...' : 'Send Quantum Request'}
        </button>
        {error && <p style={{ color: 'red', marginTop: '8px' }}>Error: {error}</p>}
      </div>

      {response && (
        <div style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', marginBottom: '1rem' }}>
          <h3>✅ Response</h3>
          <pre style={{ whiteSpace: 'pre-wrap', fontSize: '14px' }}>
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}

      <h2 style={{ marginTop: '2rem' }}>📜 History</h2>
      <ul>
        {history.map(item => (
          <li key={item.id}>
            <strong>{item.intent}</strong> (User: {item.user_id}) <em>{new Date(item.created_at).toLocaleString()}</em>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
