#!/usr/bin/env python3
import sys
import subprocess

try:
    import tkinter as tk
except ImportError:
    # Fail silently if Tkinter is missing (e.g. python3-tk missing on Ubuntu)
    sys.exit(0)

# Colors (Modern Dark Mode)
BG_COLOR = "#1e1e1e"
FG_COLOR = "#e0e0e0"
BTN_BG = "#333333"
BTN_ACTIVE_BG = "#555555"

class FloatingWidget:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG_COLOR, highlightthickness=1, highlightbackground="#444444")
        
        # Position bottom center
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        w, h = 100, 40
        x = (screen_width // 2) - (w // 2)
        y = screen_height - h - 60
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        # State
        self.is_paused = False
        
        # Drag logic bindings
        self._offsetx = 0
        self._offsety = 0
        self.root.bind('<Button-1>', self.clickwin)
        self.root.bind('<B1-Motion>', self.dragwin)
        
        # UI
        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.pack(expand=True, fill="both")
        
        self.btn_play_pause = tk.Button(
            self.frame, text="⏸", bg=BTN_BG, fg=FG_COLOR, 
            activebackground=BTN_ACTIVE_BG, borderwidth=0, 
            command=self.toggle_pause, font=("Arial", 16)
        )
        self.btn_play_pause.pack(side="left", expand=True, fill="both", padx=(1, 0), pady=1)
        
        self.btn_stop = tk.Button(
            self.frame, text="⏹", bg=BTN_BG, fg=FG_COLOR, 
            activebackground=BTN_ACTIVE_BG, borderwidth=0, 
            command=self.stop_playback, font=("Arial", 16)
        )
        self.btn_stop.pack(side="left", expand=True, fill="both", padx=(1, 1), pady=1)
        
        # Polling: check if piper is still running
        self.check_process()
        
    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def dragwin(self, event):
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f"+{x}+{y}")
        
    def toggle_pause(self):
        if not self.is_paused:
            subprocess.run("pkill -STOP -f 'piper/piper'", shell=True)
            subprocess.run("pkill -STOP -f 'aplay -r'", shell=True)
            self.btn_play_pause.config(text="▶")
            self.is_paused = True
        else:
            subprocess.run("pkill -CONT -f 'piper/piper'", shell=True)
            subprocess.run("pkill -CONT -f 'aplay -r'", shell=True)
            self.btn_play_pause.config(text="⏸")
            self.is_paused = False
            
    def stop_playback(self):
        subprocess.run("pkill -TERM -f 'piper/piper'", shell=True)
        subprocess.run("pkill -TERM -f 'aplay -r'", shell=True)
        self.root.destroy()
        
    def check_process(self):
        # Poll every 1 second: if piper process is dead, close widget automatically
        res = subprocess.run("pgrep -f 'piper/piper'", shell=True, capture_output=True)
        if not res.stdout.strip():
            self.root.destroy()
        else:
            self.root.after(1000, self.check_process)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingWidget(root)
    root.mainloop()
