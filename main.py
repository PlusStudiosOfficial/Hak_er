import tkinter as tk
from tkinter import ttk
from terminal import TerminalFrame
from cromehack import CromehackFrame

class FictionalPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hak_er")
        self.root.geometry("1024x700")
        self.root.configure(bg="#282c34")

        # Classic OS style title bar
        self.title_bar = tk.Frame(root, bg="#21252b", relief="raised", bd=2, height=35)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        # Logo and title
        self.logo = tk.Label(self.title_bar, text="Hak_OS", bg="#21252b", fg="#61afef", font=("Consolas", 16, "bold"))
        self.logo.pack(side=tk.LEFT, padx=10)

        # Window buttons (minimize, close)
        self.btn_minimize = tk.Button(self.title_bar, text="—", command=self.minimize, bg="#21252b", fg="white", bd=0, padx=10, font=("Consolas", 14))
        self.btn_minimize.pack(side=tk.RIGHT, padx=2)
        self.btn_close = tk.Button(self.title_bar, text="✕", command=self.root.quit, bg="#e06c75", fg="white", bd=0, padx=10, font=("Consolas", 14))
        self.btn_close.pack(side=tk.RIGHT, padx=2)

        # Taskbar-style navigation bar
        self.nav_bar = tk.Frame(root, bg="#21252b", height=40)
        self.nav_bar.pack(fill=tk.X, side=tk.TOP)

        self.btn_terminal = ttk.Button(self.nav_bar, text="Terminal", command=self.show_terminal)
        self.btn_terminal.pack(side=tk.LEFT, padx=8, pady=5)

        self.btn_cromehack = ttk.Button(self.nav_bar, text="CromeHack", command=self.show_cromehack)
        self.btn_cromehack.pack(side=tk.LEFT, padx=8, pady=5)

        # Content frame (terminal or browser)
        self.content_frame = tk.Frame(root, bg="#1e2127")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Instantiate apps
        self.terminal_frame = TerminalFrame(self.content_frame)
        self.cromehack_frame = CromehackFrame(self.content_frame)

        self.show_terminal()

    def minimize(self):
        self.root.iconify()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

    def show_terminal(self):
        self.clear_content_frame()
        self.terminal_frame.pack(fill=tk.BOTH, expand=True)

    def show_cromehack(self):
        self.clear_content_frame()
        self.cromehack_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")  # Clean and modern theme
    app = FictionalPCApp(root)
    root.mainloop()
