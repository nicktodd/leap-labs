// KATA: run this now, before changing anything:
//   node report.cjs
// It throws at TODO 1 (inside count-utils.cjs). That's the starting
// point.

const { countByOutcome } = require("./count-utils.cjs");

const attempts = [
  { username: "dave", outcome: "success" },
  { username: "erin", outcome: "fail" },
  { username: "dave", outcome: "fail" },
  { username: "frank", outcome: "success" },
];

const { successCount, failCount } = countByOutcome(attempts);
console.log(`${successCount} successful, ${failCount} failed`);

// TODO 2: before running this section, PREDICT the print order on paper
// (or out loud) - synchronous lines, then process.nextTick, then
// Promise.then, then setTimeout. Then uncomment and run it for real to
// check your prediction.

console.log("sync A");
setTimeout(() => console.log("setTimeout"), 0);
Promise.resolve().then(() => console.log("promise.then"));
process.nextTick(() => console.log("nextTick"));
console.log("sync B");
