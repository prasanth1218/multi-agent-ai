
# Import the required libraries
import tkinter as tk
from tkinter import ttk, messagebox

class TodoListApp:
    def __init__(self, root):
        # Create the main window
        self.root = root
        self.root.title('Todo List App')
        self.root.geometry('400x500')

        # Create the frames
        self.header_frame = tk.Frame(self.root, bg='#ff8a00')
        self.header_frame.pack(fill='x')

        self.todo_list_frame = tk.Frame(self.root, bg='#fff')
        self.todo_list_frame.pack(fill='both', expand=True)

        self.add_todo_frame = tk.Frame(self.root, bg='#fff')
        self.add_todo_frame.pack(fill='x')

        # Create the header
        self.header_label = tk.Label(self.header_frame, text='Todo List App', font=('Arial', 18, 'bold'), bg='#ff8a00', fg='#fff')
        self.header_label.pack(fill='x', padx=10, pady=10)

        # Create the todo list
        self.todo_list = tk.Listbox(self.todo_list_frame, font=('Arial', 14), width=40)
        self.todo_list.pack(fill='both', expand=True, padx=10, pady=10)

        # Create the add todo entry
        self.add_todo_label = tk.Label(self.add_todo_frame, text='Add Todo:', font=('Arial', 14), bg='#fff')
        self.add_todo_label.pack(side='left', padx=10, pady=10)

        self.add_todo_entry = tk.Entry(self.add_todo_frame, font=('Arial', 14), width=20)
        self.add_todo_entry.pack(side='left', padx=10, pady=10)

        # Create the add todo button
        self.add_todo_button = tk.Button(self.add_todo_frame, text='Add', font=('Arial', 14), command=self.add_todo)
        self.add_todo_button.pack(side='left', padx=10, pady=10)

        # Create the delete todo button
        self.delete_todo_button = tk.Button(self.add_todo_frame, text='Delete', font=('Arial', 14), command=self.delete_todo)
        self.delete_todo_button.pack(side='left', padx=10, pady=10)

    def add_todo(self):
        # Get the todo item text
        todo_item_text = self.add_todo_entry.get()

        # Check if the todo item text is not empty
        if todo_item_text:
            # Add the todo item to the list
            self.todo_list.insert('end', todo_item_text)
            # Clear the entry field
            self.add_todo_entry.delete(0, 'end')

    def delete_todo(self):
        # Get the selected todo item index
        selected_index = self.todo_list.curselection()

        # Check if an item is selected
        if selected_index:
            # Delete the todo item
            self.todo_list.delete(selected_index)

if __name__ == '__main__':
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
