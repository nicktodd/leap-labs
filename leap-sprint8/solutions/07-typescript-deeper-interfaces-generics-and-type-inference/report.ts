interface BaseRecord {
  readonly id: number;
  createdAt: string;
}

interface LoginAttempt extends BaseRecord {
  username: string;
  outcome: string;
  notes?: string;
}

const attempt: LoginAttempt = {
  id: 1,
  createdAt: "2026-01-01T09:00:00Z",
  username: "dave",
  outcome: "success",
};
console.log(attempt);

interface Result<T> {
  success: boolean;
  value?: T;
  error?: string;
}

function verifyCredentials(username: string): Result<{ username: string }> {
  const knownUsers = ["dave", "erin", "frank"];
  if (knownUsers.includes(username)) {
    return { success: true, value: { username } };
  }
  return { success: false, error: `Unknown user: ${username}` };
}

const outcome = verifyCredentials("dave");
if (outcome.success) {
  console.log("Verified:", outcome.value?.username);
} else {
  console.log("Error:", outcome.error);
}

const failedOutcome = verifyCredentials("mallory");
if (failedOutcome.success) {
  console.log("Verified:", failedOutcome.value?.username);
} else {
  console.log("Error:", failedOutcome.error);
}

function describeByUsername<T extends { username: string }>(record: T): string {
  return `Record for ${record.username}`;
}

console.log(describeByUsername({ username: "dave", outcome: "success" }));
console.log(describeByUsername({ username: "erin", verified: true }));
