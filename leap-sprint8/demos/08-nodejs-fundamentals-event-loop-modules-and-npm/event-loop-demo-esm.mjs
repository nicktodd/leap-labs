// Identical code to event-loop-demo.cjs, as an ES module instead. Run
// both and compare - the order is DIFFERENT, and it's worth stopping on:
// see the demo guide for why.

console.log("1: synchronous - runs immediately");

setTimeout(() => {
  console.log("5: setTimeout callback - a MACROTASK");
}, 0);

Promise.resolve().then(() => {
  console.log("4 (was 3 in the .cjs run): Promise.then callback");
});

process.nextTick(() => {
  console.log("3 (was 4 in the .cjs run): process.nextTick callback");
});

console.log("2: synchronous - runs immediately, straight after line 1");
