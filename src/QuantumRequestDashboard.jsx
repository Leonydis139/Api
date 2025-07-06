
import React, { useState } from 'react';

const QuantumRequestDashboard = () => { const [response, setResponse] = useState(null); const [intent, setIntent] = useState(''); const [userId, setUserId] = useState(''); const [cacheKeys, setCacheKeys] = useState(''); const [requestedComponents, setRequestedComponents] = useState(''); const [loading, setLoading] = useState(false); const [error, setError] = useState(null);

const handleSendRequest = async () => { const apiKey = import.meta.env.VITE_QUANTUM_API_KEY; const apiUrl = import.meta.env.VITE_API_URL;

if (!intent || !userId) {
  setError('Intent and User ID are required.');
  return;
}

setLoading(true);
setError(null);

try {
  const res = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      intent,
      userId: parseInt(userId, 10),
      cacheKeys: cacheKeys.split(',').map(k => k.trim()).filter(Boolean),
      requestedComponents: requestedComponents.split(',').map(k => k.trim()).filter(Boolean),
    }),
  });

  if (!res.ok) {
    const errData = await res.json();
    throw new Error(errData.detail || 'Request failed');
  }

  const data = await res.json();
  setResponse(data);
} catch (err) {
  setError(err.message);
  setResponse(null);
} finally {
  setLoading(false);
}

};

return ( <div className="p-6 font-sans max-w-2xl mx-auto"> <h1 className="text-2xl font-bold mb-4 text-blue-600">⚛️ QuantumRequest Dashboard</h1>

<div className="space-y-3 mb-4">
    <input
      className="w-full p-2 border rounded"
      type="text"
      placeholder="Intent (e.g., refreshSession)"
      value={intent}
      onChange={e => setIntent(e.target.value)}
    />
    <input
      className="w-full p-2 border rounded"
      type="number"
      placeholder="User ID (e.g., 1234)"
      value={userId}
      onChange={e => setUserId(e.target.value)}
    />
    <input
      className="w-full p-2 border rounded"
      type="text"
      placeholder="Cache Keys (comma separated)"
      value={cacheKeys}
      onChange={e => setCacheKeys(e.target.value)}
    />
    <input
      className="w-full p-2 border rounded"
      type="text"
      placeholder="Requested Components (comma separated)"
      value={requestedComponents}
      onChange={e => setRequestedComponents(e.target.value)}
    />

    <button
      onClick={handleSendRequest}
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      disabled={loading}
    >
      {loading ? 'Sending...' : 'Send Quantum Request'}
    </button>

    {error && <p className="text-red-500">Error: {error}</p>}
  </div>

  {response && (
    <div className="bg-gray-100 p-4 rounded shadow">
      <h2 className="font-semibold mb-2">Response:</h2>
      <pre className="text-sm whitespace-pre-wrap">
        {JSON.stringify(response, null, 2)}
      </pre>
    </div>
  )}
</div>

); };

export default QuantumRequestDashboard;

