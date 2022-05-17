import tkinter as tk
import random


class Color:
    DARK = "#252422"
    MAIN = "#eb5e28"
    LIGHT = "#fffcf2"


class Element:

    PADDING = 10

    def __init__(self, position):
        self.position = position

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def set_x(self, x):
        self.position = (x, self.position[1])

    def set_y(self, y):
        self.position = (self.position[0], y)


class Ball(Element):

    WIDTH = 60
    HEIGHT = 60

    def __init__(self, column, number):
        position = column.get_new_position(Ball.HEIGHT)
        column.add_element(self)
        super().__init__(position)
        self.number = number
        self.image = tk.PhotoImage(file="assets/ball.png")

    def display(self, canvas):
        canvas.create_image(self.x, self.y, image=self.image, anchor="center")
        canvas.create_text(self.x, self.y, text=str(self.number), font=("Klik-Light", 30), fill=Color.LIGHT)


class Separator(Element):

    WIDTH = 80
    HEIGHT = 4
    COLOR = Color.LIGHT

    def __init__(self, column):
        position = column.get_new_position(Separator.HEIGHT)
        column.add_element(self)
        super().__init__(position)
        self.image = tk.PhotoImage(file="assets/separator.png")

    def display(self, canvas):
        dw, dh = Separator.WIDTH // 2, Separator.HEIGHT // 2
        # canvas.create_rectangle(self.x - dw, self.y - dh, self.x + dw, self.y + dh, fill=Separator.COLOR, width=0)
        canvas.create_image(self.x, self.y, image=self.image, anchor="center")


class Column(Element):

    def __init__(self, position, size):
        super().__init__(position)
        self.size = size
        self.initial_position = position
        self.elements = []
        self.image = tk.PhotoImage(file="assets/column.png")

    def display(self, canvas):
        for element in self.elements:
            element.display(canvas)

        x, y = self.initial_position
        w, h = self.size
        # canvas.create_rectangle(x - w // 2, y - h, x + w // 2, y, outline=Separator.COLOR, width=2)
        canvas.create_image(x, y, image=self.image, anchor="s")

    def add_element(self, element):
        self.elements.append(element)

    def remove_element(self, element):
        index = None

        for i, e in enumerate(self.elements):
            if index is not None:
                e.set_y(e.y + element.HEIGHT + Element.PADDING)
            elif e == element:
                index = i

        if index is not None:
            del self.elements[index]

    def get_new_position(self, height):
        self.set_y(self.y - height - Element.PADDING)
        return self.x, self.y + height // 2


class App:

    WIDTH = 400
    HEIGHT = 700
    COLOR = Color.DARK

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Permutations")
        self.window.resizable(width=False, height=False)

        self.canvas = tk.Canvas(self.window, width=App.WIDTH, height=App.HEIGHT, background=App.COLOR, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind_all("<space>", self.next_step)
        self.canvas.bind_all("<Return>", self.reset)

        self.image = tk.PhotoImage(file="assets/title.png")

        self.reset()

    def next_step(self, event):
        if not self.columns[1].elements:
            self.change_ball(1)
        elif self.columns[0].elements:
            index = random.randint(0, len(self.balls))
            self.change_ball(index)

    def change_ball(self, index):
        self.title = f"indice : {index}"

        if index == 0:
            Separator(self.columns[1])
            index = 1

        ball = self.balls[index - 1]
        self.columns[0].remove_element(ball)
        Ball(self.columns[1], ball.number)
        del self.balls[index - 1]

        self.display()

    def display(self):
        self.canvas.delete(tk.ALL)
        for column in self.columns:
            column.display(self.canvas)
        self.canvas.create_image(App.WIDTH // 2, Element.PADDING, image=self.image, anchor="n")
        self.canvas.create_text(App.WIDTH // 2, Element.PADDING + 43, text=self.title, font=("Klik-Light", 40), fill=Color.LIGHT)

    def reset(self, event=None):
        x = App.WIDTH // 4
        y = App.HEIGHT - Element.PADDING
        size = (App.WIDTH - 4 * Element.PADDING) // 2, (14 * Element.PADDING + 6 * Separator.HEIGHT + 7 * Ball.HEIGHT)

        self.columns = [Column((x, y), size), Column((3 * x, y), size)]
        self.balls = [Ball(self.columns[0], i + 1) for i in range(7)]
        self.title = "permutations"

        self.display()

    def mainloop(self):
        self.display()

        self.window.mainloop()


app = App()
app.mainloop()