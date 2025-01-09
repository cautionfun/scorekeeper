import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime


class ScoreKeeper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scorekeeper")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg='white')

        self.create_input_ui()
        self.root.mainloop()

    def create_input_ui(self):
        self.input_frame = tk.Frame(self.root, bg='white')
        self.input_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(self.input_frame, text="Player 1 Name:", font=("Helvetica", 24), bg='white').grid(row=0, column=0, padx=10, pady=10)
        self.player1_name_entry = tk.Entry(self.input_frame, font=("Helvetica", 24))
        self.player1_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.input_frame, text="Player 2 Name:", font=("Helvetica", 24), bg='white').grid(row=1, column=0, padx=10, pady=10)
        self.player2_name_entry = tk.Entry(self.input_frame, font=("Helvetica", 24))
        self.player2_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.input_frame, text="Point Total to Win:", font=("Helvetica", 24), bg='white').grid(row=2, column=0, padx=10, pady=10)
        self.point_goal_entry = tk.Entry(self.input_frame, font=("Helvetica", 24))
        self.point_goal_entry.grid(row=2, column=1, padx=10, pady=10)

        submit_button = tk.Button(self.input_frame, text="Start Game", font=("Helvetica", 24), command=self.start_game)
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

    def start_game(self):
        player1_name = self.player1_name_entry.get()
        player2_name = self.player2_name_entry.get()
        point_goal = self.point_goal_entry.get()

        if not player1_name or not player2_name or not point_goal.isdigit():
            messagebox.showerror("Error", "Please enter valid inputs for all fields.")
            return

        self.player1_name = player1_name
        self.player2_name = player2_name
        self.point_goal = int(point_goal)
        self.player1_score = 0
        self.player2_score = 0

        self.input_frame.destroy()
        self.setup_game_ui()

    def setup_game_ui(self):
        self.left_frame = tk.Frame(self.root, bg='white', width=self.root.winfo_screenwidth() // 2, height=self.root.winfo_screenheight())
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_frame.bind("<Button-1>", self.increment_player1_score)

        self.right_frame = tk.Frame(self.root, bg='white', width=self.root.winfo_screenwidth() // 2, height=self.root.winfo_screenheight())
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.right_frame.bind("<Button-1>", self.increment_player2_score)

        self.player1_label = tk.Label(self.left_frame, text=self.player1_name, font=("Helvetica", 48), bg='white')
        self.player1_label.pack(expand=True)
        self.player1_score_label = tk.Label(self.left_frame, text=str(self.player1_score), font=("Helvetica", 96), bg='white')
        self.player1_score_label.pack(expand=True)

        self.player2_label = tk.Label(self.right_frame, text=self.player2_name, font=("Helvetica", 48), bg='white')
        self.player2_label.pack(expand=True)
        self.player2_score_label = tk.Label(self.right_frame, text=str(self.player2_score), font=("Helvetica", 96), bg='white')
        self.player2_score_label.pack(expand=True)

        self.divider = tk.Frame(self.root, bg='black', width=2, height=self.root.winfo_screenheight())
        self.divider.place(relx=0.5, rely=0, anchor='n')

    def increment_player1_score(self, event):
        self.player1_score += 1
        self.update_scores()
        self.check_winner()

    def increment_player2_score(self, event):
        self.player2_score += 1
        self.update_scores()
        self.check_winner()

    def update_scores(self):
        self.player1_score_label.config(text=str(self.player1_score))
        self.player2_score_label.config(text=str(self.player2_score))

    def check_winner(self):
        if self.player1_score >= self.point_goal or self.player2_score >= self.point_goal:
            score_diff = abs(self.player1_score - self.player2_score)
            if score_diff >= 2:
                winner = self.player1_name if self.player1_score > self.player2_score else self.player2_name
                self.save_game_history()
                self.show_game_over_dialog(winner)

    def save_game_history(self):
        date = datetime.now().strftime("%m%d%y")
        with open("game_history.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.player1_name, self.player2_name, self.player1_score, self.player2_score, date])

    def show_game_over_dialog(self, winner):
        response = messagebox.askquestion("Game Over", f"{winner} wins! Would you like a rematch?\nClick 'No' to create a new game.", icon='question')
        if response == "yes":  # "Rematch" chosen
            self.reset_game()
        elif response == "no":  # "New Game" chosen
            self.new_game()

    def reset_game(self):
        self.player1_score = 0
        self.player2_score = 0
        self.update_scores()

    def new_game(self):
        self.left_frame.destroy()
        self.right_frame.destroy()
        self.divider.destroy()
        self.create_input_ui()


if __name__ == "__main__":
    ScoreKeeper()
