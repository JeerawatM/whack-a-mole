import pygame
import random
from pygame import *
import sys


class GameManager:
    def __init__(self):
        # Define constants
        self.what_time = 0
        self.where_mole = 0
        self.start_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = 1900
        self.SCREEN_HEIGHT = 1000
        self.FPS = 60
        self.MOLE_WIDTH = 100
        self.MOLE_HEIGHT = 100
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "Whack A Mole - Game Programming - Assignment 1"
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        self.time = 5
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT),RESIZABLE)
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("images/forest.jpg")
        # Font object for displaying text
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', self.FONT_SIZE)
        # Initialize the mole's sprite sheet
        # 6 different states
        sprite_sheet = pygame.image.load("images/2.png")
        self.mole = []
        self.mole.append(sprite_sheet.subsurface(338, 0, 180, 162))
        self.mole.append(sprite_sheet.subsurface(618, 0, 180, 162))
        self.mole.append(sprite_sheet.subsurface(900, 0, 180, 162))
        self.mole.append(sprite_sheet.subsurface(1150, 0, 232, 162))
        self.mole.append(sprite_sheet.subsurface(1434, 0, 232, 162))
        self.mole.append(sprite_sheet.subsurface(1706, 0, 232, 162))
        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((350, 300))
        self.hole_positions.append((850, 300))
        self.hole_positions.append((1325, 300))
        self.hole_positions.append((350, 700))
        self.hole_positions.append((850, 700))
        self.hole_positions.append((1325, 700))
        # Init debugger
        self.debugger = Debugger("debug")
        # Sound effects
        self.soundEffect = SoundEffect()
        


    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant
    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the mole pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    # Check whether the mouse click hit the mole or not
    def is_mole_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        # if True:
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.MOLE_HEIGHT):
            return True
        else:
            return False

    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.SCREEN_WIDTH*0.75
        score_text_pos.centery = self.FONT_TOP_MARGIN+40
        self.screen.blit(score_text, score_text_pos)
        # Update the player's level
        current_test = "Time: " + str(self.countdown)
        level_test = self.font_obj.render(current_test, True, (255, 255, 255))
        level_test_pos = level_test.get_rect()
        level_test_pos.centerx = self.SCREEN_WIDTH / 4
        level_test_pos.centery = self.FONT_TOP_MARGIN+40
        self.screen.blit(level_test, level_test_pos)


    def summery(self):
        while True:
            screen.fill(WHITE)
            draw_text("My Score : "+str(self.score), font, BLACK, WIDTH // 2, HEIGHT // 4)

            mouse_pos = pygame.mouse.get_pos()

            # Draw "Start Game" button
            start_game_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
            pygame.draw.rect(screen, BLACK, start_game_rect)
            draw_text("Play Again", font, WHITE, WIDTH // 2, HEIGHT // 2 + 25)

            # Draw "Quit" button
            # quit_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)
            # pygame.draw.rect(screen, BLACK, quit_rect)
            # draw_text("Quit", font, WHITE, WIDTH // 2, HEIGHT // 2 + 125)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_game_rect.collidepoint(mouse_pos):
                        # Call your game function here
                        print("Starting Game!")
                        screen.fill(BLACK)
                        my_game.start()
                        sys.exit()
            pygame.display.update()
            
    # Start the game's main loop
    # Contains some logic for handling animations, mole hit events, etc..
    def start(self):
        cycle_time = 0
        num = -1
        loop = True
        is_down = False
        interval = 0.1
        initial_interval = 1
        frame_num = 0
        left = 0
        self.score = 0
        self.misses = 0
        self.level = 1
        self.time = 10
        self.start_time = pygame.time.get_ticks()
        # self.clock = pygame.time.Clock()
        # Time control variables
        clock = pygame.time.Clock() 

        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()
        
      

        while loop:
            # Calculate remaining time
            self.current_time = pygame.time.get_ticks()
            elapsed_time = self.current_time - self.start_time
            remaining_seconds = max(0, self.time - elapsed_time // 1200)
            self.countdown = remaining_seconds
            for event in pygame.event.get():
                # กดอะไรแล้วทำ อะไร
                if self.countdown == 0:
                    loop = False
                    self.summery()
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = False
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                    self.soundEffect.playFire()
                    if self.is_mole_hit(mouse.get_pos(), self.hole_positions[frame_num]) and num >= 0 and left == 0:
                        num = 3
                        left = 14
                        is_down = False
                        interval = 0
                        self.score += 1  # Increase player's score
                        self.level = self.get_player_level()  # Calculate player's level
                        # Stop popping sound effect
                        self.soundEffect.stopPop()
                        # Play hurt sound
                        self.soundEffect.playHurt()
                        self.update()
                    else:
                        self.misses += 1
                        self.update()

            if num > 5:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = -1
                left = 0

            if num == -1:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = 0
                is_down = False
                interval = 0.5
                frame_num = random.randint(0, 5)
            self.where_mole = frame_num

            mil = clock.tick(self.FPS)
            sec = mil / 1000.0
            cycle_time += sec
            self.what_time = cycle_time
            
            if cycle_time > interval:
                
                pic = self.mole[num]
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                self.update()
                if is_down is False:
                    num += 1
                else:
                    num -= 1
                if num == 4:
                    interval = 0.3
                elif num == 3:
                    num -= 1
                    is_down = True
                    self.soundEffect.playPop()
                    # interval = self.get_interval_by_level(initial_interval)
                    interval = 4 # get the newly decreased interval value
                else:
                    interval = 0.1
                cycle_time = 0
            # Update the display
            pygame.display.flip()
    

def play_game():
    self.score = 0
# The Debugger class - use this class for printing out debugging information
class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode is "debug":
            print("> DEBUG: " + str(message))


class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("sounds/themesong.wav")
        pygame.mixer.music.set_volume(0.01)
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.fireSound.set_volume(0.1)
        
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.popSound.set_volume(0.01)
        
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.hurtSound.set_volume(0.01)
        
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        self.levelSound.set_volume(0.01)
        pygame.mixer.music.play(-1)

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.sop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

###############################################################
# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Run the main loop
my_game = GameManager()
# my_game.start()

# Constants
WIDTH, HEIGHT = 1900,1000
MENU_FONT_SIZE = 36
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

score = 0
# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Game")

# Font for the menu
font = pygame.font.Font(None, MENU_FONT_SIZE)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
    
    
def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Simple Game", font, BLACK, WIDTH // 2, HEIGHT // 4)

        mouse_pos = pygame.mouse.get_pos()

        # Draw "Start Game" button
        start_game_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
        pygame.draw.rect(screen, BLACK, start_game_rect)
        draw_text("Start Game", font, WHITE, WIDTH // 2, HEIGHT // 2 + 25)

        # Draw "Quit" button
        quit_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)
        pygame.draw.rect(screen, BLACK, quit_rect)
        draw_text("Quit", font, WHITE, WIDTH // 2, HEIGHT // 2 + 125)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_rect.collidepoint(mouse_pos):
                    # Call your game function here
                    print("Starting Game!")
                    screen.fill(BLACK)
                    my_game.start()
                    sys.exit()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main_menu()

# Exit the game if the main loop ends
pygame.quit()
