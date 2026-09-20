/*
  TODO 1: Select the elements.
  Use document.getElementById to grab the form (id="login-form").
  Use document.querySelector to grab the username input (#username),
  the password input (#password), and the message element (.message).
*/
const form = null; // replace with document.getElementById("login-form")
const usernameInput = null; // replace with document.querySelector("#username")
const passwordInput = null; // replace with document.querySelector("#password")
const message = null; // replace with document.querySelector(".message")

function showMessage(text, kind) {
  message.textContent = text;
  message.classList.remove("hidden", "error", "success");
  message.classList.add(kind);
}

function markInvalid(input, isInvalid) {
  input.classList.toggle("invalid", isInvalid);
}

/*
  TODO 2: Handle the submit event.
  Add a "submit" listener to form. Inside it:
    - call event.preventDefault() so the page doesn't reload
    - read usernameInput.value and passwordInput.value
    - decide usernameOk (length >= 3) and passwordOk (length >= 8)
    - call markInvalid() on each input with the opposite of *Ok
    - if either is invalid, call showMessage() with kind "error" and
      return
    - otherwise call showMessage() with kind "success", then
      form.reset() and clear both invalid classes
*/


/*
  TODO 3: React as the user types.
  Add an "input" listener to usernameInput that removes the invalid
  class as soon as the value reaches 3+ characters, so the error
  clears itself without waiting for another submit.
*/
