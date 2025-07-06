import React, { useState } from 'react';

const QuantumRequestClient = () => {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendQuantumRequest = async () => {
    setLoading(true);

    const requestBody = {
      intent: 'loadDashboard',
      userId: 1,
      cacheKeys: [],
      requestedComponents: ['profile', 'permissions', 'notifications']
    };

    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/quantum`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Quantum request failed:', error);
      setResponse({ error: 'Request failed. Check console.' });
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>QuantumRequest Client</h1>
      <button onClick={sendQuantumRequest} disabled={loading} style={{ padding: '10px 20px', fontSize: '16px' }}>
        {loading ? 'Loading...' : 'Send Quantum Request'}
      </button>

      {response && (
        <pre style={{ marginTop: '2rem', backgroundColor: '#f0f0f0', padding: '1rem', borderRadius: '8px' }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default QuantumRequestClient;
