import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import json
import os
import subprocess
import webbrowser as wb
import socket
import ipaddress
import csv
'''
os.system("pip install cryptography")
frm cryptography.fernet import Fernet
'''
# File to store user data
USER_DATA_FILE = 'user_data.json'
RECENT_FILES = 'recent_files.json'
PROGRAMMING_LANGUAGES = {
    "CSS": [("CSS Files", "*.css")],
    "Python": [("Python Files", "*.py")],
    "Java": [("Java Files", "*.java")],
    "C++": [("C++ Files", "*.cpp;*.hpp")],
    "JavaScript": [("JavaScript Files", "*.js")],
    "Ruby": [("Ruby Files", "*.rb")],
    "Swift": [("Swift Files", "*.swift")],
    "HTML": [("HTML Files", "*.html;*.htm")],
    "CSS": [("CSS Files", "*.css")],
    "Go": [("Go Files", "*.go")],
    "Rust": [("Rust Files", "*.rs")]
}

# Load existing user data or create a new file if it doesn't exist
if not os.path.exists(USER_DATA_FILE):
    messagebox.showinfo(
        "File not found",
        "We cannot find your users file for this interface so we must unfortunately create a new file"
    )
    with open(USER_DATA_FILE, 'w') as file:
        json.dump({}, file)

# Load recent files or create a new file if it doesn't exist
if not os.path.exists(RECENT_FILES):
    with open(RECENT_FILES, 'w') as file:
        json.dump([], file)


def load_user_data():
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)


def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)


def load_recent_files():
    with open(RECENT_FILES, 'r') as file:
        return json.load(file)


def save_recent_file(file_path):
    recent_files = load_recent_files()
    if file_path not in recent_files:
        recent_files.insert(0, file_path)
        if len(recent_files) > 10:
            recent_files.pop()
        with open(RECENT_FILES, 'w') as file:
            json.dump(recent_files, file)


def show_user_info(user_listbox_dashboard, content_area):
    selected_user = user_listbox_dashboard.get(tk.ACTIVE)
    for widget in content_area.winfo_children():
        widget.destroy()

    if selected_user:
        user_data = load_user_data()
        password = user_data.get(selected_user)
        user_info = f"Username: {selected_user}\nPassword: {password}"

        user_info_label = tk.Label(content_area,
                                   text=user_info,
                                   font=("Ubuntu", 14),
                                   bg='white')
        user_info_label.pack(pady=10)


def create_account():
    username = simpledialog.askstring("Username", "Enter a new username:")
    password = simpledialog.askstring("Password",
                                      "Enter a new password:",
                                      show="*")

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    user_data = load_user_data()

    if username in user_data:
        messagebox.showerror("Error", "Username already exists.")
    else:
        user_data[username] = password
        save_user_data(user_data)
        update_user_list()
        messagebox.showinfo("Success", "Account created successfully!")


def login():
    selected_user = user_listbox.get(tk.ACTIVE)
    username = selected_user or simpledialog.askstring("Username",
                                                       "Enter your username:")
    password = simpledialog.askstring("Password",
                                      "Enter your password:",
                                      show="*")

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    user_data = load_user_data()

    if user_data.get(username) == password:
        show_login_progress(username)
        w.withdraw()
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def show_login_progress(username):
    progress_window = tk.Toplevel()
    progress_window.title("Logging In")
    progress_window.geometry("300x100")

    progress_label = tk.Label(progress_window,
                              text="Logging in...",
                              font=("Ubuntu", 12))
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window,
                                   orient="horizontal",
                                   mode="determinate",
                                   length=250)
    progress_bar.pack(pady=10)
    progress_bar.start()

    progress_window.after(6000,
                          lambda: complete_login(progress_window, username))


def complete_login(progress_window, username):
    progress_window.destroy()
    open_dashboard(username)


def open_dashboard(username):
    global dashboard
    dashboard = tk.Toplevel()
    dashboard.title("AxleOwner")
    dashboard.geometry("800x600")

    # Create a label for the dashboard
    Axle_label = tk.Label(dashboard,
                          text="AxleOwner Interface",
                          font=("Ubuntu", 24))
    Axle_label.pack(pady=20)

    # Sidebar without scroll
    sidebar_frame = tk.Frame(dashboard, bg='black', width=200)
    sidebar_frame.pack(side='left', fill='y')

    user_listbox_dashboard = tk.Listbox(sidebar_frame)
    user_listbox_dashboard.pack(pady=5, padx=5, fill='both', expand=True)
    update_user_list_dashboard(user_listbox_dashboard)

    show_user_info_button = tk.Button(
        sidebar_frame,
        text="Show User Info",
        bg='gray',
        fg='white',
        command=lambda: show_user_info(user_listbox_dashboard, content_area))
    show_user_info_button.pack(fill='x', pady=2, padx=5)

    language_label = tk.Label(sidebar_frame,
                              text="Select Language",
                              bg='black',
                              fg='white')
    language_label.pack(pady=5, padx=5)

    language_combobox = ttk.Combobox(sidebar_frame,
                                     values=list(PROGRAMMING_LANGUAGES.keys()),
                                     state='readonly')
    language_combobox.pack(fill='x', padx=5)

    button_files = tk.Button(
        sidebar_frame,
        text="Open File",
        bg='green',
        fg='white',
        command=lambda: open_file_dialog(language_combobox.get()))
    button_files.pack(fill='x', pady=2, padx=5)

    button_recent_files = tk.Button(
        sidebar_frame,
        text="Recent Files",
        bg='green',
        fg='white',
        command=lambda: show_recent_files(content_area))
    button_recent_files.pack(fill='x', pady=2, padx=5)

    button_files = tk.Button(sidebar_frame,
                             text="Open file explorer",
                             bg='blue',
                             fg='white',
                             command=open_file_manager)
    button_files.pack(fill='x', pady=2, padx=5)

    button_clone_repo = tk.Button(sidebar_frame,
                                  text="Open github",
                                  bg='blue',
                                  fg='white',
                                  command=clone_repository)
    button_clone_repo.pack(fill='x', pady=2, padx=5)

    button_profile = tk.Button(
        sidebar_frame,
        text="Profile",
        bg='black',
        fg='white',
        command=lambda: open_profile(username, content_area,
                                     user_listbox_dashboard))
    button_profile.pack(fill='x', pady=2, padx=5)

    button_logout = tk.Button(sidebar_frame,
                              text="Logout",
                              bg='red',
                              fg='white',
                              command=logout)
    button_logout.pack(fill='x', pady=2, padx=5)

    button_quit = tk.Button(sidebar_frame,
                            text="Quit",
                            bg='red',
                            fg='white',
                            command=quit)
    button_quit.pack(fill='x', pady=2, padx=5)

    openbutton = tk.Button(sidebar_frame,
                           text="Open Axle Interface",
                           bg='green',
                           fg='white',
                           command=open_axle_interface)
    openbutton.pack(fill='x', pady=2, padx=5)

    open_system_settings = tk.Button(sidebar_frame,
                                     text="System access buttons",
                                     bg="black",
                                     fg="gray",
                                     command=lambda: System_area(content_area))
    open_system_settings.pack(padx=2, pady=5)

    openweb = tk.Button(sidebar_frame,
                        text="Open website",
                        bg="black",
                        fg="gray",
                        command=open_website)
    openweb.pack(padx=2, pady=5)

    openprogrammersweb = tk.Button(sidebar_frame,
                                   text="Open programmer's website",
                                   bg="black",
                                   fg="gray",
                                   command=web)
    openprogrammersweb.pack(padx=2, pady=5)

    emailtrack=tk.Button(sidebar_frame,
                                   text="Locate ID",
                                   bg="black",
                                   fg="gray",
                                   command=locate_device_button)
    emailtrack.pack(padx=2,pady=5)

    # Content area with scroll
    content_frame = tk.Frame(dashboard)
    content_frame.pack(side='right', fill='both', expand=True)

    content_canvas = tk.Canvas(content_frame, bg='white')
    content_canvas.pack(side='left', fill='both', expand=True)

    scrollbar = tk.Scrollbar(content_frame,
                             orient="vertical",
                             command=content_canvas.yview)
    scrollbar.pack(side='right', fill='y')

    content_canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside canvas for content area widgets
    content_area = tk.Frame(content_canvas, bg='white')
    content_canvas.create_window((0, 0), window=content_area, anchor='nw')

    # Function to update scrollbar region
    def on_content_configure(event):
        content_canvas.configure(scrollregion=content_canvas.bbox("all"))

    content_area.bind("<Configure>", on_content_configure)
    '''
    # Example widgets in the content area
    for i in range(30):  # Add multiple widgets to make the content scrollable
        tk.Label(content_area, text=f"Content Line {i+1}", bg='white').pack()
    '''
    # Update scroll region after adding widgets
    content_area.update_idletasks()
    content_canvas.configure(scrollregion=content_canvas.bbox("all"))

def open_find_my_device(email):
    # Check if the email domain is associated with a known tracking service
    if "@gmail.com" in email.lower():
        # Open Google Find My Device
        wb.open("https://www.google.com/android/find")
    elif "@icloud.com" in email.lower():
        # Open Apple Find My iPhone
        wb.open("https://www.icloud.com/find")
    else:
        # Unsupported email domain
        error_label = tk.Label(content_area, text="Unsupported email domain. Use a Google or iCloud email.", bg="red", fg="white")
        error_label.pack()

def locate_device_button():
    # Prompt the user to enter their email address
    email = simpledialog.askstring("Enter Email", "Enter the email associated with your device:")
    if email:
        open_find_my_device(email)

def ConverttoPro():
    os.system("sc config wuauserv start= auto & net start wuauserv")

def open_axle_interface():
    os.system("python3 AxleInterfacev_7.py")

def upload_arduino_code():
        # Ask for the Arduino sketch file
        file_path = filedialog.askopenfilename(title="Select Arduino Sketch",
                                               filetypes=[("Arduino Files",
                                                           "*.ino")])
        if not file_path:
            return

        # Upload the code to the Arduino board
        try:
            # Replace 'COM_PORT' with your Arduino's COM port
            ardcom = simpledialog.askstring("Enter COM port",
                                            "Enter COM name below")
            os.system(
                f"arduino-cli upload -p {ardcom} --fqbn arduino:avr:uno {file_path}"
            )
            messagebox.showinfo("Success",
                                "Arduino code uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Failed to upload Arduino code: {e}")

def open_edit_arduino_code():
    file_path = filedialog.askopenfilename(title="Select Arduino Sketch",
                                               filetypes=[("Arduino Files",
                                                           "*.ino")])
    if not file_path:
            return

    with open(file_path, 'r') as file:
            file_content = file.read()

            # Create a new window for editing
            file_window = tk.Toplevel()
            file_window.title(f"Editing: {file_path}")
            file_window.geometry("600x400")

            text_area = tk.Text(file_window, wrap='word')
            text_area.pack(expand=True, fill='both')
            text_area.insert('1.0', file_content)

            def save_changes():
                with open(file_path, 'w') as file:
                    file.write(text_area.get('1.0', tk.END))
                    messagebox.showinfo("Success",
                                    "Arduino file saved successfully!")
            save_button = tk.Button(file_window, text="Save", command=save_changes)
            save_button.pack(pady=10)

def clone_repository():
    wb.open("github.com")
"""
"""
def monitorinfoapp():
    os.system("python3 monitor.py")
def open_profile(username, content_area, user_listbox_dashboard):
    for widget in content_area.winfo_children():
        widget.destroy()

    user_data = load_user_data()
    current_password = user_data[username]

    def update_profile():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        if not new_username or not new_password:
            messagebox.showerror("Error",
                                 "Username and password cannot be empty.")
            return

        if new_username != username and new_username in user_data:
            messagebox.showerror("Error", "Username already exists.")
            return

        # Update the user data
        user_data.pop(username)
        user_data[new_username] = new_password
        save_user_data(user_data)

        # Update the user list in the dashboard
        update_user_list_dashboard(user_listbox_dashboard)

        messagebox.showinfo("Success", "Profile updated successfully!")

    # GUI elements for profile update
    profile_label = tk.Label(content_area,
                             text="Profile",
                             font=("Ubuntu", 18),
                             bg='white')
    profile_label.pack(pady=10)

    username_label = tk.Label(content_area,
                              text="New Username:",
                              font=("Ubuntu", 14),
                              bg='white')
    username_label.pack(pady=5)
    new_username_entry = tk.Entry(content_area, font=("Ubuntu", 14))
    new_username_entry.pack(pady=5)
    new_username_entry.insert(0, username)

    password_label = tk.Label(content_area,
                              text="New Password:",
                              font=("Ubuntu", 14),
                              bg='white')
    password_label.pack(pady=5)
    new_password_entry = tk.Entry(content_area, font=("Ubuntu", 14), show="*")
    new_password_entry.pack(pady=5)
    new_password_entry.insert(0, current_password)

    update_button = tk.Button(content_area,
                              text="Update Profile",
                              font=("Ubuntu", 14),
                              command=update_profile)
    update_button.pack(pady=10)


def System_area(content_area):
    monitorinfobutton=tk.Button(content_area,
                                    text="Monitor app",
                                    bg='black',
                                    fg='green',
                                    command=monitorinfoapp)
    monitorinfobutton.pack(fill='x', pady=2, padx=5)
    
    button_con = tk.Button(content_area,
                                    text="Convert to windows pro",
                                    bg='black',
                                    fg='green',
                                    command=lambda:ConverttoPro)
    button_con.pack(fill='x', pady=2, padx=5)
    
    button_folders = tk.Button(content_area,
                                    text="Show hidden folders",
                                    bg='green',
                                    fg='white',
                                    command=lambda:display_all_hidden_folders(content_area))
    button_folders.pack(fill='x', pady=2, padx=5)
    # Add buttons to the sidebar
    button_upload_arduino = tk.Button(content_area,
                                      text="Upload Arduino Code",
                                      bg='green',
                                      fg='white',
                                      command=upload_arduino_code)
    button_upload_arduino.pack(fill='x', pady=2, padx=5)

    button_edit_arduino = tk.Button(content_area,
                                    text="Edit Arduino Code",
                                    bg='green',
                                    fg='white',
                                    command=open_edit_arduino_code)
    button_edit_arduino.pack(fill='x', pady=2, padx=5)

    partition_menu_button = tk.Button(content_area,
                                      text="Enter partition CMD",
                                      bg="black",
                                      fg="white",
                                      command=diskpart)
    partition_menu_button.pack(padx=15, pady=3)

    user_settings_button = tk.Button(content_area,
                                     text="Open user access settings",
                                     bg="black",
                                     fg="white",
                                     command=user_display)
    user_settings_button.pack(padx=15, pady=3)

    display_users_button = tk.Button(content_area,
                                     text="Show all users",
                                     bg="black",
                                     fg="white",
                                     command=lambda: user_show(content_area))
    display_users_button.pack(padx=15, pady=3)

    activate_users = tk.Button(content_area,
                               text="Activate a user",
                               bg="black",
                               fg="white",
                               command=user_activate)
    activate_users.pack(padx=15, pady=3)

    open_cmd = tk.Button(content_area,
                         text="Open CMD",
                         bg="black",
                         fg="white",
                         command=open_CMD)
    open_cmd.pack(padx=15, pady=3)

    install_app = tk.Button(content_area,
                            text="Install using winget",
                            bg="black",
                            fg="white",
                            command=lambda: installer(content_area))
    install_app.pack(padx=15, pady=1)

    button_encrypt = tk.Button(content_area,
                               text="Encrypt File",
                               bg='gray',
                               fg='black',
                               command=encrypt_file)
    button_encrypt.pack(fill='x', pady=2, padx=5)

    button_decrypt = tk.Button(content_area,
                               text="Decrypt File",
                               bg='gray',
                               fg='black',
                               command=decrypt_file)
    button_decrypt.pack(fill='x', pady=2, padx=5)

    button_OSmakeropen = tk.Button(content_area,
                                   text="Open OS maker",
                                   bg='gray',
                                   fg='black',
                                   command=open_OSmaker)
    button_OSmakeropen.pack(fill='x', pady=2, padx=5)

    button_usersinfo = tk.Button(
        content_area,
        text="Show user data",
        bg="black",
        fg="white",
        command=lambda: userinfodisplayseq(content_area))
    button_usersinfo.pack(fill='x', pady=2, padx=5)

    createIP = tk.Button(content_area,
                         text="Create new IP",
                         bg="cyan",
                         fg="black",
                         command=create_ip_address)
    createIP.pack(fill='x')

    connectIP = tk.Button(content_area,
                          text="Connect to IP",
                          bg="cyan",
                          fg="black",
                          command=connect_to_ip)
    connectIP.pack(fill='x')

    AppsList=tk.Button(content_area,text="Winget installed apps",bg="green",fg="black",command=lambda:display_all_installed_apps(content_area))
    AppsList.pack(fill='x')

    powershell_button=tk.Button(content_area,text="Open Powershell",bg="green",fg="black",command=powershell_open)
    powershell_button.pack(fill='x')

    openregedit=tk.Button(content_area,text="Open registry editor",bg="green",fg="black",command=regedit)
    openregedit.pack(fill='x')

    InstallGodMode=tk.Button(content_area,text="Install Super God Mode",bg="green",fg="black",command=InstallGodModePro)
    InstallGodMode.pack(fill='x')

    PIPinspectbutton=tk.Button(content_area,text="show python environment data",bg="green",fg="black",command=lambda:PIPinspect(content_area))
    PIPinspectbutton.pack(fill='x')

def PIPinspect(content_area):
    # Clear previous content in the content area
    for widget in content_area.winfo_children():
        widget.destroy()

    # Run the command and capture its output
    try:
        result = subprocess.check_output("pip3 inspect",
                                         shell=True,
                                         text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e}"

    # Display the result in a Text widget
    text_widget = tk.Text(content_area, wrap='word', font=("Ubuntu", 12))
    text_widget.insert('1.0', result)
    text_widget.pack(expand=True, fill='both')

def display_all_installed_apps(content_area):
    try:
        # Get the list of installed apps using winget
        result = subprocess.check_output(
            "winget list",
            shell=True,
            text=True,
            encoding='utf-8'
        )
        
        # Split the result into lines
        apps = result.split('\n')
        
        # Create a .csv file and write the apps list into it
        with open("installed_apps.csv", mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write headers (assuming winget outputs Name, ID, Version, etc.)
            writer.writerow(["Name", "ID", "Version", "Source"])
            
            # Display headers in the GUI
            tree = ttk.Treeview(content_area, columns=("Name", "ID", "Version", "Source"), show="headings")
            tree.heading("Name", text="Name")
            tree.heading("ID", text="ID")
            tree.heading("Version", text="Version")
            tree.heading("Source", text="Source")
            tree.pack(fill="both", expand=True)
            
            # Write each app's information into the CSV and display in the GUI
            for app in apps:
                # Split each app's info into columns by whitespace
                app_info = app.split()
                if len(app_info) >= 4:  # Make sure there are enough columns
                    writer.writerow(app_info[:4])  # Adjust according to the output structure
                    # Insert the app info into the Treeview (GUI)
                    tree.insert("", tk.END, values=app_info[:4])

        # Display a success message in the content_area
        success_label = tk.Label(content_area, text="Data saved to installed_apps.csv", bg="green", fg="white")
        success_label.pack()

    except subprocess.CalledProcessError as e:
        error_label = tk.Label(content_area, text=f"Error: {str(e)}", bg="red", fg="white")
        error_label.pack()

    except Exception as e:
        error_label = tk.Label(content_area, text=f"Exception: {str(e)}", bg="red", fg="white")
        error_label.pack()



def regedit():
    os.system("regedit.exe")

def InstallGodModePro():
    wb.open("https://github.com/ThioJoe/Windows-Super-God-Mode")

def powershell_open():
    os.system("powershell")
    
def display_all_hidden_folders(content_area):
    # Clear previous content in the content area
    for widget in content_area.winfo_children():
        widget.destroy()

    # Run the command and capture its output
    try:
        result = subprocess.check_output("dir /r",
                                         shell=True,
                                         text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e}"

    # Display the result in a Text widget
    text_widget = tk.Text(content_area, wrap='word', font=("Ubuntu", 12))
    text_widget.insert('1.0', result)
    text_widget.pack(expand=True, fill='both')

def create_ip_address():
    ip_str = simpledialog.askstring("IP entry", "IP entry system")
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip
    except ValueError as e:
        print(f"Invalid IP address: {e}")
        return None


def connect_to_ip():
    os.system("python3 IPconnect.py")


def open_OSmaker():
    os.system("python3 AxleOS.py")


def show_recent_files(content_area):
    for widget in content_area.winfo_children():
        widget.destroy()

    recent_files = load_recent_files()
    if not recent_files:
        no_recent_files_label = tk.Label(content_area,
                                         text="No recent files.",
                                         font=("Ubuntu", 14),
                                         bg='white')
        no_recent_files_label.pack(pady=10)
    else:
        recent_files_label = tk.Label(content_area,
                                      text="Recent Files",
                                      font=("Ubuntu", 18),
                                      bg='white')
        recent_files_label.pack(pady=10)

        for file_path in recent_files:
            file_button = tk.Button(content_area,
                                    text=file_path,
                                    font=("Ubuntu", 14),
                                    bg='white',
                                    command=lambda p=file_path: open_file(p))
            file_button.pack(pady=5)


def open_file_dialog(selected_language):
    if not selected_language:
        messagebox.showerror("Error", "Please select a programming language.")
        return

    filetypes = PROGRAMMING_LANGUAGES.get(selected_language,
                                          [("All Files", "*.*")])
    file_path = filedialog.askopenfilename(filetypes=filetypes)

    if file_path:
        open_file(file_path)


def open_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    save_recent_file(file_path)

    file_window = tk.Toplevel()
    file_window.title(f"Editing: {file_path}")
    file_window.geometry("600x400")

    text_area = tk.Text(file_window, wrap='word')
    text_area.pack(expand=True, fill='both')
    text_area.insert('1.0', file_content)

    def save_changes():
        with open(file_path, 'w') as file:
            file.write(text_area.get('1.0', tk.END))
        messagebox.showinfo("Success", "File saved successfully!")

    save_button = tk.Button(file_window, text="Save", command=save_changes)
    save_button.pack(pady=10)


def open_install_package_dialog():
    package_name = simpledialog.askstring(
        "Install Package", "Enter the package name to install:")
    if package_name:
        try:
            os.system(f"pip install {package_name}")
            messagebox.showinfo(
                "Success", f"Package '{package_name}' installed successfully!")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to install package '{package_name}': {e}")


def diskpart():
    os.system("diskpart")


def logout():
    global dashboard
    if dashboard:
        dashboard.destroy()
    w.deiconify()


def update_user_list():
    user_data = load_user_data()
    user_listbox.delete(0, tk.END)
    for username in user_data.keys():
        user_listbox.insert(tk.END, username)


def update_user_list_dashboard(user_listbox_dashboard):
    user_listbox_dashboard.delete(0, tk.END)
    user_data = load_user_data()
    for username in user_data:
        user_listbox_dashboard.insert(tk.END, username)


def quit():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        w.destroy()


def open_file_manager():
    os.system("explorer.exe")


def open_control_panel():
    os.system("control.exe")


def user_display():
    messagebox.showinfo("User accessibility", "User access settings opened")
    os.system("netplwiz")


def user_show(content_area):
    # Clear previous content in the content area
    for widget in content_area.winfo_children():
        widget.destroy()

    # Run the command and capture its output
    try:
        result = subprocess.check_output("net user", shell=True, text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e}"

    # Display the result in a Text widget
    text_widget = tk.Text(content_area, wrap='word', font=("Ubuntu", 12))
    text_widget.insert('1.0', result)
    text_widget.pack(expand=True, fill='both')

    # Disable the text widget so the content is read-only
    text_widget.config(state='disabled')


def web():
    ask = simpledialog.askstring("Link name", "Enter website name below")
    if ask == "Colab" or ask == "colab":
        wb.open("colab.research.google.com")
    elif ask == "Github" or ask == "github":
        wb.open("github.com")
    elif ask == "Google" or ask == "google":
        wb.open("google.com")
    elif ask == "Replit" or ask == "replit":
        wb.open("www.replit.com")


def user_activate():
    username = simpledialog.askstring(
        "username input", "enter system username here for reactivation")
    os.system(f"net user {username} \active=yes")


def permission_access():
    messagebox.askyesno(
        "Permissions warning",
        "It appears you have chosen to use master ownership abilities\n So we must warn you that once you use this ability\n There is no going back."
    )
    path = simpledialog.askstring("Path Input",
                                  "Enter the file or folder path - ")
    try:
        # Taking ownership of the file/folder
        takeown_command = f'takeown /F "{path}" /R /D Y'
        os.system(takeown_command)
        '''
        # Granting full permissions to the specified user
        icacls_command = f'icacls "{path}" /grant {username}:F /T'
        os.system(icacls_command)
        '''
        print(f"Ownership and full permissions granted for {path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def open_website():
    webinput = simpledialog.askstring("Open website", "Enter URL below v")
    wb.open(webinput)


def open_CMD():
    os.system("cmd")


def installer(content_area):
    i = simpledialog.askstring("Installer", "Install application")
    # Clear previous content in the content area
    for widget in content_area.winfo_children():
        widget.destroy()

    # Run the command and capture its output
    try:
        result = subprocess.check_output(f"winget install {i}",
                                         shell=True,
                                         text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e}"

    # Display the result in a Text widget
    text_widget = tk.Text(content_area, wrap='word', font=("Ubuntu", 12))
    text_widget.insert('1.0', result)
    text_widget.pack(expand=True, fill='both')

    # Disable the text widget so the content is read-only
    text_widget.config(state='disabled')


def encrypt_file():
    # Get the file path from the user
    file_path = simpledialog.askstring(
        "File Path", "Enter the file path you want to encrypt:")
    if not file_path:
        return  # Exit if no path is provided

    try:
        # Use the cipher command to encrypt the file
        result = subprocess.run(f'cipher /e "{file_path}"',
                                shell=True,
                                capture_output=True,
                                text=True)
        if "encrypted" in result.stdout.lower():
            messagebox.showinfo("Success",
                                f"File '{file_path}' encrypted successfully!")
        else:
            messagebox.showerror(
                "Error",
                f"Failed to encrypt file '{file_path}': {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred while encrypting: {e}")


def decrypt_file():
    # Get the file path from the user
    file_path = simpledialog.askstring(
        "File Path", "Enter the file path you want to decrypt:")
    if not file_path:
        return  # Exit if no path is provided

    try:
        # Use the cipher command to decrypt the file
        result = subprocess.run(f'cipher /d "{file_path}"',
                                shell=True,
                                capture_output=True,
                                text=True)
        if "decrypted" in result.stdout.lower():
            messagebox.showinfo("Success",
                                f"File '{file_path}' decrypted successfully!")
        else:
            messagebox.showerror(
                "Error",
                f"Failed to decrypt file '{file_path}': {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred while decrypting: {e}")


def userinfodisplayseq(content_area):
    # Clear previous content in the content area
    for widget in content_area.winfo_children():
        widget.destroy()

    # Run the command and capture its output
    try:
        infoask = simpledialog.askstring("Show user data",
                                         "Enter username for information")
        result = subprocess.check_output(f"net user {infoask}",
                                         shell=True,
                                         text=True)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e}"

    # Display the result in a Text widget
    text_widget = tk.Text(content_area, wrap='word', font=("Ubuntu", 12))
    text_widget.insert('1.0', result)
    text_widget.pack(expand=True, fill='both')

'''
def encryptor():
    path = simpledialog.askstring("Path", "Enter folder path")
    if not path:
        return  # Exit if no path is provided
    # Get the password from the user
    passkey = simpledialog.askstring("Password", "Enter folder password", show='X')
    if not passkey:
        messagebox.showerror("Error","no password found")
        return  # Exit if no password is provided
    try:
        # Open the file in binary mode for reading
        with open(path, 'rb') as file:
            data = file.read()
        # Create a Fernet object with the password as the key
        f = Fernet(passkey.encode()) 
        # Encrypt the data
        encrypted_data = f.encrypt(data)
        # Write the encrypted data back to the file
        with open(path, 'wb') as file:
            file.write(encrypted_data)
        messagebox.showinfo("Success", f"File '{path}' encrypted successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{path}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while encrypting: {e}")
'''
# Main window
w = tk.Tk()
w.title("AxleOwner Interface")
w.geometry("400x300")

textext = tk.Label(w, text="Login", font=("Ubuntu", 15))
textext.pack(pady=10, padx=10)

# User list box
user_listbox = tk.Listbox(w)
user_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
update_user_list()

# Login and create account buttons
button_login = tk.Button(w, text="Login", command=login)
button_login.pack(pady=5)

button_create_account = tk.Button(w, text="Register", command=create_account)
button_create_account.pack(pady=5)

w.mainloop()
