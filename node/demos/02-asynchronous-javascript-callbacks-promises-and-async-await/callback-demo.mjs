import { verifyCredentialsCallback } from "./verify-credentials.mjs";

console.log("--- a single callback ---");
console.log("Checking alice...");
verifyCredentialsCallback("alice", (err, result) => {
  if (err) {
    console.log("Error:", err.message);
    return;
  }
  console.log("Verified:", result.username);
});
console.log("This line runs BEFORE the callback above - verifyCredentialsCallback returns immediately");

// Give the first block's setTimeout a moment to fire before starting the
// next one, purely so the two demo sections don't interleave in the
// console. Not something you'd do in real code.
setTimeout(() => {
  console.log("");
  console.log("--- callback hell: three checks, nested ---");
  verifyCredentialsCallback("alice", (err1, result1) => {
    if (err1) {
      console.log("Error:", err1.message);
      return;
    }
    console.log("Verified:", result1.username);
    verifyCredentialsCallback("bob", (err2, result2) => {
      if (err2) {
        console.log("Error:", err2.message);
        return;
      }
      console.log("Verified:", result2.username);
      verifyCredentialsCallback("dave", (err3, result3) => {
        if (err3) {
          console.log("Error:", err3.message);
          return;
        }
        console.log("Verified:", result3.username);
      });
    });
  });
}, 100);
