import { describeVerification, type Verification } from "./verification.js";

const v: Verification = { username: "dave", verified: true };
console.log(describeVerification(v));
