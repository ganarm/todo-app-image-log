// CRUD operations via fetch API
async function fetchTasks() {
  const res = await fetch('/api/tasks');
  const data = await res.json();
  renderTasks(data);
}

async function addTask(e) {
  e.preventDefault();
  const form = e.target;
  const body = {
    title: form.title.value,
    description: form.description.value,
    priority: form.priority.value,
    due_date: form.due_date.value
  };
  await fetch('/api/tasks', {
    method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body)
  });
  form.reset();
  fetchTasks();
}

// Similarly implement update, delete, toggle complete

document.addEventListener('DOMContentLoaded', () => {
  fetchTasks();
  document.getElementById('task-form').addEventListener('submit', addTask);
});