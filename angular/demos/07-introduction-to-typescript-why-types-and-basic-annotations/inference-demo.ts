// TypeScript infers types even without annotations - hover in VS Code to
// see it, or let a wrong usage prove it at compile time.
let username = "alice"; // inferred as string, no annotation needed
username = "bob"; // fine - still a string

const attemptCount = 3; // inferred as the LITERAL type 3, since const
console.log(typeof username, typeof attemptCount);

// any opts OUT of type checking entirely - avoid it. Everything after
// this point on a variable typed any is back to plain JavaScript rules.
let riskyValue: any = "alice";
riskyValue = 42; // no error - any accepts anything, which defeats the point
console.log(riskyValue);
