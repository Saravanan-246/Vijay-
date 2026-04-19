const API_URL = import.meta.env.VITE_API_URL;

export const runCode = async ({ code, input = "" }) => {
  const res = await fetch(`${API_URL}/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code,
      input, // ✅ MUST BE HERE
    }),
  });

  if (!res.ok) {
    throw new Error("API request failed");
  }

  return res.json();
};