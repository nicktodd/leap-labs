// require() is CommonJS's import - synchronous, and resolved at the
// exact line it's called, not hoisted to the top of the file the way
// ESM's import is.
const { isKnownUser, KNOWN_USERS } = require("./verify-utils.cjs");

console.log(KNOWN_USERS);
console.log(isKnownUser("alice"));
console.log(isKnownUser("mallory"));
