import turtle, random

class Game:
    '''
    Purpose: 
            Represents the board that the game is played on as well as conditions to 
            stop and start the game. It also manages the score and handles the game flow.
    Instance variables:
            self.score: Holds the player's score.
            
    Methods: 
            setup_screen: Sets up the screen and drawing the board.
            draw_board: Draws the board for the game.
            show_start_screen: Displays the start screen with game instructions.
            start_game: Initializes the game when the user clicks to start.
            gameloop: Main game loop that updates the game state and checks for game over.
            show_game_over: Displays the Game Over screen.
            update_score_display: Displays the current score on the screen.
            increase_score: Increases the score when the snake eats food.
            restart_game: Restarts the game after Game Over.
            quit_game: Exits the game.
    '''
    def __init__(self):
        self.score = 0  # Initialize score
        self.setup_screen()
        self.show_start_screen()
        turtle.listen()
        turtle.mainloop()
    
    def setup_screen(self):
        '''
        Purpose:
                Sets up the window size, drawing the board, and adjusting scrolls.
        '''
        turtle.clearscreen()
        turtle.setup(700, 700)
        turtle.setworldcoordinates(-40, -40, 640, 640)
        cv = turtle.getcanvas()
        cv.adjustScrolls()
        turtle.hideturtle()
        turtle.delay(0)
        turtle.tracer(0, 0)
        turtle.speed(0)
        self.draw_board()
    
    def draw_board(self):
        '''
        Purpose:
                Draws the square board for the game.
        '''
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()
        turtle.setheading(0)
        for i in range(4):
            turtle.forward(600)
            turtle.left(90)
    
    def show_start_screen(self):
        '''
        Purpose:
                Displays the start screen with game title and instructions to click to start.
        '''
        turtle.penup()
        turtle.goto(300, 350)
        turtle.pendown()
        turtle.write('SNAKE GAME', align='center', font=('Arial', 30, 'normal'))
        
        turtle.penup()
        turtle.goto(300, 300)
        turtle.pendown()
        turtle.write('Click anywhere to start', align='center', font=('Arial', 16, 'normal'))
        
        turtle.onscreenclick(self.start_game)
    
    def start_game(self, x, y):
        '''
        Purpose:
                Initializes the game when the player clicks to start.
        '''
        turtle.clear()
        self.draw_board()
        self.score = 0  # Reset score when the game starts
        self.update_score_display()
        
        self.player = Snake(315, 315, 'green', self)
        self.fruit = Food(15 + 30*random.randint(0,19), 15 + 30*random.randint(0,19), 'red')
        self.gameloop()
        
        turtle.onkeypress(self.player.go_down, 'Down')
        turtle.onkeypress(self.player.go_up, 'Up')
        turtle.onkeypress(self.player.go_left, 'Left')
        turtle.onkeypress(self.player.go_right, 'Right')
        turtle.onkeypress(self.restart_game, 'r')
        turtle.onkeypress(self.quit_game, 'q')
    
    def gameloop(self):
        '''
        Purpose:
                Main game loop that updates the game state and checks for game over.
        '''
        if not self.player.game_over: 
            self.player.move(self.fruit)
            turtle.ontimer(self.gameloop, 200)
        else:
            self.show_game_over()
        turtle.update()
    
    def show_game_over(self):
        '''
        Purpose:
                Displays the Game Over screen and gives options to restart or quit.
        '''
        turtle.penup()
        turtle.goto(300, 350)
        turtle.pendown()
        turtle.write('Game Over', align='center', font=('Arial', 30, 'normal'))
        
        turtle.penup()
        turtle.goto(300, 300)
        turtle.pendown()
        turtle.write('Press R to restart or Q to quit', align='center', font=('Arial', 16, 'normal'))
    
    def update_score_display(self):
        '''
        Purpose:
                Displays the current score on the screen.
        '''
        turtle.penup()
        turtle.goto(50, -30)  # Move score to bottom left under the board
        turtle.pendown()
        turtle.color("black")
        turtle.write(f"Score: {self.score}", align='left', font=('Arial', 16, 'normal'))
    
    def increase_score(self):
        '''
        Purpose:
                Increases the score when the snake eats food.
        '''
        self.score += 1
        turtle.clear()
        self.draw_board()
        self.update_score_display()
    
    def restart_game(self):
        '''
        Purpose:
                Restarts the game after Game Over.
        '''
        turtle.clearscreen()
        self.setup_screen()
        self.start_game(0, 0)
    
    def quit_game(self):
        '''
        Purpose:
                Exits the game.
        '''
        turtle.bye()

class Snake:
    '''
    Purpose: 
            Represents the snake that the player controls. 
    Instance variables:
            self.x = x: Represents the x coordinate of the snake's position.
            self.y = y: Represents the y coordinate of the snake's position.
            self.color = color: Represents the color of the snake.
            self.segments = []: Holds the segments of the snake's body.
            self.vx = 30: Velocity of the snake in the x direction.
            self.vy = 0: Velocity of the snake in the y direction.
            self.game_over = False: Whether the game is over or not.
            self.game: Reference to the Game instance.
    Methods: 
            grow: Adds a new segment to the snake's body.
            move: Moves the snake and checks if it collides with food or walls.
            go_down: Moves the snake down.
            go_up: Moves the snake up.
            go_left: Moves the snake left.
            go_right: Moves the snake right.
    '''
    def __init__(self, x, y, color, game):
        self.x = x
        self.y = y
        self.color = color
        self.segments = []
        self.grow()
        self.vx = 30
        self.vy = 0 
        self.game_over = False
        self.game = game  # Reference to Game instance
    
    def grow(self):
        '''
        Purpose:
                Adds a new segment to the snake's body.
        '''
        head = turtle.Turtle()
        head.speed(0)
        head.color(self.color)
        head.shape('square')
        head.shapesize(1.5, 1.5)
        head.penup()
        head.setpos(self.x, self.y)
        self.segments.append(head)
    
    def move(self, Food):
        '''
        Purpose:
                Moves the snake and checks if it collides with food or walls.
        '''
        self.x += self.vx
        self.y += self.vy
        self.segments[-1].setpos(self.x, self.y)
        
        if self.x == Food.x and self.y == Food.y:
            self.grow()
            Food.random_move()
            self.game.increase_score()  # Increase score when eating an apple
        
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].setpos(x, y)
        
        self.segments[0].setpos(self.x, self.y)
        
        if self.x > 600 or self.y > 600 or self.x < 0 or self.y < 0:
            self.game_over = True
        
        for segment in self.segments[1:-1]:
            if segment.xcor() == self.x and segment.ycor() == self.y:
                self.game_over = True
    
    def go_down(self): 
        '''
        Purpose:
                Moves the snake down the y-axis.
        '''
        if self.vy == 0:
            self.vx = 0 
            self.vy = -30
    
    def go_up(self):
        '''
        Purpose:
                Moves the snake up the y-axis.
        '''
        if self.vy == 0:
            self.vx = 0
            self.vy = 30
    
    def go_left(self):
        '''
        Purpose:
                Moves the snake left the x-axis.
        '''
        if self.vx == 0:
            self.vx = -30
            self.vy = 0
    
    def go_right(self):
        '''
        Purpose:
                Moves the snake right the x-axis.
        '''
        if self.vx == 0:
            self.vx = 30
            self.vy = 0

class Food:
    '''
    Purpose: 
            Represents the food (apple) that the snake eats to grow.
    Instance variables:
            self.x = x: Represents the x coordinate of the food.
            self.y = y: Represents the y coordinate of the food.
            self.color = color: Represents the color of the food.
            self.apl = turtle.Turtle(): Creates food as a turtle object.
    
    Methods:
            random_move: Moves the food to a new random position.
    '''
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.apl = turtle.Turtle()
        self.apl.speed(0)
        self.apl.color(self.color)
        self.apl.shape('circle')
        self.apl.shapesize(1.5, 1.5)
        self.apl.penup()
        self.apl.setpos(self.x, self.y)
    
    def random_move(self):
        '''
        Purpose:
                Moves the food to a new random position.
        '''
        self.x = 15 + 30 * random.randint(0, 19)
        self.y = 15 + 30 * random.randint(0, 19)
        self.apl.setpos(self.x, self.y)

if __name__ == '__main__':
    Game()




    

