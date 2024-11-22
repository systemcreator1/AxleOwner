import socket
import tkinter as tk
from tkinter import messagebox

# Function to scan ports automatically and find an open one
def find_open_port(ip_address):
    # Define a range of ports to scan (you can expand or modify this list)
    for port in range(20, 1025):  # Scanning common lower-range ports
        try:
            # Create socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)  # Set a short timeout to prevent long waits
            result = s.connect_ex((ip_address, port))  # Try to connect to the port
            
            if result == 0:
                # Port is open
                messagebox.showinfo("Connection Status", f"Successfully connected to {ip_address}:{port}")
                open_shell(s, ip_address, port)  # Open the shell upon successful connection
                return port  # Return the open port
            s.close()
        except Exception as e:
            print(f"Error trying port {port}: {e}")
    
    messagebox.showerror("No Open Port", "Could not find any open ports.")
    return None

# Function to open a basic interactive shell once connected
def open_shell(sock, ip_address, port):
    try:
        # Simple shell prompt to send commands
        while True:
            command = input(f"{ip_address}:{port}> ")
            if command.lower() == 'exit':
                break
            sock.send(command.encode() + b'\n')
            try:
                response = sock.recv(4096).decode()
                print(response)
            except socket.timeout:
                print("No response from the server.")
    except Exception as e:
        messagebox.showerror("Shell Error", f"Error during shell interaction: {e}")
    finally:
        sock.close()

# Function triggered by GUI to start the auto-connect process
def start_connection():
    ip_address = ip_entry.get()
    open_port = find_open_port(ip_address)
    if open_port:
        print(f"Open port found: {open_port}")
    else:
        print("No open ports were found.")

# Creating the GUI window
root = tk.Tk()
root.title("Port Finder and Shell Connector")

# IP Address Label and Entry
tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

# Connect Button
connect_button = tk.Button(root, text="Find Port and Connect", command=start_connection)
connect_button.grid(row=1, columnspan=2, pady=10)

# Start the tkinter loop
root.mainloop()
