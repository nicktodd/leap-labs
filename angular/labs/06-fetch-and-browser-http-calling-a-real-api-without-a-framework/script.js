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

/*
  TODO 1: Mark the submit handler async and prevent the page reload.
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    ...
  });
*/
form.addEventListener("submit", (event) => {
  event.preventDefault();

  /*
    TODO 2: Call fetch() with await.
    POST to AUTH_URL with headers: { "Content-Type": "application/json" }
    and body: JSON.stringify({ username: usernameInput.value.trim(),
    password: passwordInput.value }). Store the result in a variable
    called response.
  */

  /*
    TODO 3: Check response.ok.
    fetch() does NOT reject on a 401 or 500 - only on a network
    failure. If !response.ok, await response.json() for the error
    body and call showMessage(`Login failed: ${body.message}`,
    "error"), then return.
  */

  /*
    TODO 4: Read the successful body and show it.
    await response.json(), then showMessage() with the accessToken
    (data.accessToken.slice(0, 20) + "...") and kind "success".
  */

  /*
    TODO 5: Wrap TODOs 2-4 in try/catch/finally.
    catch (err) handles a NETWORK failure (service down, CORS
    blocked) - console.error it and showMessage() with kind "error".
    finally re-enables submitBtn regardless of outcome. Disable
    submitBtn and show a "Logging in..." message before the try
    block starts.
  */
});
