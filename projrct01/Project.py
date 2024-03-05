from dataclasses import dataclass
import pygame
import sys
pygame.init()

clock = pygame.time.Clock()
FPS = 120

#กำหนดขนาดหน้าจอ
screen_menu = 400
screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Parallax_RPG")

scroll = 1

#เพิ่มพื้นหลัง
bg_list = ["Background","Tree","Floor","Light"]
bg_images = []
for i in range(0,4):
    for x in range(1,5):
        bg_image = pygame.image.load(f"Background_layers/{bg_list[i]}/{bg_list[i]}{x}.png").convert_alpha()
        bg_image = pygame.transform.scale(bg_image,(screen_width,(screen_height - screen_menu)))
        bg_images.append(bg_image)

bg_start = pygame.image.load(f"Background_layers/Background/Background6.png").convert_alpha()
bg_starts = pygame.transform.scale(bg_start,(screen_width,screen_height ))
panel_image = pygame.image.load(f"Panel_layer/panel_Example1.png").convert_alpha()
panel_images = pygame.transform.scale(panel_image,(screen_width,(screen_height - screen_menu))) 

class Button:
    def __init__(self, color, x, y, width, height,image ="", text=''):
        self.color = color
        self.x = x
        self.y = y
        self.image = image
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.Font("Font/dpcomic.ttf", 25)

    def draw_Button(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.image:
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
            image_rect = self.image.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            screen.blit(self.image, image_rect)

        if self.text != '':
            text = self.font.render(self.text, 1, WHITE)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
bg_width = bg_images[0].get_width()

def draw_images():
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i,((x * bg_width) - scroll * speed,0))
            speed += 0.2

def deaw_panel():
    screen.blit(panel_images,(0,550))

def deaw_bg_start():
    screen.blit(bg_starts,(0,0))

#Soud efffect
pygame.mixer.music.load('soud/music/Pixel 7.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
sound_slash1 = pygame.mixer.Sound("soud/slash/mixkit-impact-of-a-strong-punch-2155.mp3")
sound_slash2 = pygame.mixer.Sound("soud/slash/mixkit-quick-saber-cut-2158.mp3")
sound_slash3 = pygame.mixer.Sound("soud/slash/slash-21834.mp3")
sound_slash4 = pygame.mixer.Sound("soud/slash/sword-slash-and-swing-185432.mp3")
sound_slash5 = pygame.mixer.Sound("soud/slash/sword-slash-with-metallic-impact-185435.mp3")
sound_slash6 = pygame.mixer.Sound("soud/slash/sword-sound-2-36274.mp3")
sound_explosion = pygame.mixer.Sound("soud/explosion/medium-explosion-40472.mp3")
sound_magic1 = pygame.mixer.Sound("soud/spell/magic-smite-6012.mp3")
sound_magic2 = pygame.mixer.Sound("soud/spell/magic-spell-6005.mp3")
sound_magic3 = pygame.mixer.Sound("soud/spell/magic-strike-5856.mp3")
sound_charater1 = pygame.mixer.Sound("soud/Charater/mixkit-female-exclamation-of-pain-2206.wav")
sound_charater2 = pygame.mixer.Sound("soud/Charater/giant-breath-1-184041.mp3")
sound_start = pygame.mixer.Sound("soud/Charater/game-start-6104.mp3")
sound_slide2 = pygame.mixer.Sound("soud/dash/whoosh-transitions-sfx-03-118230.mp3")
sound_hurt1 = pygame.mixer.Sound("soud/hurt/086126_hurt-3-82783.mp3")
sound_hurt2 = pygame.mixer.Sound("soud/hurt/robotic-male-grunting-in-pain-99420.mp3")
sound_Ui = pygame.mixer.Sound("soud/ui/button-pressed-38129.mp3")
sound_game_over = pygame.mixer.Sound("soud/ui/mixkit-retro-arcade-game-over-470.wav")
sound_hurt2.set_volume(0.6)

#ตัวละคร
@dataclass
class Charater:
    name: str = ""
    hp: int = 100
    hp_max: int = 100
    mp: int = 50
    mp_max: int = 50
    ap: int = 0
    atk: int = 10
    action: str = "Idle"
    deltatime: int = 0
    frame: int = 1
    fps: int =10
    step: int = 5
    x: int = 0
    y: int = 0
    scale_x: int = 0
    scale_y: int = 0
    spell_step: int = 15
    spell_frame: int = 0
    Effect_step: int = 14
    Effect_frame: int = 0
    turn: bool = True

    def blit(self, screen,deltatime = 0):
        self.deltatime += deltatime
        if self.deltatime >= 1000/self.fps:
            self.deltatime -= 1000/self.fps
            self.frame = (self.frame+1)%(self.step + 1)
        Charater_images = pygame.image.load(f"Charater_player/{self.name}/{self.action}/{self.name}_{self.action}_{self.frame}.png").convert_alpha()
        Charater_images = pygame.transform.scale(Charater_images,(self.scale_x,self.scale_y))
        screen.blit(Charater_images,(self.x,self.y))

    def Animation_reset(self):

        #Action Player
        if self.name == "Warrior" and (self.action == "Attack" or self.action == "Dash-Attack" or self.action == "Dash" or self.action == "Crouch" or self.action == "Slide" or self.action == "Dash_Ulti" or self.action == "Ultimate"):
            if self.name == "Warrior" and self.action == "Slide" and self.frame >=4 :           
                Monter.hp -= Player.atk
                if Player.mp < 50 :
                    Player.mp += 10
                self.action = "Attack"
                self.step = 11
                self.frame = 0 
            if self.name == "Warrior" and self.action == "Crouch" and self.frame >= 5:
                self.action = "Idle"
                self.step = 5
                self.frame = 0
                Monter.turn = True
            if self.name == "Warrior" and self.action == "Attack" and self.frame >= 11:
                self.action = "Idle"
                self.step = 5
                self.frame = 0
            if self.name == "Warrior" and self.action == "Dash-Attack" and self.frame >= 9:
                self.action = "Idle"
                self.step = 5
                self.frame = 0
            if self.name == "Warrior" and self.action == "Dash" and self.frame >= 6:
                self.action = "Dash-Attack"
                self.step = 9
                self.frame = 0
                Player.atk = 15
                Monter.hp -= Player.atk
                Player.atk = 10
                Player.mp -= 20
            if self.name == "Warrior" and self.action == "Dash_Ulti" and self.frame >= 6:
                self.action = "Ultimate"
                self.step = 21
                self.frame = 0
            if self.action == "Ultimate" and self.frame == 1:
                Player.atk = 10
                Monter.hp -= Player.atk
                Player.atk = 10
                
            if self.name == "Warrior" and self.action == "Ultimate" and self.frame == 18:
                Monter.hp -= 5
        
        #Action Monters
        if self.name == "Bringer-of-Death" and (self.action == "Attack" or self.action == "Walk" or self.action == "Attack_No_Effect" or self.action == "Walk_No_Effect" or self.action == "Cast" or self.action == "Idle"):
            if self.name == "Bringer-of-Death" and self.action == "Walk_No_Effect" and self.frame >= 3:
                Player.hp -= Monter.atk
                if Monter.mp < 50 :
                    Monter.mp += 10
                self.action = "Attack_No_Effect"
                self.step = 8
                self.frame = 0
            if self.name == "Bringer-of-Death" and self.action == "Attack_No_Effect" and self.frame >= 8:
                self.action = "Idle"
                self.step = 7
                self.frame = 0
                Player.turn = True
            if self.name == "Bringer-of-Death" and self.action == "Walk" and self.frame >= 3:
                self.action = "Attack"
                self.step = 10
                self.frame = 0
                Monter.atk = 10
                Player.hp -= Monter.atk   
                Monter.atk = 5
                Monter.mp -= 20             
            if self.name == "Bringer-of-Death" and self.action == "Attack" and self.frame >= 9:
                self.action = "Idle"
                self.step = 7
                self.frame = 0
                Player.turn = True
            if self.name == "Bringer-of-Death" and self.action == "Cast" and self.frame >= 8:
                self.action = "Idle"
                self.step = 7
                self.frame = 0
            if Spell.action == "Idle" and Spell.spell_frame == 10:
                Player.action = "Hurt"
                Player.step = 3
                Player.frame = 0
                Monter.atk = 20
                Player.hp -= Monter.atk
                Monter.atk = 5
                Player.turn = True
            

    def blit_spell(self, screen,deltatime = 0):
        global sound_playing1
        if Cast == True:
            self.deltatime += deltatime
            if self.deltatime >= 1000/self.fps:
                    self.deltatime -= 1000/self.fps
                    self.spell_frame = (self.spell_frame+1)%(self.spell_step + 1)
            Spell_image = pygame.image.load(f"Charater_player/Bringer-of-Death/Spell/Bringer-of-Death_Spell_{self.spell_frame}.png").convert_alpha()
            Spell_image = pygame.transform.scale(Spell_image,(Spell.scale_x,Spell.scale_y))
            screen.blit(Spell_image,(Spell.x,Spell.y))
            if self.spell_frame == 1 and sound_playing1:
                sound_magic3.play()
                sound_playing1 = False

    def blit_Effect(self, screen,deltatime = 0):
        global sound_playing1
        if Smoke == True:
            self.deltatime += deltatime
            if self.deltatime >= 1000/self.fps:
                    self.deltatime -= 1000/self.fps
                    self.Effect_frame = (self.Effect_frame+1)%(self.Effect_step + 1)
            Effect_image = pygame.image.load(f"Charater_player/Effect/Smoke/Effect_Smoke_{self.Effect_frame}.png").convert_alpha()
            Effect_image = pygame.transform.scale(Effect_image,(Effect.scale_x,Effect.scale_y))
            Effect_image.set_colorkey(BACKGROUND_COLOR1)
            screen.blit(Effect_image,(Effect.x,Effect.y))
            if self.Effect_frame == 1 and sound_playing1:
                sound_explosion.play()
                sound_playing1 = False

    def Check_hp(self):
        if Player.action == "Idle" and ((Monter.action == "Attack" and Monter.frame == 4) or (Monter.action == "Attack_No_Effect" and Monter.frame == 4)) :
            Player.action = "Hurt"
            Player.step = 3
            Player.frame = 0

        if Monter.action == "Idle" and ((Player.action == "Attack" and Player.frame <= 5 <= 10) or (Player.action == "Dash-Attack" and Player.frame == 3) or (Player.action == "Ultimate" and Player.frame <=5 <= 20)) :
            Monter.action = "Hurt"
            Monter.step = 2
            Monter.frame = 0
        
        if Player.action == "Hurt" and Player.frame == 3:
                Player.action = "Idle"
                Player.step = 5
                Player.frame = 0

        if Monter.action == "Hurt" and Monter.frame == 2:
                Monter.action = "Idle"
                Monter.step = 7
                Monter.frame = 0

    def limit_hp_mp_ap(self):
        if self.hp < 0:
            self.hp = 0
        if self.mp < 0:
            self.mp = 0
        if self.ap < 0:
            self.mp = 0
        if self.mp > self.mp_max:
            self.mp = self.mp_max
        if self.ap > 6:
            self.ap = 6
    
def set_sound():
    global sound_playing
    global sound_playing1
    if Player.action == "Attack" and Player.frame <= 3 and not sound_playing :
        sound_slash6.play()
        sound_playing = True
    if Player.action == "Attack" and Player.frame <= 9 and not sound_playing :
        sound_slash6.play()
        sound_playing = True
    if Player.action == "Dash-Attack" and Player.frame <= 3 and not sound_playing :
        sound_slash1.play()
        sound_playing = True
    if Player.action == "Ultimate" and Player.frame <= 3 and not sound_playing :
        sound_slash6.play()
        sound_playing = True
    if Player.action == "Ultimate" and Player.frame <= 9 and not sound_playing :
        sound_slash6.play()
        sound_playing = True
    if Player.action == "Ultimate" and Player.frame <= 12 and not sound_playing :
        sound_slash1.play()
        sound_playing = True
    if Player.action == "Hurt" and Player.frame <= 1 and not sound_playing :
        sound_hurt1.play()
        sound_playing = True
    if (Player.action == "Dash" or Player.action == "Dash_Ulti" or Player.action == "Slide") and Player.frame <= 1 and not sound_playing :
        sound_slide2.play()
        sound_playing = True
    
    if Monter.action == "Hurt" and Monter.frame <= 1 and not sound_playing1 :
        sound_hurt2.play()
        sound_playing1 = True
    if Monter.action == "Attack" and Monter.frame <= 2 and not sound_playing1 :
        sound_slash4.play()
        sound_playing1 = True
    if Monter.action == "Attack_No_Effect" and Monter.frame <= 1 and not sound_playing1 :
        sound_slash2.play()
        sound_playing1 = True
    if Monter.action == "Cast" and Monter.frame <= 1 and not sound_playing1 :
        sound_magic1.play()
        sound_playing1 = True
    if Effect.Effect_frame == 2 and not sound_playing1 :
        sound_explosion.play()
        sound_playing1 = True

def Death_Animation():
    global end_game1
    global end_game2
    global GAME_OVER
    if Player.hp <= 0 and Player.action != "Death":
        sound_charater1.play()
        Player.action = "Death"
        Player.step = 10
        Player.frame = 0
    if Player.action == "Death" and Player.frame >= 9:
        end_game1 = True
        GAME_OVER = True
    if Monter.hp <= 0 and Monter.action != "Death":
        sound_charater2.play()
        Monter.hp = 0
        Monter.action = "Death"
        Monter.step = 9
        Monter.frame = 0
    if Monter.action == "Death" and Monter.frame >= 9:
        end_game2 = True
        GAME_OVER = True
    

BACKGROUND_COLOR1 = (42,37,27)
Smoke = False
Cast = False
Slash = False

#coler
black = (0,0,0)
WHITE = (255, 255, 255)

#ตัวละคร
Player = Charater("Warrior",150,150,50,50,0,atk = 10,step = 5,x = 500, y = 420,scale_x = 220,scale_y = 220)
Monter = Charater("Bringer-of-Death",200,200,20,20,0,atk = 5,step = 7,x = 1000,y = 320, scale_x = 320,scale_y = 320,turn = False)

#Spell
Spell = Charater(x = 410,y = 220, scale_x = 400,scale_y = 400)

#Effect
Effect = Charater(x = 370,y = 220, scale_x = 500,scale_y = 500)
Effect_slash = Charater(x = 1100,y = 450, scale_x = 200,scale_y = 250,Effect_step = 250,fps=10)


#ปุ่ม
Button1_image = pygame.image.load("Button_images/Button1.png").convert_alpha()
Button2_image = pygame.image.load("Button_images/Button2.png").convert_alpha()
Button3_image = pygame.image.load("Button_images/Play.png").convert_alpha()
Button3_image_rect = Button3_image.get_rect(center=(screen_width // 2, screen_height // 2))
GAME_OVER_TEXT = pygame.image.load("Button_images/GAMEOVER.png").convert_alpha()
GAME_OVER_TEXT = pygame.transform.scale(GAME_OVER_TEXT,(500,500))
Quit_image = pygame.image.load("Button_images/Power.png").convert_alpha()
Quit_image = pygame.transform.scale(Quit_image,(100,100))
Quit_image_rect = Quit_image.get_rect(center=(screen_width // 2, screen_height // 2))

button1 = Button(black, 220, 720, 150, 75,Button1_image, 'Normal Attck')
button2 = Button(black, 220, 720 + 80, 150, 75,Button1_image, 'Skill')
button3 = Button(black, 220, 720 + 160, 150, 75,Button1_image, 'Ultimage')

font = pygame.font.Font('Font/dpcomic.ttf', size=50)
font_start = pygame.font.Font('Font/dpcomic.ttf', size=100)

# เวลาที่เริ่มต้น
start_time = pygame.time.get_ticks()

WattingMP = False
WattingAP = False

#game loop
run = True
start = True
turn_ = 1
end_game1 = False
end_game2 = False
GAME_OVER = False
RETURN_GAME = False

sound_playing = False 
sound_playing1 = False
sound_gameover = True
while run:

    #ตัวจับเวลา นับเวลา
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000 
    
    #draw Background
    draw_images()

    #draw panel
    deaw_panel()

    set_sound()
    
    #เตือนMPไม่พอ
    Mp_not_enough = font.render("Need MP 20", True, (BACKGROUND_COLOR1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if Button3_image_rect.collidepoint(event.pos):
                sound_Ui.play()
                start = False
            if GAME_OVER == False :
                if Player.turn == True:
                    if button1.is_over(pygame.mouse.get_pos()):
                        Player.action = "Slide"
                        Player.step = 4
                        Player.frame = 0
                        Player.ap += 1
                        Player.turn = False
                        WattingMP = False
                        WattingAP = False
                    if button2.is_over(pygame.mouse.get_pos()):
                        if Player.mp >= 20:
                            Player.action = "Dash"
                            Player.step = 6
                            Player.frame = 0
                            Player.ap += 2
                            Player.turn = False
                            WattingAP = False
                        else:
                            WattingMP = True
                            WattingAP = False
                    if button3.is_over(pygame.mouse.get_pos()):
                        if Player.ap >= 6:
                            Player.action = "Dash_Ulti"
                            Player.step = 6
                            Player.frame = 0
                            Player.ap = 0
                            Player.turn = False
                        else:
                            WattingAP = True
                            WattingMP = False
                turn_ += 1
            
    #AI monter
                        
    if Monter.turn == True :
        if Monter.ap == 6:
            if Monter.ap >= 6:
                Monter.action = "Cast"
                Monter.step = 8
                Monter.frame = 0
                Monter.ap = 0
                Monter.turn = False
        elif Monter.mp <=10:
            Monter.action = "Walk_No_Effect"
            Monter.step = 7
            Monter.frame = 0
            Monter.ap += 1
            Monter.turn = False
        elif Monter.mp >= 20:
            if Monter.mp >= 20:
                Monter.action = "Walk"
                Monter.step = 7
                Monter.frame = 0
                Monter.ap += 1
                Monter.turn = False
        turn_  += 1
    

    #คำเตื่อนต้องการ MP
    Watting_MP = font.render("Requires 20 MP to use the skill.", True, (WHITE))
    Watting_AP = font.render("Requires 6 AP to use the skill.", True, (WHITE))
    if WattingMP == True:
        screen.blit(Watting_MP,(800,300))
    if WattingAP == True:
        screen.blit(Watting_AP,(800,300))

    #action player
    if Player.action == "Dash-Attack" and Player.frame >= 8 and  Player.x != 500:
        for i in range(2):
                if Player.x >= 800:
                    Player.y -=20
                if Player.x <= 800:
                    Player.y +=20
                    scroll -= 2

    if Player.action == "Attack" and Player.frame >= 10 and  Player.x != 500:
        for i in range(2):
                if Player.x >= 800:
                    Player.y -=20
                if Player.x <= 800:
                    Player.y +=20
                    scroll -= 2
    
    if Player.action == "Ultimate" and Player.frame >= 20 and  Player.x != 500:
        for i in range(2):
                if Player.x >= 800:
                    Player.y -=20
                if Player.x <= 800:
                    Player.y +=20
                    scroll -= 2

    if (Player.action == "Dash" or Player.action == "Slide" or Player.action == "Dash_Ulti") and Player.x <= 1000 :
        Player.x +=50
        scroll += 2

    if Player.action == "Dash-Attack" and Player.frame >= 8 and  Player.x != 500:
        for i in range(3):
            if Player.x != 500:
                Player.x -=30
                scroll -= 2
    
    if Player.action == "Attack" and Player.frame >= 10 and  Player.x != 500:
        for i in range(3):
            if Player.x != 500:
                Player.x -=32
                scroll -= 2
    
    if Player.action == "Ultimate" and Player.frame >= 20 and  Player.x != 500:
        for i in range(3):
            if Player.x != 500:
                Player.x -=32
                scroll -= 2
    
    #action monster
    if Monter.action == "Dash-Attack"and Monter.frame >= 8 and  Monter.x != 500:
        for i in range(2):
                if Monter.x >= 800:
                    Monter.y -=20
                if Monter.x <= 800:
                    Monter.y +=20
                    scroll -= 2

    if Monter.action == "Attack"and Monter.frame >= 10 and  Monter.x != 500:
        for i in range(2):
                if Monter.x >= 800:
                    Monter.y -=20
                if Monter.x <= 800:
                    Monter.y +=20
                    scroll -= 2

    if (Monter.action == "Walk" or Monter.action == "Walk_No_Effect")  and Monter.x >= 550 :
        Monter.x -=50
        scroll -= 2

    if Monter.action == "Attack" and Monter.frame >= 8 and  Monter.x != 1000:
        for i in range(3):
            if Monter.x != 1000:
                Monter.x +=30
                scroll += 2
        
    if Monter.action == "Attack_No_Effect" and Monter.frame >= 7 and  Monter.x != 1000:
        for i in range(3):
            if Monter.x != 1000:
                Monter.x +=30
                scroll += 2
    
    if Monter.action == "Attack" and Monter.frame >= 10 and  Monter.x != 500:
        for i in range(3):
            if Monter.x != 500:
                Monter.x -=32
                scroll -= 2
                
    #Spell Start => End
    if Monter.action == "Cast" and Monter.frame == 8:
        Cast = True
    if Spell.spell_frame == 15:
        Cast = False
        Spell.spell_frame = 0

    #Effect Start => End
    if Spell.spell_frame == 7:
        Smoke = True
    if Effect.Effect_frame == 14:
        Smoke = False
        Effect.Effect_frame = 0

    if Player.action == "Ultimate":
        Slash = True
    if Effect_slash.Effect_frame == 22:
        Slash = False
        Effect_slash.Effect_frame = 0
    
    #reset position player
    if Player.y == 380 and Player.x <= 600 :
        Player.y = 420
        Player.x = 500
        if Player.x == 500 and Player.y == 420:
            Player.action = "Crouch"
            Player.step = 5
            Player.frame = 0

    #reset position monster
    if  (Monter.action == "Attack_No_Effect" or Monter.action == "Attack") and Monter.x >= 900  :
        Monter.y = 320
        Monter.x = 1000

    

    #ทำให้ไม่ออกนอกฉากหลัง
    if scroll < -5 :
        scroll = -5

    #เช็ตว่าhpลดไหม
    Player.Check_hp()
    Monter.Check_hp()
    
    Death_Animation()

    Player.limit_hp_mp_ap()
    Monter.limit_hp_mp_ap()
        

    #print("Monter.x ",Monter.x)
    #print("Monter.y ",Monter.y)

    #update action charater
    Player.Animation_reset()
    Monter.Animation_reset()

    #Hurt animation
    #FPS
    t = clock.tick(120)
    text = f'{clock.get_fps():.2f} FPS'
    msg = font.render(text, True, (WHITE))

    #ข้อมูลตัวละคร
    Hp_Player = font.render(f"HP: {Player.hp}/{Player.hp_max}", True, (BACKGROUND_COLOR1))
    MP_Player = font.render(f"MP: {Player.mp}/{Player.mp_max}", True, (BACKGROUND_COLOR1))
    Ulti_Player = font.render(f"AP: {Player.ap}/6", True, (BACKGROUND_COLOR1))

    Hp_Monter = font.render(f"HP: {Monter.hp}/{Monter.hp_max}", True, (BACKGROUND_COLOR1))
    MP_Monter = font.render(f"MP: {Monter.mp}/{Monter.mp_max}", True, (BACKGROUND_COLOR1))
    Ulti_Monter = font.render(f"AP: {Monter.ap}/6", True, (BACKGROUND_COLOR1))

    #นับเวลาไปเรื่อยๆ
    #text2 = font.render(f"Elapsed Time: {elapsed_time / 1000:.2f} seconds", True, WHITE)
    
    clock.tick(80)

    Name_Game1 = font_start.render(f"Parallax_RPG", True, (black))
    Name_Game2 = font_start.render(f"Parallax_RPG", True, (WHITE))

    #หน้าเริ่มเกม
    if start == True:
        deaw_bg_start()
        screen.blit(Name_Game1, (700, 300))
        screen.blit(Name_Game2, (710, 300))

        screen.blit(Button3_image,(900,500))

    if start == False :
        #แสดงข้อมูลตัวละคร Player
        screen.blit(Hp_Player, (500, 730))
        screen.blit(MP_Player, (500, 790))
        screen.blit(Ulti_Player, (500, 850))

        #แสดงข้อมูลตัวละคร Ulti_Monter
        screen.blit(Hp_Monter, (1200, 730))
        screen.blit(MP_Monter, (1200, 790))
        screen.blit(Ulti_Monter, (1200, 850))
        #Turn
        Turn_Numder = font.render(f"TURN: {turn_}", True, (WHITE))
        elapsed = font.render(f"time: {elapsed_time}", True, (WHITE))

        #แสดงปุ่ม
        button1.draw_Button(screen, WHITE)
        button2.draw_Button(screen, WHITE)
        button3.draw_Button(screen, WHITE)

        #แสดงรอบและเวลา FPS
        if GAME_OVER == False:
            screen.blit(elapsed,(700,200))
            screen.blit(Turn_Numder,(1000,200))
            screen.blit(msg, (200, 200))

        #display charater
        if end_game2 == False :
            Monter.blit(screen,t)
        if end_game1 == False :
            Player.blit(screen,t)
        Spell.blit_spell(screen,t)
        Effect.blit_Effect(screen,t)

    if not pygame.mixer.get_busy():
            sound_playing = False
            sound_playing1 = False

    if GAME_OVER == True :
        screen.blit(GAME_OVER_TEXT,(700,100))
        screen.blit(Quit_image,(900,500))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Quit_image_rect.collidepoint(event.pos) and GAME_OVER == True:
                    sound_Ui.play()
                    run = False
    if GAME_OVER == True and sound_gameover == True:
        sound_game_over.play()
        sound_gameover = False

    
    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()