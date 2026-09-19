const { countByOutcome } = require("./count-utils.cjs");

const attempts = [
  { username: "dave", outcome: "success" },
  { username: "erin", outcome: "fail" },
  { username: "dave", outcome: "fail" },
  { username: "frank", outcome: "success" },
];

const { successCount, failCount } = countByOutcome(attempts);
console.log(`${successCount} successful, ${failCount} failed`);

console.log("sync A");
setTimeout(() => console.log("setTimeout"), 0);
Promise.resolve().then(() => console.log("promise.then"));
process.nextTick(() => console.log("nextTick"));
console.log("sync B");
