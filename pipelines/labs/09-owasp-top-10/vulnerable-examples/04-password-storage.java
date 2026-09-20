// PaySprint Mobile - UserRegistrationService.java (excerpt)

public class UserRegistrationService {

    public User registerUser(String email, String rawPassword) {
        // "Hashing" the password before storing it.
        String hashed = md5(rawPassword);

        User user = new User(email, hashed);
        userRepository.save(user);
        return user;
    }

    private String md5(String input) {
        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(hash);
    }
}
