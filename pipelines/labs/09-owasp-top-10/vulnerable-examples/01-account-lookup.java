// PaySprint Mobile - AccountController.java (excerpt)

@RestController
public class AccountController {

    @Autowired
    private AccountRepository accountRepository;

    @GetMapping("/api/accounts/{accountId}")
    public Account getAccount(@PathVariable Long accountId) {
        // Fetches whatever account ID is in the URL, no ownership check.
        return accountRepository.findById(accountId)
                .orElseThrow(() -> new NotFoundException("Account not found"));
    }

    @GetMapping("/api/accounts/{accountId}/statement")
    public Statement getStatement(@PathVariable Long accountId) {
        return statementService.generateFor(accountId);
    }
}
