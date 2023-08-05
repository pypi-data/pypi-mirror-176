import os, time, threading

GAME = False

class Screen:
  class set:
    def cam_size(weidth:int, height:int):
      global camw, camh
      camw = weidth
      camh = height

    def cam_pos(x:int, y:int):
      global camx, camy
      camx = x
      camy = y

    def background(bck_grnd:list):
      global bck_sc
      bck_sc = bck_grnd

    def player_pos(x:int,y:int):
      global playerx, playery
      playerx = x
      playery = y
      
  class background:
    def show():
      if not GAME:
        pass
      global playerx, playery ,bck_sc
      by = 1
      bx = 1
      bck_lvl = ""
      for todo1 in bck_sc:
        for todo2 in todo1:
          if bx == playerx and by == playery:
            bck_lvl += "P"
          else:
            bck_lvl += todo2
          bx += 1
        bck_lvl += "\n"
        by += 1
        bx = 1
      os.system("clear")
      print(bck_lvl)
  
class Player:
  def GoUp():
    global playery
    playery -= 1
  def GoDown():
    global playery
    playery += 1
  def GoLeft():
    global playerx
    playerx -= 1
  def GoRight():
    global playerx
    playerx += 1

class Game:  
  def START():
    global GAME
    GAME = True
    gl = threading.Thread(target=Game.do_not_open.game_loop)
    gl.start()
  
  def STOP():
    global GAME
    GAME = False
  
  class do_not_open:
    def game_loop():
      while GAME:
        time.sleep(0.6)
        Screen.background.show()
      print("Game has stopped")
  
