import React, { useState } from 'react';

const QuantumRequestDashboard = () => {
  const [response, setResponse] = useState(null);
  const [intent, setIntent] = useState('');
  const [userId, setUserId] = useState('');
  const [cacheKeys, setCacheKeys] = useState('');
  const [requestedComponents, setRequestedComponents] = useState('');

  const handleSendRequest = async () => {
    const apiKey = import.meta.env.VITE_QUANTUM_API_KEY;
    const apiUrl = import.meta.env.VITE_API_URL;

    try {
      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          intent,
          userId: parseInt(userId, 10),
          cacheKeys: cacheKeys
            .split(',')
            .map(k => k.trim())
            .filter(k => k),
          requestedComponents: requestedComponents
            .split(',')
            .map(k => k.trim())
            .filter(k => k)
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Request failed');
      }

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Request failed:', error);
      setResponse({ error: error.message });
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>⚛️ QuantumRequest Dashboard</h1>

      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Intent"
          value={intent}
          onChange={e => setIntent(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <input
          type="number"
          placeholder="User ID"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <input
          type="text"
          placeholder="Cache Keys (comma separated)"
          value={cacheKeys}
          onChange={e => setCacheKeys(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <input
          type="text"
          placeholder="Requested Components (comma separated)"
          value={requestedComponents}
          onChange={e => setRequestedComponents(e.target.value)}
          style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
        />
        <button
          onClick={handleSendRequest}
          style={{
            padding: '10px 20px',
            backgroundColor: '#2563eb',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Send Quantum Request
        </button>
      </div>

      {response && (
        <pre
          style={{
            background: '#f4f4f4',
            padding: '1rem',
            borderRadius: '4px',
            whiteSpace: 'pre-wrap'
          }}
        >
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default QuantumRequestDashboard;
