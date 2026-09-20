import { describeAttempt, type Attempt } from "./attempt.js";

const attempt: Attempt = { username: "alice", outcome: "success" };
console.log(describeAttempt(attempt));
