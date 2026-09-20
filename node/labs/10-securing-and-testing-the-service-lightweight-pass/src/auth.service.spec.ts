import { AuthService, JWT_SECRET } from "./auth.service";
import * as jwt from "jsonwebtoken";

describe("AuthService", () => {
  let service: AuthService;

  beforeEach(() => {
    service = new AuthService();
  });

  it("logs in and receives a valid access token and refresh token", async () => {
    await service.register("carol", "mission123", ["MISSION_OPERATOR"]);
    // TODO 1: log in as carol with the correct password, then assert that
    // accessToken and refreshToken are both strings, and that they are
    // NOT equal to each other.
    throw new Error("TODO 1: not implemented");
  });

  it("issues an access token that validates and carries the right claims", async () => {
    await service.register("carol", "mission123", ["MISSION_OPERATOR"]);
    // TODO 2: log in, then verify the accessToken with
    // jwt.verify(accessToken, JWT_SECRET) and assert the decoded
    // payload's sub is "carol" and roles is ["MISSION_OPERATOR"].
    throw new Error("TODO 2: not implemented");
  });

  it("rejects login with an incorrect password", async () => {
    await service.register("carol", "mission123", ["MISSION_OPERATOR"]);
    // TODO 3: assert that service.login("carol", "wrong-password")
    // rejects (hint: expect(...).rejects.toThrow()).
    throw new Error("TODO 3: not implemented");
  });
});
