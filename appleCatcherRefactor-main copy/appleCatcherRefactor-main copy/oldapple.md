from processing import *
import random




class Apple:
  def __init__(self,difficulty):
    self.appley = 0
    self.speed = difficulty
    
    self.applex = random.randint(0 , 450)
    

    self.appleImage = loadImage ("apple.png")


  def move(self):
    self.appley += self.speed
  def display(self):
    image(self.appleImage, self.applex, self.appley, 70, 50)