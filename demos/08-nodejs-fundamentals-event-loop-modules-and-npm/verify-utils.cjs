// CommonJS module - Node's ORIGINAL module system, still the default for
// any .js file unless "type": "module" is set in package.json, or the
// file uses .mjs.

const KNOWN_USERS = ["alice", "bob", "carol"];

function isKnownUser(username) {
  return KNOWN_USERS.includes(username);
}

// module.exports is the ENTIRE public surface of this file - there's no
// per-declaration export keyword like ESM's export.
module.exports = { isKnownUser, KNOWN_USERS };
