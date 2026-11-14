const listEl = document.getElementById("task-list");
const statsEl = document.getElementById("stats");
const titleInput = document.getElementById("new-title");
const searchInput = document.getElementById("search");

async function api(path, options = {}) {
  const res = await fetch("/api" + path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    throw new Error("Request failed: " + res.status);
  }
  return res.status === 204 ? null : res.json();
}

function render(tasks) {
  listEl.innerHTML = "";
  tasks.forEach((t) => {
    const li = document.createElement("li");
    li.className = t.done ? "done" : "";
    li.innerHTML = `<input type="checkbox" ${t.done ? "checked" : ""}>
      <span class="title">${t.title}</span>
      <button class="del">✕</button>`;
    li.querySelector("input").addEventListener("change", () => toggleTask(t.id));
    li.querySelector(".del").addEventListener("click", () => deleteTask(t.id));
    listEl.appendChild(li);
  });
}

async function loadTasks() {
  const q = encodeURIComponent(searchInput.value);
  render(await api("/tasks?search=" + q));
}

async function loadStats() {
  try {
    const s = await api("/stats");
    statsEl.textContent = `${s.done}/${s.total} done (${s.percent}%)`;
  } catch (e) {
    statsEl.textContent = "Stats unavailable";
  }
}

async function refresh() {
  await Promise.all([loadTasks(), loadStats()]);
}

async function addTask() {
  const title = titleInput.value.trim();
  if (!title) return;
  await api("/tasks", { method: "POST", body: JSON.stringify({ title }) });
  titleInput.value = "";
  refresh();
}

async function toggleTask(id) {
  await api(`/tasks/${id}/toggle`, { method: "PUT" });
  refresh();
}

async function deleteTask(id) {
  await api(`/tasks/${id}`, { method: "DELETE" });
  refresh();
}

async function clearAll() {
  let token = localStorage.getItem("adminToken");
  if (!token) {
    token = prompt("Admin token:");
    if (!token) return;
    localStorage.setItem("adminToken", token);
  }
  try {
    await api("/tasks", { method: "DELETE", headers: { "X-Admin-Token": token } });
  } catch (e) {
    localStorage.removeItem("adminToken");
    alert("Not authorized");
  }
  refresh();
}

document.getElementById("add-btn").addEventListener("click", addTask);
titleInput.addEventListener("keydown", (e) => e.key === "Enter" && addTask());
searchInput.addEventListener("input", loadTasks);
document.getElementById("clear-btn").addEventListener("click", clearAll);

refresh();
