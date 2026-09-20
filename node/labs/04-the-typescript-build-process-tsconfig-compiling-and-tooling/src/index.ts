// TODO 2: this import is missing the required file extension under
// NodeNext module resolution - fix it once TODO 1's tsconfig is in place
// and you see the real TS2835 error tsc gives you.
import { describeVerification, type Verification } from "./verification";

const v: Verification = { username: "dave", verified: true };
console.log(describeVerification(v));
