import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, simpledialog, messagebox
import json
import os

language_extensions = {
            "Python": ".py",
            "Java": ".java",
            "C++": ".cpp",
            "JavaScript": ".js",
            "Ruby": ".rb",
            "Swift": ".swift",
            "HTML": ".html",
            "CSS": ".css",
            "Go": ".go",
            "Rust": ".rs"
        }

programming_languages = ["Python", "Java", "C++", "JavaScript", "Ruby", "Swift", "HTML", "CSS", "Go", "Rust"]

USER_DATA_FILE = "user_data.json"
RECENTLY_ACCESSED_MEMORY_SIZE = 50  # Number of recent files to store in RAM

recently_accessed_memory = {}
class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading...")
        self.root.geometry("300x150")

        self.label_loading = ttk.Label(root, text="Axle Interface", font=("Showcard Gothic", 12))
        self.label_loading.pack(pady=20)

        self.loading_indicator = ttk.Progressbar(root, mode='indeterminate', length=200)
        self.loading_indicator.pack(pady=10)
        self.loading_indicator.start(10)  # Start the animation

        self.root.after(5000, self.complete_loading)  # Simulate loading for 5 seconds

    def complete_loading(self):
        # Stop the loading animation and destroy the loading screen
        self.loading_indicator.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    loading_screen = LoadingScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
# Load existing user data from the file
try:
    with open(USER_DATA_FILE, 'r') as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

def save_user_data():
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file)

def register():
    username = simpledialog.askstring("Register", "Enter a new username:")
    password = simpledialog.askstring("Register", "Enter a password:", show='*')

    if username and password:
        user_data[username] = {"password": password, "details": []}
        save_user_data()
        tk.messagebox.showinfo("Registration Successful", "User registered successfully!")
    else:
        tk.messagebox.showwarning("Registration Failed", "Please enter a valid username and password.")

def login(username):
    if username in user_data:
        password = user_data[username]["password"]
        open_gui(username)
    else:
        tk.messagebox.showerror("Login Failed", "User not found.")

def open_gui(username):
    for file_path, content in recently_accessed_memory.items():
        text.insert(tk.END, f"Recent File: {os.path.basename(file_path)}\n{content}\n\n")

    # Create a button to display the RAM content
    def open_ram():
        ram_window = tk.Toplevel(window)
        ram_window.title("Recently Accessed Memory (RAM)")

        # Create a label to display RAM content
        ram_label = tk.Label(ram_window, text="Recently Accessed Memory (RAM)")
        ram_label.pack(pady=10)

        # Create a listbox to display RAM content
        ram_listbox = tk.Listbox(ram_window, width=50, height=20)
        ram_listbox.pack(pady=10)

        # Display RAM content
        for file_path in recently_accessed_memory.keys():
            ram_listbox.insert(tk.END, os.path.basename(file_path))
    # Create the main window
    window = tk.Tk()
    window.title("Axle Interface")

    # Create a label
    label = tk.Label(window, text=f"Welcome, {username}! Select a programming language and enter text:")
    label.pack(pady=10)

    # Create a variable to store the selected language
    language_var = tk.StringVar(window)
    language_var.set(programming_languages[0])  # Set the default language

    # Create a dropdown (Combobox) with programming languages
    language_dropdown = ttk.Combobox(window, values=programming_languages, textvariable=language_var)
    language_dropdown.pack(pady=10)

    # Create a large text writing area (ScrolledText widget)
    text = scrolledtext.ScrolledText(window, width=40, height=10, wrap=tk.WORD)
    text.pack(pady=10)

    # Load and display recently accessed files, if any
    for file_path, content in recently_accessed_memory.items():
        text.insert(tk.END, f"Recent File: {os.path.basename(file_path)}\n{content}\n\n")

    # Create a button to display the selected language and user input
    def on_button_click():
        selected_language = language_var.get()
        user_input = text.get("1.0", "end-1c")
        label.config(text=f"Selected language: {selected_language}\nUser input:\n{user_input}")

        # Save details for the current user
        if username in user_data:
            user_data[username].setdefault("details", []).append({"language": selected_language, "input": user_input})
            save_user_data()

        # Update recently accessed memory
        recently_accessed_memory[filedialog.askopenfilename()] = user_input
    def open_file():
        selected_language = language_var.get()
        file_extension = language_extensions.get(selected_language, ".*")  # Default to any file type if not found

        file_path = filedialog.askopenfilename(
            filetypes=[(f"{selected_language} Files", f"*{file_extension}"), ("All Files", "*.*")]
    )
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                text.delete('1.0', tk.END)  # Clear existing text in the Text widget
                text.insert(tk.END, content)


    ram_button = tk.Button(window, text="Open RAM", command=open_ram)
    ram_button.pack(pady=10)
    # Create a button to save the user input to a file
    def save_to_file():
        selected_language = language_var.get()
        user_input = text.get("1.0", "end-1c")

        file_extension = language_extensions.get(selected_language, ".txt")

        file_path = filedialog.asksaveasfilename(defaultextension=file_extension,
                                                   filetypes=[(f"{selected_language} Files", f"*{file_extension}")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write(user_input)
            label.config(text=f"File saved as: {file_path}")

        # Update recently accessed memory
        recently_accessed_memory[file_path] = user_input

    save_button = tk.Button(window, text="Save", command=save_to_file)
    save_button.pack(pady=10)

    open_button = tk.Button(window, text="Open File", command=open_file)
    open_button.pack(pady=10)
    # Run the application
    window.mainloop()

def select_account(event):
    selected_account = account_listbox.get(account_listbox.curselection())
    if selected_account:
        login(selected_account)

def add_account():
    register()

def login_existing_account():
    username = simpledialog.askstring("Login", "Enter your username:")
    login(username)

# Create a button to add a new account
add_account_button = tk.Button(text="Add Account", command=add_account)
add_account_button.pack(pady=10)

# Create a button to login with an existing account
login_existing_button = tk.Button(text="Login with Existing Account", command=login_existing_account)
login_existing_button.pack(pady=10)

# Create a Listbox for selecting accounts
account_listbox = tk.Listbox(selectmode=tk.SINGLE)
for account in user_data.keys():
    account_listbox.insert(tk.END, account)
account_listbox.bind("<Double-Button-1>", select_account)
account_listbox.pack(pady=10)

# Create a button to log in
login_button = tk.Button(text="Login", command=lambda: login(account_listbox.get(tk.ACTIVE)))
login_button.pack(pady=10)

# Run the main application
tk.mainloop()
