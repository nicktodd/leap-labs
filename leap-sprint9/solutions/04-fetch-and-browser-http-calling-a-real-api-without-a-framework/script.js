const form = document.getElementById("login-form");
const usernameInput = document.querySelector("#username");
const passwordInput = document.querySelector("#password");
const message = document.querySelector(".message");
const submitBtn = document.getElementById("submit-btn");

const AUTH_URL = "http://localhost:3000/auth/login";

function showMessage(text, kind) {
  message.textContent = text;
  message.classList.remove("hidden", "error", "success");
  message.classList.add(kind);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  submitBtn.disabled = true;
  showMessage("Logging in...", "success");

  try {
    const response = await fetch(AUTH_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: usernameInput.value.trim(),
        password: passwordInput.value,
      }),
    });

    // fetch() only rejects on a NETWORK failure - a 401 or 500 still
    // resolves normally, so response.ok has to be checked by hand.
    if (!response.ok) {
      const body = await response.json();
      showMessage(`Login failed: ${body.message}`, "error");
      return;
    }

    const data = await response.json();
    showMessage(`Logged in. Token starts: ${data.accessToken.slice(0, 20)}...`, "success");
  } catch (err) {
    // A network failure (service down, CORS block) lands here, NOT
    // in the response.ok check above - fetch() never even got a
    // response to inspect.
    console.error("fetch() rejected:", err);
    showMessage(`Request failed: ${err.message}`, "error");
  } finally {
    submitBtn.disabled = false;
  }
});
