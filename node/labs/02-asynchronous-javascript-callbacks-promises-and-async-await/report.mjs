// KATA: two TODOs. Run this now, before changing anything - it throws at
// TODO 1. That's the starting point.

import { verifyCredentials } from "./verify-credentials.mjs";

const usernames = ["dave", "erin", "mallory"]; // mallory is NOT a known user

// TODO 1: write an async function checkSequentially(usernames) that awaits
// verifyCredentials for each username IN ORDER (a for...of loop), using
// try/catch PER ITERATION so one failure doesn't stop the loop. Print
// "Verified: <username>" on success, "Not verified: <username> (<error
// message>)" on failure.
async function checkSequentially(usernames) {
  throw new Error("TODO 1: implement checkSequentially");
}

// TODO 2: write an async function checkConcurrently(usernames) that starts
// all the checks at once with Promise.allSettled (NOT Promise.all -
// Promise.all would reject the whole thing on mallory's failure, and we
// want every result, success or not). For each outcome, print the same
// two message formats as TODO 1.
async function checkConcurrently(usernames) {
  throw new Error("TODO 2: implement checkConcurrently");
}

console.log("--- sequential ---");
await checkSequentially(usernames);
console.log("--- concurrent ---");
await checkConcurrently(usernames);
