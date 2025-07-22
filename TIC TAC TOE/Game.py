import tkinter as tk
from tkinter import messagebox

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("TIC TAC TOE — Made with ❤️ by Aman")
        self.root.geometry("420x540")
        self.root.config(bg="#121212")

        self.player = "X"
        self.ai = "O"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_title()
        self.create_board()

    def create_title(self):
        tk.Label(
            self.root,
            text="TIC TAC TOE — Made by Aman",
            font=("Segoe UI", 18, "bold"),
            bg="#121212",
            fg="#00f0ff",
            pady=20
        ).pack()

    def create_board(self):
        frame = tk.Frame(self.root, bg="#121212")
        frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    frame,
                    text="",
                    font=("Segoe UI", 36, "bold"),
                    width=4,
                    height=2,
                    bg="#1e1e2f",
                    fg="#f0f0f0",
                    activebackground="#00adb5",
                    relief="flat",
                    command=lambda r=i, c=j: self.player_move(r, c)
                )
                btn.grid(row=i, column=j, padx=6, pady=6)
                self.buttons[i][j] = btn

        self.reset_btn = tk.Button(
            self.root,
            text="🔁 Play Again",
            font=("Segoe UI", 14),
            bg="#00adb5",
            fg="#ffffff",
            activebackground="#007b8a",
            relief="flat",
            padx=10,
            pady=5,
            command=self.reset_game
        )
        self.reset_btn.pack(pady=20)

    def player_move(self, row, col):
        if self.board[row][col] == "" and not self.check_winner(self.player) and not self.check_winner(self.ai):
            self.board[row][col] = self.player
            self.buttons[row][col]["text"] = self.player

            if self.check_winner(self.player):
                self.highlight_winner(self.player)
                messagebox.showinfo("Game Over", "🎉 You Win!")
                self.disable_buttons()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.disable_buttons()
            else:
                self.root.after(400, self.ai_move)

    def ai_move(self):
        best_score = float('-inf')
        move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = self.ai
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)

        if move:
            i, j = move
            self.board[i][j] = self.ai
            self.buttons[i][j]["text"] = self.ai

            if self.check_winner(self.ai):
                self.highlight_winner(self.ai)
                messagebox.showinfo("Game Over", "😎 AI Wins!")
                self.disable_buttons()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.disable_buttons()

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner_on_board(board, self.ai):
            return 1
        if self.check_winner_on_board(board, self.player):
            return -1
        if all(cell != "" for row in board for cell in row):
            return 0

        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.ai
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best = max(best, score)
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.player
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best = min(best, score)
            return best

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                self.winning_coords = [(i, j) for j in range(3)]
                return True
            if all(self.board[j][i] == player for j in range(3)):
                self.winning_coords = [(j, i) for j in range(3)]
                return True
        if all(self.board[i][i] == player for i in range(3)):
            self.winning_coords = [(i, i) for i in range(3)]
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            self.winning_coords = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def check_winner_on_board(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def highlight_winner(self, player):
        for i, j in self.winning_coords:
            self.buttons[i][j].config(bg="#00ff88")

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.config(text="", state="normal", bg="#1e1e2f")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeAI(root)
    root.mainloop()
