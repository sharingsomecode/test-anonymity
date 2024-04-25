#!/usr/bin/python3

"""
 Software allowing to present short movies in order to test the degree of anonymity.
 In order to use it, you have to adapt paths, etc 
 (see "Variables to adjust to your case")

 Each pedestrian (and the associated movie) is refered to by a number
 between 1 and nbf.
 num is the number of the pedestrian that has to be recognized.

 q is the quality level, or degree of pixelation (corresponding variable
 in the software is 'qpixel').
 q=1 is the best quality (no pixelation), while q=8 is the worse (max pixelation)

 This software assumes that some movies with various degrees of pixelation
 were produced and stored in "folder" (to be adjusted below).

 Other variables internal to the software:
 Movies are shuffled in order to be presented in random order.
 pps is the number of the current pedestrian.
 pp is the position after shuffle of pedestrian pps.

 Credits:
 This software was written by C. Appert.

 Both functions imdisplay_modif and preview_modif are inspired from
 the functions imdisplay  and preview of module moviepy,
 that can be found here:
 https://github.com/Zulko/moviepy/blob/master/moviepy/video/io/preview.py
 We have slightly modified them to be able to indicate in which window
 and at which position the movie should be displayed.
"""

import os, sys
import subprocess
import pygame as pg
import numpy as np
import random
import time
from moviepy.editor import VideoFileClip,concatenate_videoclips
from pygame.locals import *

########################################################################
## Variables to adjust to your case
########################################################################

#number of videos to show, for each quality level
#nbf = 24
nbf = 2

# Reading the name of local home
homename = subprocess.getoutput("echo ~")

# Location of the movies.
folder= homename+"/movie_place/" 
print("Movies are read from ",folder)

# Name of the movies.
movie_name="aller_"
print("Movie corresponding to pedestrian 3 with quality q=8 is called ",movie_name+"3"+"_q"+"8"+".mpg")

# Location where results should be stored
fname2= homename+"/results/"
print("Results are stored in ",fname2)

# Extra variables (do not change them if you don't understand)
sizew = width, height = 1130, 680 # window size
yfilmK,xfilmK = 600,800 # dimensions of the subwindow in which movies are shown.
posx,posy=10,30 #Distance between the video and the top left point in the presentation window.
colorbg = (125,250,250) # background color
colorinset = (75,200,200) # inset color

########################################################################

def numdisplay(num, screen=None,posx=20,posy=50,color=(0,200,200)):
    """Writes a number on a colored disk on the given pygame screen """
    if screen is not None:
      # width=0 -> fill circle
      pg.draw.circle(screen,color,(posx,posy),40,0)
      if pg.font:
        font = pg.font.Font(None, 72)
        text = font.render(str(num), 1, (10, 10, 10))
        textpos = text.get_rect(centerx=posx,centery=posy)
        backgrd.blit(text,textpos)
      pg.display.flip()

def qnumdisplay(num, screen=None,posx=20,posy=50,color=(0,200,200)):
    """Writes the quality level 'q' on a colored disk on the given pygame screen """
    if screen is not None:
      # width=0 -> fill circle
      pg.draw.circle(screen,color,(posx,posy),50,0)
      if pg.font:
        font = pg.font.Font(None, 72)
        text = font.render("q="+str(num), 1, (10, 10, 10))
        textpos = text.get_rect(centerx=posx,centery=posy)
        backgrd.blit(text,textpos)
      pg.display.flip()

def imdisplay_modif(imarray, screen=None,posx=0,posy=0):
    """Splashes the given image array on the given pygame screen

    posx,posy
      specifies at which location the image should be played.
    """
    a = pg.surfarray.make_surface(imarray.swapaxes(0, 1))
    if screen is None:
        screen = pg.display.set_mode(imarray.shape[:2][::-1])
    screen.blit(a, (posx, posy))
    pg.display.flip()

def preview_modif(clip,fps=30,screen=None,posx=0,posy=0):
    """ 
    Displays the clip in a window, at the given frames per second
    (of movie) rate. It will avoid that the clip be played faster
    than normal, but it cannot avoid the clip to be played slower
    than normal if the computations are complex. In this case, try
    reducing the ``fps``.
    No audio can be played.
    
    Parameters
    ------------
    
    fps
      Number of frames per seconds in the displayed video.
        
    screen
      screen on which the video should be played.
      
    posx,posy
      specifies at which location the video should be played.
    """
    img = clip.get_frame(0)
    if screen is not None:
      # Check that the screen which has been given is large enough for the video
      maxx,maxy = screen.get_size()
      sizev = img.shape
      if posx+sizev[1] > maxx or posy+sizev[0] > maxy:
        # x and y axis of img are inverted, as seen from the use of swap in imdisplay_modif.
        print("PBL with window size!!!")
        exit()
    imdisplay_modif(img, screen, posx, posy)

    t0 = time.time()
    for t in np.arange(1.0 / fps, clip.duration-.001, 1.0 / fps):

        img = clip.get_frame(t)
        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                print("Interrupt")

        t1 = time.time()
        time.sleep(max(0, t - (t1-t0)))
        imdisplay_modif(img, screen, posx, posy)

def reading_q(string_esc,qpixel,pp,target,pps,rect_erase3,screen=None):
    """ Reads from the keyboard the new value of q """
    going2out = 0
    going2 = True
    # Handle Input Events
    for event2 in pg.event.get():
        # If the user exits with "escape"
        if event2.type == KEYDOWN and event2.key == K_ESCAPE:
            # output of the results in a file
            fichier2 = open(fname2,'a')
            fichier2.write(string_esc)
            fichier2.close()
            exit()
        # Reading the new quality level
        elif event2.type == KEYDOWN and event2.unicode.isdigit():
            qpixel = int(event2.unicode)
            going2out = 1
        # Figures may require to press Left Shift key, and we don't want that it triggers a reaction:
        elif event2.type == KEYDOWN and event2.key == K_LSHIFT:
            # If key SHIFT is pressed
            pass
        elif event2.type == KEYDOWN:
          # If any other key is pressed (we could just pass but here we display an error message giving information on the pressed key)
          if pg.font:
            backgrd.fill(colorbg,rect_erase3)
            font = pg.font.Font(None, 36)
            # event2.key allows to see to which key number the key that was pressed corresponds
            # Useful if you have to adjust key numbers.
            text = font.render("Non valid key "+str(event2.key), 1, (10, 10, 10))
            backgrd.blit(text, (50,y_aff + 100))
            rect_erase3 = text.get_rect(x=50,y=y_aff+100)

            # Display The Background
            if screen is not None:
               screen.blit(backgrd, (0, 0))
               pg.display.flip()

        if going2out == 1:
            backgrd.fill(colorbg,rect_erase2)
            backgrd.fill(colorbg,rect_erase3)

            qnumdisplay(qpixel, backgrd,xnum+80,ynum,color=colorinset)
            going2 = False
            # Shuffle the pedestrians
            random.shuffle(target)
            pp=1
            numdisplay(pp, backgrd,xnum,ynum,color=colorinset)
            pps=target[pp-1]
    return going2,qpixel,pp,target,pps

# First, we must initialize pygame.
pg.init()
#black = 0, 0, 0
white = (250,250,250)

x_aff = 10 + xfilmK + 5
y_aff = 100
rect_erase = ((100,height-100),(100+10,80))
xnum = 30 + xfilmK
ynum = 50

# Reading instructions from the experiment manager.
nums=input('Number of the pedestrian that has to be recognized?')
qpixels=input('Initial pixelation level?')
qpixel=int(qpixels)
num = int(nums)

# Name of the output file
fname2 = fname2+"res"+nums+".txt"

# Initial list of pedestrian numbers
prim = [x+1 for x in range(nbf)] # we shift because range(nbf) goes from 0 to nbf-1
# Shuffled list of pedestrian numbers, in order to present the movies in random order.
target = [x+1 for x in range(nbf)]
random.shuffle(target)

# Creating the interacting window
mafenetre = pg.display.set_mode(sizew)
pg.display.set_caption('Test anonymity')

# Create The Backgound, we call it backgrd
backgrd = pg.Surface(mafenetre.get_size())
# convert is used to have the correct pixel code. We need to do this for each image we want to display.
backgrd = backgrd.convert()
backgrd.fill(colorbg)

# Put Text On The Background, Centered
if pg.font:
    font = pg.font.Font(None, 36)
    text = font.render("Try to identify the person", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=backgrd.get_width()/2)
    backgrd.blit(text, textpos)

# Number of the current pedestrian in the shuffled list
pp=1
# Corresponding umber of the current pedestrian in the initial list
pps=target[pp-1]
# Displaying pedestrian number and quality level
numdisplay(pp, backgrd,xnum,ynum,color=colorinset)
qnumdisplay(qpixel, backgrd,xnum+80,ynum,color=colorinset)
# Display The Background
mafenetre.blit(backgrd, (0, 0))
pg.display.flip()

trouve = 0
noanswer = 1
while noanswer:
  if trouve==1:
    pps = num
  ## Reading the movie corresponding to the current pedestrian
  fa = folder+movie_name+str(pps)+"_q"+qpixels+".mpg"
  filmt = VideoFileClip(fa)

  ## If several movies have to be concatenated, please uncomment
  ## and adjust movie names

  #filma = VideoFileClip(fa)
  #fr = folder+"retour_"+str(pps)+"_q"+qpixels+".mpg"
  #filmr = VideoFileClip(fr)
  #filmt = concatenate_videoclips([filma,filmr])

  fps1 = filmt.fps
  preview_modif(filmt,fps1,mafenetre,posx,posy)

  # Display of instructions
  # Define display area to the right of the movie: ((left,top),(width,height))
  backgrd.fill(colorinset,((x_aff,y_aff),(width-x_aff-5,350)))
  if pg.font:
    font = pg.font.Font(None, 36)
    text = font.render("space = play current film", 1, (10, 10, 10))
    backgrd.blit(text, (x_aff + 10,y_aff + 50))
    text = font.render("n = next film", 1, (10, 10, 10))
    backgrd.blit(text, (x_aff + 10,y_aff + 100))
    text = font.render("p = previous film", 1, (10, 10, 10))
    backgrd.blit(text, (x_aff + 10,y_aff + 150))
    text = font.render("q = change quality", 1, (10, 10, 10))
    backgrd.blit(text, (x_aff + 10,y_aff + 200))
    text = font.render("y = It's him/her!", 1, (10, 10, 10))
    backgrd.blit(text, (x_aff + 10,y_aff + 250))
    text = font.render("Escape = Exit", 1, (10, 10, 10))
    backgrd.blit(text, (x_aff + 10,y_aff + 300))

    # Display The Background
    mafenetre.blit(backgrd, (0, 0))
    pg.display.flip()

  # Wait for instructions
  going = True
  while going:

    # Handle Input Events
    # commands like QUIT... require : from pygame.locals import *
    for event in pg.event.get():
      # If the user exits with "escape"
      if event.type == KEYDOWN and event.key == K_ESCAPE:
          # output of the results in a file
          fichier2 = open(fname2,'a')
          fichier2.write("exit with escape\n")
          if trouve == 0:
            line1 = "q = "+qpixels+":\ntarget = ["
            for nn in target:
              line1 = line1 + str(nn) + ","
            line1 = line1 + "]\npp = " + str(pp) +"\npps = "+str(pps)+"\n"
            fichier2.write(line1)
          elif trouve == 1:
            line1 = "q = "+qpixels+"\n"
            fichier2.write(line1)
          else:
            line1 = "weird\n"
            fichier2.write(line1)
          fichier2.close()

          exit()
      # If the user pressed "n" for "next" movie
      elif event.type == KEYDOWN and event.key == K_n:
          backgrd.fill(colorbg,rect_erase)
          if pp<nbf:
            pp = pp+1
            pps=target[pp-1]
            numdisplay(pp, backgrd,xnum,ynum,color=colorinset)
          else:
            text = font.render("This is already the last movie", 1, (10, 10, 10))
            backgrd.blit(text, (100,height-50))
            rect_erase = text.get_rect(x=100,y=height-50)
      # If the user pressed "p" for "previous" movie
      elif event.type == KEYDOWN and event.key == K_p:
          backgrd.fill(colorbg,rect_erase)
          if pp> 1:
            pp = pp-1
            pps=target[pp-1]
            numdisplay(pp, backgrd,xnum,ynum,color=colorinset)
          else:
            text = font.render("This is already the first movie", 1, (10, 10, 10))
            backgrd.blit(text, (100,height-50))
            rect_erase = text.get_rect(x=100,y=height-50)
      # If the user pressed "space" in order to play the current film
      elif event.type == KEYDOWN and event.key == K_SPACE:
          backgrd.fill(colorbg,rect_erase)
          going = False
      # If the user pressed "y" as "yes, I recognized the person".
      elif event.type == KEYDOWN and event.key == K_y:
          backgrd.fill(colorbg,rect_erase)

          # If the user indeed recognized the person successfully:
          if pps == num:
            # output of the results in a file
            fichier2 = open(fname2,'a')
            fichier2.write("recognition is a success\n")
            line1 = "q = "+qpixels+":\ntarget = ["
            for nn in target:
              line1 = line1 + str(nn) + ","
            line1 = line1 + "]\npp = " + str(pp) +"\npps = "+str(pps)+"\n"
            fichier2.write(line1)
            fichier2.close()

            if pg.font:
              font = pg.font.Font(None, 72)
              text = font.render("Bravo!", 1, (10, 10, 10))
              backgrd.blit(text, (30,y_aff + 50))
              rect_erase4 = text.get_rect(x=30,y=y_aff+50)

              # Display The Background
              mafenetre.blit(backgrd, (0, 0))
              pg.display.flip()
              trouve = 1
          # If the user actually recognized the wrong person...
          else :
            # output of the results in a file
            fichier2 = open(fname2,'a')
            fichier2.write("recognition failed\n")
            line1 = "q = "+qpixels+":\ntarget = ["
            for nn in target:
              line1 = line1 + str(nn) + ","
            line1 = line1 + "]\npp = " + str(pp) +"\npps = "+str(pps)+"\n"
            fichier2.write(line1)
            fichier2.close()

            # ... then the user is invited to change the pixelation level for a new try
            if pg.font:
              font = pg.font.Font(None, 72)
              text = font.render("Pixelation q?", 1, (10, 10, 10))
              backgrd.blit(text, (50,y_aff + 50))
              rect_erase2 = text.get_rect(x=50,y=y_aff+50)
              rect_erase3 = rect_erase2 #just so that rect_erase3 is defined

              # Display The Background
              mafenetre.blit(backgrd, (0, 0))
              pg.display.flip()
            going2 = True
            string_esc="exit with escape in y\n"
            while going2:
              # Reading the new quality level
              going2,qpixel,pp,target,pps = reading_q(string_esc,qpixel,pp,target,pps,rect_erase3,mafenetre)
              qpixels = str(qpixel)

      # If the user pressed "q" for "change quality"
      elif event.type == KEYDOWN and event.key == K_q:
          backgrd.fill(colorbg,rect_erase)
          if trouve == 1:
            backgrd.fill(colorbg,rect_erase4)

          # output of the results in a file
          fichier2 = open(fname2,'a')
          fichier2.write("quality was changed using q\n")
          if trouve == 0:
            line1 = "q = "+qpixels+":\ntarget = ["
            for nn in target:
              line1 = line1 + str(nn) + ","
            line1 = line1 + "]\npp = " + str(pp) +"\npps = "+str(pps)+"\n"
            fichier2.write(line1)
          elif trouve == 1:
            line1 = "q = "+qpixels+"\n"
            fichier2.write(line1)
          else:
            line1 = "weird\n"
            fichier2.write(line1)
          fichier2.close()

          if pg.font:
              font = pg.font.Font(None, 72)
              text = font.render("Pixelation q?", 1, (10, 10, 10))
              backgrd.blit(text, (50,y_aff + 50))
              rect_erase2 = text.get_rect(x=50,y=y_aff+50)
              rect_erase3 = rect_erase2 #just so that rect_erase3 is defined

              # Display The Background
              mafenetre.blit(backgrd, (0, 0))
              pg.display.flip()
          going2 = True
          string_esc="exit with escape in q\n"
          while going2:
              # Reading the new quality level
              going2,qpixel,pp,target,pps = reading_q(string_esc,qpixel,pp,target,pps,rect_erase3,mafenetre)
              qpixels = str(qpixel)

      # Draw Everything
      mafenetre.blit(backgrd, (0, 0))
      pg.display.flip()

pg.quit()
# Game Over

