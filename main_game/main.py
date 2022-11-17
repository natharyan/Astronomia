import pygame
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
#import sqlite3
import mysql.connector as dat
import random
from game import Game

"""
cur.execute("create table user(\
                        username varchar(20) NOT NULL,\
                        password varchar(20) NOT NULL,
                        level int DEFAULT 0,\
                        PRIMARY KEY(username))")
"""

def play_music():
    mixer.init()
    mixer.music.load("./assets/sounds/1.mp3")
    mixer.music.play(-1)

def info_screen(level_num: int, planet_name: str, planet_desc_list, image_path: str, game_bool: bool = True):
    play_music()
    l = planet_desc_list
    l1 = random.sample(l, 3)
    txt1, txt2, txt3 = l1
    level = Tk()
    level.configure(bg="#1e1e1e")
    level.title(f"Level {level_num} Completed!")
    w = 900  # width for the Tk root
    h = 600  # height for the Tk root
    ws = level.winfo_screenwidth()  # width of the screen
    hs = level.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    bg = ImageTk.PhotoImage(file="./assets/sprites/space.png")
    planet_img = (Image.open(image_path))
    resized_planet = planet_img.resize((180, 180), Image.ANTIALIAS)
    planet = ImageTk.PhotoImage(resized_planet)
    canvas = Canvas(level, width=900, height=600) # Create a canvas
    canvas.pack(expand=True, fill=BOTH)
    canvas.create_image(0, 0, image=bg, anchor="nw") # Add the image in the canvas
    canvas.create_image(365, 100, image=planet, anchor="nw")
    level.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def go_lobby():
        level.destroy()
        lobby()

    Label(level, text=f"{planet_name} Reached!", bg="#000", fg="#fff",
          font=("Impact", 40, "bold")).place(relx=0.5, y=50, anchor='center')
    Label(level, text=txt1, bg="#000", fg="#fff",
          font=("Century Gothic", 15)).place(relx=0.5, y=320, anchor='center')
    Label(level, text=txt2, bg="#000", fg="#fff",
          font=("Century Gothic", 15)).place(relx=0.5, y=360, anchor='center')
    Label(level, text=txt3, bg="#000", fg="#fff",
          font=("Century Gothic", 15)).place(relx=0.5, y=400, anchor='center')
    if game_bool:
        def game_start():
            mixer.music.stop()
            level.destroy()
            message = maingame(global_level) # "won" or "lost"
            check(message)
        Button(level, text="Play", width=10, height=2, bg="orange",
               command=game_start, font=("Impact", 20, "bold")).place(x=328, y=430)
    if level_num==8:
        Button(level, text="Lobby", width=10, height=2, bg="orange",
           command=go_lobby, font=("Impact", 20, "bold")).place(x=395, y=430)
    else:
        Button(level, text="Lobby", width=10, height=2, bg="orange",
            command=go_lobby, font=("Impact", 20, "bold")).place(x=468, y=430)
        Label(level, text=f"Planet {level_num} - {planet_name}", bg="#000", fg="#fff",
            font=("Impact", 30, "bold")).place(x=347, y=500)

    global_level = level_num
    level.mainloop()
    
def maingame(level):
    main_game = Game(level)
    message = main_game.main_loop()  # "won" or "lost"
    return message

def check(message):
    print("check function called")
    if message == "won":
        qry = "UPDATE user SET level=level+1 WHERE username='%s';" % (uname,)
        cur.execute(qry)
        conn.commit()
        qry = "SELECT level FROM user WHERE username='%s';" % (uname,)
        cur.execute(qry)
        level_new = cur.fetchone()[0]
        print('Current level:', level_new)
        info_screen(**level_characteristics[level_new])
    elif message == "lost":
        play_music()
        lobby()

def lobby():
    global global_level
    lobby_screen = Tk()
    lobby_screen.configure(bg="#1e1e1e")
    lobby_screen.title("Game Lobby")
    w = 900  
    h = 600  
    ws = lobby_screen.winfo_screenwidth()
    hs = lobby_screen.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    qry = "SELECT level FROM user WHERE username='%s';" % (uname,)
    cur.execute(qry)
    global_level = cur.fetchone()[0]
    print('level =', global_level, type(global_level))
    shipno = global_level+1
    if shipno == 9:
        shipno = 8
    bg = ImageTk.PhotoImage(file="./assets/sprites/space.png")
    shipimg = (Image.open("./assets/sprites/spaceship"+str(shipno)+".png"))
    platform = (Image.open("./assets/sprites/platform.png"))
    controls = (Image.open("./assets/sprites/controls.png"))
    parts = (Image.open("./assets/sprites/parts.png"))
    if shipno == 6:
        resized_shipimg = shipimg.resize((180, 230), Image.ANTIALIAS)
    elif shipno == 7:
        resized_shipimg = shipimg.resize((180, 220), Image.ANTIALIAS)
    elif shipno == 8:
        resized_shipimg = shipimg.resize((120, 250), Image.ANTIALIAS)
    else:
        resized_shipimg = shipimg.resize((180, 180), Image.ANTIALIAS)
    shipimg = ImageTk.PhotoImage(resized_shipimg)
    resized_platform = platform.resize((200, 90), Image.ANTIALIAS)
    platform = ImageTk.PhotoImage(resized_platform)
    resized_controls = controls.resize((320, 230), Image.ANTIALIAS)
    controls = ImageTk.PhotoImage(resized_controls)
    resized_parts = parts.resize((300, 200), Image.ANTIALIAS)
    parts = ImageTk.PhotoImage(resized_parts)
    canvas = Canvas(lobby_screen, width=900, height=600)
    canvas.pack(expand=True, fill=BOTH)
    canvas.create_image(0, 0, image=bg, anchor="nw")
    canvas.create_image(352, 355, image=platform, anchor="nw")
    canvas.create_image(0, 0, image=controls, anchor="nw")
    canvas.create_image(600, 50, image=parts, anchor="nw")
    if shipno == 6:
        canvas.create_image(360, 190, image=shipimg, anchor="nw")
    elif shipno == 7:
        canvas.create_image(360, 195, image=shipimg, anchor="nw")
    elif shipno == 8:
        canvas.create_image(387, 170, image=shipimg, anchor="nw")
    else:
        canvas.create_image(360, 215, image=shipimg, anchor="nw")
    canvas.create_rectangle(0, 600, 200, 250,
                            outline="white", fill=None,
                            width=2)
    canvas.create_rectangle(700, 600, 900, 250,
                            outline="white", fill=None,
                            width=2)
    lobby_screen.geometry('%dx%d+%d+%d' % (w, h, x, y))
    l = ['1-Mercury', '2-Venus', '3-Earth', '4-Mars',
         '5-Jupiter', '6-Saturn', '7-Uranus', '8-Neptune']
    l1 = l[:global_level]
    Label(lobby_screen, text="Levels Completed:", width=16, bg="#fff", fg="#000",
          font=("Impact", 20)).place(x=10, y=260)
    if len(l1) == 0:
        Label(lobby_screen, text="No Level Completed", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=300)
    if '1-Mercury' in l1:
        Label(lobby_screen, text="1-Mercury", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=300)
    if '2-Venus' in l1:
        Label(lobby_screen, text="2-Venus", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=335)
    if '3-Earth' in l1:
        Label(lobby_screen, text="3-Earth", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=370)
    if '4-Mars' in l1:
        Label(lobby_screen, text="4-Mars", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=405)
    if '5-Jupiter' in l1:
        Label(lobby_screen, text="5-Jupiter", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=440)
    if '6-Saturn' in l1:
        Label(lobby_screen, text="6-Saturn", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=475)
    if '7-Uranus' in l1:
        Label(lobby_screen, text="7-Uranus", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=510)
    if '8-Neptune' in l1:
        Label(lobby_screen, text="8-Neptune", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=10, y=545)

    def level_value(x):
        mixer.music.stop()
        lobby_screen.destroy()
        maingame(x)
        play_music()
        lobby()

    Label(lobby_screen, text="Play Again:", width=16, bg="#fff", fg="#000",
          font=("Impact", 20)).place(x=708, y=260)
    if len(l1) == 0:
        Label(lobby_screen, text="No Level Completed", width=16, bg="#fff", fg="#000",
              font=("Century Gothic", 18)).place(x=708, y=300)
    if '1-Mercury' in l1:
        Button(lobby_screen, text="Level 1", width=16,
               command=lambda: level_value(0), font=("Century Gothic", 18)).place(x=708, y=300)
    if '2-Venus' in l1:
        Button(lobby_screen, text="Level 2", width=16,
               command=lambda: level_value(1), font=("Century Gothic", 18)).place(x=708, y=335)
    if '3-Earth' in l1:
        Button(lobby_screen, text="Level 3", width=16,
               command=lambda: level_value(2), font=("Century Gothic", 18)).place(x=708, y=370)
    if '4-Mars' in l1:
        Button(lobby_screen, text="Level 4", width=16,
               command=lambda: level_value(3), font=("Century Gothic", 18)).place(x=708, y=405)
    if '5-Jupiter' in l1:
        Button(lobby_screen, text="Level 5", width=16,
               command=lambda: level_value(4), font=("Century Gothic", 18)).place(x=708, y=440)
    if '6-Saturn' in l1:
        Button(lobby_screen, text="Level 6", width=16,
               command=lambda: level_value(5), font=("Century Gothic", 18)).place(x=708, y=475)
    if '7-Uranus' in l1:
        Button(lobby_screen, text="Level 7", width=16,
               command=lambda: level_value(6), font=("Century Gothic", 18)).place(x=708, y=510)
    if '8-Neptune' in l1:
        Button(lobby_screen, text="Level 8", width=16,
               command=lambda: level_value(7), font=("Century Gothic", 18)).place(x=708, y=545)
    maneuver_stat=2.5+(0.25*(global_level+1))
    acc_stat=0.1+(0.025*(global_level+1))
    speed_stat=2+(0.5*(global_level+1))
    maneuver_stat,acc_stat,speed_stat = round(maneuver_stat,2), round(acc_stat,2),round(speed_stat,2)
    print(maneuver_stat,acc_stat,speed_stat)
    Label(lobby_screen, text="ASTRONOMIA", bg="#000", fg="#fff",
          font=("Impact", 55, "bold")).place(x=302, y=20)
    Label(lobby_screen, text=f"WELCOME, {uname}", bg="#000", fg="#fff",
          font=("Impact", 35)).place(relx=0.5, y=150, anchor="center")
    Label(lobby_screen, text="Spaceship Stats:", width=16, bg="#000", fg="#fff",
          font=("Impact", 20)).place(x=205, y=260)
    Label(lobby_screen, text=f"Rotation: {maneuver_stat}°", bg="#000", fg="#fff",
          font=("Sawasdee", 13)).place(x=224, y=295)
    Label(lobby_screen, text=f"Acc: {acc_stat}m/s^2", bg="#000", fg="#fff",
          font=("Sawasdee", 13)).place(x=224, y=320)
    Label(lobby_screen, text=f"Bullets: {speed_stat}m/s", bg="#000", fg="#fff",
          font=("Sawasdee", 13)).place(x=224, y=345)

    def game_start():
        mixer.music.stop()
        lobby_screen.destroy()
        message = maingame(global_level) # "won" or "lost"
        check(message)

    if len(l1) >= 8:
        Label(lobby_screen, text="Game Completed!", width=14, height=2,
              font=("Impact", 20, "bold")).place(x=372, y=480)
    elif len(l1) == 0:
        Button(lobby_screen, text="Start", width=10, height=2,
               command=game_start, font=("Impact", 20, "bold")).place(x=396, y=480)
    else:
        Button(lobby_screen, text="Continue", width=10, height=2,
               command=game_start, font=("Impact", 20, "bold")).place(x=396, y=480)
    
    def Close():
        print("Exit")
        lobby_screen.destroy()

    Button(lobby_screen, text="Exit", width=10, height=1,
               command=Close, font=("Impact", 20, "bold")).place(x=778, y=8)
    
    lobby_screen.mainloop()


def login():
    global uname
    flag = 0
    exist = False
    uname = username.get()
    pwd = password.get()
    if uname == '' or pwd == '':
        message.set("fill the empty field!!!")
    else:
        qry = 'select * from user'
        cur.execute(qry)
        print("Values entered:")
        for x in cur:
            print(x)
            if x[0] == uname and x[1] == pwd:
                exist = True
            elif x[0] == uname and x[1] != pwd:
                message.set("Wrong password!")

        print('username =', username.get(), 'password =', password.get())
        if not exist:
            print("Creating new record")
            query = "INSERT INTO user(username,password) VALUES(%s,%s)"
            cur.execute(query, (uname, pwd))
            conn.commit()

        elif exist:
            print("Record already exists")

        message.set("Login success")
        print("Login success")
        pygame.time.delay(1000)
        flag = 1

    if flag:
        login_screen.destroy()
        lobby()

def Loginform():
    global login_screen
    play_music()
    login_screen = Tk()
    login_screen.configure(bg="#1e1e1e")
    login_screen.title("Login")
    w = 900  # width for the Tk root
    h = 600  # height for the Tk root
    ws = login_screen.winfo_screenwidth()  # width of the screen
    hs = login_screen.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    bg = ImageTk.PhotoImage(file="./assets/sprites/space.png")
    shipimg = (Image.open("./assets/sprites/spaceship1.png"))
    resized_shipimg = shipimg.resize((160, 160), Image.ANTIALIAS)
    shipimg = ImageTk.PhotoImage(resized_shipimg)
    saturn = (Image.open("./assets/sprites/saturn.png"))
    jupiter = (Image.open("./assets/sprites/jupiter.png"))
    earth = (Image.open("./assets/sprites/earth.png"))
    mercury = (Image.open("./assets/sprites/mercury.png"))
    mars = (Image.open("./assets/sprites/mars.png"))
    venus = (Image.open("./assets/sprites/venus.png"))
    uranus = (Image.open("./assets/sprites/uranus.png"))
    neptune = (Image.open("./assets/sprites/neptune.png"))
    resized_planet1 = saturn.resize((195, 190), Image.ANTIALIAS)
    planet1 = ImageTk.PhotoImage(resized_planet1)
    resized_planet2 = jupiter.resize((180, 190), Image.ANTIALIAS)
    planet2 = ImageTk.PhotoImage(resized_planet2)
    resized_planet3 = earth.resize((180, 190), Image.ANTIALIAS)
    planet3 = ImageTk.PhotoImage(resized_planet3)
    resized_planet4 = mercury.resize((110, 110), Image.ANTIALIAS)
    planet4 = ImageTk.PhotoImage(resized_planet4)
    resized_planet5 = mars.resize((110, 110), Image.ANTIALIAS)
    planet5 = ImageTk.PhotoImage(resized_planet5)
    resized_planet6 = venus.resize((110, 110), Image.ANTIALIAS)
    planet6 = ImageTk.PhotoImage(resized_planet6)
    resized_planet7 = uranus.resize((180, 180), Image.ANTIALIAS)
    planet7 = ImageTk.PhotoImage(resized_planet7)
    resized_planet8 = neptune.resize((120, 120), Image.ANTIALIAS)
    planet8 = ImageTk.PhotoImage(resized_planet8)
    canvas = Canvas(login_screen, width=900, height=600)
    canvas.pack(expand=True, fill=BOTH)
    canvas.create_image(0, 0, image=bg, anchor="nw")
    canvas.create_image(375, 100, image=shipimg, anchor="nw")
    canvas.create_image(110, 200, image=planet1, anchor="nw")
    canvas.create_image(30, 50, image=planet2, anchor="nw")
    canvas.create_image(680, 200, image=planet3, anchor="nw")
    canvas.create_image(640, 90, image=planet4, anchor="nw")
    canvas.create_image(750, 50, image=planet5, anchor="nw")
    canvas.create_image(10, 350, image=planet6, anchor="nw")
    canvas.create_image(130, 380, image=planet7, anchor="nw")
    canvas.create_image(640, 380, image=planet8, anchor="nw")
    login_screen.geometry('%dx%d+%d+%d' % (w, h, x, y))

    global message
    global username
    global password
    username = StringVar()
    password = StringVar()
    message = StringVar()

    Label(login_screen, text="Username", bg="#000", fg="#fff",
          font=("Impact", 20, "bold")).place(x=410, y=270)

    Entry(login_screen, textvariable=username, bg="#000", fg="#fff",
          font=("Impact", 20)).place(x=340, y=300)

    Label(login_screen, text="Password", bg="#000", fg="#fff",
          font=("Impact", 20, "bold")).place(x=410, y=358)

    Entry(login_screen, textvariable=password, bg="#000", fg="#fff",
          font=("Impact", 20)).place(x=340, y=390)

    Label(login_screen, text="", textvariable=message, bg="#000",
          fg="#fff", font=("Impact", 15, "bold")).place(x=320, y=440)

    Button(login_screen, text="Login", width=10, height=1, bg="orange",
           command=login, font=("Impact", 20, "bold")).place(x=401, y=480)
    Label(login_screen, text="ASTRONOMIA", bg="#000", fg="#fff",
          font=("Impact", 55, "bold")).place(x=310, y=20)
    login_screen.mainloop()

level_characteristics = {
    1:  {
        'level_num': 1,
        'planet_name': "Mercury",
        'planet_desc_list': ['Not only is Mercury the smallest planet, it is also shrinking!','Although it is closest to the sun, it still has ice on its surface','As Mercury moves along its orbit, it leaves a trail of hydrogen behind it','The biggest crater in Mercury could fit Western Europe.'],
        'image_path': "./assets/sprites/mercury.png",
        "game_bool": True
    },
    2:  {
        'level_num': 2,
        'planet_name': "Venus",
        'planet_desc_list': ['A day on Venus is longer than a year.','Venus is hotter than Mercury despite being further away from the Sun.','Unlike other planets in our solar system, Venus spins clockwise.','Venus is the second brightest natural object in the night sky after the Moon.'],
        'image_path': "./assets/sprites/venus.png",
        "game_bool": True
    },
    3:  {
        'level_num': 3,
        'planet_name': "Earth",
        'planet_desc_list': ['The Earth\'s rotation is gradually slowing.','The Earth was once believed to be the centre of the universe.','Earth is the only planet not named after a god.','The Earth is the densest planet in the Solar System.','Earth\'s core is as hot as the Sun\'s surface.','We weigh less at the equator than at the poles.'],
        'image_path': "./assets/sprites/earth.png",
        "game_bool": True
    },
    4:  {
        'level_num': 4,
        'planet_name': "Mars",
        'planet_desc_list': ['Mars and Earth have approximately the same landmass.','Mars is home to the tallest mountain in the solar system.','Only 18 missions to Mars have been successful.','Mars has the largest dust storms in the solar system.','You could jump 3 times as higher on mars than on earth.','Mars has the largest canyon in our solar system, which is 6-7KM deep.'],
        'image_path': "./assets/sprites/mars.png",
        "game_bool": True
    },
    5:  {
        'level_num': 5,
        'planet_name': "Jupiter",
        'planet_desc_list': ['Jupiter is the largest planet in the Solar System.','Jupiter is the fastest spinning planet in the Solar System.','The clouds on Jupiter are 50 km thick','Jupiter\'s great red spot is thrice as large as earth','Jupiter is a failed star'],
        'image_path': "./assets/sprites/jupiter.png",
        "game_bool": True
    },
    6:  {
        'level_num': 6,
        'planet_name': "Saturn",
        'planet_desc_list': ['Saturn is the most distant planet that can be seen with the naked eye.','Saturn has the most moons - 82','Saturn could float in water because it is mostly made of gas.','The rings of Saturn are made up of bits of ice, dust and rock.','Saturn was first found by the Assyrians in the 8th century AD','Its rings, although large are only 20 metres thick'],
        'image_path': "./assets/sprites/saturn.png",
        "game_bool": True
    },
    7:  {
        'level_num': 7,
        'planet_name': "Uranus",
        'planet_desc_list': ['Uranus is the coldest planet in the Solar System.','Uranus is the only planet which spins on its side.','Its moons are named after characters created by Shakespeare.','Due to high pressure, diamonds are formed on its surface.','Uranus is blue due to the presence of methane'],
        'image_path': "./assets/sprites/uranus.png",
        "game_bool": True
    },
    8:  {
        'level_num': 8,
        'planet_name': "Neptune",
        'planet_desc_list': ['Neptune’s surface gravity is almost Earth-like','Voyager 2 is the only craft that has reached as far as Neptune.','It takes Neptune 165 years to orbit the Sun.','Neptune has the strongest winds in the Solar System.'],
        'image_path': "./assets/sprites/neptune.png",
        "game_bool": False
    }
}


if __name__ == "__main__":
    conn = conn = dat.connect(
        host="localhost", user="root", passwd="", database="Astronomia")
    cur = conn.cursor()

    Loginform()
