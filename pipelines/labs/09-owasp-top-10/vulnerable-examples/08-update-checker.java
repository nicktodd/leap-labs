// PaySprint Mobile - AutoUpdateService.java (excerpt)
// Runs on app startup to fetch and apply a remote configuration bundle.

public class AutoUpdateService {

    public void applyLatestConfig() {
        String url = "http://config.paysprint-updates.example.com/latest-config.json";

        String json = httpClient.get(url);
        Config config = objectMapper.readValue(json, Config.class);

        // Applied directly, no signature check, no checksum, plain HTTP.
        configManager.apply(config);
    }
}
