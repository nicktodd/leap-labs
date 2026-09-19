# Demo: Module 11 — Secure Coding in Practice

**Duration:** 12 minutes
**Prerequisite:** The `starter/` codebase from this lab open in IntelliJ. GitHub Copilot Chat
available.

## Part 1: Recap, quickly (1 min)

Narration: Module 09 taught you to name a category on sight. Module 10 practised fixing
isolated snippets on Secure Code Warrior. Today's codebase is more realistic: five
vulnerabilities across several files in one small backend, exactly the shape of a real code
review.

## Part 2: Core defences, briefly (2 min)

Three defences come up repeatedly across today's fixes, worth naming before diving in:

- **Input validation**: check that data coming in is the shape/range/type you expect, before
  you use it for anything
- **Output encoding**: escape data before it's rendered somewhere it could be misinterpreted
  (HTML, SQL, shell commands)
- **Parameterised queries**: never build a query by concatenating user input into a string, bind
  it as a parameter instead

## Part 3: Using Copilot responsibly for a fix (5 min)

Open `UserRegistrationService.java`. Ask Copilot Chat:

```text
This uses MD5 to hash passwords before storing them. What's wrong with that, and what should
I use instead?
```

Narration: Copilot will very likely name the risk correctly. But watch what it suggests as a
replacement, a common, plausible-but-wrong suggestion is **SHA-256**. Ask the room: is SHA-256
actually a fix? Answer: no, SHA-256 is still a fast, general-purpose hash, exactly the same
underlying problem as MD5, just with a longer digest. It's *not* designed to be slow or salted
the way a password hashing algorithm needs to be. The correct fix is a purpose-built algorithm:
**bcrypt, scrypt, or Argon2**.

This is the module's key lesson made concrete: Copilot can introduce (or fail to fully fix) a
vulnerability if you accept its first suggestion without checking it against what you actually
know, in this case, from Module 09's model answers.

## Part 4: One more, together (3 min)

Open `TransactionSearchDao.java` and ask Copilot to suggest a fix for the SQL injection risk.
Narration: watch for a subtly wrong suggestion here too, some models suggest **escaping quotes**
in the input string rather than switching to a `PreparedStatement`. Escaping is fragile and
easy to get wrong (there's always another edge case); a parameterised query removes the entire
class of problem. Accept only the `PreparedStatement`-based fix.

## Part 5: Handing off to the lab (1 min)

Narration: the lab has five vulnerabilities across the codebase, not two. Use Copilot on all
five, but the acceptance criteria for this lab is explicit: every fix must be *reviewed*, not
just pasted in.

## Key message

Copilot is fast at naming a problem and proposing *a* fix. It is not reliably fast at proposing
the *right* fix, especially for security-sensitive code, where a plausible-sounding
almost-right answer (SHA-256, string escaping) can be more dangerous than an obviously wrong
one, because it looks solved.
