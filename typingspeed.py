import tkinter as tk
from tkinter import messagebox
import time
import random
import json
import os

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("ProType v4.0 | Professional Speed Suite")
        self.root.geometry("950x650")
        self.root.configure(bg="#121212")

        # Persistence
        self.data_file = "typing_stats.json"
        self.stats = self.load_stats()
        
        self.sample_texts = [
            "Programming is not about what you know; it's about what you can figure out.",
            "The best way to predict the future is to invent it yourself.",
            "Quality is not an act, it is a habit that we must cultivate.",
            "To understand recursion, one must first understand recursion.",
            "Simplicity is the ultimate sophistication in modern design."
        ]
        
        self.target_text = random.choice(self.sample_texts)
        self.start_time = None
        self.running = False

        self.setup_ui()

    def load_stats(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except: pass
        return {"high_score": 0, "low_score": 0}

    def setup_ui(self):
        # --- SIDEBAR (Controls) ---
        self.sidebar = tk.Frame(self.root, bg="#1e1e1e", width=200)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="CONTROLS", fg="#555", bg="#1e1e1e", font=("Arial", 10, "bold")).pack(pady=20)

        # Reset Button
        self.btn_reset = tk.Button(self.sidebar, text="Reset Test", command=self.next_round, 
                                   bg="#3498db", fg="white", relief="flat", width=15, pady=10)
        self.btn_reset.pack(pady=10, padx=20)

        # Clear Stats Button
        self.btn_clear = tk.Button(self.sidebar, text="Clear Stats", command=self.clear_stats, 
                                   bg="#e67e22", fg="white", relief="flat", width=15, pady=10)
        self.btn_clear.pack(pady=10, padx=20)

        # Exit Button
        self.btn_exit = tk.Button(self.sidebar, text="Exit App", command=self.root.quit, 
                                  bg="#e74c3c", fg="white", relief="flat", width=15, pady=10)
        self.btn_exit.pack(side="bottom", pady=30)

        # --- MAIN CONTENT ---
        self.main_container = tk.Frame(self.root, bg="#121212")
        self.main_container.pack(side="right", expand=True, fill="both")

        # Persistent Stats Bar
        self.stats_bar = tk.Frame(self.main_container, bg="#252525", height=40)
        self.stats_bar.pack(fill="x")
        
        self.lbl_best = tk.Label(self.stats_bar, text=f"🏆 BEST: {self.stats['high_score']} WPM", 
                                 bg="#252525", fg="#2ecc71", font=("Arial", 11, "bold"))
        self.lbl_best.pack(side="left", padx=20)

        # Display Text
        self.sample_label = tk.Label(self.main_container, text=self.target_text, font=("Courier New", 20), 
                                     bg="#121212", fg="#ffffff", wraplength=600, pady=60)
        self.sample_label.pack()

        # Input Area
        self.input_entry = tk.Text(self.main_container, font=("Consolas", 16), height=4, width=50, 
                                   bg="#1e1e1e", fg="white", insertbackground="white", 
                                   padx=20, pady=20, relief="solid", borderwidth=1)
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<KeyPress>", self.start_timer)
        self.input_entry.bind("<KeyRelease>", self.check_typing)

        self.live_info = tk.Label(self.main_container, text="Ready to type?", bg="#121212", fg="#7f8c8d", font=("Arial", 12))
        self.live_info.pack(pady=20)

    def start_timer(self, event):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def check_typing(self, event):
        user_text = self.input_entry.get("1.0", tk.END).strip()
        if not user_text: return

        elapsed = max(time.time() - self.start_time, 0.1)
        wpm = round((len(user_text) / 5) / (elapsed / 60))
        
        # Color validation
        if self.target_text.startswith(user_text):
            self.input_entry.config(highlightbackground="#2ecc71", highlightthickness=2)
        else:
            self.input_entry.config(highlightbackground="#e74c3c", highlightthickness=2)

        self.live_info.config(text=f"Live Speed: {wpm} WPM")

        if user_text == self.target_text:
            self.running = False
            self.process_completion(wpm)

    def process_completion(self, wpm):
        # Update Data
        is_new_high = wpm > self.stats["high_score"]
        if is_new_high: self.stats["high_score"] = wpm
        
        if (self.stats["low_score"] == 0 or wpm < self.stats["low_score"]) and wpm > 5:
            self.stats["low_score"] = wpm

        with open(self.data_file, "w") as f:
            json.dump(self.stats, f)

        # Show result popup
        msg = f"Speed: {wpm} WPM\n" + ("🎉 NEW HIGH SCORE!" if is_new_high else "")
        messagebox.showinfo("Paragraph Complete", msg)
        
        self.lbl_best.config(text=f"🏆 BEST: {self.stats['high_score']} WPM")
        self.next_round()

    def clear_stats(self):
        if messagebox.askyesno("Confirm", "Reset all your lifetime statistics?"):
            self.stats = {"high_score": 0, "low_score": 0}
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            self.lbl_best.config(text="🏆 BEST: 0 WPM")

    def next_round(self):
        self.running = False
        self.start_time = None
        self.target_text = random.choice(self.sample_texts)
        self.sample_label.config(text=self.target_text)
        self.input_entry.delete("1.0", tk.END)
        self.input_entry.config(highlightthickness=0)
        self.live_info.config(text="Next round ready!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()