export async function sendQuantumRequest() {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/quantum`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${import.meta.env.VITE_QUANTUM_API_KEY}`,
    },
    body: JSON.stringify({
      intent: "getUserData",
      userId: 123,
      cacheKeys: [],
      requestedComponents: ["profile", "permissions", "notifications"],
    }),
  });

  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();
  console.log(data);
  return data;
}
