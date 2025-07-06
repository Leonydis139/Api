
import React, { useState } from 'react';

const QuantumRequestDashboard = () => { const [response, setResponse] = useState(null); const [intent, setIntent] = useState(''); const [userId, setUserId] = useState(''); const [cacheKeys, setCacheKeys] = useState(''); const [requestedComponents, setRequestedComponents] = useState(''); const [loading, setLoading] = useState(false); const [error, setError] = useState(null); const [success, setSuccess] = useState(false);

const apiKey = import.meta.env.VITE_QUANTUM_API_KEY || ''; const apiUrl = import.meta.env.VITE_API_URL || '';

const handleSendRequest = async () => { if (!apiKey || !apiUrl) { setError('API Key or API URL is missing in environment variables.'); return; }

if (!intent.trim() || !userId.trim()) {
  setError('Please provide both Intent and User ID.');
  return;
}

setLoading(true);
setError(null);
setSuccess(false);

try {
  const payload = {
    intent: intent.trim(),
    userId: parseInt(userId, 10),
    cacheKeys: cacheKeys ? cacheKeys.split(',').map(k => k.trim()).filter(Boolean) : [],
    requestedComponents: requestedComponents ? requestedComponents.split(',').map(k => k.trim()).filter(Boolean) : [],
  };

  const res = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || `Request failed with status ${res.status}`);
  }

  const result = await res.json();
  setResponse(result);
  setSuccess(true);
} catch (err) {
  setError(err.message || 'Unexpected error occurred.');
  setResponse(null);
} finally {
  setLoading(false);
}

};

return ( <div className="p-6 font-sans max-w-2xl mx-auto"> <h1 className="text-3xl font-bold mb-4 text-blue-700">⚛️ QuantumRequest Dashboard</h1>

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
      className={`px-4 py-2 rounded text-white ${loading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'}`}
      disabled={loading}
    >
      {loading ? 'Sending...' : 'Send Quantum Request'}
    </button>

    {error && <p className="text-red-600">❌ {error}</p>}
    {success && <p className="text-green-600">✅ Request sent successfully!</p>}
  </div>

  {response && (
    <div className="bg-gray-100 p-4 rounded shadow">
      <h2 className="font-semibold mb-2 text-gray-800">Response:</h2>
      <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(response, null, 2)}</pre>
    </div>
  )}
</div>

); };

export default QuantumRequestDashboard;

