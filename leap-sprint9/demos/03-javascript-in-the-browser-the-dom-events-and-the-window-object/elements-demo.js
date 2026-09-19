// getElementById - exactly one match, fastest, oldest API
const checklist = document.getElementById("checklist");

// querySelectorAll - any CSS selector, returns a static NodeList
const tasks = document.querySelectorAll(".task");
console.log(`Found ${tasks.length} tasks`);

// Click each task to toggle it done - event delegation would be the
// production approach, but a direct loop is clearer for a first look.
tasks.forEach((task) => {
  task.addEventListener("click", () => {
    task.classList.toggle("done");
  });
});

// createElement + appendChild - building a NEW element from nothing
document.getElementById("add-task").addEventListener("click", () => {
  const li = document.createElement("li");
  li.textContent = "New task - click to mark done";
  li.className = "task";
  li.addEventListener("click", () => li.classList.toggle("done"));
  checklist.appendChild(li);
});
