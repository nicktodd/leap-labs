# Lab 8 Model Answers

## Verified Output

```
{
  id: 1,
  createdAt: '2026-01-01T09:00:00Z',
  username: 'dave',
  outcome: 'success'
}
Verified: dave
Error: Unknown user: mallory
Record for dave
Record for erin
```

## Key Points

- **TODO 1**: `BaseRecord`'s two fields, then `LoginAttempt extends BaseRecord` adding
  its own three. The `?` on `notes` is what lets the `attempt` object below omit it
  entirely without error.
- **TODO 2**: `interface Result<T>` - the `<T>` goes directly after the interface name,
  and `T` is then usable inside the interface body exactly like any other type name.
- **TODO 3**: `<T extends { username: string }>` before the parameter list, then `T` as
  the parameter's type. The constraint is an inline object type, not a named interface
  - it doesn't require `LoginAttempt` or any other named type, just SOME object with at
  least a `username` field.

## The Reflection Question

TypeScript uses **structural typing** - `describeByUsername` accepts any value whose
SHAPE matches the constraint, regardless of what interface (if any) it was declared
against. Neither `{ username: "dave", outcome: "success" }` nor
`{ username: "erin", verified: true }` is ever declared as a `LoginAttempt` or
anything else; `tsc` just checks that each object literal HAS a `username: string`
field and allows the extra ones through.

Java's generics work differently: `<T extends Named>` requires `T` to actually
IMPLEMENT the `Named` interface - declared, explicit, checked at the class level, not
inferred from whatever fields happen to be present. This is the difference between
TypeScript's **structural typing** ("does this value look right") and Java's
**nominal typing** ("does this value's declared type say it's the right thing") - a
distinction worth naming explicitly here, since it's the first time this week has
made it visible.
