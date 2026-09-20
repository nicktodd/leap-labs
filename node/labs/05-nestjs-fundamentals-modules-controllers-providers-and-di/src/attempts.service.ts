import { Injectable } from "@nestjs/common";

const attempts = [
  { username: "dave", outcome: "success" },
  { username: "erin", outcome: "fail" },
  { username: "dave", outcome: "fail" },
  { username: "frank", outcome: "success" },
];

@Injectable()
export class AttemptsService {
  // TODO 1: implement getSummary() to return { successCount, failCount },
  // counted from the attempts array above - identical logic to Module
  // 2/3's counting.
  getSummary() {
    throw new Error("TODO 1: implement getSummary");
  }
}
