const taskInput = document.getElementById('taskInput');
const addButton = document.getElementById('addButton');
const taskList = document.getElementById('taskList');
const API_URL = '/api/tasks';

document.addEventListener('DOMContentLoaded', async () => {
	const response = await fetch(API_URL);
	const tasks = await response.json();

	tasks.forEach(task => {
		createTaskElement(task.title, task.id, task.completed);
	});
});

addButton.addEventListener('click', async () => {
	const text = taskInput.value.trim();

	if (text === '') return;

	const response = await fetch(API_URL, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({title: text})
	});

	if (response.ok) {
		const newTask = await response.json();
		createTaskElement(newTask.title, newTask.id, newTask.completed);
		taskInput.value = '';
	}
});

function createTaskElement(text, id, completed) {
	const li = document.createElement('li');

	
	li.style.marginTop = '10px';
	li.style.paddingLeft = '10px';
	li.style.textAlign = 'left';
	li.id = `task-${id}`;

	li.innerHTML = `
		<span class="task-text ${completed ? 'completed' : ''}">${text}</span>
		<button class="delete-btn" style="margin-left: 15px; cursor: pointer;">X</button>
	`;

	if(completed) {
		li.classList.add('task-done');
	}

	const taskText = li.querySelector('.task-text');
	const deleteBtn = li.querySelector('.delete-btn');

	taskText.addEventListener('click', async () => {
		const isCompleted = taskText.classList.contains('completed');
		
		const response = await fetch(`${API_URL}/${id}`, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ completed: !isCompleted })
		});

		if (response.ok) {
			taskText.classList.toggle('completed');
			li.classList.toggle('task-done');
		}
	});

	deleteBtn.addEventListener('click', async () => {
		const response = await fetch(`${API_URL}/${id}`, {
			method: 'DELETE'
		});

		if (response.ok) {
			li.remove();
		}
	});

	taskList.appendChild(li);
}
