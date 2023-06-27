import pygame
from network import Network
from game import Game

WIDTH = 600
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
pygame.font.init()


# Make class for buttons
class Button:
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 150
        self.height = 100
    
    def draw(self):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, 1, (255,255,255))
        window.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
    
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


# Redraw display
def redraw_window(game, p):
    window.fill((128,128,128))

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Waiting for Other Player...", 1, (255,0,0))
        window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    
    else:
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Your Move", 1, (0,255,255))
        window.blit(text, (60, 150))

        text = font.render("Opponents", 1, (0,255,255))
        window.blit(text, (340, 150))

        move1 = game.get_move(0)
        move2 = game.get_move(1)

        if game.both_went():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went and p == 1:
                text1 = font.render("Locked In", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0,0,0))
            
            if game.p2Went and p == 0:
                text2 = font.render("Locked In", 1, (0,0,0))
            elif game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0,0,0))
            
        if p == 0:
            window.blit(text1, (80, 250))
            window.blit(text2, (360, 250))
        else:
            window.blit(text2, (80, 250))
            window.blit(text1, (360, 250))
            
        for btn in btns:
            btn.draw()

    pygame.display.update()


btns = [Button("Rock", 50, 400, (0,0,0)), Button("Scissors", 225, 400, (255,0,0)), Button("Paper", 400, 400, (0,0,255))]

# Start game
def main():
    run = True

    # Initialize network
    n = Network()
    player = int(n.get_player())
    clock = pygame.time.Clock()
    print("You are Player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        
        if game.both_went():
            redraw_window(game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            winner = game.winner()
            if winner == player:
                text = font.render("You Won!", 1, (0,255,0))
            elif winner == -1:
                text = font.render("You Tied", 1, (0,0,0))
            else:
                text = font.render("You Lost!", 1, (255,0,0))

            window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0 and not game.p1Went:
                            n.send(btn.text)
                        elif player == 1 and not game.p2Went:
                            n.send(btn.text)
        
        redraw_window(game, player)


def main_menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window.fill((128,128,128))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Click to Play!", 1, (255,0,0))
        window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


# Start program
while True:
    main_menu()
