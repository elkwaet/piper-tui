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
        self.root.configure(bg="#222222", highlightthickness=1, highlightbackground="#555555")
        
        # Geometry
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        w, h = 110, 48
        
        # Default position (bottom center)
        x = (screen_width // 2) - (w // 2)
        y = screen_height - h - 60
        
        # Load saved position if exists
        try:
            from pathlib import Path
            self.pos_file = Path.home() / ".config" / "piper-tui" / "widget_pos.txt"
            if self.pos_file.exists():
                with open(self.pos_file, "r") as f:
                    pos = f.read().strip()
                    if "+" in pos:
                        saved_x, saved_y = pos.split("+")
                        x, y = int(saved_x), int(saved_y)
        except Exception:
            pass

        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        # State
        self.is_paused = False
        
        # Drag logic bindings
        self._offsetx = 0
        self._offsety = 0
        self.root.bind('<Button-1>', self.clickwin)
        self.root.bind('<B1-Motion>', self.dragwin)
        self.root.bind('<ButtonRelease-1>', self.save_position)
        
        # UI (Frame acts as the "grip" border)
        self.frame = tk.Frame(self.root, bg="#222222", cursor="fleur")
        self.frame.pack(expand=True, fill="both")
        
        # Binding drag directly on the frame too, for better UX
        self.frame.bind('<Button-1>', self.clickwin)
        self.frame.bind('<B1-Motion>', self.dragwin)
        self.frame.bind('<ButtonRelease-1>', self.save_position)
        
        self.btn_play_pause = tk.Button(
            self.frame, text="⏸", bg=BTN_BG, fg=FG_COLOR, 
            activebackground=BTN_ACTIVE_BG, borderwidth=0, 
            command=self.toggle_pause, font=("Arial", 16)
        )
        self.btn_play_pause.pack(side="left", expand=True, fill="both", padx=(4, 2), pady=4)
        
        self.btn_stop = tk.Button(
            self.frame, text="⏹", bg=BTN_BG, fg=FG_COLOR, 
            activebackground=BTN_ACTIVE_BG, borderwidth=0, 
            command=self.stop_playback, font=("Arial", 16)
        )
        self.btn_stop.pack(side="left", expand=True, fill="both", padx=(2, 4), pady=4)
        
        # Polling: check if piper is still running
        self.check_process()
        
    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def dragwin(self, event):
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f"+{x}+{y}")
        
    def save_position(self, event):
        try:
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            with open(self.pos_file, "w") as f:
                f.write(f"{x}+{y}")
        except Exception:
            pass
        
    def toggle_pause(self):
        if not self.is_paused:
            subprocess.run("pkill -STOP -x piper", shell=True)
            subprocess.run("pkill -STOP -x aplay", shell=True)
            self.btn_play_pause.config(text="▶")
            self.is_paused = True
        else:
            subprocess.run("pkill -CONT -x piper", shell=True)
            subprocess.run("pkill -CONT -x aplay", shell=True)
            self.btn_play_pause.config(text="⏸")
            self.is_paused = False
            
    def stop_playback(self):
        subprocess.run("pkill -TERM -x piper", shell=True)
        subprocess.run("pkill -TERM -x aplay", shell=True)
        self.root.destroy()
        
    def check_process(self):
        # Poll every 1 second: if both piper and aplay are dead, close widget automatically
        # For short texts, piper finishes quickly but aplay continues playing the buffer.
        res_aplay = subprocess.run("pgrep -x aplay", shell=True, capture_output=True)
        res_piper = subprocess.run("pgrep -x piper", shell=True, capture_output=True)
        if not res_aplay.stdout.strip() and not res_piper.stdout.strip():
            self.root.destroy()
        else:
            self.root.after(1000, self.check_process)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingWidget(root)
    root.mainloop()
