import tkinter as tk
import webview

class CromehackFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.btn_open_browser = tk.Button(
            self,
            text="Open Browser",
            command=self.open_browser,
            bg="#282c34",
            fg="#61afef",
            font=("Consolas", 14)
        )
        self.btn_open_browser.pack(pady=20)

        self.webview_window = None
        self.browser_open = False

    def open_browser(self):
        if self.browser_open:
            # Already open, prevent opening more windows
            return

        self.browser_open = True
        self.webview_window = webview.create_window(
            "CromeHack",
            "cromehack.html",
            width=900,
            height=600,
            resizable=True,
            fullscreen=False,
        )
        # webview.start with gui='tk' does NOT block and allows coexistence with tkinter
        webview.start(gui='tk', debug=True)
        self.browser_open = False
