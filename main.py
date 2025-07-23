import tkinter
import tkinter.messagebox
import functools
import os
import sys


def resource_path(path: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = getattr(sys, "_MEIPASS")
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, os.path.normpath(path))


class Application:
    def __init__(self):
        self.frames = []
        self.buttons = []
        self.status = []
        self.player = "cross"
        self.game_over = False
        self.root = tkinter.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("300x340")
        self.root.minsize(300, 340)
        self.circle = tkinter.PhotoImage(file=resource_path("Images/Circle.png"))
        self.cross = tkinter.PhotoImage(file=resource_path("Images/Cross.png"))
        self.blank = tkinter.PhotoImage(file=resource_path("Images/Empty.png"))
        self.num = tkinter.StringVar()
        self.content_frame = tkinter.Frame(self.root)
        self.content_frame.pack()
        tkinter.Label(self.content_frame, text="Tic Tac Toe rules\n"
                                               "Two players take turns to click buttons on the\n"
                                               "screen, each button can only be clicked by\n"
                                               "one player once. The player who first forms a\n"
                                               "horizontal, vertical, or diagonal line of \n"
                                               "clicked buttons wins.").pack()
        tkinter.Button(self.content_frame, text="Next", command=self.board_size).pack()
        self.root.mainloop()

    def board_size(self):
        widgets = self.content_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        top_frame = tkinter.Frame(self.content_frame)
        top_frame.pack()
        tkinter.Label(top_frame, text="Enter board size:\n").pack(side="left")
        tkinter.Entry(top_frame, width=2, textvariable=self.num).pack(side="left")
        self.text = tkinter.Label(top_frame, text="")
        self.text.pack()
        bottom_frame = tkinter.Frame(self.content_frame)
        bottom_frame.pack()
        tkinter.Button(bottom_frame, text="Start", command=self.check_input).pack()
        self.update_text()

    def update_text(self):
        if len(self.num.get()) > 2:
            self.num.set(self.num.get()[0:2])
        if self.num.get().isdigit():
            self.text.config(text="x " + str(self.num.get()))
        elif self.num.get() == "":
            self.text.config(text="x 0")
        else:
            self.text.config(text="x 0")
            self.num.set("0")
        self.update = self.root.after(5, self.update_text)

    def check_input(self):
        size = self.num.get()
        if not size.isdigit():
            tkinter.messagebox.showerror("Error", "Please enter a number.")
        elif int(size) < 3 or int(size) > 20:
            tkinter.messagebox.showerror("Error", "Please enter a number between 3 and 20")
        else:
            if int(size[0:2]) > 9:
                self.root.geometry(str(340 + 22 * (int(size[0:2]) - 9)) + "x" + str(405 + 22 * (int(size[0:2]) - 9)))
                self.root.minsize(340 + 22 * (int(size[0:2]) - 9), 405 + 22 * (int(size[0:2]) - 9))
            else:
                self.root.geometry("300x340")
                self.root.minsize(300, 340)
            self.game(int(size[0:2]))

    def draw_board(self, size):
        for row in range(0, size):
            self.frames.append(tkinter.Frame(self.content_frame))
            self.frames[row].pack()
        for row in range(0, size):
            self.status.append([])
            self.buttons.append([])
            for button in range(0, size):
                self.status[row].append("Empty")
                self.buttons[row].append(tkinter.Button(self.frames[row], image=self.blank, width=22, height=22,
                                                        command=functools.partial(self.mark_button, [row, button])))
                self.buttons[row][button].pack(side="left")

    def mark_button(self, index):
        if self.status[index[0]][index[1]] == "Empty" and (not self.game_over):
            self.game_over = True
            self.status[index[0]][index[1]] = self.player
            if self.player == "circle":
                self.buttons[index[0]][index[1]]["image"] = self.circle
            else:
                self.buttons[index[0]][index[1]]["image"] = self.cross
            if self.player == "circle":
                self.player = "cross"
                self.image["image"] = self.cross
            else:
                self.player = "circle"
                self.image["image"] = self.circle

    def resize_board(self):
        widgets = self.content_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.player = "cross"
        self.frames.clear()
        self.buttons.clear()
        self.status.clear()
        self.game_over = False
        self.board_size()

    def reset(self):
        self.player = "cross"
        self.hidden_frame.destroy()
        self.image.pack_forget()
        self.text.pack_forget()
        self.hidden_frame = tkinter.Frame(self.top_frame)
        self.hidden_frame.pack(side="left")
        self.hidden_image = tkinter.Label(self.hidden_frame, image=self.cross)
        self.image.pack(side="left")
        self.text.pack(side="left")
        self.retry.destroy()
        self.resize.destroy()
        self.image["image"] = self.cross
        self.text["text"] = "'s turn to click."
        for row in range(0, self.size):
            for button in range(0, self.size):
                self.buttons[row][button]["image"] = self.blank
                self.buttons[row][button]["background"] = "SystemButtonFace"
                self.status[row][button] = "Empty"
        self.game_over = False
        self.check_winner()

    def game(self, size):
        self.root.after_cancel(self.update)
        widgets = self.content_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.size = size
        self.top_frame = tkinter.Frame(self.content_frame)
        self.top_frame.pack()
        self.hidden_frame = tkinter.Frame(self.top_frame)
        self.hidden_frame.pack(side="left")
        self.hidden_image = tkinter.Label(self.hidden_frame, image=self.cross)
        self.image = tkinter.Label(self.top_frame, image=self.cross)
        self.image.pack(side="left")
        self.text = tkinter.Label(self.top_frame, text="'s turn to click.")
        self.text.pack(side="left")
        self.draw_board(size)
        self.bottom_frame = tkinter.Frame(self.content_frame)
        self.bottom_frame.pack()
        self.check_winner()

    def check_winner(self):
        full = True
        winner = []
        for row in range(0, self.size):
            horizontal = True
            vertical = True
            diagonal1 = True
            diagonal2 = True
            for button in range(1, self.size):
                if horizontal:
                    if self.status[row][button] != self.status[row][button - 1] or self.status[row][button] == "Empty":
                        horizontal = False
                if vertical:
                    if self.status[button][row] != self.status[button - 1][row] or self.status[button][row] == "Empty":
                        vertical = False
                if diagonal1:
                    if self.status[button][button] != self.status[button - 1][button - 1] or\
                            self.status[button][button] == "Empty":
                        diagonal1 = False
                if diagonal2:
                    if self.status[self.size - button - 1][button] != self.status[self.size - button][button - 1] or\
                            self.status[self.size - button - 1][button] == "Empty":
                        diagonal2 = False
                if (not horizontal) and (not vertical) and (not diagonal1) and (not diagonal2):
                    break
                if button == self.size - 1:
                    if horizontal:
                        winner.append(self.status[row][0])
                        winner.append("horizontal")
                        winner.append([row, 0])
                    elif vertical:
                        winner.append(self.status[0][row])
                        winner.append("vertical")
                        winner.append([0, row])
                    elif diagonal1:
                        winner.append(self.status[0][0])
                        winner.append("diagonal1")
                        winner.append([0, 0])
                    elif diagonal2:
                        winner.append(self.status[0][self.size - 1])
                        winner.append("diagonal2")
                        winner.append([0, self.size - 1])
            if len(winner):
                break
        if not len(winner):
            for row in range(0, self.size):
                for button in range(0, self.size):
                    if self.status[row][button] == "Empty":
                        full = False
                        break
                if not full:
                    break
        else:
            full = False
        self.update = self.root.after(5, self.check_winner)
        if full:
            self.game_over = True
            self.root.after_cancel(self.update)
            self.text["text"] = "Draw!"
            self.image["image"] = self.circle
            self.hidden_image.pack()
            self.retry = tkinter.Button(self.bottom_frame, text="Retry", width=12, command=self.reset)
            self.retry.pack()
            self.resize = tkinter.Button(self.bottom_frame, text="Resize Board", width=12, command=self.resize_board)
            self.resize.pack()
        elif len(winner):
            self.game_over = True
            self.root.after_cancel(self.update)
            if winner[1] == "horizontal":
                for button in range(0, self.size):
                    self.buttons[winner[2][0]][button]["background"] = "yellow"
            elif winner[1] == "vertical":
                for button in range(0, self.size):
                    self.buttons[button][winner[2][1]]["background"] = "yellow"
            elif winner[1] == "diagonal1":
                for button in range(0, self.size):
                    self.buttons[button][button]["background"] = "yellow"
            elif winner[1] == "diagonal2":
                for button in range(0, self.size):
                    self.buttons[self.size - button - 1][button]["background"] = "yellow"
            self.text["text"] = "Wins!"
            if winner[0] == "circle":
                self.image["image"] = self.circle
            else:
                self.image["image"] = self.cross
            self.retry = tkinter.Button(self.bottom_frame, text="Retry", width=12, command=self.reset)
            self.retry.pack()
            self.resize = tkinter.Button(self.bottom_frame, text="Resize Board", width=12, command=self.resize_board)
            self.resize.pack()
        else:
            self.game_over = False


if __name__ == "__main__":
    Application()
