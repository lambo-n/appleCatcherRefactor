from processing import * 
import random
from oldapple import*


# put button in menu state to go to shop
# in shop, put more buttons for different upgrades
#adding a currency (alps)

def setup ():
  
  global heart, basketx, baskety, basket,pauseimg,resumeimg,alps,alpsimg,speed,orange
  global applelist,score,lives,difficulty,gameState,orangeBought,notEnoughTimer
  global orangeEquip,pearOwned,pearBought,pearEquipped,pear,settings,previousState
  
  global orangeOwned,orangeEquipped
  global orangeBoughtFlashFrames,orangeBoughtFlashMax,pearBoughtFlashFrames,pearBoughtFlashMax
  global bgIndex,bgColors,showCords,bgSettings,baseSpeed,boosterList,speedBoostTimer,boostAmmount,boostLength,boosterSpawnCooldown
  global orangeOwned , orangeEquipped, orangeBoughtFlashFrames,orangeBoughtFlashMax,orange,pearBoughtFlashMax
  
  global basketx, baskety, basket,difficulty,gameState,lives,score,applelist,alps,alpsimg,speed,orange,orangeBought
  global orangeEquip,pearOwned,pearBought,pearEquipped,pear,settings,previousState,trailPoints,save
  
  global bgColors,bgIndex,showCords,bgSettings,trailOwned,trailBought,trailEquipped,trailBoughtFlashMax,trailBoughtFlashFrames,trail,trailMaxLength,saveIcon,saveLevel
  alpsimg=loadImage("pixil-frame-0 (6).png")
  pauseimg=loadImage("pause.png")
  heart=loadImage("heartemoji.png")
  resumeimg=loadImage("resume.png")
  basket= loadImage("download__4_-removebg-preview.png")
  basketx=191
  baskety=220
  orange=loadImage("ORANGE.png")
  pear=loadImage("PEAR.png")
  settings=loadImage("settings.png")
  trail=loadImage("trail.png")
  showCords=True
  save = False
  saveIcon =loadImage("saveicon.png")
  saveLevel = 1
                                                                
 
  size(500,500)
              

  applelist = []
  shop= []
  score = 0
  lives = 3
  difficulty=3
  gameState = "menu"
  previousState= "menu"
  alps=100
  speed=9
  baseSpeed=9
  boosterList=[]
  speedBoostTimer=0
  boostAmmount=5
  boostLength=150
  boosterSpawnCooldown=0
  trailPoints= []
  trailMaxLength = 30
  bgColors=[(21, 39, 237),(219, 98, 22),(56, 217, 75),(245, 232, 93),(0,255,0),(255, 255, 0),(0, 255, 255),(255, 0, 255),(255, 165, 0),(128, 0, 128),(255, 192, 203),(165, 42, 42),(0, 128, 0),(0, 0, 128),(0, 128, 128),(128, 128, 0),(128, 128, 128)]
  bgIndex=0
  bgSettings=[(30,30,30),(219, 98, 22),(56, 217, 75),(245, 232, 93),(0,255,0),(255, 255, 0),(0, 255, 255),(255, 0, 255),(255, 165, 0),(128, 0, 128),(255, 192, 203),(165, 42, 42),(0, 128, 0),(0, 0, 128),(0, 128, 128),(128, 128, 0),(128, 128, 128)]
  orangeBought = False
  notEnoughTimer=0

  
  orangeOwned = False
  orangeEquipped = False
  orangeBoughtFlashMax = 45
  orangeBoughtFlashFrames = 0
  
  
  
  pearOwned = False
  pearBought = False
  pearEquipped = False
  pearBoughtFlashMax = 45 
  pearBoughtFlashFrames = 0
  
  trailOwned = False
  trailBought = False
  trailEquipped = False
  trailBoughtFlashMax = 45
  trailBoughtFlashFrames = 0
  
  
def currentBasketImg():
  global basket, orangeEquipped, orange,pearOwned,pearBought,pearEquipped,pear,trailOwned,trailBought,trailEquipped,trail
  
  if pearEquipped:
    return pear
  if orangeEquipped: 
    return orange
  return basket
  
def createBooster():
  
  return {
    "x":random.randint(30,470),
    "y":-20,
    "size":40,
    "fallSpeed":4}

    

def drawBooster(booster):
  fill(255,230,0)
  ellipse(booster["x"],booster["y"],booster["size"],booster["size"])
  fill(0,120,255)
  textSize(18)
  text("S",booster["x"] - 5, booster["y"] + 6)
  

def startGame(level):
  global gameState,difficulty,baseSpeed,speed,speedBoostTimer,boosterList, saveLevel
  global applelist, score, lives, basketx, baskety
  
  if level == 1:
    difficulty=1
    baseSpeed=9
    saveLevel = 1

  elif level == 2:
   difficulty=3
   baseSpeed=9
   saveLevel = 2
   
  elif level == 3:
   difficulty=6
   baseSpeed=11
   saveLevel= 3  
  
  speed = baseSpeed
  speedBoostTimer=0
  boosterList=[]
  applelist = []
  score=0
  lives = 3
  basketx=191
  baskety=220
  gameState = "play"
  
  
def drawTrail():
  global trailPoints,trailMaxLength
  
  noStroke()
  
  for i in range(len(trailPoints)):
    x,y=trailPoints[i]
    
    size = 10
    alpha = 70
    
    fill(237, 9, 9,alpha)
    ellipse(x,y,size,size)
    
  stroke(0)  
   
def draw():
  
  global heart, basketx, baskety, basket,pauseimg,resumeimg,alps,alpsimg,speed,orange
  global applelist,score,lives,difficulty,gameState,orangeBought,notEnoughTimer
  global orangeEquip,pearOwned,pearBought,pearEquipped,pear,settings,previousState
  
  global orangeOwned,orangeEquipped
  global orangeBoughtFlashFrames,orangeBoughtFlashMax,pearBoughtFlashFrames,pearBoughtFlashMax
  global bgIndex,bgColors,showCords,bgSettings,baseSpeed,boosterList,speedBoostTimer,boostAmmount,boostLength,boosterSpawnCooldown
  global orangeOwned , orangeEquipped, orangeBoughtFlashFrames,orangeBoughtFlashMax,orange,pearBoughtFlashMax
  
  global basketx, baskety, basket,difficulty,gameState,lives,score,applelist,alps,alpsimg,speed,orange,orangeBought
  global orangeEquip,pearOwned,pearBought,pearEquipped,pear,settings,previousState
  
  global bgColors,bgIndex,showCords,bgSettings,baseSpeed,boosterList,speedBoostTimer,save
  global boostAmmount,boostLength,boosterSpawnCooldown,trail,trailOwned,trailPoints,trailMaxLength,trailBoughtFlashFrames,trailMaxLength,saveLevel
  

  
  background(bgColors[bgIndex][0], bgColors[bgIndex][1], bgColors[bgIndex][2])
  
  image(alpsimg,220,-50,200,200)
  
  fill(48, 217, 205)
  textSize(20)
  text(":",345 ,36)
  
  text(alps, 357,36)
  
  if orangeBoughtFlashFrames > 0:
     orangeBoughtFlashFrames -=1
  
  if pearBoughtFlashFrames > 0:
     pearBoughtFlashFrames -=1
     
  if trailBoughtFlashFrames > 0:
     trailBoughtFlashFrames -=1
      
 

  
  if gameState == "menu":

    #these are the level rectangle thinges

    fill(255,255,255)
    rect(75,200,100,50)
    rect(200,200,100,50)             
    rect(325,200,100,50)
    rect (200,350,100,50)
    rect(0,0,50,50)
    image(settings,-10,0,70,50)
    

   

    #these are the level text 
    fill(31, 150, 255)
    textSize(20)
    text("Level 1", 94,234)
    text("Level 2", 219,234)  
    text("Level 3", 344,234)
    text("Shop", 226,384)
    
    if save:
      fill(255,255,255)
      rect(50,0,100,50)
      
      fill(31, 150, 25)
      textSize(17)
      text("Continue", 65,24)
      text("Level "+str(saveLevel),72, 43)
    
    if keyPressed:
      if (key=='1'):  
        startGame(1)

        
     
        

      if (key=='2'):
        startGame(2)


        
      if (key=='3'):
        startGame(3)

        
      if (key=='`'):
        gameState = "shop"


      if (key=="s" or key=="S"):
        gameState = "settings"
   
      if (key=="c" or key=="C"):
        gameState = "paused"

       
    
    # this is the mouse location stuff very precise and also the speed and difficulty of levels
    
    
  
    
    if mousePressed:
       #lvl 1
      if 75 <= mouseX <=175 and 200 <= mouseY <= 250:
        startGame(1)
       
        #lvl 2
      if 200 <= mouseX <=300 and 200 <= mouseY <= 250:
        startGame(2)
       
       #lvl 3
      if 325 <= mouseX <=425 and 200 <= mouseY <= 250:
        startGame(3)
       
      if 200 <=mouseX <=300 and 350 <= mouseY <=400:
        gameState="shop"
        
      if 0 <= mouseX <= 50 and 0 <= mouseY <= 50:
        previousState = "menu"
        gameState = "settings"
        
      if 51 <=mouseX <= 148 and 0 <= mouseY <= 50 and save:
        gameState = "paused"

          
          
        

        
        
        
        
        
     
      
  #this is the shop display players probably dont go here because their poor🥀 🥀 🥀 
  elif gameState=="shop":
    
    image(alpsimg,330,387,200,200)
    
    fill(48, 217, 205)
    textSize(20)
    text(":",455 ,470)
    
    text(alps,465,472)
  
    
    
    fill(255,255,255)
    rect(0,0,500,50)
    
    fill(237, 22, 22)
    textSize(40)
    text("WELCOME TO THE SHOP",11,40,10)
    
    fill(255,255,255)
    rect(0,430,100,69)
    fill(237, 22, 22)
    textSize(14)
    text("Back To Menu", 6,474,20)
    
    
    

    #this is the orange rectangle
    fill(255,255,255)
    rect(10,70,80,70) 
    
   
    fill(255,255,255)
    rect(10,150,80,30)
    #These following rectangles are for the pear basket
    
    fill(255,255,255)
    rect(230,71,80,70)
    
    fill(255,255,255)
    rect(230,150,80,30)
    
    if keyPressed:
      if (key=="t" or key=="T"):
        gameState = "menu"
        
      if (key=="b" or key=="B"):
        gameState = "menu"
    
    
    orangeHoveringButton = (mouseX >= 10 and mouseX <= 90 and mouseY >= 150 and mouseY <= 180)
    
    if orangeBoughtFlashFrames > 0:
      fill (0,128,0)
      textSize(20)
      text("Bought", 18.5,172)
    else:
      if not orangeOwned:
        if orangeHoveringButton:
          if alps >=6 :
            fill(0,128,0)
            textSize(20)
            text("Buy",32,172)
          else:
            fill(232,46,53)
            textSize(13)
            text("Not enough" ,17,170)
        
        else:
          fill(237,141,45)
          textSize(20)
          text("6 Alps",22,173)
      else:
        if orangeEquipped:
          if orangeHoveringButton:
            fill(237,141,45)
            textSize(18)
            text("Unequip",17.5,171)
            
          else:
            fill(237,141,45)
            textSize(18)
            text("Unequip",17.5,171)
        else:
          if orangeHoveringButton:
            fill(0,128,0)
            textSize(20)
            text("Equip",24,171)
            
            
          else:
            fill(237,141,45)
            textSize(20)
            text("Equip",24,171)
            
            
        
            
    #this is the orange image also annoying to position fr
    image(orange,20,70,60,60)
    

    #Pear rectangle positions
    fill(255,255,255)
    rect(120,70,80,70) 
    
   
    fill(255,255,255)
    rect(120,150,80,30)
    
    PEAR_COST = 8 
    pearHoveringButton = (mouseX >= 121 and mouseX <= 199 and mouseY >= 150 and mouseY <= 180)
    
    if pearBoughtFlashFrames > 0:
      fill (0,128,0)
      textSize(20)
      text("Bought", 128,173)
    else:
      if not pearOwned:
        if pearHoveringButton:
          if alps >=8 :
            fill(0,128,0)
            textSize(20)
            text("Buy",141,172)
          else:
            fill(232,46,53)
            textSize(13)
            text("Not enough" ,126,170)
        
        else:
          fill(237,141,45)
          textSize(20)
          text("8 Alps",132,173.5)
      else:
        if pearEquipped:
          if pearHoveringButton:
            fill(237,141,45)
            textSize(18)
            text("Unequip",127,172)
            
          else:
            fill(237,141,45)
            textSize(18)
            text("Unequip",127,172)
        else:
          if pearHoveringButton:
            fill(0,128,0)
            textSize(20)
            text("Equip",134,173)
            
            
          else:
            fill(237,141,45)
            textSize(20)
            text("Equip",134,173)
            

    
    
    
    #Pear image positions
    image(pear,121,64,80,80)
    
    #-------------------------------------------------------------------------------------------------
    #Trail shop 
    
    
    
    
    TRAIL_COST = 9 
    trailHoveringButton = (mouseX >= 231 and mouseX <= 308 and mouseY >= 150 and mouseY <= 180)
    
    if trailBoughtFlashFrames > 0:
      fill (0,128,0)
      textSize(20)
      text("Bought", 238,173)
    else:
      if not trailOwned:
        if trailHoveringButton:
          if alps >=9 :
            fill(0,128,0)
            textSize(20)
            text("Buy",251,173)
          
          else:
            fill(232,46,53)
            textSize(13)
            text("Not enough" ,238,170)
        
        else:
          fill(237,141,45)
          textSize(20)
          text("9 Alps",242,173.5)
      else:
        
        if trailEquipped:
          if trailHoveringButton:
            fill(237,141,45)
            textSize(18)
            text("Unequip",237,172)
            
          else:
            fill(237,141,45)
            textSize(18)
            text("Unequip",237,172)
        else:
          if trailHoveringButton:
            fill(0,128,0)
            textSize(20)
            text("Equip",244,173)
            
            
          else:
            fill(237,141,45)
            textSize(20)
            text("Equip",244,173)
            

    image(trail,240,76,60,60)

  elif gameState == "settings":

    background(bgSettings[bgIndex][0], bgSettings[bgIndex][1], bgSettings[bgIndex][2])
    textSize(40)
    text("SETTINGS", 150, 60)
    
    fill(255,255,255)
    rect(410,460,90,40) 
    fill(0,0,0)
    textSize(18)
    text("Back",433,490)
    
    
    fill (220,220,220)
    rect (110,120,270,50)
    fill(0,0,0)
    textSize(18)
    text("Background color",170,150)
    
    
    fill(220,220,220)
    rect(110,180,270,50)
    fill(0,0,0)
    textSize(18)
    cordsLabel = "Cords:ON" if showCords else "Cords:OFF"
    text(cordsLabel,200,210)
    
    if keyPressed:
      if (key=="b" or key=="B"):
        gameState = "menu"

      if (key=="c" or key=="C"):
        showCords = False
        
      if (key=="g" or key=="G"):
        pass

#this is the paused gamestate dont abuse it you noob players  
  elif gameState == "paused": 
    
    if trailEquipped:
      drawTrail()
      
      
    image(currentBasketImg(),basketx,baskety,100,50)
    for apple in applelist:
      apple.display()
    for booster in boosterList:
      drawBooster(booster)
    showScore()
    showLives()
    
    
    
    fill(255, 255, 255)
    rect(447, 10, 50, 50)# x, y, w, h
    image(resumeimg,448,11,50,50)
    fill (255,255,255)
    rect(320,11,100,50)
    fill(0,0,0)
    text("Menu",338,44)
    fill (255,255,255)
    rect(254,11,50,50)
    image(settings, 244,11,70,50)
    
    if speedBoostTimer>0:
      fill(255,240,0)
      textSize(20)
      text("BOOST READY",180,90)
    if keyPressed:  
      if (key=="q" or key=="Q"):
        gameState = "play"
    
      if (key=="b" or key=="B"):
        gameState = "menu"
        
      if (key=="s" or key=="S"):
        gameState = "settings"
  
   #game over things u prob see this screen a lot players who are bad at the game (get better)  
  elif gameState =="gameOver":
    
    background(0,0,0)
     
    fill(80, 240, 31)
    textSize(75)
    text("GAME OVER", 20,250) 
    
    textSize(35)
    fill(73, 217, 48)
    text("Final Score: " + str(score),138.5,423,100)
    #text(str(score),299,450.5,100)
    
    if keyPressed:
       if (key==' '):
        
          gameState="menu"
    
    
    
    
    
    fill(80,240,31)
    rect (150,300,200,50)
    

    
    
    fill (35, 161, 156)
    textSize(40)
    text("MENU" , 193,340)
    
    
    
    
    
    #so this is the game over button
    #ik you press it too much and you are not getting a shortut just get better at thhe game ig
    if mousePressed:
      if 150 <= mouseX <=325 and 300 <= mouseY <= 350: 
        
        save=False 
        applelist = []
        boosterList=[]
        score=0
        lives = 3
        gameState= "menu"  
        speedBoostTimer=0
        speed=baseSpeed
        basketx=191
        baskety=220
        trailPoints = []
    
  #this is the apple spawn things and if you play in level 1 alot just quit already i dont want you hereu here
  elif gameState=="play":
    spawnChance = random.randint(1,57)
    if spawnChance == 8:
      applelist.append(Apple(difficulty))
    
    if boosterSpawnCooldown > 0:
      boosterSpawnCooldown -=1 
    else:
      boosterChance = random.randint(1,220)
      if boosterChance == 12:
        boosterList.append(createBooster()) 
        boosterSpawnCooldown = 120
        
    if speedBoostTimer > 0:
      speedBoostTimer -= 1
      speed = baseSpeed + boostAmmount
    else:
      speed=baseSpeed
    
    if trailEquipped:
     trailPoints.append((basketx + 50, baskety +30))
     
     if len(trailPoints)>trailMaxLength:
       trailPoints.pop(0)
       
     drawTrail()     

    image(currentBasketImg(),basketx,baskety,100,50)
  

    
    for apple in applelist[:]:
      apple.move()
      apple.display()
      
      if apple.appley >= 425:
        applelist.remove(apple)
        lives-=1
      elif basketx-49<= apple.applex <= basketx + 100 and  baskety - 49 <= apple.appley <= baskety:
        applelist.remove(apple)
        score += 1
       
        #these are alps your prob poor and cant afford anything 🥀 🥀 🥀 🥀
        if score % 5 ==0 and difficulty==1:
         alps +=1
         
        if score % 3 ==0 and difficulty==3:
         alps +=1  
         
        if score % 2 ==0 and difficulty==6:
         alps +=1   
         
    for booster in boosterList[:]:
      booster["y"]+=booster ["fallSpeed"]
      drawBooster(booster)
          
      if booster["y"]>520:
        boosterList.remove(booster)
      elif basketx - 20 <= booster["x"] <= basketx + 100 and baskety - 35 <= booster["y"] <= baskety + 20:   
        boosterList.remove(booster)
        speedBoostTimer = boostLength
        
        
    if speedBoostTimer > 0:
       fill(255,230,0)
       textSize(22)
       text("Boost!",210,80)    
        
    #these are the basket controls
    if keyPressed:
      if (keyCode==LEFT  or key== 'a' or key== 'A') and basketx >= 0 :
        basketx=basketx - speed
      
      if (keyCode==RIGHT  or key== 'd' or key=='D') and basketx<=400: 
        basketx=basketx + speed
        
      if (keyCode==DOWN  or key== 's' or key== 'S')  and baskety<=450:
        baskety=baskety + speed
      
      if (keyCode==UP  or key== 'w' or key=='W')  and baskety>=0:
        baskety=baskety - speed
        
      if (key=="`"):
        gameState = "paused"
        
       
      
    


        
        
   
   #this is the life controls your so bad you def loose a lot of these
    if lives<=0:
      gameState = "gameOver"
     
    showScore()
    showLives()
    

    
    fill(255, 255, 255)
    rect(447, 10, 50, 50)  # x, y, w, h
    image(pauseimg,448,11,50,50)
  
  # mouse cordinantes
  
  if showCords:
    fill (255, 0, 0)
    textSize(15) 
    text(str(mouseX) + ", " + str(mouseY), 20, 497)

 #these are the scores and their text ik you dont get that high of a score noob      
def showScore():
  
  fill (255, 255, 255)        
  textSize(25)
  scoreText= "Score: " + str(score)
  text(scoreText,41,38)
  
#these are the show lives so they stay on your screen (they probably dont stay on ur screen cause ur bad)
def showLives():
  global lives,heart
  heartX = 330
  heartY = 425
  for i in range(lives):
    image(heart,heartX, heartY, 70,50)
    heartX+= 50

#this is the pause gamestate 
def mousePressed():
  global gameState, applelist,score,lives,basketx,baskety,orangeBought,notEnoughTimer,orangeEquipped,previousState
  global orangeOwned,orangeBoughtFlashFrames, orangeBoughtFlashMax,alps,pearOwned,pearBought,pearEquipped,pear,pearBoughtFlashFrames,pearBoughtFlashMax
  global previousState,bgIndex,bgColors,showCords,bgSettings,boosterList,speedBoostTimer,speed,baseSpeed,speed,trail,trailBoughtFlashFrames,trailOwned,trailEquipped,trailBought,trailBoughtFlashMax,trailPoints
  global save,saveLevel
  if 447 <= mouseX <= 497 and 10 <= mouseY <= 60:
    if gameState == "play":
      gameState="paused"
      return
    
    elif gameState=="paused":
      gameState="play"
      return
      
    if 200 <= mouseX <= 250 and 10 <= mouseY <= 60:
      gameState = "settings" #Next time I need to add an option to go back to the game
      #that was happening before pressing the settings button and the gamestate should stay in paused
  
  if 320 <= mouseX <= 420 and 11 <= mouseY <= 61:
    if gameState=="paused":
      # applelist = []
      # score=0
      # lives = 3
      # gameState= "menu"
      # speedBoostTimer=0
      # speed=baseSpeed
      # boosterList=[]
      # basketx=191
      # baskety=220
      
      gameState = "menu"
      save = True
    return
  
  if gameState == "paused":
    if 244<= mouseX <= 314 and 10 <= mouseY <= 61:
      previousState = "paused"
      gameState = "settings"
      return 
  
  if gameState == "settings":
    if 411 <= mouseX <= 498 and 461 <= mouseY <= 500:
      gameState = previousState
      return 
      
    
    if 112 <= mouseX <= 378 and 123 <= mouseY <= 172:
      bgIndex = (bgIndex+1) % len(bgColors)
      return
    
    if 110 <= mouseX <= 382 and 182 <= mouseY <= 231:
      showCords=not showCords
      return
    
     
      
  if gameState == "shop":
    if 20 <= mouseX <= 90 and 433 <= mouseY <= 493:
      gameState = "menu"
      return
    if 10 <= mouseX <= 90 and 150 <= mouseY <= 180:
      
      if orangeBoughtFlashFrames > 0:
        return
      if not orangeOwned:
        if alps >= 6:
          orangeOwned = True
          orangeEquipped = False
          alps -= 6
          orangeBoughtFlashFrames = orangeBoughtFlashMax
        return
      orangeEquipped = not orangeEquipped
      if orangeEquipped:
        pearEquipped = False
      return
    
    if 121 <= mouseX <= 199 and 150 <= mouseY <= 180:
      if pearBoughtFlashFrames > 0:
        return
      PEAR_COST = 8
      if not pearOwned:
        if alps >= PEAR_COST:
          pearOwned = True
          alps -= PEAR_COST
          pearBoughtFlashFrames = pearBoughtFlashMax
        return
    
      pearEquipped = not pearEquipped
      if pearEquipped:
        orangeEquipped = False
      return
    
#------------------------------------------------------------------------------------    
    #Trail mousepressed
    
    if 231 <= mouseX <= 308 and 150 <= mouseY <= 180:
      if trailBoughtFlashFrames > 0:
        return
      TRAIL_COST = 9
      
      if not trailOwned:
        if alps >= TRAIL_COST:
          trailOwned = True
          alps -= TRAIL_COST
          trailBoughtFlashFrames = trailBoughtFlashMax
        return
    
      trailEquipped = not trailEquipped
      trailPoints = []
      return
    
    
    
        


      
run ()
