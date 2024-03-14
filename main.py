import pygame
import random
from pygame import *
import sys

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from sklearn.linear_model import LinearRegression


class GameManager:
    def __init__(self):
        
        self.countercrush = 0
        # Define constants
        self.what_time = 0
        self.where_mole = 0
        self.start_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = 1900
        self.SCREEN_HEIGHT = 1000
        self.FPS = 60
        self.MOLE_WIDTH = 150
        self.MOLE_HEIGHT = 150
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
        self.background = pygame.image.load("images/white-background.jpg")
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
    # Contains some logic for handling animations, mole hit events, etc...
    def detectDirection(self,values, display):
        if len(values) == 10 :
                if values[0][0] == 'RL':
                    for i in range (0, len(values)-1):
                        if values[i][0] == 'LR':
                            cv2.circle(display[i], values[i-1][1], 10, (0,255,0), -1)
                            print('prehit')
                            return display[i]
                            
                elif values[0][0] == 'LR':
                    for i in range (0, len(values)-1):
                        if values[i][0] == 'RL':
                            cv2.circle(display[i], values[i-1][1], 10, (0,255,0), -1)
                            print('prehit')
                            return display[i]
        return False
    def detect_mole(self,image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # Define the lower and upper boundaries for the brown color in LAB
        lower_brown = np.array([20, 120, 130])  # Adjust these values based on your specific shade of brown
        upper_brown = np.array([190, 180, 170])   # Adjust these values based on your specific shade of brown
        # Create a mask using inRange to threshold the brown color
        mask = cv2.inRange(lab, lower_brown, upper_brown)

        # Apply the mask to the original image
        contours_mole, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours_mole, -1, (255, 0, 0), -1)
        cv2.imwrite('mole.jpg',image)
        return contours_mole

    def detect_green_ball(self,image):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the lower and upper boundaries for the green color (adjust as needed)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])

        # Threshold the image to extract the green ball
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Find contours of the green ball
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the original image for visualization
        cv2.drawContours(image, contours_green, -1, (0, 255, 0), 1)
        cv2.imwrite('ball.jpg',image)

        return contours_green


    def detect_shadows(self,image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold the image to extract shadows
        _, mask_shadows = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

        # Find contours of shadows
        contours_shadows, _ = cv2.findContours(mask_shadows, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the original image for visualization
        cv2.drawContours(image, contours_shadows, -1, (0, 0, 255), -1)
        cv2.imwrite('shadow.jpg',image)

        return contours_shadows

    def check_intersection(self,contours_objects, contours_shadows):
        # Check for intersections between object and shadow contours
        for contour_object in contours_objects:
            for contour_shadow in contours_shadows:
                # Iterate over the points in the contour
                for point in contour_shadow[:, 0]:
                    # Convert point to tuple of float values
                    pt = tuple(map(float, point))
                    # Check for intersection
                    intersection = cv2.pointPolygonTest(contour_object, pt, False)
                    if intersection >= 0:
                        return True  
        return False


    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-v", "--video",
    #                 help="path to the (optional) video file")
    # ap.add_argument("-b", "--buffer", type=int, default=10,
    #                 help="max buffer size")
    # args = vars(ap.parse_args())

    # # define the lower and upper boundaries of the "green"
    # # ball in the HSV color space
    # greenLower = (40, 40, 40)
    # greenUpper = (80, 255, 255)
    # # initialize the list of tracked points, the frame counter,
    # # and the coordinate deltas
    # pts = deque(maxlen=args["buffer"])
    # counter = 0
    # countercrush = 0
    # (dX, dY) = (0, 0)
    # direction = ""
    # # if a video pat

    # tx = deque(maxlen=args["buffer"])
    # ty = deque(maxlen=args["buffer"])

    # slopes = deque(maxlen=args["buffer"])

    # frames = deque(maxlen=args["buffer"])

    # predicted_y = None
    # sampling = None


    # #  was not supplied, grab the reference
    # # to the webcam
    # if not args.get("video", False):
    #     vs = VideoStream(src=0).start()
    # # otherwise, grab a reference to the video file
    # else:
    #     vs = cv2.VideoCapture(args["video"])
    # # allow the camera or video file to warm up
    # time.sleep(2.0)

    
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
        self.time = 100
        self.start_time = pygame.time.get_ticks()
        # self.clock = pygame.time.Clock()
        # Time control variables
        clock = pygame.time.Clock() 

        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()
        
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=10,
                        help="max buffer size")
        args = vars(ap.parse_args())

        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space
        greenLower = (40, 40, 40)
        greenUpper = (80, 255, 255)
        # initialize the list of tracked points, the frame counter,
        # and the coordinate deltas
        pts = deque(maxlen=args["buffer"])
        counter = 0
        self.countercrush = 0
        (dX, dY) = (0, 0)
        direction = ""
        # if a video pat

        tx = deque(maxlen=args["buffer"])
        ty = deque(maxlen=args["buffer"])

        slopes = deque(maxlen=args["buffer"])

        frames = deque(maxlen=args["buffer"])

        predicted_y = None
        sampling = None


        #  was not supplied, grab the reference
        # to the webcam
        if not args.get("video", False):
            vs = VideoStream(src=0).start()
        # otherwise, grab a reference to the video file
        else:
            vs = cv2.VideoCapture(args["video"])
        # allow the camera or video file to warm up
        time.sleep(2.0)

        while loop:
            detect = np.zeros((720, 1080, 3), np.uint8)
            frame = vs.read()
            # handle the frame from VideoCapture or VideoStream
            frame = frame[1] if args.get("video", False) else frame

            frame = imutils.resize(frame, width=1080)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    # cv2.circle(frame, (int(x), int(y)), int(radius),
                    #            (0, 255, 255), 2)
                    # cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    pts.appendleft(center)
                    tx.appendleft(center[0])
                    ty.appendleft(center[1])
                    ttx = np.array(tx)
                    tty = np.array(ty)

                    ttx = ttx.reshape(-1, 1)
                    model = LinearRegression()
                    model.fit(ttx, tty)
                    slope = model.coef_[0]
                    intercept = model.intercept_
                    predicted_y = model.predict(ttx)      
            else:
                pts.appendleft(center)

        # loop over the set of tracked points
            for i in np.arange(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                    # print('nothing',slopes)
                    # slopes.clear() 
                    break
                
                # check to see if enough points have been accumulated in
                # the buffer
                if counter >= 10 and i == 1 and pts[-5] is not None:
                    # compute the difference between the x and y
                    # coordinates and re-initialize the direction
                    # text variables
                    dX = pts[-5][0] - pts[i][0]
                    dY = pts[-5][1] - pts[i][1]
                    (dirX, dirY) = ("", "")

                    # พิมพ์ค่า y ที่ทำนายได้
                    # print("Predicted y:", predicted_y)
                    # sampling = predicted_y

                    if dX > 1:
                        slopes.appendleft(('LR',pts[i]))
                        frames.appendleft(frame)
                        # print('LR')
                    if dX < -1:
                        slopes.appendleft(('RL',pts[i]))
                        frames.appendleft(frame)
                        # print('RL')
                    if np.abs(dX) > 1:
                        dirX = "East" if np.sign(dX) == 1 else "West"
                    # ensure there is significant movement in the
                    # y-direction
                    if np.abs(dY) > 20:
                        dirY = "North" if np.sign(dY) == 1 else "South"
                    # handle when both directions are non-empty
                    if dirX != "" and dirY != "":
                        direction = "{}-{}".format(dirY, dirX)
                    # otherwise, only one direction is non-empty
                    else:
                        direction = dirX if dirX != "" else dirY
                    # print(slopes)
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)

                # print(tx[i-1],predicted_y[i-1])
                # cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
                # cv2.line(frame, (tx[0],int(predicted_y[0])), (tx[i],int(predicted_y[i])), (255, 0, 0), 2)
                # cv2.line(detect, pts[i - 1], pts[i], (0, 0, 255), thickness)
                # print(predicted_y,counter)

            if len(frames) == 10: 
                if self.detectDirection(slopes, frames) is not False:
                    cv2.imwrite('hit.jpg',self.detectDirection(slopes, frames))
                    ball = self.detect_green_ball(self.detectDirection(slopes, frames))
                    shadow = self.detect_shadows(self.detectDirection(slopes, frames))
                    mole = self.detect_mole(self.detectDirection(slopes, frames))
                    if self.check_intersection(ball, mole):
                        self.countercrush += 1
                        print('hit!',self.countercrush)

                    slopes.clear()
                    frames.clear()
                    time.sleep(1.0)
                
            # show the movement deltas and the direction of movement on
            # the frame
            cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 0, 255), 3)
            # cv2.putText(frame, sampling, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            # 	0.65, (0, 0, 255), 3)
            # print(sampling)
            cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)

            # show the frame to our screen and increment the frame counter
            cv2.imshow("Frame", frame)
            # cv2.imshow("Detect", detect)

            key = cv2.waitKey(1) & 0xFF
            counter += 1
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
        # if we are not using a video file, stop the camera video stream
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
        if not args.get("video", False):
                vs.stop()
            # otherwise, release the camera
        else:
            vs.release()
            # close all windows
        cv2.destroyAllWindows()

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

if __name__ == "__main__":
    main_menu()

# Exit the game if the main loop ends
pygame.quit()





from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from sklearn.linear_model import LinearRegression



# def detectDirection(values, display):
#     if len(values) == 10 :
#             if values[0][0] == 'RL':
#                 for i in range (0, len(values)-1):
#                     if values[i][0] == 'LR':
#                         cv2.circle(display[i], values[i-1][1], 10, (0,255,0), -1)
#                         print('prehit')
#                         return display[i]
                        
#             elif values[0][0] == 'LR':
#                 for i in range (0, len(values)-1):
#                     if values[i][0] == 'RL':
#                         cv2.circle(display[i], values[i-1][1], 10, (0,255,0), -1)
#                         print('prehit')
#                         return display[i]
#     return False
# def detect_mole(image):
#     lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

#     # Define the lower and upper boundaries for the brown color in LAB
#     lower_brown = np.array([20, 120, 130])  # Adjust these values based on your specific shade of brown
#     upper_brown = np.array([190, 180, 170])   # Adjust these values based on your specific shade of brown
#     # Create a mask using inRange to threshold the brown color
#     mask = cv2.inRange(lab, lower_brown, upper_brown)

#     # Apply the mask to the original image
#     contours_mole, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(image, contours_mole, -1, (255, 0, 0), -1)
#     cv2.imwrite('mole.jpg',image)
#     return contours_mole

# def detect_green_ball(image):
#     # Convert BGR to HSV
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define the lower and upper boundaries for the green color (adjust as needed)
#     lower_green = np.array([40, 40, 40])
#     upper_green = np.array([80, 255, 255])

#     # Threshold the image to extract the green ball
#     mask_green = cv2.inRange(hsv, lower_green, upper_green)

#     # Find contours of the green ball
#     contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Draw contours on the original image for visualization
#     cv2.drawContours(image, contours_green, -1, (0, 255, 0), 1)
#     cv2.imwrite('ball.jpg',image)

#     return contours_green


# def detect_shadows(image):
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Threshold the image to extract shadows
#     _, mask_shadows = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

#     # Find contours of shadows
#     contours_shadows, _ = cv2.findContours(mask_shadows, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Draw contours on the original image for visualization
#     cv2.drawContours(image, contours_shadows, -1, (0, 0, 255), -1)
#     cv2.imwrite('shadow.jpg',image)

#     return contours_shadows

# def check_intersection(contours_objects, contours_shadows):
#     # Check for intersections between object and shadow contours
#     for contour_object in contours_objects:
#         for contour_shadow in contours_shadows:
#             # Iterate over the points in the contour
#             for point in contour_shadow[:, 0]:
#                 # Convert point to tuple of float values
#                 pt = tuple(map(float, point))
#                 # Check for intersection
#                 intersection = cv2.pointPolygonTest(contour_object, pt, False)
#                 if intersection >= 0:
#                     return True  
#     return False


# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
#                 help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=10,
#                 help="max buffer size")
# args = vars(ap.parse_args())

# # define the lower and upper boundaries of the "green"
# # ball in the HSV color space
# greenLower = (40, 40, 40)
# greenUpper = (80, 255, 255)
# # initialize the list of tracked points, the frame counter,
# # and the coordinate deltas
# pts = deque(maxlen=args["buffer"])
# counter = 0
# countercrush = 0
# (dX, dY) = (0, 0)
# direction = ""
# # if a video pat

# tx = deque(maxlen=args["buffer"])
# ty = deque(maxlen=args["buffer"])

# slopes = deque(maxlen=args["buffer"])

# frames = deque(maxlen=args["buffer"])

# predicted_y = None
# sampling = None


# #  was not supplied, grab the reference
# # to the webcam
# if not args.get("video", False):
#     vs = VideoStream(src=0).start()
# # otherwise, grab a reference to the video file
# else:
#     vs = cv2.VideoCapture(args["video"])
# # allow the camera or video file to warm up

# time.sleep(2.0)

# # keep looping
# while True:
#     # grab the current frame
#     detect = np.zeros((720, 1080, 3), np.uint8)
#     frame = vs.read()
#     # handle the frame from VideoCapture or VideoStream
#     frame = frame[1] if args.get("video", False) else frame

#     frame = imutils.resize(frame, width=1080)
#     blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#     hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#     # construct a mask for the color "green", then perform
#     # a series of dilations and erosions to remove any small
#     # blobs left in the mask
#     mask = cv2.inRange(hsv, greenLower, greenUpper)
#     mask = cv2.erode(mask, None, iterations=2)
#     mask = cv2.dilate(mask, None, iterations=2)
#     # find contours in the mask and initialize the current
#     # (x, y) center of the ball
#     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
#                             cv2.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#     center = None

#     # only proceed if at least one contour was found
#     if len(cnts) > 0:
#         # find the largest contour in the mask, then use
#         # it to compute the minimum enclosing circle and
#         # centroid
#         c = max(cnts, key=cv2.contourArea)
#         ((x, y), radius) = cv2.minEnclosingCircle(c)
#         M = cv2.moments(c)
#         center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#         # only proceed if the radius meets a minimum size
#         if radius > 10:
#             # draw the circle and centroid on the frame,
#             # then update the list of tracked points
#             # cv2.circle(frame, (int(x), int(y)), int(radius),
#             #            (0, 255, 255), 2)
#             # cv2.circle(frame, center, 5, (0, 0, 255), -1)
#             pts.appendleft(center)
#             tx.appendleft(center[0])
#             ty.appendleft(center[1])
#             ttx = np.array(tx)
#             tty = np.array(ty)

#             ttx = ttx.reshape(-1, 1)
#             model = LinearRegression()
#             model.fit(ttx, tty)
#             slope = model.coef_[0]
#             intercept = model.intercept_
#             predicted_y = model.predict(ttx)      
#     else:
#         pts.appendleft(center)

# # loop over the set of tracked points
#     for i in np.arange(1, len(pts)):
#         # if either of the tracked points are None, ignore
#         # them
#         if pts[i - 1] is None or pts[i] is None:
#             # print('nothing',slopes)
#             # slopes.clear() 
#             break
        
#         # check to see if enough points have been accumulated in
#         # the buffer
#         if counter >= 10 and i == 1 and pts[-10] is not None:
#             # compute the difference between the x and y
#             # coordinates and re-initialize the direction
#             # text variables
#             dX = pts[-10][0] - pts[i][0]
#             dY = pts[-10][1] - pts[i][1]
#             (dirX, dirY) = ("", "")

#             # พิมพ์ค่า y ที่ทำนายได้
#             # print("Predicted y:", predicted_y)
#             # sampling = predicted_y

#             if dX > 1:
#                 slopes.appendleft(('LR',pts[i]))
#                 frames.appendleft(frame)
#                 # print('LR')
#             if dX < -1:
#                 slopes.appendleft(('RL',pts[i]))
#                 frames.appendleft(frame)
#                 # print('RL')
#             if np.abs(dX) > 1:
#                 dirX = "East" if np.sign(dX) == 1 else "West"
#             # ensure there is significant movement in the
#             # y-direction
#             if np.abs(dY) > 20:
#                 dirY = "North" if np.sign(dY) == 1 else "South"
#             # handle when both directions are non-empty
#             if dirX != "" and dirY != "":
#                 direction = "{}-{}".format(dirY, dirX)
#             # otherwise, only one direction is non-empty
#             else:
#                 direction = dirX if dirX != "" else dirY
#             # print(slopes)
#         # otherwise, compute the thickness of the line and
#         # draw the connecting lines
#         thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)

#         # print(tx[i-1],predicted_y[i-1])
#         # cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
#         # cv2.line(frame, (tx[0],int(predicted_y[0])), (tx[i],int(predicted_y[i])), (255, 0, 0), 2)
#         # cv2.line(detect, pts[i - 1], pts[i], (0, 0, 255), thickness)
#         # print(predicted_y,counter)

#     if len(frames) == 10: 
#         if detectDirection(slopes, frames) is not False:
#             cv2.imwrite('hit.jpg',detectDirection(slopes, frames))
#             ball = detect_green_ball(detectDirection(slopes, frames))
#             shadow = detect_shadows(detectDirection(slopes, frames))
#             mole = detect_mole(detectDirection(slopes, frames))
#             if check_intersection(ball, mole):
#                 countercrush += 1
#                 print('hit!',countercrush)

#             slopes.clear()
#             frames.clear()
#             time.sleep(1.0)
        
#     # show the movement deltas and the direction of movement on
#     # the frame
#     cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.65, (0, 0, 255), 3)
#     # cv2.putText(frame, sampling, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#     # 	0.65, (0, 0, 255), 3)
#     # print(sampling)
#     cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
#                 (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.35, (0, 0, 255), 1)

#     # show the frame to our screen and increment the frame counter
#     cv2.imshow("Frame", frame)
#     # cv2.imshow("Detect", detect)

#     key = cv2.waitKey(1) & 0xFF
#     counter += 1
#     # if the 'q' key is pressed, stop the loop
#     if key == ord("q"):
#         break
# # if we are not using a video file, stop the camera video stream
# if not args.get("video", False):
#     vs.stop()
# # otherwise, release the camera
# else:
#     vs.release()
# # close all windows
# cv2.destroyAllWindows()