const BASE_URL = "https://uninterpretively-unsharpening-kittie.ngrok-free.dev";


/**
 * SERVICE: Upload & Encrypt
 * Handles sending the payload file and the audio key to the backend.
 */
export const uploadFile = async (file, audio) => {
  const form = new FormData();
  form.append("file", file);
  form.append("audio", audio);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: form,
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Upload failed");
  return data;
};

/**
 * SERVICE: Download & Decrypt
 * Handles sending the room code and audio key to retrieve the decrypted file.
 */
export const downloadFile = async (roomCode, audio) => {
  const form = new FormData();
  form.append("room_code", roomCode.trim().toUpperCase());
  form.append("audio", audio);

  const res = await fetch(`${BASE_URL}/download`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.error || "Download failed");
  }

  // Return the response directly to handle the Blob in the component
  return res;
};

/**
 * SERVICE: Room Check
 * Bonus utility to verify if a room exists before attempting download.
 */
export const checkRoom = async (roomCode) => {
  const res = await fetch(`${BASE_URL}/check-room?room=${roomCode.trim().toUpperCase()}`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Room not found");
  return data;
};