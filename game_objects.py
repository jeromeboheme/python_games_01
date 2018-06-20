
class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item
    
    def get_position(self):
        return self.canvas.coords(self.item)
    
    def move(self, x, y):
        self.canvas.move(self.item, x, y)
    
    def delete(self):
        self.canvas.delete(self.item)

class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [0, -1]
        self.speed = 3
        item = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill='white')
        super(Ball, self).__init__(canvas, item)

    # Makes the ball bounce on the walls
    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if (coords[0] <= 0 or coords[2] >= width):  # hit a vertical wall
            self.direction[0] *= -1
        if (coords[1] <= 0):                        # hit the top wall
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)
    
    # Computes the output a collision with multiple objects
    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5           # ball center in absolute coordinates
        if (len(game_objects) > 1):                 # if collision with multiple objects, we assume it is from below or above
            self.direction[1] *= -1
        elif (len(game_objects) == 1):
            game_object = game_objects[0]
            obj_coords = game_object.get_position()
            if (x > obj_coords[2]):                 # object touched on the right side
                self.direction[0] = 1
            elif x < obj_coords[0]:                 # object touched on the left side
                self.direction[0] = -1
            elif isinstance(game_object, Brick):    # object touched the upper or lower side of a brick
                self.direction[1] *= -1
            else:                                   # object touched the upper or lower side of the paddle
                self.direction[1] *= -1
                # if the touch is in the center, we only need to invert the second component of the vector...
                # if the touch is on the left we increase the left 
                paddle_center_x = (obj_coords[0] + obj_coords[2]) * 0.5
                max_left_x = paddle_center_x - 10
                min_right_x = paddle_center_x + 10
                if (x < max_left_x):               # increase the angle to the left
                    if (self.direction[0] == -2 or self.direction[0] == -1):
                        self.direction[0] = -2
                    elif (self.direction[0] == 0):
                        self.direction[0] = -1
                    elif (self.direction[0] == 1):
                        self.direction[0] = 0
                    elif (self.direction[0] == 2):
                        self.direction[0] = 1
                elif (x > min_right_x):            # increase the angle to the right
                    if (self.direction[0] == 2 or self.direction[0] == 1):
                        self.direction[0] = 2
                    elif (self.direction[0] == 0):
                        self.direction[0] = 1
                    elif (self.direction[0] == -1):
                        self.direction[0] = 0
                    elif (self.direction[0] == -2):
                        self.direction[0] = -1
                # if touch in the middle we do not change de x component
                
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()

class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2, fill='blue', tags='paddle')
        super(Paddle, self).__init__(canvas, item)
    
    def set_ball(self, ball):
        self.ball = ball
    
    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)

class Brick(GameObject):
    COLORS = {1: '#999999', 2: '#555555', 3: '#222222'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[self.hits]
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2, fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if (self.hits <= 0):
            self.delete()
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])
