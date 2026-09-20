const KNOWN_USERS = ["dave", "erin", "frank"];

export function verifyCredentials(username) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (KNOWN_USERS.includes(username)) {
        resolve({ username, verified: true });
      } else {
        reject(new Error(`Unknown user: ${username}`));
      }
    }, 20);
  });
}
