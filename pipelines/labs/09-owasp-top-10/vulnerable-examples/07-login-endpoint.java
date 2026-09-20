// PaySprint Mobile - LoginController.java (excerpt)

@RestController
public class LoginController {

    @PostMapping("/api/login")
    public LoginResponse login(@RequestBody LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail());

        if (user != null && user.getPasswordHash().equals(md5(request.getPassword()))) {
            String token = UUID.randomUUID().toString();
            sessionStore.put(token, user.getId());
            return new LoginResponse(token);
        }

        // No limit on failed attempts, no delay, no lockout.
        return new LoginResponse(null, "Invalid email or password");
    }
}
