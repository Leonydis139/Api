import React, { useState } from "react";

const QuantumRequestClient = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const sendQuantumRequest = async () => {
    setLoading(true);
    setError("");

    const requestBody = {
      intent: "loadUserDashboard",
      userId: 123,
      cacheKeys: [],
      requestedComponents: ["profile","permissions","notifications","settings","activity"]
    };

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/quantum`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": import.meta.env.VITE_QUANTUM_API_KEY
          },
          body: JSON.stringify(requestBody),
        }
      );
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      setData(await res.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 font-sans max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-4">QuantumRequest v2 Dashboard</h1>
      <button
        onClick={sendQuantumRequest}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        {loading ? "Loading..." : "Send Quantum Request"}
      </button>

      {error && <p className="mt-4 text-red-500">Error: {error}</p>}

      {data && (
        <div className="mt-6 space-y-4">
          <h2 className="text-xl">Components</h2>
          <pre className="bg-gray-100 p-4 rounded">{JSON.stringify(data.components, null, 2)}</pre>

          <h2 className="text-xl">Micro-Functions</h2>
          <pre className="bg-gray-100 p-4 rounded">{JSON.stringify(data.microFunctions, null, 2)}</pre>

          <h2 className="text-xl">Next Intents</h2>
          <ul className="list-disc pl-5">
            {data.nextIntents.map((i) => <li key={i}>{i}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
};

export default QuantumRequestClient;
