import { verifyCredentials } from "./verify-credentials.mjs";

console.log("--- the same three checks, as a Promise chain ---");
verifyCredentials("alice")
  .then((result) => {
    console.log("Verified:", result.username);
    return verifyCredentials("bob");
  })
  .then((result) => {
    console.log("Verified:", result.username);
    return verifyCredentials("dave");
  })
  .then((result) => {
    console.log("Verified:", result.username);
  })
  .catch((err) => {
    console.log("Error:", err.message);
  })
  .then(() => {
    // Runs after either the success chain or the .catch above - a good
    // place for cleanup that must happen either way.
    console.log("");
    console.log("--- Promise.all: same three checks, running concurrently ---");
    return Promise.all([
      verifyCredentials("alice"),
      verifyCredentials("bob"),
      verifyCredentials("carol"),
    ]);
  })
  .then((results) => {
    console.log(results.map((r) => r.username));
  });
