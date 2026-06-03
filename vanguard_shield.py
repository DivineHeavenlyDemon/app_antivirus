import os
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import psutil
import datetime
import shutil

# --- TACTICAL PATHS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUARANTINE_DIR = os.path.join(SCRIPT_DIR, "quarantine")
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")

class VanguardShieldV1:
    def __init__(self, root):
        self.root = root
        self.root.title("VANGUARD: SHIELD MALWARE ANALYZER")
        self.root.geometry("950x750")
        self.root.configure(bg="#0d1117")

        self.scanning = False
        self.setup_ui()
        self.heartbeat()
        self.log("SYSTEM", "Vanguard Shield Online. Quarantine Protocol Active.", "INFO")

    def setup_ui(self):
        # 1. HEADER
        header = tk.Frame(self.root, bg="#161b22", pady=10)
        header.pack(fill="x")
        tk.Label(header, text="🛡️ VANGUARD SHIELD", bg="#161b22", fg="#ff7b72", font=("Arial", 12, "bold")).pack(side="left", padx=20)
        self.ram_label = tk.Label(header, text="RAM: 0%", bg="#161b22", fg="#79c0ff", font=("Courier", 10))
        self.ram_label.pack(side="right", padx=20)

        # 2. CONTROL PANEL
        ctrl = tk.Frame(self.root, bg="#0d1117", pady=20)
        ctrl.pack(fill="x", padx=20)
        
        tk.Button(ctrl, text="📁 SELECT TARGET", command=self.select_file, bg="#238636", fg="white", font=("Arial", 10, "bold"), padx=20).pack(side="left")
        
        self.file_var = tk.StringVar(value="Select file for deep analysis...")
        self.file_entry = tk.Entry(ctrl, textvariable=self.file_var, bg="#161b22", fg="#8b949e", state="readonly", 
                                   borderwidth=1, relief="flat", highlightthickness=1, highlightbackground="#30363d")
        self.file_entry.pack(side="left", fill="x", expand=True, padx=15)

        # 3. TERMINAL LOG
        log_frame = tk.LabelFrame(self.root, text=" INTELLIGENCE & THREAT REPORTS ", bg="#0d1117", fg="#8b949e", font=("Courier", 8))
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.terminal = tk.Text(log_frame, bg="black", fg="#00ff00", font=("Courier", 10), state="disabled", wrap="word")
        self.terminal.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.terminal.tag_config("INFO", foreground="#00ff00")
        self.terminal.tag_config("WARN", foreground="#f1c40f")
        self.terminal.tag_config("THREAT", foreground="#ff3333", font=("Courier", 10, "bold"))

        # 4. STATUS BAR
        self.status = tk.Label(self.root, text="READY FOR SCOUTING", bg="#21262d", fg="white")
        self.status.pack(side="bottom", fill="x")

    def log(self, sender, msg, level="INFO"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.terminal.config(state="normal")
        self.terminal.insert("end", f"[{ts}] [{sender}] ", "INFO")
        self.terminal.insert("end", f"{msg}\n", level)
        self.terminal.see("end")
        self.terminal.config(state="disabled")

    def select_file(self):
        if self.scanning: return
        path = filedialog.askopenfilename()
        if path:
            self.file_var.set(path)
            self.log("SHIELD", f"Locking target: {os.path.basename(path)}", "WARN")
            self.engage_scan(path)

    def engage_scan(self, path):
        self.scanning = True
        self.status.config(text="SCANNING TARGET...", bg="#7f1d1d")
        threading.Thread(target=self.run_clamscan, args=(path,), daemon=True).start()

    def run_clamscan(self, path):
        try:
            # Clamscan command: -i shows infected files only
            process = subprocess.Popen(
                ['clamscan', '-i', path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.root.after(0, lambda: self.log("RESULT", "TARGET CLEAN. No threat patterns found.", "INFO"))
            elif process.returncode == 1:
                self.root.after(0, lambda: self.log("ALERT", "🚨 THREAT DETECTED! INITIATING QUARANTINE...", "THREAT"))
                self.quarantine_file(path, stdout)
            else:
                self.root.after(0, lambda: self.log("ERROR", f"Scanner failure: {stderr}", "THREAT"))

        except Exception as e:
            self.root.after(0, lambda: self.log("CRITICAL", str(e), "THREAT"))
        
        self.root.after(0, self.reset_ui)

    def quarantine_file(self, source_path, scan_report):
        """Moves infected file to the quarantine folder and renames it."""
        try:
            filename = os.path.basename(source_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"THREAT_{timestamp}_{filename}.locked"
            dest_path = os.path.join(QUARANTINE_DIR, new_name)
            
            shutil.move(source_path, dest_path)
            self.root.after(0, lambda: self.log("SHIELD", f"Quarantined to: {new_name}", "WARN"))
            
            # Save a log report
            log_name = f"REPORT_{timestamp}_{filename}.txt"
            with open(os.path.join(LOGS_DIR, log_name), "w") as f:
                f.write(f"VANGUARD THREAT REPORT\n{'='*30}\n")
                f.write(f"Source: {source_path}\nQuarantine: {dest_path}\n\n")
                f.write(f"CLAMAV OUTPUT:\n{scan_report}")
                
        except Exception as e:
            self.root.after(0, lambda: self.log("SHIELD", f"Quarantine failed: {str(e)}", "THREAT"))

    def reset_ui(self):
        self.scanning = False
        self.status.config(text="READY FOR SCOUTING", bg="#21262d")

    def heartbeat(self):
        ram = psutil.virtual_memory().percent
        self.ram_label.config(text=f"RAM: {ram}%", fg="#00ff00" if ram < 80 else "#ff3333")
        self.root.after(3000, self.heartbeat)

if __name__ == "__main__":
    root = tk.Tk()
    app = VanguardShieldV1(root)
    root.mainloop()
