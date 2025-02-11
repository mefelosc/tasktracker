import argparse
import json
import os
from datetime import datetime

# Nome do arquivo onde as tarefas serão armazenadas
TASKS_FILE = "tasks.json"

# Função para carregar as tarefas do arquivo JSON
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []  # Retorna uma lista vazia se o arquivo não existir
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []  # Em caso de erro na decodificação, retorna lista vazia

# Função para salvar as tarefas no arquivo JSON
def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

# Função para obter o próximo ID único para uma nova tarefa
def get_next_id(tasks):
    if not tasks:
        return 1
    max_id = max(task["id"] for task in tasks)
    return max_id + 1

# Função para adicionar uma nova tarefa
def add_task(description):
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    now = datetime.now().isoformat()
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

# Função para atualizar a descrição de uma tarefa
def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print("Task not found.")

# Função para remover uma tarefa pelo ID
def delete_task(task_id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed_task = tasks.pop(i)
            save_tasks(tasks)
            print(f"Task {removed_task['id']} deleted successfully.")
            return
    print("Task not found.")

# Função para marcar uma tarefa como in-progress
def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as in-progress.")
            return
    print("Task not found.")

# Função para marcar uma tarefa como done
def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as done.")
            return
    print("Task not found.")

# Função para listar tarefas (com filtro opcional por status)
def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task["status"] == filter_status]
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"ID: {task['id']}")
        print(f"Description: {task['description']}")
        print(f"Status: {task['status']}")
        print(f"Created At: {task['createdAt']}")
        print(f"Updated At: {task['updatedAt']}")
        print("-" * 40)

# Função principal que configura os comandos e argumentos da CLI
def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Comando para adicionar uma tarefa
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="Task description")

    # Comando para atualizar uma tarefa
    parser_update = subparsers.add_parser("update", help="Update a task's description")
    parser_update.add_argument("id", type=int, help="Task ID")
    parser_update.add_argument("description", help="New task description")

    # Comando para deletar uma tarefa
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Task ID")

    # Comando para marcar uma tarefa como in-progress
    parser_mip = subparsers.add_parser("mark-in-progress", help="Mark a task as in-progress")
    parser_mip.add_argument("id", type=int, help="Task ID")

    # Comando para marcar uma tarefa como done
    parser_md = subparsers.add_parser("mark-done", help="Mark a task as done")
    parser_md.add_argument("id", type=int, help="Task ID")

    # Comando para listar tarefas com filtro opcional
    parser_list = subparsers.add_parser("list", help="List tasks")
    parser_list.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"],
                             help="Filter tasks by status (optional)")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark-in-progress":
        mark_in_progress(args.id)
    elif args.command == "mark-done":
        mark_done(args.id)
    elif args.command == "list":
        list_tasks(args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
