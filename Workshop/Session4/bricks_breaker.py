"""
Optional features:
    1. rockets can't go outside of the canvas
    2. showing eclapsed time
    3. add new game button
    4. pause/resume option(in menu / 'p' key)
    5. exit option(in menu / 'q' key)
    6. new game option in (menu / 'n' key)
    there is a difference between option 3 and 6; 3 create a new game by given configuration but 6 restart the game from begining
"""

from random import randint, sample
from time import perf_counter
import tkinter as tk
from tkinter import messagebox

welcome_text = \
"""
Welcome to AP4002 Bricks Breaker Game!
"""
messagebox.showinfo(title="Welcome", message = welcome_text)


def segment_cicle_collision(segment_start, segment_end, circle_center, circle_radius):
    """ Check if a segment and a circle has interfernece or not """
    x1, y1 = segment_start
    x2, y2 = segment_end
    xc, yc = circle_center
    r = circle_radius
    x1, x2, xc, r = float(x1), float(x2), float(xc), float(r)
    y1, y2, yc, r = float(y1), float(y2), float(yc), float(r)
    a = (x2-x1)**2 + (y2-y1)**2
    b = 2*((x2-x1)*(x1-xc) + (y2-y1)*(y1-yc))
    c = xc**2 + yc**2 + x1**2 + y1**2 - 2*(xc*x1 + yc*y1) - r**2
    delta = b**2 - 4*a*c
    if delta < 0:
        return False
    else:
        t1 = (-b + delta**0.5)/(2*a)
        t2 = (-b - delta**0.5)/(2*a)
        if t1 >= 0 and t1 <= 1:
            return True
        elif t2 >= 0 and t2 <= 1:
            return True
        else:
            return False 
def interact(ball, bat, direction = False):
    """ Check if a ball(the bottom point of it) and a bat has interfernece or not """
    xball = ball.x
    yball = ball.y
    x1, y1, x2, y2 = bat.pos()
    if not direction:    
        return  (x1<=xball<=x2 and (y1<=yball+ball.radius<=y2 or y1<=yball-Ball.radius<=y2)) or ((x1<=xball+ball.radius<=x2 or x1<=xball-ball.radius<=x2)  and (y1<=yball<=y2 ))
    ans = dict()
    ans["Horizontal"] = segment_cicle_collision((x1, y1), (x1, y2), (xball, yball), ball.radius) or \
                        segment_cicle_collision((x2, y1), (x2, y2), (xball, yball), ball.radius)
    ans["Vertical"] = segment_cicle_collision((x1, y1), (x2, y1), (xball, yball), ball.radius) or \
                        segment_cicle_collision((x1, y2), (x2, y2), (xball, yball), ball.radius)
    return ans    
def change_color(color, container):
    container.config(bg=color)
    for child in container.winfo_children():
        # child has children, go through its children
        change_color(color, child)

        
class GameObject():
    def __init__(self, parent, fill, position, shape_type):
        if not shape_type in ("rectangle", "oval"):
            raise ValueError("shape must be 'rectangle' or 'oval'")
        if len(position)!=4:
            raise ValueError("position must be a list of four numbers")
        self.parent = parent
        self.fill = fill
        self.position = position
        self.shape = eval(f"self.parent.create_{shape_type}({position[0]}, {position[1]}, {position[2]}, {position[3]}, fill = '{fill}')")
    def pos(self):
        """ return the position of the ball """
        return self.parent.coords(self.shape)
    @property
    def x(self):
        return (self.pos()[0]+self.pos()[2])/2
    @property
    def y(self):
        return (self.pos()[1]+self.pos()[3])/2
class Menu:
    def __init__(self, parent):
        global mode
        self.main = tk.Frame(parent.root)
        self.main.configure(width=600, height=parent.board_height)
        self.main.grid(row=0, column=1)   
        if parent.running:    
            tk.Label(self.main, text="Eclapsed Time:", bg="light green", font=("Lucida", 10)).grid(row=2, column=0, columnspan=2, padx=0, pady=0)
            
            self.timeLabel = EclapsedTime(self.main, text="0", font=("Lucida", 12),  width=10)
            self.timeLabel.grid(row=3, column=0, columnspan=2)

        tk.Label(self.main, text="___________________" ).grid(row=4, column=0, columnspan=2, sticky="N")
        self.new_game_frame = tk.Frame(self.main)
        self.new_game_frame.configure(border=3)
        self.new_game_frame.grid(row=5, column=0, columnspan=2, padx=0, pady=0)

        self.create_radio_button(title = "Screen size?", name = "screen_size", texts = ["1", "2", "3"], parent = self.new_game_frame, row = 0, column = 0, default=3)

        #Ball speed
        ball_speed_frame = tk.Frame(self.new_game_frame, bg="black")
        ball_speed_frame.grid(row=1, column=0, sticky="N")
        tk.Label(ball_speed_frame, text="Ball speed of x accel:", font=("Lucida", 10)).grid(row=0, column=0)
        self.ball_speed_x = tk.IntVar(value = 2)
        tk.Entry(ball_speed_frame, textvariable=self.ball_speed_x, width=5, font=("Lucida", 10)).grid(row=0, column=1)
        tk.Label(ball_speed_frame, text="Ball speed of y accel:", font=("Lucida", 10)).grid(row=1, column=0)
        self.ball_speed_y = tk.IntVar(value = 2)
        tk.Entry(ball_speed_frame, textvariable=self.ball_speed_y, width=5, font=("Lucida", 10)).grid(row=1, column=1)
        #new game button
        newGameCommand = lambda :main.run(
            screen_size = int(self.screen_size.get()),
            ball_speed = (self.ball_speed_x.get(), self.ball_speed_y.get())
        )
        self.create_button(name = "new_game_button", text="New game!", parent = self.new_game_frame, command = newGameCommand, row=4, column=0)
    
    def create_button(self, name, text, parent, command, row, column):
        setattr(self, name, tk.Button(parent, text=text, command=command))
        getattr(self, name).grid(row=row, column=column)
    
    def create_radio_button(self, *, title, name, texts, parent, row, column, mode = "Horizontal", values = None, columnspan = 1, default = 1):
        if values == None:
            values = texts.copy()
        if not mode in ("Horizontal", "Vertical"):
            raise ValueError("mode must be either Horizontal or Vertical")
        variable = tk.StringVar()
        setattr(self, name, variable)
        frame = tk.Frame(parent)
        frame.grid(row=row, column=column, columnspan=columnspan)
        tk.Label(frame, text = title).grid(row = 0, column = 0, columnspan = len(texts))
        for i, j, w in tuple(zip(texts, values, range(len(texts)))):
            x = 1; y = w
            if mode == "Vertical":
                x, y = y, x
            tk.Radiobutton(frame, text=i, variable=variable, value=j, bg="light blue").grid(row = x, column=y)
        variable.set(values[default-1])
    
    def destroy(self):
        try:
            self.timeLabel.destroy()
        except AttributeError:
            pass
        
    def config(self, *args, **kwargs):
        self.main.config(*args, **kwargs)
class Game:
    board_height = 210
    board_width = 280

    def __init__(self, xaccel = 2, yaccel = -2, hardenss = 2, num_of_rows = 3, size = 1):
        self.running = False
        self.balls = None
        self.hardness = hardenss
        self.num_of_rows = num_of_rows
        self.root = tk.Tk()
        self.root.title("AP4002 Bricks breaker Game")
        self.root.focus_force()
        self.menu = Menu(self)
        self.menu_bar_create()
        self.screen_size = -1
    def menu_bar_create(self, main_window = None):
        if main_window == None:
            main_window = self.root
        menubar = tk.Menu(main_window, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
        file = tk.Menu(menubar, tearoff=0, foreground='black')  
        def new_game(*args):
            global main
            self.root.destroy()
            main = Game()
        file.add_command(label="New", command = new_game)    
        self.root.bind_all("<n>", new_game) 
        file.add_separator()  
        file.add_command(label="Exit", command=main_window.quit)
        self.root.bind_all("<q>", main_window.quit) 
        def pause(*args):
            self.running = not self.running 
            try:
                self.menu.timeLabel.running = not self.menu.timeLabel.running 

                if self.running:
                    for i in self.balls:
                        i.move()
                    self.menu.timeLabel.run()
                    self.interact_check()
            except (AttributeError, TypeError):
                pass            
        file.add_command(label="Pause/Resume", command=pause) 
        self.root.bind_all("<p>", pause) 
        menubar.add_cascade(label="Game", menu=file)  


        minimap = tk.BooleanVar()
        minimap.set(True)
        darkmode = tk.BooleanVar()
        darkmode.set(False)


        help = tk.Menu(menubar, tearoff=0)  
        help.add_command(label="About", command=lambda:0)  
        menubar.add_cascade(label="Help", menu=help)  
            
        main_window.config(menu=menubar)

    def run(self, screen_size = 1, ball_speed = (2, 2)):
        """ run the game """
        self.running = False
        if self.screen_size!=screen_size:
            self.screen_size = screen_size
            Game.board_height = screen_size*7*30
            Game.board_width = screen_size*7*40
            self.root.destroy()
            self.root = tk.Tk()
            self.root.title("AP4002 Pong Game")
            self.root.focus_force()
            self.canvas = tk.Canvas(self.root, width=self.board_width, height=self.board_height, bg='turquoise')
            self.canvas.grid(row=0,column=0)
        self.running = True
        
        self.canvas.delete('all')
        
        Bat.width = main.board_width//7
        Bat.height = main.board_height//40
        self.bat = Bat(parent = self.canvas, fill="blue", position=(self.board_width//2-50, self.board_height-Bat.height))
        x1 = self.board_width//2; y1 = self.board_height//2
        Ball.radius = (main.board_height*main.board_width)**0.5//75

        self.balls = [Ball(parent = self.canvas, position = (x1, y1), xaccel=ball_speed[0], yaccel=ball_speed[1])]
        
        Brick.width = self.board_width//7
        Brick.height = self.board_height//20
        
        self.bricks = []
        self.initial_bricks()
        self.menu = Menu(parent = self)
        self.interact_check()
        self.menu_bar_create()
        self.root.mainloop()

    def bricks_generator(self, row = 0):
        """ generate bricks """
        for i in sample(range(0, self.board_width//Brick.width), self.hardness*2):
            self.bricks.append(Brick(parent = self.canvas, position=(i*Brick.width, row*Brick.height), fill="red", hitpoint=randint(1, 3)))

    def initial_bricks(self):
        """ generate initial bricks """
        for i in range(self.num_of_rows):
            self.bricks_generator(row = i)
            
    def interact_check(self):
        if not self.running:
            return
        try:
            # ball and bat interaction
            for i in self.balls:
                if interact(i, self.bat) :
                    if (self.board_height//2-i.y)*i.yaccel<0:
                        i.y_rotate()
            # ball and brick interaction
            for i in self.balls:
                for j in self.bricks:
                    o = interact(i, j, direction=True)
                    if any(o.values()):
                        if o["Horizontal"]:
                            i.x_rotate()
                        
                        elif o["Vertical"]:
                            i.y_rotate()
                        
                        if j.hitted():
                            self.bricks.remove(j)

            if self.balls[0].y>self.board_height:
                self.game_over()
            if len(self.bricks)==0:
                self.won_game()
            self.root.after(10, self.interact_check)
        except ValueError as e:
            print(type(e))
            print(e)

    def game_over(self):
        self.running = False
        self.menu.timeLabel.running = False
        self.canvas.create_text(self.board_width//2, self.board_height//2, text="Game Over", font=("Arial", 30))
    def won_game(self):
        self.running = False
        self.menu.timeLabel.running = False
        self.canvas.create_text(self.board_width//2, self.board_height//2, text="You won!", font=("Arial", 30))

    def make_dark_mode(self):
        try:
            self.canvas.config(bg = "#4E4B4B")
        except AttributeError:
            pass
        change_color(color = "#6E6D6D", container = self.root)
main = Game()

class Ball(GameObject):
    radius = (main.board_height*main.board_width)**0.5//75
    def __init__(self, parent, fill = "yellow", position=None, xaccel=2, yaccel=2):
        if position==None or len(position)!=2:
            x1, y1 = 30, 30
        else:
            x1, y1 = position

        self.accelerations = [xaccel, yaccel]
        super().__init__(parent, fill, (x1, y1, x1+2*self.radius, y1+2*self.radius), "oval")
        self.move()
    @property
    def xaccel(self):
        return self.accelerations[0]
    @property
    def yaccel(self):
        return self.accelerations[1]
    

    def x_rotate(self):
        self.accelerations[0] = -1*self.accelerations[0]
    def y_rotate(self):
        self.accelerations[1] = -1*self.accelerations[1]
    def move(self):
        if not main.running:
            return
        """ move ball every 5 millisecond  """

        xaccel, yaccel = self.accelerations
        x1, y1, _, y2 = self.pos()

        if self.x+-self.radius+self.xaccel<=0 or self.x+self.xaccel+self.radius>=main.board_width:
            self.x_rotate()
        if y1+yaccel<=0:
            self.y_rotate()

        self.parent.move(self.shape, xaccel, yaccel)
        self.parent.after(10, self.move)
    
        
#creating bat
class Bat(GameObject):
    height = main.board_height//40
    width = main.board_width//7
    def __init__(self, parent, fill = "blue", position=None, right_key = "Right", left_key = "Left"):

        if position==None or len(position)!=2:
            x1, y1 = (main.board_width//2-self.width//2, main.board_height-self.height )
        else:
            x1, y1 = position

        self.right_key = right_key
        self.left_key = left_key
        super().__init__(parent, fill, (x1, y1, x1+self.width, y1+self.height), "rectangle")
        parent.bind_all(f"<{right_key}>", self.move)
        parent.bind_all(f"<{left_key}>", self.move)
        #self.parent = parent
        
        self.score = 0
    def move(self, event):
        """ moveing bat (need binding by tkinter canvas) """
        if not main.running:
            return
        x1, *_ = main.canvas.coords(self.shape)
        if event.keysym == self.right_key and x1<=main.board_width-110:
            main.canvas.move(self.shape, 10,0)
        elif event.keysym == self.left_key and x1>=10:
            main.canvas.move(self.shape, -10,0)
class EclapsedTime(tk.Label):
    def __init__(self, *args, **kwargs):
        self.initial_time = perf_counter()
        if not "text" in kwargs.keys():
            kwargs["text"] = "0"
        self.running = True 
        super().__init__(*args, **kwargs)
        self.__timeCalc()
        
    def run(self):
        self.__timeCalc()
    def __timeCalc(self):
        """ function for calculating eclapsed time and updating the timelabel (automatically runs every second) """
        if not self.running:
            return
        # get the current local time from the PC
        current_time = perf_counter()
        # if time string has changed, update it
        self.config(text=int(current_time-self.initial_time))
        try:
            if self.running:
                self.after(1000, self.__timeCalc)
        except:
            pass
    def destroy(self):
        self.running = False
        super().destroy()

def id_generator(start = 1):
    while True:
        yield start
        start += 1
bricks_id_generator = id_generator()
class Brick(GameObject):
    width = main.board_width//7
    height = main.board_height//20
    def __init__(self, parent, position = None, fill = "red", hitpoint = 1):
        if position==None or len(position)!=2:
            x1, y1 = (randint(0, main.board_width//self.width)*self.width, randint(0, main.board_height//self.height)*self.height)
        else:
            x1, y1 = position

        super().__init__(parent, fill, (x1, y1, x1+self.width, y1+self.height), shape_type="rectangle")
        self.id = next(bricks_id_generator)
        self.hitpoint = hitpoint
        self.text = self.parent.create_text(self.x, self.y, text = self.hitpoint, fill="black", font = ("Arial", 12))

    def hitted(self):
        self.hitpoint -= 1
        self.parent.itemconfig(self.text, text=self.hitpoint)
        #self.text.configure(text = self.hitpoint)
        if self.hitpoint == 0:
            self.destroy()
            return True
        return False
    def destroy(self):
        self.parent.delete(self.shape)
        self.parent.delete(self.text)
        
    def __eq__(self, other):
        if not isinstance(other, Brick):
            return NotImplemented
        return self.id == other.id
main.root.mainloop()