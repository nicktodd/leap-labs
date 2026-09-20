import { Injectable } from "@nestjs/common";

const attempts = [
  { username: "dave", outcome: "success" },
  { username: "erin", outcome: "fail" },
  { username: "dave", outcome: "fail" },
  { username: "frank", outcome: "success" },
];

@Injectable()
export class AttemptsService {
  getSummary() {
    let successCount = 0;
    let failCount = 0;
    for (const { outcome } of attempts) {
      if (outcome === "success") {
        successCount++;
      } else {
        failCount++;
      }
    }
    return { successCount, failCount };
  }
}
