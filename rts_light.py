import pygame,random
import sys
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Display Window")

run = True





w, h = pygame.display.get_surface().get_size()



screenSizeX = 40
screenSizeY = 40
tileW = w / screenSizeX
tileH = h / screenSizeY
scrollModX = 0 
scrollModY = 0

mapDimension = 100

mapTracker = [''] * (mapDimension*mapDimension)



treeImage = pygame.image.load('Tree.png')
treeImage = pygame.transform.scale(treeImage,(round(tileW),round(tileH)))
castleImage = pygame.image.load('castle.png')
castleImage = pygame.transform.scale(castleImage,(round(tileW*2),round(tileH*2)))
houseImage = pygame.image.load('house.png')
houseImage = pygame.transform.scale(houseImage,(round(tileW),round(tileH))) 
npcImage = pygame.image.load('npc.png')
npcImage = pygame.transform.scale(npcImage,(round(tileW/2),round(tileH/2))) 
roadImage = pygame.image.load('road.png')
roadImage = pygame.transform.scale(roadImage,(round(tileW),round(tileH)))
waterImage = pygame.image.load('water.png')
waterImage = pygame.transform.scale(waterImage,(round(tileW),round(tileH)))
groundImage = pygame.image.load('ground.png')
groundImage = pygame.transform.scale(groundImage,(round(tileW),round(tileH)))
mountainImage = pygame.image.load('mountain.png')
mountainImage = pygame.transform.scale(mountainImage,(round(tileW),round(tileH)))


map = []
npcs = []

commandToggle = False




# Create your dictionary class
class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
          
    # Function to add key:value
    def add(self, key, value):
        self[key] = value


font = pygame.font.SysFont('System',30)

stats = {'Population':0, 'Recruitment':0, 'Wood':0, 'Food':0, 'Fuel':0, 'Ammo':0}

trackedSeedsGround = my_dictionary()
trackedSeedsForest = my_dictionary()
trackedSeedsMountain = my_dictionary()  

def generateMap():
     
     for i in range(40):
          seedX = random.randint(0,60)
          seedY = random.randint(0,60)
          for j in range(random.randint(10,10)):
               for k in range(random.randint(10,10)):
                    genX = seedX + j+random.randint(1,2)
                    genY = seedY + k     
                    if (str(genX)+":"+str(genY)) not in trackedSeedsGround:
                         trackedSeedsGround.add(str(genX)+":"+str(genY),'true')

                         map.append({'x':genX, 'y':genY,'image':groundImage, 'hp':5,'type':'earth'})
               
     for i in map:
          if(i['type'] == 'earth' and random.randint(1,10) < 3):
               for j in range(random.randint(3,8)):
                    genX = i['x'] + random.randint(-1,1)
                    genY = i['y'] + random.randint(-1,1)
                    if (str(genX)+":"+str(genY)) not in trackedSeedsForest:
                         if(str(genX)+":"+str(genY) in trackedSeedsGround):
                              trackedSeedsForest.add(str(genX)+":"+str(genY),'true')
                              map.append({'x':genX, 'y':genY,'image':treeImage, 'hp':5,'type':'tree'})
          else:
               genX = i['x']
               genY = i['y']
               if (str(genX)+":"+str(genY)) not in trackedSeedsForest and random.randint(1,100) < 2:
                    for j in range(4):
                         newX = genX + random.randint(-1,1)
                         newY = genY + random.randint(-1,1)
                         if(str(newX)+":"+str(newY) in trackedSeedsGround):
                              map.append({'x':newX, 'y':newY,'image':houseImage,'hp':15,'type':'house'})
     for i in map:
          if(i['type'] == 'earth' and random.randint(1,1000) < 10):
               for j in range(10):
                    genX = i['x'] + j + random.randint(-3,0)
                    genY = i['y'] + j + random.randint(-3,0)
                    if(str(genX)+":"+str(genY) in trackedSeedsGround):
                         map.append({'x':genX, 'y':genY,'image':mountainImage,'hp':100,'type':'mountain'})

def renderMap():
     for i in map:
          if(i['hp'] > 0):
               if(scrollModX <= i['x']*tileW <= scrollModX + (screenSizeX*tileW)):
                    if(scrollModY <= i['y']*tileH <=scrollModY + (screenSizeY*tileH)):
                         screen.blit(i['image'],(i['x']*tileW - scrollModX,i['y']*tileH - scrollModY))


def npcGenerate():
     for i in map:
          if i['image'] == houseImage:
               for j in range(random.randint(1,1)):
                    npcs.append({'x':i['x']+random.randint(-2,2), 'y':i['y']+random.randint(-2,2),'image':npcImage, 'state': 'passive','selected':False, 'dest':[0,0],'collisionCount':0,'type':'peasent', 'hp':0,'skills':[]})
                    stats['Population']+=1


def renderNPC():
     for i in npcs:
          screen.blit(i['image'],(i['x']*tileW+(tileW/4) - scrollModX,i['y']*tileH+(tileH/4) - scrollModY))
          if(i['selected']):
               pygame.draw.rect(screen,(0,0,0),(i['x']*tileW - scrollModX,i['y']*tileH - scrollModY,tileW,tileH),1)
               

def npcAI():
     count = 0
     for i in npcs:
          if(i['state'] == 'excited'):
               i['x'] += random.randint(-1,1)
               i['y'] += random.randint(-1,1)
          elif(i['state'] == 'commanded'):
               if(i['x'] < i['dest'][0]):
                    i['x']+=1
                    if(collisionDetection([i['x'],i['y']], [i['x'],i['y']],count)):
                         i['x']+= -1
               if(i['x'] > i['dest'][0]):
                    i['x']-=1
                    if(collisionDetection([i['x'],i['y']], [i['x'],i['y']],count)):
                         i['x']+= 1
               if(i['y'] < i['dest'][1]):
                    i['y']+=1
                    if(collisionDetection([i['x'],i['y']], [i['x'],i['y']],count)):
                         i['y']+= -1
               if(i['y'] > i['dest'][1]):
                    i['y']-=1
                    if(collisionDetection([i['x'],i['y']], [i['x'],i['y']],count)):
                         i['y']+= 1

               if(i['collisionCount'] > 10):
                    i['state'] = 'passive'
                    i['collisionCount'] = 0

               if(i['x'] == i['dest'][0]):
                    if(i['y'] == i['dest'][1]):
                         i['state'] = 'passive'
          count+=1   
          

def sortMap():
     for i in map:
          if(i['type'] == 'keep'):
               map.remove(i)
               map.append(i)
     for i in map:
          if(i['type'] == 'peasent'):
               map.remove(i)
               map.append(i)



def hitDetection(pos):
     for i in npcs:
          if((pos[0] - (tileW/2) + scrollModX) < (i['x'] * tileW) < (pos[0] + (tileW/2)+scrollModX)):
               if((pos[1] - (tileH/2) + scrollModY) < (i['y'] * tileH) < (pos[1] + (tileH/2) + scrollModY)):
                    i['selected'] = not i['selected']
               else:
                    if(i['selected']):
                         i['dest'] = [round((pos[0]+scrollModX)/tileW),round((pos[1]+scrollModY)/tileH)]
                         i['state'] = 'commanded'
                         i['selected'] = False
          else:
               if(i['selected']):
                    i['dest'] = [round((pos[0]+scrollModX)/tileW),round((pos[1]+scrollModY)/tileH)]
                    i['state'] = 'commanded'
                    i['selected'] = False





def roadGenerate():
     startX = 0
     startY = 0
     endX = 0
     endY = 0

     startEndToggle = True
     runPath = False

     for i in map:
          if(i['type']=="keep"):
               startX = i['x']
               startY = i['y']
               for j in map:
                    if(j['type']=='keep' and (abs(i['x'] - j['x']) < 20 and abs(i['y'] - j['y']) < 20) and i != j):
                         endX = j['x']
                         endY = j['y']
                         runPath = True
                         count = 0
                         notFound = True
                         leftRightToggle = False
                         while(notFound):
                              count+=1
                              leftRightToggle = not leftRightToggle
                              if(leftRightToggle):
                                   if(startX < endX):
                                        startX+=1
                                   elif(startX > endX):
                                        startX-=1
                                   map.append({'x':startX, 'y':startY,'image':roadImage,'hp':3,'type':'road'})
                              else:
                                   if(startY < endY):
                                        startY+=1
                                   elif(startY > endY):
                                        startY-=1
                                   map.append({'x':startX, 'y':startY,'image':roadImage,'hp':3,'type':'road'})
                              if(startX == endX and startY == endY):
                                   notFound = False
                              if(count > 100):
                                   notFound = False

def riverGenerate():
     for i in range(4):
          startX = random.randint(10,40)
          startY = random.randint(10,40)
          endX = startX + (random.randint(-100,100))
          endY = startY + (random.randint(-100,100))
          runPath = True
          count = 0
          leftRightToggle = False
          notFound = True
          while(notFound):
               count+=1
               leftRightToggle = not leftRightToggle
               if(leftRightToggle):
                    if(startX < endX):
                         startX+=1
                    elif(startX > endX):
                         startX-=1
                         map.append({'x':startX, 'y':startY,'image':waterImage,'hp':3,'type':'water'})
               else:
                    if(startY < endY):
                         startY+=1
                    elif(startY > endY):
                         startY-=1
                         map.append({'x':startX, 'y':startY,'image':waterImage,'hp':3,'type':'water'})
               if(startX == endX and startY == endY):
                    notFound = False
               if(count > 80):
                    notFound = False






def command(pos):
     for i in npcs: 
          if(i['selected']):
               i['dest'] = [round((pos[0]+scrollModX)/tileW),round((pos[1]+scrollModY)/tileH)]
               i['state'] = 'commanded'
               i['selected'] = False

def select(pos):
      for i in npcs:
          if((pos[0] - (tileW) + scrollModX) < ((i['x']) * tileW) < (pos[0]+scrollModX)):
               if((pos[1] - (tileH) + scrollModY) < (i['y'] * tileH) < (pos[1] + (tileH) + scrollModY)):
                    i['selected'] = not i['selected']

def npcCollision():
     for i in npcs:
          for j in map:
               if(i['x'] == j['x'] and i['y'] == j['y'] and j['type'] != 'earth'):
                    j['hp']-=1


def renderUI():
     statsLabels = ['Population', 'Recruitment', 'Wood', 'Food', 'Fuel', 'Ammo']
     count = 0
     pygame.draw.rect(screen,(0,0,0),(tileW*33,tileH*5,tileW*5,tileH*15),0)
     for i in statsLabels:
          text_surface = font.render(i+':'+str(stats[i]),False,(255,255,255))
          screen.blit(text_surface,(tileW*34,tileH*(7+count)))
          count +=1

timer = pygame.time.get_ticks()
aiTimer = pygame.time.get_ticks()


def collisionDetection(newCords,oldCords,count):
     collision = False
     newCount = 0
     for i in npcs:
          pos = [i['x'],i['y']]
          if pos == newCords and newCount != count:
               collision = True
          newCount+=1

     return collision

def collisionReset():
     for i in range(len(npcs)):
          for j in range(len(npcs)):
               if(npcs[i]['x'] == npcs[j]['x'] and npcs[i]['y'] == npcs[j]['y'] and i != j and npcs[j]['type'] != 'peasent'):
                    npcs[i]['x'] += random.randint(-1,1)
                    npcs[i]['y'] += random.randint(-1,1)
                    npcs[i]['collisionCount']+=1



def npcCull():
     for i in map: 
          if(i['hp']<1):
               map.remove(i)
               if(i['type'] == 'tree'):
                    stats['Wood']+=1





generateMap()
#riverGenerate()
roadGenerate()
npcGenerate()



sortMap()

while run:


     screen.fill((0,94,184))

     for eve in pygame.event.get():
          if eve.type==pygame.QUIT:
               pygame.quit()
               sys.exit()
               run = False
          elif eve.type == pygame.KEYDOWN:
               if(eve.key == pygame.K_ESCAPE):
                    run = False
          elif eve.type == pygame.MOUSEBUTTONUP:

               x,y = pygame.mouse.get_pos()

               if(eve.button == 1):
                    pygame.draw.rect(screen,(0,0,0),(x-(tileW/2),y-(tileH/2),tileW,tileH),0)
                    hitDetection([x,y])
               elif(eve.button == 3):
                    select([x,y])
     x,y = pygame.mouse.get_pos()




     if pygame.time.get_ticks()-timer > 30:
          timer = pygame.time.get_ticks()
          if(x > (w - tileW*2)):
               scrollModX += tileW
          if(x < tileW*2):
               scrollModX -= tileW
          if(y > (h - tileH*2)):
               scrollModY += tileH
          if(y < tileH * 2):
               scrollModY -= tileH
          renderMap()
          renderNPC()
          renderUI()
          pygame.display.flip()
     if pygame.time.get_ticks() - aiTimer > 200:
          aiTimer = pygame.time.get_ticks()
          npcAI()
          collisionReset()
          npcCollision()
          npcCull()

