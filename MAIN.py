import pygame
import sys
from pygame.locals import *
import time

resAlphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
               "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]
extAlphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
               ";", ":", ",", ".", "'", '"', "!", "£", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?", "@", "#", "~", "-", "_", "[", "]", "{", "}", "+", "=", "|", " ", "/", "`", "¬", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Special Variables
resizeWidth = None
resizeHeight = None
screenClicked = False

##EVENT HANDLER##


def eventGet():
    global resizeWidth
    global resizeHeight
    global screenClicked
    screenClicked = False

    for event in pygame.event.get():
        # detect screen close
        if event.type == QUIT:
            pygame.quit()
            quit()

        # detect screen resizing and places new dimensions
        # into resizeWidth/Height that is used in Window class

        if event.type == pygame.VIDEORESIZE:
            resizeWidth = event.w
            resizeHeight = event.h

        # detecting screen clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            screenClicked = True

        # detecting keyboard presses
            # figure this out


def startInternalGameLoop(tick, render):
    SPT = 1.0/60.0  # seconds per tick
    last_time = 0
    accum_time = 0
    fps = 0
    while True:
        start_time = time.time() # start time of the loop

        end_time = time.perf_counter()
        delta = end_time - last_time
        last_time = end_time

        accum_time += delta
        while accum_time >= SPT:
            tick(delta)
            accum_time -= SPT

        # render
        if (time.time() - start_time) > 0:
            fps = 1.0 / (time.time() - start_time) # FPS = 1 / time to process loop
        render(fps)
    

    # lastFrameTime = 0
    # while True:
    #     # dt is the time delta in seconds (float).
    #     currentTime = time.time()
    #     dt = currentTime - lastFrameTime
    #     lastFrameTime = currentTime

    #     cb(dt)


##WINDOW CLASS##
class Window():
    def __init__(self, width, height, name, resizable=False):
        self.width = width  # screen width
        self.height = height  # screen height
        self.name = name  # screen title displayed
        self.resizable = resizable  # whether the screen can be resized by the user

    def initScreen(self):
        pygame.init()
        if self.resizable:
            self.windowSurface = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE, 32)
        else:
            self.windowSurface = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE, 32)
        pygame.display.set_caption(self.name)

    def startLoop(self, tick, render):
        startInternalGameLoop(tick, render)

    def screenUpdate(self):
        global resizeWidth
        global resizeHeight
        if resizeWidth != None:
            self.width = resizeHeight
            self.height = resizeHeight
            self.windowSurface = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE, 32)
        pygame.screen.update()


##TEXT CLASS##
class Text():
    def __init__(self, font, fontsize, words, colourRGB, x, y):
        self.font = font  # the font (duh)
        self.fontsize = fontsize  # the size of the font (shock horror)
        self.words = words  # the actual text
        self.colour = colourRGB  # colour in form (R,G,B)
        self.x = x  # the x coordinate for the screen
        self.y = y  # the y coordinate for the screen

        self.font = pygame.font.SysFont(
            self.font, self.fontsize)  # gets the font
        # creates the text in the font required
        self.text = self.font.render(self.words, True, self.colour)
        self.textRect = self.text.get_rect()  # Draws box around text for alignment
        self.textRect.left = x  # sets x coord
        self.textRect.top = y  # sets y coord

    def showText(self, window):
        # blits the text to the screen
        window.windowSurface.blit(self.text, self.textRect)
