// PaySprint Mobile - AvatarController.java (excerpt)
// Lets a customer set their profile picture from an image URL.

@RestController
public class AvatarController {

    @PostMapping("/api/profile/avatar")
    public void setAvatarFromUrl(@RequestParam String imageUrl) {
        // Fetches whatever URL the customer supplies, server-side, no restriction.
        byte[] imageBytes = httpClient.get(imageUrl);
        avatarStorage.save(currentUser(), imageBytes);
    }
}
