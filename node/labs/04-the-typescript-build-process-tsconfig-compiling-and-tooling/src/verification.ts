export interface Verification {
  username: string;
  verified: boolean;
}

export function describeVerification(v: Verification): string {
  return v.verified ? `${v.username} is verified` : `${v.username} is NOT verified`;
}
