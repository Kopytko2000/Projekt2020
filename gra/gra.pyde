
add_library('sound') #musicie sobie miski doinstalowac bibliotkę - sketch - import library - Add Library - sound i będzię dzwięk! <3
###### I niech stanie się gra #######

import sys
import random
import time
import processing.sound
w = 1366 
h = 768

statusGry = 1 # 1 - wprowadź imię
              # 2 - graj
              # 3 - koniec gry 

imie = ''
punkty = 0


#Colors

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (240 ,255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 140, 0)
CHOCOLATE = (123, 63, 0)
PINK = (255, 192, 203)
GREY = (128, 128, 128)

#ZMIENNE

global kosmos, Komandor #przez Komandor, intro rozumiem gracza
kosmos = "kosmos.jpg"
#intro = "Elite Dangerous intro.mp3" 
tlo2 = "bg_robocze2_TWH.png" #screen CMDR KartonowyMakaron The Winged Hussars 
#komputer_pokladowy = "gretting-commanders.mp3"
powi = "bg_robocze4_TWH.png"

#KLASY

class Sprite(): # <3
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        
        
class Powitanie():
    def wyswietl(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(80, 90, 600, 100)
        myFont = createFont("Candara Bold", 50)
        textFont(myFont)
        fill(0, 0, 0)
        text("Hello! Press start to begin.", 80, 100)
        
class Start():
    def pokaz(self):
        strokeWeight(0)
        fill(184, 57, 90, 80)
        rect(90, 280, 400, 150)
        myFont = createFont("Candara Bold", 45)
        textFont(myFont)
        fill(255)
        text("START!", 90, 265)
        text("Kliknij enter", 90, 330)
        
class Zamknij():
    def pokaz(self):
        fill(255)
        myFont = createFont("Candara Bold", 25)
        text("ESC", 690, 450)
    
          
class Wyjdz():
    def zobacz(self):
        strokeWeight(5)
        fill(255, 192, 203)
        rect(w/2, h/2-15, w/2, 90)
        textSize(40)
        fill(236, 69, 153)
        text("Are you sure you want to leave?",w/2, h/2)

        
class Statek():
    maksymalnaPredkosc = 6 # maksymalna prędkość statku
    maksymalnePrzyspieszenie = 6 # maksymalne przyspieszenie statku    
    def __init__(self):    
        self.pozycja = PVector(0, 0)
        self.predkosc = PVector(0, 0)
        self.przyspieszenie = PVector(0, 0)
        self.orientacja = 0 # położenie dzioba statku - kąt w radianach
        self.ochloniecie = 0 # 'cooldown' strzelania - każda klatka animacji zmniejsza tę wartość o 1. Następny pocisk można wystrzelić tylko gdy == 0
        self.rozmiar = 8

    def animuj(self):
        if self.przyspieszenie.magSq() == 0:
            self.predkosc.x *= 0.98 # 
            self.predkosc.y *= 0.98 # efekt zwalniania, gdy nie jest trzymany przycisk gazu 
        else:
            self.predkosc.x += self.przyspieszenie.x
            self.predkosc.y += self.przyspieszenie.y
            self.predkosc.limit(self.maksymalnaPredkosc)
            
        self.pozycja.x += self.predkosc.x;
        self.pozycja.y += self.predkosc.y;
        self.ochloniecie -= 1

    def strzel(self):
        if self.ochloniecie > 0:
            return None
        
        # stwórz nowy pocisk z takim kierunkiem, w jakim jest zwrócony statek
        pozycjaPocisku = self.pozycja.copy()        
        predkoscPocisku = PVector.fromAngle(self.orientacja)
        self.ochloniecie = 20
        return Pocisk(pozycjaPocisku, predkoscPocisku)
                            
    def rysuj(self):
        pushMatrix() # zachowaj macierz transformacji
        stroke(255) 
        fill(255)
        translate(self.pozycja.x, self.pozycja.y) # przesuń środek układu współrzędnych na statek                
        rotate(self.orientacja) # wykonaj obrót układu współrzędnych o kąt zgodny z orientacją statku.
                                # Wszystkie operacje na wierzchołkach będą wykonywane w kontekście takiego
                                # układu. Wywołanie popMatrix() na końcu przywraca układ do poprzedniego stanu.                                        
        circle(0, 0, 5 * self.rozmiar)
        line(0, 0, 50, 0)
        popMatrix() # przywróć macierz transformacji
        
    
    def doPrzodu(self): # ustaw predkość do przodu
        PVector.fromAngle(self.orientacja, self.przyspieszenie)
        self.przyspieszenie.limit(self.maksymalnePrzyspieszenie)
        
    def doTylu(self): # ustaw prędkość do tyłu
        PVector.fromAngle(self.orientacja, self.przyspieszenie)
        self.przyspieszenie.x = -self.przyspieszenie.x # 
        self.przyspieszenie.y = -self.przyspieszenie.y # odwróć wektor
        self.przyspieszenie.limit(self.maksymalnePrzyspieszenie)
                
    def bezNapedu(self): # wyzeruj przyspieszenie
        self.przyspieszenie.x = 0
        self.przyspieszenie.y = 0

    def obrotLewo(self): # skręć w lewo
        self.orientacja -= 0.18
        if self.orientacja < 0:
            self.orientacja += TWO_PI
    
    def obrotPrawo(self): # skręć w prawo
        self.orientacja += 0.18
        if self.orientacja >= TWO_PI:
            self.orientacja -= TWO_PI

            
 class Score():  #przy pomocy tej klasy można utworzyć instancje wyświetlającą na ekranie wynik
    def __init__(self):
        self.points = 0
        self.highestScore = -1
        
    def increase(self):
        self.points += 1
        
    def reset(self):
        self.points = 0
    
    def setHighest(self):
        if self.points > self.highestScore:
            self.highestScore = self.points
            

        
#class Blocker(sprite.Sprite):
 #   def __init__(self, size, color, row, column):
  #      sprite.Sprite.__init__(self)
   #     self.h = size
    #    self.= size
     #   self.color = color
      #  self.image = Powierzchnia((self.w, self.h)) #trzeba tylko dodać obrazek tych blokerów
       # self.image.fill(self.color)
        #self.rect = self.image.get_rect()
        #self.row = row
        #self.column = column

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
        
        
def wprowadzImie():
    tlo2 = loadImage("bg_robocze2_TWH.png")
    background(tlo2)
    textSize(32)
    fill(255)
    text('Gora/dol - poruszanie do przodu/do tylu', - w / 4 + 420, -70)
    text('Lewo/prawo - obrot', - w / 4 + 420, -30)
    text('Spacja - strzal', - w / 4 + 420, 10)
    text('Your Name Commander: ' + imie, - w / 4 + 420, 190)
    powitanie = Powitanie()
    start = Start()
    powitanie.wyswietl()
    start.pokaz() 
        
def koniecGry():
    background(127)
    
def keyReleased():
    global imie
    global statusGry    
    if statusGry == 2:
        graj()
    if statusGry == 3:
        koniecGry()
        
statek = Statek()
pociski = []
kamienie = []    
        
def graj(): #na razie puki nie ma gry
    global statusGry
    background(0)
    
    statek.animuj()
    statek.rysuj()      
        
    for pocisk in pociski:
        pocisk.animuj()
        pocisk.rysuj()
 
    if len(pociski) != 0 and pociski[0].czyJestMartwy(): # wystarczy sprawdzić tylko pierwszy pocisk - następne nie mogą być jeszcze martwe
        pociski.pop(0)
            
def keyTyped():
    global imie
    global statusGry
    if statusGry == 1:        
        if key == ENTER:
            statusGry = 2   
        if key == ESC:
            statusGry = 3
        if key == BACKSPACE:
            if len(imie) != 0:
                imie = imie[:-1] # usuń ostatni znak
                
        else:
            imie = imie + key          
    
def setup():
    size(w, h)
    frameRate(30)
    imageMode(CENTER)
    textAlign(CENTER)
    rectMode(CENTER)
    #myFont = createFont("Book Antiqua", 15)
    #textFont(myFont)
    pass
    global tlo
    tlo = loadImage
    print(type(log))

    
    #dzwiek

    intro = SoundFile(this, "Elite Dangerous intro.mp3")
    intro.play()
    komputer_pokladowy = SoundFile(this, "gretting-commanders.mp3")
    komputer_pokladowy.play()
    
    
def draw():
    translate(630, 300) # przsuń środek układu współrzędnych na środek okna
    if statusGry == 1: # wprowadź imię
        wprowadzImie()
    elif statusGry == 2: # graj
        graj()
    elif statusGry == 3: #wyświetl ekran końcowy
        koniecGry()
    
    # może ktoś się odważy wprowadzić ruch gracza/przeciwników/strzał?
    # trzeba rozróżnić sytuacje: menu od gry na jakąś zmienną logiczną
