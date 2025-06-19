import tkinter as tk
from tkinter import scrolledtext

class TerminalFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.terminal_output = scrolledtext.ScrolledText(self, bg="black", fg="#33ff33", font=("Consolas", 12))
        self.terminal_output.pack(fill=tk.BOTH, expand=True)

        self.terminal_input = tk.Entry(self, bg="#111", fg="#33ff33", font=("Consolas", 12), insertbackground="#33ff33")
        self.terminal_input.pack(fill=tk.X)
        self.terminal_input.bind("<Return>", self.process_command)

        # Fake state
        self.servers = {
            "11231": {
                "name": "Qoogle",
                "passwords": ["lem0nP@ssw0rd", "s3cur3p@ssw0rd", "m1n1m4l1sm0", "PlusWithYou"],
                "mails": ["luis@moc", "ana@moc", "carlos@moc", "plusstudiosofficial@gmail.com"],
                "files": {
                    "passwords.txt": "lem0nP@ssw0rd\ns3cur3p@ssw0rd\nm1n1m4l1sm0\nPlusWithYou",
                    "config.sys": "system=active\nsecurity=high\nbackup=enabled",
                    "logs.log": "01/06/2025: Login success\n02/06/2025: Password changed"
                }
            },
            "44556": {
                "name": "Lemovo",
                "passwords": ["p4sSw0rdLem0vo", "lemov0s3cure", "securekeyboard"],
                "mails": ["maria@moc", "jose@moc", "carmen@moc"],
                "files": {
                    "passwords.txt": "p4sSw0rdLem0vo\nlemov0s3cure\nsecurekeyboard",
                    "config.sys": "system=standby\nsecurity=medium\nbackup=disabled",
                    "logs.log": "03/06/2025: System reboot\n04/06/2025: Firewall enabled"
                }
            }
        }

        self.connected_ip = None
        self.connected_server = None

        self.print_welcome()

    def print_welcome(self):
        self.write(" ===== Hak_OS Terminal =====")
        self.write("Type help() to get started.")

    def write(self, text):
        self.terminal_output.insert(tk.END, text + "\n")
        self.terminal_output.see(tk.END)

    def process_command(self, event):
        cmd = self.terminal_input.get().strip()
        if not cmd:
            return
        self.write(f"> {cmd}")
        self.terminal_input.delete(0, tk.END)
        try:
            response = self.handle_command(cmd)
            if response:
                self.write(response)
        except Exception as e:
            self.write(f"Internal ERROR: {e}")

    def handle_command(self, cmd):
        cmd_lower = cmd.lower()

        if cmd_lower == "help()":
            return (
                "Available commands:\n"
                "entry('IP')\nconnect('Server', 'pass')\nscan_servers()\n"
                "list_mails()\nread_mail('email')\nls_files()\ncat_file('file')\n"
                "shutdownserversof('IP')\nclear()\nwhoami()\ngetip()\nlistservers()\n"
                "ping('IP')\ntrace('IP')\nscanports('IP')\nlistprocesses()\n"
                "killprocess('name')\ngetosinfo()\ngetusers()\ncreatefile('file')\n"
                "deletefile('file')\nexit()"
            )

        if cmd_lower.startswith("entry("):
            ip = self.extract_arg(cmd)
            if ip in self.servers:
                self.connected_ip = ip
                return f"Connected to {self.servers[ip]['name']} (IP: {ip})"
            return "ERROR: IP not found."

        if cmd_lower == "scan_servers()":
            return self.list_servers()

        if cmd_lower.startswith("connect("):
            args = self.extract_args(cmd)
            if len(args) != 2:
                return "Usage: connect('Server', 'password')"
            if not self.connected_ip:
                return "ERROR: Not connected to any server."
            if "pass" in args[1].lower():
                self.connected_server = args[0]
                return f"Connected to server {args[0]}"
            return "Incorrect password."

        if cmd_lower == "list_mails()":
            return "\n".join(self.servers[self.connected_ip]["mails"]) if self.connected_ip else "ERROR: Not connected."

        if cmd_lower.startswith("read_mail("):
            mail = self.extract_arg(cmd)
            return f"Message from {mail}: Change your password urgently." if self.connected_ip and mail in self.servers[self.connected_ip]["mails"] else "ERROR: Mail not found."

        if cmd_lower == "ls_files()":
            return "\n".join(self.servers[self.connected_ip]["files"].keys()) if self.connected_ip else "ERROR: Not connected."

        if cmd_lower.startswith("cat_file("):
            filename = self.extract_arg(cmd)
            files = self.servers[self.connected_ip]["files"] if self.connected_ip else {}
            return files.get(filename, "ERROR: File not found.")

        if cmd_lower.startswith("shutdownserversof("):
            ip = self.extract_arg(cmd)
            return f"Shutting down {self.servers[ip]['name']}... OK" if ip in self.servers else "ERROR: Invalid IP."

        if cmd_lower == "clear()":
            self.terminal_output.delete('1.0', tk.END)
            return ""

        if cmd_lower == "whoami()":
            return "hacker@virtual_pc"

        if cmd_lower == "getip()":
            return f"Current IP: {self.connected_ip}" if self.connected_ip else "Not connected."

        if cmd_lower == "listservers()":
            return self.list_servers()

        if cmd_lower.startswith("ping("):
            ip = self.extract_arg(cmd)
            return f"Ping to {ip} -> OK"

        if cmd_lower.startswith("trace("):
            ip = self.extract_arg(cmd)
            return f"1 -> 192.168.0.1\n2 -> 10.0.0.1\n3 -> {ip}"

        if cmd_lower.startswith("scanports("):
            ip = self.extract_arg(cmd)
            return f"Scanning ports on {ip}: 80 open, 443 open"

        if cmd_lower == "listprocesses()":
            return "systemd\npython3\nbash\nexplorer.exe"

        if cmd_lower.startswith("killprocess("):
            proc = self.extract_arg(cmd)
            return f"Process '{proc}' terminated."

        if cmd_lower == "getosinfo()":
            return "+Studios OS v1.0.0 - Kernel H4kSim"

        if cmd_lower == "getusers()":
            return "admin\nroot\nguest"

        if cmd_lower.startswith("createfile("):
            filename = self.extract_arg(cmd)
            self.servers[self.connected_ip]["files"][filename] = ""
            return f"File '{filename}' created."

        if cmd_lower.startswith("deletefile("):
            filename = self.extract_arg(cmd)
            if filename in self.servers[self.connected_ip]["files"]:
                del self.servers[self.connected_ip]["files"][filename]
                return f"File '{filename}' deleted."
            return "File not found."

        if cmd_lower == "exit()":
            return "To close, use the system window."

        return "Command not recognized. Use help()"

    def extract_arg(self, cmd):
        try:
            return cmd[cmd.index("(")+1 : cmd.rindex(")")].strip("'\"")
        except:
            return ""

    def extract_args(self, cmd):
        try:
            args = cmd[cmd.index("(")+1 : cmd.rindex(")")].split(",")
            return [arg.strip().strip("'\"") for arg in args]
        except:
            return []

    def list_servers(self):
        return "\n".join([f"{data['name']} ({ip})" for ip, data in self.servers.items()])
