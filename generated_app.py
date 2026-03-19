
import tkinter as tk
from tkinter import messagebox

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        self.tasks = []

        # Create GUI components
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack(padx=10, pady=10)

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(padx=10)

        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack(padx=10, pady=10)

        self.delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(padx=10)

        self.save_tasks_button = tk.Button(self.root, text="Save Tasks", command=self.save_tasks)
        self.save_tasks_button.pack(padx=10)

        self.load_tasks_button = tk.Button(self.root, text="Load Tasks", command=self.load_tasks)
        self.load_tasks_button.pack(padx=10)

    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty")

    def delete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(task_index)
            self.tasks.pop(task_index)
        except:
            messagebox.showwarning("Warning", "No task selected")

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for task in self.tasks:
                f.write(task + "\n")
        messagebox.showinfo("Info", "Tasks saved to tasks.txt")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                self.tasks = [line.strip() for line in f.readlines()]
            self.task_listbox.delete(0, tk.END)
            for task in self.tasks:
                self.task_listbox.insert(tk.END, task)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No tasks file found")

root = tk.Tk()
app = TodoListApp(root)
root.mainloop()
