// The classic demo of Node's execution order - sync code, then
// microtasks (process.nextTick, then Promise callbacks), then
// macrotasks (setTimeout), even though everything below is scheduled
// before any of the code below it has run.
//
// .cjs (CommonJS) rather than .mjs deliberately - see the demo guide for
// why the same code in an ES module prints a different, genuinely
// surprising order.

console.log("1: synchronous - runs immediately");

setTimeout(() => {
  console.log("5: setTimeout callback - a MACROTASK");
}, 0);

Promise.resolve().then(() => {
  console.log("4: Promise.then callback - a MICROTASK");
});

process.nextTick(() => {
  console.log("3: process.nextTick callback - Node's OWN microtask queue, drained before Promise's");
});

console.log("2: synchronous - runs immediately, straight after line 1");
