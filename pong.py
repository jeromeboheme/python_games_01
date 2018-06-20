import tkinter as tk
import game_objects as go

class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#aaaaff', width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = go.Paddle(self.canvas, self.width / 2, 326)
        self.items[self.paddle.item] = self.paddle
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)
        
        self.hud = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    def add_ball(self):
        if (self.ball is not None):
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = go.Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)
    
    def add_brick(self, x, y, hits):
        brick = go.Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, str, size='40'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=str, font=font)
    
    def update_lives_text(self):
        str = 'Lives : %s' % self.lives
        if self.hud is None:
            self.hud = self.draw_text(50, 20, str, 15)
        else:
            self.canvas.itemconfig(self.hud, text=str)
    
    def setup_game(self):
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200, "Press space to start")
        self.canvas.bind('<space>', lambda _: self.start_game())
    
    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()
    
    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:                                 # broke all bricks !
            self.ball.speed = None
            self.draw_text(300, 200, 'You win !')
        elif self.ball.get_position()[3] >= self.height:    # lost the ball...
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'Game over !')
            else:
                self.after(1000, self.setup_game)
        else:                                               # regular loop...
            self.ball.update()
            self.after(20, self.game_loop)                  # 60 frame per second (refresh every 15ms)
            
    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello Pong !')
    game = Game(root)
    root.mainloop()