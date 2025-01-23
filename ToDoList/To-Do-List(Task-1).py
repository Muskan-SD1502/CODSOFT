import sqlite3
import tkinter as tk
from tkinter import messagebox, Scrollbar


class ToDoListApp:
    def __init__(self, root):
        self.connection = sqlite3.connect("todo_list.db")
        self.cursor = self.connection.cursor()
        self._create_table()

        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("500x450")

        # Title Label
        title_label = tk.Label(root, text="To-Do List", font=("Helvetica", 16, "bold"), pady=10)
        title_label.pack()

        # Frame for Input and Buttons
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 12))
        self.task_entry.grid(row=0, column=0, padx=10, pady=5)

        self.add_button = tk.Button(input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.add_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(input_frame, text="Update Task", command=self.update_task, bg="#FFA500", fg="white", font=("Helvetica", 10, "bold"))
        self.update_button.grid(row=1, column=1, padx=10, pady=5)

        # Frame for Task List
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(list_frame, width=40, height=12, font=("Helvetica", 12), selectmode=tk.SINGLE)
        self.task_listbox.grid(row=0, column=0)

        scrollbar = Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Frame for Action Buttons
        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)

        self.complete_button = tk.Button(action_frame, text="Mark Complete", command=self.mark_complete, bg="#008CBA", fg="white", font=("Helvetica", 10, "bold"))
        self.complete_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(action_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white", font=("Helvetica", 10, "bold"))
        self.delete_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(action_frame, text="Reset Tasks", command=self.reset_tasks, bg="#FF0000", fg="white", font=("Helvetica", 10, "bold"))
        self.reset_button.grid(row=0, column=2, padx=10)

        self.load_tasks()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "pending"))
            self.connection.commit()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

    def update_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_listbox.get(selected_task).split(".")[0]
            new_task = self.task_entry.get().strip()
            if new_task:
                self.cursor.execute("UPDATE tasks SET task = ?, status = ? WHERE id = ?", (new_task, "pending", task_id))
                self.connection.commit()
                self.task_entry.delete(0, tk.END)
                self.load_tasks()
            else:
                messagebox.showwarning("Input Error", "Task cannot be empty!")
        else:
            messagebox.showwarning("Selection Error", "No task selected!")

    def mark_complete(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_listbox.get(selected_task).split(".")[0]
            self.cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", ("completed", task_id))
            self.connection.commit()
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "No task selected!")

    def delete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_listbox.get(selected_task).split(".")[0]
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.connection.commit()
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "No task selected!")

    def reset_tasks(self):
        response = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete all tasks?")
        if response:
            self.cursor.execute("DELETE FROM tasks")
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'tasks'")
            self.connection.commit()
            self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, task, status FROM tasks")
        for task in self.cursor.fetchall():
            status = "✓" if task[2] == "completed" else "✗"
            self.task_listbox.insert(tk.END, f"{task[0]}. [{status}] {task[1]}")

    def close(self):
        self.connection.close()


def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
