// A second, small demo file - just for SCOPE, run separately from
// login-attempts.js so each concept gets its own clear, real example.

// BLOCK SCOPE: `let` and `const` only exist inside the { } block they were
// declared in.
if (true) {
  let insideBlock = "only exists in here";
  console.log("Inside the block:", insideBlock);
}
try {
  console.log(insideBlock);
} catch (e) {
  console.log("Outside the block:", e.message);
}

console.log("");

// `var` IGNORES block scope - it "leaks" out to the nearest FUNCTION (or,
// at the top level, the whole file). This is the actual, concrete reason
// var causes real bugs: a variable you thought was local to an if-block
// or a loop is still there afterwards, and can silently collide with
// something else that reuses the same name.
if (true) {
  var leaksOut = "declared inside the block...";
}
console.log("Outside the block:", leaksOut, "(var leaked out!)");
