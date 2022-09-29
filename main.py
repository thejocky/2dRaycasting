#!/usr/bin/python3


import math
import pygame
from pygame.locals import * # print
import random
import time


BLOCK_SIZE = 75
MAP = [[1,1,1,1,1,1,1,1,1,1,1,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,1,0,0,0,0,1]
      ,[1,0,0,0,0,0,1,1,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,0,0,0,0,0,0,0,0,0,0,1]
      ,[1,1,1,1,1,1,1,1,1,1,1,1]]


if int(2000//len(MAP[0])) <= (1000//len(MAP)):
  BLOCK_SIZE = 800//len(MAP[0])
else:
  BLOCK_SIZE = 600//len(MAP)


WIDTH = len(MAP[0])*BLOCK_SIZE
HIGHT = len(MAP)*BLOCK_SIZE




# Player info

x = BLOCK_SIZE*1.5
y = BLOCK_SIZE*1.5
x_1 = x
y_1 = y
angle = 0

FOV = 50
walk = 2
sprint = walk*2
HB = 10 # hit box or radius of character
PIX_PER_RAY = 4 # how pixels for each ray, more means less lag

# FOV_ANGLES = []
# b = 5
# a = b*math.tan(FOV/2)
# pixel = -FOV//2
# for j in range(10//PIX_PER_RAY):
#   if abs(pixel)
#     A = math.atan(a/abs(pixel))
#     FOV_ANGLES.append(A+FOV//2)
#     pixel+=FOV/10
#   else:
#     FOV_ANGLES
# print (FOV_ANGLES)

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)



# initualizing screen

screen = pygame.display.set_mode((WIDTH, HIGHT))



def draw_map(MAP):
  for j in range(len(MAP)):
    for k in range(len(MAP[0])):
      if MAP[j][k]:
        pygame.draw.rect(screen, red, (k*BLOCK_SIZE, j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

   


def check_boarder(x, y):
  check = 0
  if MAP[round((y-HB-6)//BLOCK_SIZE)][round((x-HB-5)//BLOCK_SIZE)]:
    return 0
  if MAP[round((y-HB-6)//BLOCK_SIZE)][round((x+HB+5)//BLOCK_SIZE)]:
    return 0
  if MAP[round((y+HB+6)//BLOCK_SIZE)][round((x+HB+5)//BLOCK_SIZE)]:
    return 0
  if MAP[round((y+HB+6)//BLOCK_SIZE)][round((x-HB-5)//BLOCK_SIZE)]:
    return 0
  return 1


def distance(pos_1, pos_2):
  """ distance((x_1, y_1), (x_2, y_2))
    Finds distance between two points"""
  return abs(math.sqrt(((pos_1[0]-pos_2[0])**2)+((pos_1[1]-pos_2[1])**2)))


def drawray(angle, x, y):
  if angle >= 360:
    angle -= 360
  point_x = 0
  point_y = 0
  square_y = int(y//BLOCK_SIZE)
  square_x = int(x//BLOCK_SIZE)
  print(square_x, square_y)
  empty = True
  
  if angle % 90 == 0:
    if angle == 0:
      point_y = y
      while  not MAP[square_y][square_x]:
        square_x += 1
      point_x = square_x * BLOCK_SIZE

    elif angle == 180:
      point_y = y
      while  not MAP[square_y][square_x]:
        square_x -= 1
      point_x = (square_x+1) * BLOCK_SIZE

    elif angle == 270:
      point_x = x
      while not MAP[square_y][square_x]:
        square_y -= 1
      point_y = (square_y+1) * BLOCK_SIZE

    elif angle == 90:
      point_x = x
      while not MAP[square_y][square_x]:
        square_y += 1
      point_y = square_y * BLOCK_SIZE



  else:
    x_off = (1/math.tan(math.radians(angle)))*BLOCK_SIZE
    y_off = (-(math.tan(math.radians(angle))))*BLOCK_SIZE
    print (x_off, y_off, angle)
    x_count = 0
    y_count = 0

    if angle > 180:
      y_1 = y%BLOCK_SIZE
      first_y = (-y_1)/math.tan(math.radians(angle))# x offset for reach y
      if angle < 270:
        x_1 = x%BLOCK_SIZE
        first_x = (-x_1)*math.tan(math.radians(angle))# y offset for reach x
        point_1 = ((x+first_y), (y-y_1))
        point_2 = ((x-x_1), (y+first_x))
        while not MAP[square_y][square_x]:
           if distance(point_1, (x, y)) <= distance(point_2, (x, y)):
             square_y -= 1
             point_x = point_1[0]
             point_y = point_1[1]
             point_1 = (point_1[0]-x_off, point_1[1]-BLOCK_SIZE)
           else:
             square_x -= 1
             point_x = point_2[0]
             point_y = point_2[1] 
             point_2 = (point_2[0]-BLOCK_SIZE, point_2[1]+y_off)



      else:
        x_1 = BLOCK_SIZE-(x%BLOCK_SIZE)
        first_x = (-x_1)*math.tan(math.radians(angle))# y offset for
        point_1 = ((x+first_y), (y-y_1))
        point_2 = ((x+x_1), (y-first_x))
        while not MAP[square_y][square_x]:
          if distance(point_1, (x, y)) <= distance(point_2, (x, y)):
            square_y -= 1
            point_x = point_1[0]
            point_y = point_1[1]
            point_1 = (point_1[0]-x_off, point_1[1]-BLOCK_SIZE)
            
            
          else:
            square_x += 1
            point_x = point_2[0]
            point_y = point_2[1] 
            point_2 = (point_2[0]+BLOCK_SIZE, point_2[1]-y_off)
             


    else:
        y_1 = BLOCK_SIZE-(y%BLOCK_SIZE)
        first_y = (-y_1)/math.tan(math.radians(angle))# x offset for


        if angle > 90:
            x_1 = x%BLOCK_SIZE
            first_x = (-x_1)*math.tan(math.radians(angle))# y offset for reach x
            point_1 = (x-first_y, y+y_1)
            point_2 = (x-x_1, y+first_x)
            while not MAP[square_y][square_x]:
                if distance(point_1, (x, y)) < distance(point_2, (x, y)):
                    square_y += 1
                    point_x = point_1[0]
                    point_y = point_1[1]
                    point_1 = (point_1[0]+x_off, point_1[1]+BLOCK_SIZE)

                else:
                    square_x -= 1
                    point_x = point_2[0]
                    point_y = point_2[1] 
                    point_2 = (point_2[0]-BLOCK_SIZE, point_2[1]+y_off)

        else:
            x_1 = BLOCK_SIZE-(x%BLOCK_SIZE)
            first_x = (-x_1)*math.tan(math.radians(angle))# y offset for reach x
            point_1 = ((x-first_y), (y+y_1))
            point_2 = ((x+x_1), (y-first_x))
            while not MAP[square_y][square_x]:
                if distance(point_1, (x, y)) < distance(point_2, (x, y)):
                    square_y += 1
                    point_x = point_1[0]
                    point_y = point_1[1]
                    point_1 = (point_1[0]+x_off, point_1[1]+BLOCK_SIZE)
                else:
                    square_x += 1
                    point_x = point_2[0]
                    point_y = point_2[1] 
                    point_2 = (point_2[0]+BLOCK_SIZE, point_2[1]-y_off)


    pygame.draw.line(screen, white, (x, y), (round(point_x), round(point_y)), 1)



# main

draw_map(MAP)
move = False
while (True):
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()


  keys = pygame.key.get_pressed()
  # if 1 in keys:
  x_1 = x
  y_1 = y
  if keys[pygame.K_w]:
    if keys[pygame.K_LSHIFT]:
      x_1 += sprint * math.cos(math.radians(angle+(FOV/2)))
      y_1 += sprint * math.sin(math.radians(angle+(FOV/2)))

    else:
      x_1 += walk * math.cos(math.radians(angle+(FOV/2)))
      y_1 += walk * math.sin(math.radians(angle+(FOV/2)))
    move = True
  if keys[pygame.K_a]:
    x_1 += walk * math.cos(math.radians(angle+(FOV/2)-90))
    y_1 += walk * math.sin(math.radians(angle+(FOV/2)-90))
    move = True
  if keys[pygame.K_d]:
    x_1 += walk * math.cos(math.radians(angle+(FOV/2)+90))
    y_1 += walk * math.sin(math.radians(angle+(FOV/2)+90))
    move = True
  if keys[pygame.K_s]:
    x_1 += walk * math.cos(math.radians(angle+(FOV/2)+180))
    y_1 += walk * math.sin(math.radians(angle+(FOV/2)+180))
    move = True
  if move:
    if check_boarder(x_1, y):
      x = x_1
    if check_boarder(x, y_1):
      y = y_1
    move = False



  if keys[pygame.K_e]:
    angle += 2
  elif keys[pygame.K_q]:
    angle -= 2
  
  if angle >= 360:
    angle -= 360
  elif angle < 0:
    angle += 360

  screen.fill(black)
  draw_map(MAP)


  for j in range(WIDTH//PIX_PER_RAY):
    drawray(angle+((FOV/(WIDTH//PIX_PER_RAY))*j), x, y)
  draw_map(MAP)
#   drawray(angle+(FOV//2), x, y)


  pygame.draw.circle(screen, white, (round(x), round(y)), HB, 0)
  x_1 = round(x + 30 * math.cos(math.radians(angle+(FOV//2))))
  y_1 = round(y + 30 * math.sin(math.radians(angle+(FOV//2))))
  pygame.draw.line(screen, white, (x, y), (x_1, y_1), 1)
  pygame.display.update()

  pygame.draw.circle(screen, black, (round(x), round(y)), HB, 0)


  
  
