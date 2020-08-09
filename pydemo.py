# import sys, pygame
# from pygame.locals import *
# import time

# class board:
#     rows = 10
#     cols = 10

#     def __init__(self, value, row, col, width ,height):
#         self.value = value
#         self.temp = 0
#         self.row = row
#         self.col = col
#         self.width = width
#         self.height = height
#         self.selected = False #check if the current grid is selected

#     def drawboard(pygame,screen):
#    pygame.draw.line
#      pygame.draw.rect(screen ,(0,255,0),(100,100,100,100),10)
#      pygame.draw.rect(screen ,(255,0,0),(100,100,100,100))



# pygame.init()

# size = width, height = 1600, 800
# speed = [2, 2]
# black = 0, 0, 0

# screen = pygame.display.set_mode(size)

# ball = pygame.image.load("landmine.jpg")
# ballrect = ball.get_rect()
# ic = pygame.image.load("landminepng.jpg")
# pygame.display.set_icon(ic)

# while 1:
#     t = time.localtime()
#     displayt = time.asctime(t)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: sys.exit()
#     pressed = pygame.key.get_pressed()
#     if pressed[pygame.K_a]==True:
#         print(displayt)
#     screen.fill((0,0,255))
#     #pygame.draw.rect(screen ,(255,0,0),(100,100,100,100))
#     drawboard(pygame,screen)
#     # draw local time on board
#     fnt = pygame.font.SysFont("comicsans", 40)
#     text = fnt.render("Time: " + displayt, 1, (0,0,0))
#     screen.blit(text, (540, 560))
#     # ballrect = ballrect.move(speed)
#     # if ballrect.left < 0 or ballrect.right > width:
#     #     speed[0] = -speed[0]
#     # if ballrect.top < 0 or ballrect.bottom > height:
#     #     speed[1] = -speed[1]

    
#     #screen.blit(ball, ballrect)
#     pygame.display.update()

# pygame.quit()