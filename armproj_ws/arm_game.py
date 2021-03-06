#!/usr/bin/env python

import pygame
import numpy as np
import random
import time
import socket
import json

# path='/home/jingyan/Documents/spring_proj/armproj_ws/img/'
path='C:\\Users\\pthms\\Desktop\\ling\\children_ability_assessment_sys\\armproj_ws\\img\\'
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

class gamer(object):
    def __init__(self):

        pygame.init()
        pygame.mixer.music.load(path+'music.mp3')
        pygame.mixer.music.play(-1)
        self.screenwidth=1290
        self.screenheight=768
        self.win=pygame.display.set_mode((self.screenwidth,self.screenheight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Arm Assessment Game")
        #initilize elements:
        self.progressbar_init()
        self.rain_init()
        self.showpic_init()
        self.dirt_init()
        self.rainbow_init()
        self.house_init()
        self.hint_init()
        self.buttons_init()
        ######################

        self.indi_mode_flag=False
        # while True:
        #     self.game_logic()
        
###ELEMENT INITILIZATION############

    def progressbar_init(self):
        self.progress=progressbar_generator(self.screenwidth-40,self.screenheight,40,0,(65, 220, 244))
    def rain_init(self):
        self.rain=rain_drop_generator(0,0)
        self.rain_flag=False
        self.rain_counter=0
    def showpic_init(self):
        # alpha=225
        self.bgpic=showpic_generator()
        self.picswitch_flag=False
        self.pic_counter=0
        self.pic_amount=2
        self.picrot=0
        self.picscale=1
    def hint_init(self):
        self.hint_flag=False
        font=pygame.font.SysFont("comicsansms",75)
        self.hint=font.render("Chanllenge! Can You Copy Yourself ?", True, (43, 9, 183))
    def dirt_init(self):
        self.dirt=dirt_generator()
        self.clean_flag=False
        self.fade_flag=False
        self.fade_counter=0
        self.dirt_amount=25
        self.dirt_x=[]
        self.dirt_y=[]
        self.dirt_flag=True
        for i in range(self.dirt_amount):
            self.dirt_x.append(random.randint(10,self.bgpic.picw-self.dirt.width))
            self.dirt_y.append(random.randint(70,self.bgpic.pich-self.dirt.height))
            i+=1
    def rainbow_init(self):
        self.rainbow=rainbow_generator()
        self.rainbow_movecount=0
        self.rainbow_vel=2
        self.text_flag=False
        font=pygame.font.SysFont("comicsansms",30)
        self.text=font.render("You Earn The Picture!", True, (255, 250, 117))
    def house_init(self):
        self.house=house_generator()
        self.plus1_flag=False

    def buttons_init(self):
        self.reference_b=False
        self.indicative_b=False
        self.finish_b=False
        self.copied_b=False
        self.start_reference=False
########################################

    def game_logic(self,signal=None,threshold=None,ref_inx=None):
#in while loop (callback)
        self.record_flag=False
        self.record_tag=None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        
        keys=pygame.key.get_pressed()


        if not self.indi_mode_flag:
            ####PROGRESS BAR
            if self.reference_b:
                self.reference_b=False
                self.start_reference=True

            if self.start_reference:
                self.record_flag=True
                self.record_tag='reference'
                if signal[ref_inx]>threshold and self.progress.height>=-self.screenheight:
                # if keys[pygame.K_UP] and self.progress.height>=-self.screenheight:
                    self.progress.height-= self.progress.vel*2
                elif self.progress.height<0:
                    self.progress.height+=self.progress.vel*2
                

                ###RAIN DROP####
            if self.progress.height<=(-self.screenheight+10):
  
                self.rain_flag=True
                self.rain_counter+=1
                if self.rain_counter==1:
                    self.rain.effect.play()                
                if self.rain_counter>9:
                    self.rain_counter=0
                    self.fade_flag=True
                
            else:
                try:
                    self.rain.effect.stop()
                except: pass

                self.rain_flag=False
                self.rain_counter=0
                self.fade_flag=False
        else:
            if self.indicative_b:
                self.indicative_b=False
                self.hint_flag=False
            if not self.hint_flag:
                if not self.fade_flag:
                    self.record_flag=True
                    self.record_tag='indicative'
                    
                if self.copied_b:
                    self.fade_flag=True
                    self.copied_b=False
                
        ###FADE DIRT#####
        if self.fade_flag and not self.clean_flag:
            self.fade_counter+=5
            if self.fade_counter>210:
                self.fade_flag=False
                self.clean_flag=True
                self.dirt_flag=False
                self.fade_counter=0

        ###RAINBOW###       
        if self.clean_flag:
            self.record_flag=False
            self.record_tag=None
            self.progress.height=0
            self.rainbow_movecount+=self.rainbow_vel
            if self.rainbow_movecount>80:
                self.text_flag=True
            if self.rainbow_movecount >=150:
                self.rainbow_movecount=0
                self.clean_flag=False
                self.text_flag=False
                self.picswitch_flag=True
                time.sleep(1.0)

        ##SWITCH PIC
        if self.picswitch_flag:
            self.record_flag=False
            self.record_tag=None
            self.picrot-=1
            self.picscale-=0.05
            if self.picscale<=0.3:
                self.plus1_flag=True
            if self.picscale<=0:
                self.picrot=0
                self.picscale=1
                self.pic_counter+=1
                self.picswitch_flag=False
                self.dirt_init()
                self.plus1_flag=False
                time.sleep(1.0)
                self.indi_mode_flag= not self.indi_mode_flag
                self.start_reference= False
                if self.indi_mode_flag:
                    self.hint_flag=True
                if self.pic_counter>self.pic_amount-1:
                    self.pic_counter=0
            self.temp_picshow=pygame.transform.rotozoom(self.bgpic.showpic[self.pic_counter],self.picrot,self.picscale)
            self.temp_frame=pygame.transform.rotozoom(self.bgpic.frame,self.picrot,self.picscale)

            # self.send_flag(record_flag)
        self.draw()  
        if self.finish_b:
            pygame.quit()
        return self.record_flag,self.record_tag
        # pygame.quit()
    
    def draw(self):
        ##BG PIC
        if self.picswitch_flag:
            showpic=self.temp_picshow
            frame=self.temp_frame
        else:
            showpic=self.bgpic.showpic[self.pic_counter]
            frame=self.bgpic.frame
        self.win.blit(self.bgpic.bg,(0,0))
        
        if not self.hint_flag:
            
            if not self.indi_mode_flag:
                if not self.start_reference:
                    self.reference_b=self.repull_b=button(self.win,'Continue',self.screenwidth//2-260,self.screenheight//2+250,120,70,red,bright_red)
                    self.finish_b=button(self.win,'Finish',self.screenwidth//2+120,self.screenheight//2+250,120,70,green,bright_green)
            else:
                self.copied_b=button(self.win,'Copied',self.screenwidth-200,self.screenheight//2,120,70,green,bright_green)
            
            if self.start_reference or self.indi_mode_flag:
                self.win.blit(showpic,(20,70))
                self.win.blit(frame,(0,60))
            
            ##HOUSE
            self.win.blit(self.house.house,(self.house.x,self.house.y))
            if self.plus1_flag:
                self.win.blit(self.house.plus1,(self.house.x+115,self.house.y))
            
            ##DIRT
            if self.start_reference or self.indi_mode_flag:
                if self.dirt_flag:
                    for i in range(self.dirt_amount):
                        self.blit_alpha(self.dirt.dirt_img,(self.dirt_x[i],self.dirt_y[i]),225-self.fade_counter)
            
            ##PROGRESS
            if not self.clean_flag:
                pygame.draw.rect(self.win,self.progress.color, (self.progress.x,self.progress.y,self.progress.width,self.progress.height))
            elif self.clean_flag:
                pygame.draw.rect(self.win,self.progress.color, (self.progress.x,self.progress.y,self.progress.width,self.screenheight))

            ##RAIN DROP

            if self.rain_flag and not self.clean_flag:     
                self.win.blit(self.rain.rain_img[int(self.rain_counter//6)],(self.rain.x,self.rain.y))
                
            ##RAINBOW
            if self.clean_flag:
                if self.rainbow_movecount==self.rainbow_vel:
                    self.rainbow.effect.play()
                self.win.blit(self.rainbow.rainbow,(self.rainbow.x+self.rainbow_movecount,self.rainbow.y))
                self.win.blit(self.rainbow.rainbow,(self.rainbow.x-self.rainbow_movecount,self.rainbow.y))
            if self.text_flag:
                self.win.blit(self.text,(self.rainbow.x-15,self.rainbow.y+50))
        else:
            self.win.blit(self.hint,(self.screenwidth//2-self.hint.get_width()//2,self.screenheight//2-self.hint.get_height()//2))
            self.indicative_b=button(self.win,'I Am Ready',self.screenwidth//2-60,self.screenheight//2+200,120,70,green,bright_green)

        pygame.display.update()

        
    def blit_alpha(self, source, location, opacity):
        target=self.win
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

class progressbar_generator(object):
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.color=color
class rain_drop_generator(object):
    def __init__(self,x,y):
        global path
        self.rain_img=[pygame.image.load(path+'raindrops.png'),pygame.image.load(path+'raindrops2.png')]
        self.x=x
        self.y=y
        self.effect=pygame.mixer.Sound(path+'bubbles_sfx.wav')

class showpic_generator(object):
    def __init__(self):
        
        global path
        self.framew=1050
        self.frameh=600
        self.picw=self.framew-30
        self.pich=self.frameh-10
        self.showpic=[pygame.image.load(path+'bg_test.png'),pygame.image.load(path+'bg_test2.jpg')]
        for i in range(len(self.showpic)):
            self.showpic[i]=pygame.transform.scale(self.showpic[i],(self.picw,self.pich))
        self.frame=pygame.image.load(path+'photo_frame.png')
        self.frame=pygame.transform.scale(self.frame,(self.framew,self.frameh))
        self.bg=pygame.image.load(path+'bg2.jpg')
        self.bg=pygame.transform.scale(self.bg,(1290,768))
        
class dirt_generator(object):
    def __init__(self):
        global path
        self.width=150
        self.height=150
        self.dirt_img=pygame.image.load(path+'dirt.png')
        self.dirt_img=pygame.transform.scale(self.dirt_img,(self.width,self.height))
        # self.dirt_img.set_alpha(10)
        
class rainbow_generator(object):
    def __init__(self):
        global path
        self.width=180
        self.height=90
        self.x=480
        self.y=550
        self.rainbow=pygame.image.load(path+'rainbow.png')
        self.rainbow=pygame.transform.scale(self.rainbow,(self.width,self.height))
        self.effect=pygame.mixer.Sound(path+'applause2_x.wav')
class house_generator(object):
    def __init__(self):
        global path
        self.width=200
        self.height=100
        self.x=-18
        self.y=10
        self.house=pygame.image.load(path+'house.png')
        self.house=pygame.transform.scale(self.house,(self.width,self.height))
        self.plus1=pygame.image.load(path+'plus1.png')
        self.plus1=pygame.transform.scale(self.plus1,(75,75))
def button(gameDisplay,msg,x,y,w,h,ic,ac,tc=(0,0,0),action=None):
    """
    gameDisplay: pygame window
    msg: text on the button
    x,y: position
    w,h: width and height
    ic, ac: color of the button when not activated and activiated
    tc: text color, default: black
    action: function of this button
    return: boolean, if this button is clicked
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    check = False

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
    
        if click[0] == 1:
            check=True  
            if action != None:
                action() 
                  

    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",23)
    textSurf = smallText.render(msg, True, tc)
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    return check

def main():
    gamer()    
            
if __name__ == '__main__':
	main()