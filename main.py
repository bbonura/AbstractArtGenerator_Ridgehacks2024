#
# All the code for this project is in a single file :)
#

import turtle
import random
# for hsv to rgb
import colorsys
import tkinter as tk
from tkinter.filedialog import asksaveasfile
import os
from wand.image import Image
import shutil


# Fullscreen the canvas
screen = turtle.Screen()
screen.setup(1.0, 1.0)

# Begin!
t = turtle.Turtle()
r = random.Random()

# changes rbg from out of 1 to out of 256
turtle.colormode(255)

# makes turtle as fast as possible
t.speed(0)

# preset color palettes (rgb)
PASTEL = [(205, 180, 219), (255, 200, 221), (255, 175, 204), (189, 224, 254), (162, 210, 255)]
SUNSET = [(238,175,97), (251,144,98),	(238,93,108), 	(106,13,131),(255, 255, 76)]
VINTAGE = [(121, 125, 98), (186, 165, 135), (241, 220, 167),(255, 203, 105), (232, 172, 101)]

# 
# Functions to draw each shape
#
def draw_rectangle(length, width, angle, xpos, ypos, color):
  t.penup()
  t.setpos(xpos, ypos)
  t.pendown()
  t.rt(angle)
  t.color(color)
  t.begin_fill()
  for i in range(2):
    t.forward(length)
    t.right(90)
    t.forward(width)
    t.right(90)
  t.end_fill()

def draw_circle(radius, xpos, ypos, color):
  t.penup()
  t.setpos(xpos, ypos)
  t.color(color)
  t.begin_fill()
  t.circle(radius)
  t.end_fill()

def draw_triangle(leg1, leg2, angle1, angle2, xpos, ypos, color):
  t.penup()
  t.setpos(xpos, ypos)
  t.pendown()
  t.rt(angle1)
  t.color(color)
  t.begin_fill()
  t.fd(leg1)
  t.rt(angle2)
  t.fd(leg2)
  t.setpos(xpos, ypos)
  t.end_fill()

# draws a randomized shape
# color should be a tuple in the form of (r, g, b)
def draw_random(color, scale):

  canvasWidth = turtle.window_width()
  canvasHeight = turtle.window_height()
  r, g, b = color

  x = random.randint(0, canvasWidth) - canvasWidth/2
  y = random.randint(0, canvasHeight) - canvasHeight/2

  # random shape
  shape = random.randint(1, 3)

  match shape:
    case 1:
      radius = random.randint(5*scale, 50*scale)
      draw_circle(radius, x, y, (r, g, b))

    case 2:
      l = random.randint(5*scale, 80*scale)
      w = random.randint(5*scale, 80*scale)
      angle = random.randint(0, 359)
      draw_rectangle(l, w, angle, x, y, (r, g, b))

    case 3:
      leg1 = random.randint(5*scale, 80*scale)
      leg2 = random.randint(5*scale, 80*scale)
      angle1 = random.randint(0, 359)
      angle2 = random.randint(0, 359)
      draw_triangle(leg1, leg2, angle1, angle2, x, y, (r, g, b))

  #uncomment to draw after every shape:
  #screen.update()

# draws all shapes, cycles through color list
def draw_all(rgb_list, num_shapes, scale):
  for i in range(num_shapes):
    draw_random(rgb_list[i % len(rgb_list)], scale)

#takes in h (0-360), s (0-100), v (0-100) as floats
def hsv_to_rgb(h, s, v):
  """Red falls between 0 and 60 degrees.
  Yellow falls between 61 and 120 degrees.
  Green falls between 121 and 180 degrees.
  Cyan falls between 181 and 240 degrees.
  Blue falls between 241 and 300 degrees.
  Magenta falls between 301 and 360 degrees.

  0-100% saturation (i.e. radius of color wheel)

  0-100% value (i.e. brightness)"""
  return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h/360, s/100, v/100))

# takes an hsv tuple and returns list of rgb tuples
def make_color_palette(initial_color):

  # make an analogous color palette
  h, s, v = initial_color
  result = []
  for i in range(-2, 3):
    result.append(hsv_to_rgb(h + i * 15, s, v))
  return result

def start_turtle(initial_color, num_shapes, scale):

  # turns off tracer, i will update screen after every shape
  screen.tracer(0)

  # draw all
  match initial_color.lower():
    case "vintage":
      draw_all(VINTAGE, num_shapes, scale)
    case "pastel":
      draw_all(PASTEL, num_shapes, scale)
    case "sunset":
      draw_all(SUNSET, num_shapes, scale)
    case _:
      initial_color = (r.randrange(0, 361), r.randrange(50,101), r.randrange(30,101)) # hsv
      palette = make_color_palette(initial_color) # rgb
      draw_all(palette, num_shapes, scale)

  #save_image()
  screen.update()
  #screen.mainloop()

def tkinter_input_window():
  root = tk.Tk()
  root.geometry( "450x450" )
  
  v = tk.StringVar(root, "random")

  # Dictionary to create multiple buttons
  values = {"Random" : "random",
          "Pastel" : "pastel",
          "Sunset" : "sunset",
          "Vintage" : "vintage"}

  # Loop is used to create multiple Radiobuttons
  # rather than creating each button separately
  for (text, value) in values.items():
    tk.Radiobutton(root, text = text, variable = v,
                  value = value).pack(ipady = 5)

  def clicked_ok():
    color = v.get()
    num_shapes = int(slider.get())
    scale = int(slider2.get())
    root.destroy()
    start_turtle(color, num_shapes, scale)

  # number of shapes
  label3 = tk.Label( root , text = "\nInput number of shapes:" ).pack()
  slider = tk.Scale(root, orient='horizontal', from_=50, to=1000, troughcolor="gray", bd="0")
  slider.pack()

  # scale
  label4 = tk.Label( root , text = "\nInput scale:" ).pack()
  slider2 = tk.Scale(root, orient='horizontal', from_=1, to=10, troughcolor="gray", bd="0")
  slider2.pack()


  ok_button = tk.Button( root , text = "OK" , command = clicked_ok ).pack()

  # Execute tkinter
  root.mainloop()


def save_image(_, __):

  dir = os.path.join(os.path.dirname(__file__), "tempImages")

  psFile = os.path.join(dir, "AbstractArt.ps")
  pngFile = os.path.join(dir, "AbstractArt.png")

  turtle.getcanvas().postscript(file=psFile)
  with Image(filename=psFile) as img:
    img.format = 'png'
    img.save(filename=pngFile)
  file = asksaveasfile(defaultextension=".png", filetypes=[("png file", ".png")])
  shutil.move(pngFile, file.name)

  os.remove(psFile) # optional
  

screen.onscreenclick(save_image)

if __name__ == "__main__":
  tkinter_input_window()
  #start_turtle()




