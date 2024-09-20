import tkinter as tk
from tkinter import ttk
import requests
import json
import threading
import time
import socket
# from server_gui 
# run automatically when bash start.sh is running is started
class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Quiz Server GUI")
        master.geometry("900x600")
        master.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=('Arial', 12))
        self.style.configure("TButton", background="#584294", foreground="white", font=('Arial', 12))
        self.style.configure("Player.TFrame", background="#ffffff", borderwidth=1, relief="raised")
        self.style.configure("PlayerHeader.TLabel", background="#584294", foreground="white", font=('Arial', 14, 'bold'), padding=5)
        self.style.configure("PlayerInfo.TLabel", background="#ffffff", font=('Arial', 12), padding=2)
        self.style.configure("Horizontal.TProgressbar", background="#584294", troughcolor="#e0e0e0", bordercolor="#f0f0f0", lightcolor="#584294", darkcolor="#584294")

        self.main_frame = ttk.Frame(master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(self.main_frame, text="Quiz Server Status", font=('Arial', 24, 'bold'), foreground="#584294")
        self.title_label.pack(pady=20)

        self.players_canvas = tk.Canvas(self.main_frame, bg="#f0f0f0", highlightthickness=0)
        self.players_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.players_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.players_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.players_canvas.bind('<Configure>', lambda e: self.players_canvas.configure(scrollregion=self.players_canvas.bbox("all")))

        self.player_frame = ttk.Frame(self.players_canvas)
        self.players_canvas.create_window((0, 0), window=self.player_frame, anchor="nw")

        self.players = {}
        self.start_polling()
    def get_ip_address():
        """Get the IP address of the device running the server."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))  
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = "127.0.0.1"  
        finally:
            s.close()
        return ip_address

    def start_polling(self):
        def poll_server():
            while True:
                try:
                    response = requests.get('http://localhost:5001/get_status')
                    if response.status_code == 200:
                        data = response.json()
                        self.master.after(0, self.update_players, data)
                except requests.RequestException as e:
                    print(f"Error polling server: {e}")
                # poll every second
                time.sleep(1)  
        # start polling thread
        thread = threading.Thread(target=poll_server)
        thread.daemon = True
        thread.start()

    def update_players(self, players_data):
        for player_data in players_data:
            self.update_player(player_data)

    def update_player(self, data):
        player_id = data['player_id']
        if player_id not in self.players:
            player_frame = ttk.Frame(self.player_frame, padding="10", style="Player.TFrame")
            player_frame.pack(fill=tk.X, padx=10, pady=5)

            header_frame = ttk.Frame(player_frame)
            header_frame.pack(fill=tk.X)

            ip_label = ttk.Label(header_frame, text=f"Player: {player_id}", style="PlayerHeader.TLabel")
            ip_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            score_label = ttk.Label(header_frame, text="Score: 0", style="PlayerHeader.TLabel")
            score_label.pack(side=tk.RIGHT)

            question_label = ttk.Label(player_frame, text="Question: 0/5", style="PlayerInfo.TLabel")
            question_label.pack(anchor=tk.W, pady=(5, 0))

            answer_label = ttk.Label(player_frame, text="Last Answer: None", style="PlayerInfo.TLabel")
            answer_label.pack(anchor=tk.W)

            progress_bar = ttk.Progressbar(player_frame, length=200, mode='determinate', style="Horizontal.TProgressbar")
            progress_bar.pack(fill=tk.X, pady=(5, 0))

            game_over_label = ttk.Label(player_frame, text="", style="PlayerInfo.TLabel", foreground="#584294")
            game_over_label.pack(anchor=tk.W, pady=(5, 0))

            self.players[player_id] = {
                'frame': player_frame,
                'score': score_label,
                'question': question_label,
                'answer': answer_label,
                'progress': progress_bar,
                'game_over': game_over_label
            }
        else:
            player = self.players[player_id]
            player['score'].config(text=f"Score: {data['score']}")
            current_question = data['current_question'] + 1
            player['question'].config(text=f"Question: {current_question}/5")
            player['answer'].config(text=f"Last Answer: {data.get('last_answer', 'None')}")
            player['progress']['value'] = (current_question / 5) * 100
            
            if current_question > 5:
                player['game_over'].config(text=f"Game Over! Final Score: {data['score']}")
            else:
                player['game_over'].config(text="")

        self.players_canvas.configure(scrollregion=self.players_canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    gui = ServerGUI(root)
    root.mainloop()