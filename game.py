import pygame
import time
import random
import torch

class Ball():
    def __init__(self):
        self.img = pygame.image.load('Soccerball.png')
        self.dx = 0
        self.dy = 0
        self.dimension = 20
        self.x = 190
        self.y = 240

    def reset(self):
        self.dx = 0
        self.dy = 0
        self.x = 190
        self.y = 240
    
    def draw(self, soccerField, player1, player2, gameDisplay, display=False):
        self.setPosition(self.x + self.dx, self.y + self.dy, soccerField, player1, player2)

        if self.y == soccerField.topBorder:
            if inBetween(self.x, soccerField.goalStart, soccerField.goalEnd) and inBetween(self.x + self.dimension, soccerField.goalStart, soccerField.goalEnd):
                if self.dy != 0:
                    player2.goals += 1
                    self.reset()
                    player1.reset()
                    player2.reset()
        
        if self.y + self.dimension == soccerField.bottomBorder:
            if inBetween(self.x, soccerField.goalStart, soccerField.goalEnd) and inBetween(self.x + self.dimension, soccerField.goalStart, soccerField.goalEnd):
                if self.dy != 0:
                    player1.goals += 1
                    self.reset()
                    player1.reset()
                    player2.reset()

        if self.dx > 0:
            self.dx -= 1
        elif self.dx < 0:
            self.dx += 1
        if self.dy > 0:
            self.dy -= 1
        elif self.dy < 0:
            self.dy += 1
        
        if display:
            gameDisplay.blit(self.img, (self.x, self.y))

    def setPosition(self, x, y, soccerField, player1, player2):
        # if a player has the ball, it goes with them unless stolen by the other player
        if player1.possession:
            if (inBetween(x, player2.x, player2.x + player2.dimension) or inBetween(x + self.dimension, player2.x, player2.x + player2.dimension)) and (inBetween(y, player2.y, player2.y + player2.dimension) or inBetween(y + self.dimension, player2.y, player2.y + player2.dimension)):
                # do a steal
                player1.possession = False

                if self.x < player1.x:
                    self.dx = -1
                elif self.x > player1.x:
                    self.dx = 1

                if self.y < player1.y:
                    self.dy = -1
                elif self.y > player1.y:
                    self.dy = 1

                self.x = player1.x + player1.dimension
                self.y = player1.y + player1.dimension
            else:
                player1.possession = True
                self.x = player1.x + player1.dimension
                self.y = player1.y + player1.dimension
                self.dx = 0
                self.dy = 0
        
        elif player2.possession:
            if (inBetween(x, player1.x, player1.x + player1.dimension) or inBetween(x + self.dimension, player1.x, player1.x + player1.dimension)) and (inBetween(y, player1.y, player1.y + player1.dimension) or inBetween(y + self.dimension, player1.y, player1.y + player1.dimension)):
                # do a steal
                player2.possession = False

                if self.x < player1.x:
                    self.dx = -1
                elif self.x > player1.x:
                    self.dx = 1

                if self.y < player1.y:
                    self.dy = -1
                elif self.y > player1.y:
                    self.dy = 1

                self.x = player1.x + player1.dimension
                self.y = player1.y + player1.dimension
            else:
                player2.possession = True
                self.x = player2.x + player2.dimension
                self.y = player2.y + player2.dimension
                self.dx = 0
                self.dy = 0
        
        else:
            player1.possession = False
            player2.possession = False
        
            # if the ball travels on its own to the border of the field, it stops there
            if x + self.dimension > soccerField.rightBorder:
                self.x = soccerField.rightBorder - self.dimension
            elif x < soccerField.leftBorder:
                self.x = soccerField.leftBorder
            else:
                self.x = x

            if y + self.dimension > soccerField.bottomBorder:
                self.y = soccerField.bottomBorder - self.dimension
            elif y < soccerField.topBorder:
                self.y = soccerField.topBorder
            else:
                self.y = y

            # if the ball is next to a player, they get position of it
            if inBetween(x, player1.x, player1.x + player1.dimension) or inBetween(x + self.dimension, player1.x, player1.x + player1.dimension):
                if inBetween(y, player1.y, player1.y + player1.dimension) or inBetween(y + self.dimension, player1.y, player1.y + player1.dimension):
                    player1.possession = True
                    player2.possession = False
                    self.x = player1.x + player1.dimension
                    self.y = player1.y + player1.dimension
                    self.dx = 0
                    self.dy = 0
            
            if inBetween(x, player2.x, player2.x + player2.dimension) or inBetween(x + self.dimension, player2.x, player2.x + player2.dimension):
                if inBetween(y, player2.y, player2.y + player2.dimension) or inBetween(y + self.dimension, player2.y, player2.y + player2.dimension):
                    player2.possession = True
                    player1.possession = False
                    self.x = player2.x + player2.dimension
                    self.y = player2.y + player2.dimension
                    self.dx = 0
                    self.dy = 0

class Field():
    def __init__(self):
        self.img = pygame.image.load('pitch.png')
        self.topBorder = 25
        self.leftBorder = 25
        self.bottomBorder = 475
        self.rightBorder = 375
        self.goalStart = 150
        self.goalEnd = 250

    def draw(self, gameDisplay, display=False):
        if display:
            gameDisplay.blit(self.img,(0,0))

class Player():
    def __init__(self, num):
        if (num == 1):
            self.img = pygame.image.load('player1.png')
            self.direction = 1
            self.y = 25
        elif (num == 2):
            self.img = pygame.image.load('player2.png')
            self.direction = -1
            self.y = 415

        self.num = num
        self.x = 170
        self.dx = 0
        self.dy = 0
        self.dimension = 60
        self.possession = False 
        self.kickForce = 12
        self.goals = 0    
        
    def reset(self):
        if (self.num == 1):
            self.y = 25
        elif (self.num == 2):
            self.y = 415
        
        self.x = 170
        self.dx = 0
        self.dy = 0

    def draw(self, soccerField, gameDisplay, display=False):
        self.setPosition(self.x + self.dx, self.y + self.dy, soccerField)
        if display:
            gameDisplay.blit(self.img,(self.x, self.y))

    def setPosition(self, x, y, soccerField):
        if x + self.dimension > soccerField.rightBorder:
            self.x = soccerField.rightBorder - self.dimension
        elif x < soccerField.leftBorder:
            self.x = soccerField.leftBorder
        else:
            self.x = x
        
        if y + self.dimension > soccerField.bottomBorder:
            self.y = soccerField.bottomBorder - self.dimension
        elif y < soccerField.topBorder:
            self.y = soccerField.topBorder
        else:
            self.y = y
    
    def kick(self, soccerBall):
        if self.possession:
            self.possession = False
            soccerBall.dy = self.direction*self.kickForce
            if self.num == 2:
                soccerBall.y = self.y - soccerBall.dimension

class SoccerGame():
    def __init__(self, display_width=400, display_height=500):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('Soccer')
        self.n_action_space = 5
        self.n_observation_space = 14

    def step(self, player_1_action, player_2_action):
        done = False
        p1_rew = 0
        p2_rew = 0
        p1_possession_initial = self.p1.possession
        p2_possession_initial = self.p2.possession

        if player_1_action == 0:
            if self.p1.possession:
                self.p1.dx = -3
            else:
                self.p1.dx = -5
            
        elif player_1_action == 1:
            if self.p1.possession:
                self.p1.dx = 3
            else:
                self.p1.dx = 5

        elif player_1_action == 2:
            if self.p1.possession:
                self.p1.dy = -3
            else:
                self.p1.dy = -5

        elif player_1_action == 3:
            if self.p1.possession:
                self.p1.dy = 3
            else:
                self.p1.dy = 5

        elif player_1_action == 4:
            self.p1.kick(self.ball)

        if player_2_action == 0:
            if self.p2.possession:
                self.p2.dx = -3
            else:
                self.p2.dx = -5
            
        elif player_2_action == 1:
            if self.p2.possession:
                self.p2.dx = 3
            else:
                self.p2.dx = 5

        elif player_2_action == 2:
            if self.p2.possession:
                self.p2.dy = -3
            else:
                self.p2.dy = -5

        elif player_2_action == 3:
            if self.p2.possession:
                self.p2.dy = 3
            else:
                self.p2.dy = 5

        elif player_2_action == 4:
            self.p2.kick(self.ball)
        
        self.field.draw(self.gameDisplay, self.display) 
        self.p2.draw(self.field, self.gameDisplay, self.display)
        self.p1.draw(self.field, self.gameDisplay, self.display)
        self.ball.draw(self.field, self.p1, self.p2, self.gameDisplay, self.display)
        displayScores(self.p1, self.p2, self.gameDisplay, self.display)

        if self.display:
            pygame.display.update()
            self.clock.tick(60)

        # done if a goal was scored
        if self.p1.goals != 0 and self.p2.goals != 0:
            done = True
            if self.p1.goals != 0:
                p1_rew += 30000
                p2_rew += -10000
            else:
                p1_rew += -10000
                p2_rew += 30000

        # reward for gaining possession
        if self.p1.possession and not p1_possession_initial:
            p1_rew += 10
            p2_rew += -10
        elif self.p1.possession:
            p1_rew += 3
            p2_rew += -1

        if self.p2.possession and not p2_possession_initial:
            p2_rew += 10
            p1_rew += -10
        elif self.p2.possession:
            p2_rew += 3
            p1_rew += -1

        next_state = torch.tensor([self.p1.x, self.p1.y, self.p1.dx, self.p1.dy, int(self.p1.possession), self.p2.x, self.p2.y, self.p2.dx, self.p2.dy, int(self.p2.possession), self.ball.x, self.ball.y, self.ball.dx, self.ball.dy])

        if done:
            next_state = None
        
        return (next_state, torch.tensor(p1_rew), torch.tensor(p2_rew), done)
    
    def reset(self, display=False):
        self.clock = pygame.time.Clock()
        self.display=display
        self.ball = Ball()
        self.p1 = Player(1)
        self.p2 = Player(2)
        self.field = Field()

        return torch.tensor([self.p1.x, self.p1.y, self.p1.dx, self.p1.dy, int(self.p1.possession), self.p2.x, self.p2.y, self.p2.dx, self.p2.dy, int(self.p2.possession), self.ball.x, self.ball.y, self.ball.dx, self.ball.dy]) # initial state vector

def inBetween(x, y, z):
    # returns true if the number x is in between y and z
    if x >= y and x <= z:
        return True
    else:
        return False

def displayScores(player1, player2, gameDisplay, display=False):
    if display:
        display_width = 400
        player1_str = "P1: " + str(player1.goals)
        player2_str = "P2: " + str(player2.goals)

        red = (255, 0, 0)
        black = (0, 0, 0)

        font = pygame.font.SysFont(None, 25)

        player1_txt = font.render(player1_str, True, red)
        player2_txt = font.render(player2_str, True, black)

        gameDisplay.blit(player1_txt, (0, 0))
        gameDisplay.blit(player2_txt, (display_width - player2_txt.get_width(), 0))


if __name__ == '__main__':
    done = False
    game = SoccerGame()
    s_0 = game.reset(display=False)
    while not done:
        action_1 = random.randrange(0, 5)
        action_2 = random.randrange(0, 5)
        s_1, p1_r, p2_r, done = game.step(action_1, action_2)
        if p1_r != 0:
            print("P1 Reward: {}, Action: {}".format(p1_r, action_1))
        if p2_r != 0:
            print("P2 Reward: {}, Action: {}".format(p2_r, action_2))
