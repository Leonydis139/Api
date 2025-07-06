/**
 * Sends a QuantumRequest to the backend API.
 *
 * @param {Object} options - Request options.
 * @param {string} options.intent - The intent of the request (required).
 * @param {number} options.userId - The user ID associated with the request (required).
 * @param {Array<string>} [options.cacheKeys=[]] - Optional cache keys.
 * @param {Array<string>} [options.requestedComponents=[]] - Optional requested components.
 * @returns {Promise<Object>} - The response data from the server.
 * @throws {Error} - If request fails or required env variables are missing.
 */
export async function sendQuantumRequest({
  intent,
  userId,
  cacheKeys = [],
  requestedComponents = [],
}) {
  const apiUrl = import.meta.env.VITE_API_BASE_URL;
  const apiKey = import.meta.env.VITE_QUANTUM_API_KEY;

  if (!apiUrl || !apiKey) {
    throw new Error("❗ Missing API URL or API Key in environment variables.");
  }

  if (!intent || !userId) {
    throw new Error("❗ 'intent' and 'userId' are required parameters.");
  }

  try {
    const response = await fetch(`${apiUrl}/quantum`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        intent,
        userId,
        cacheKeys,
        requestedComponents,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const message = errorData.detail || response.statusText || "Request failed.";
      throw new Error(`❗ Error ${response.status}: ${message}`);
    }

    const data = await response.json();
    console.log("✅ QuantumRequest response:", data);
    return data;
  } catch (error) {
    console.error("❌ QuantumRequest failed:", error);
    throw error;
  }
}
