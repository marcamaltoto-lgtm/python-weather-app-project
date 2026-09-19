from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests 
from PIL import Image, ImageTk
from tkinter import messagebox
from timezonefinder import TimezoneFinder

#on creer la fonction weather qui nous permettra de connaitre la meteo en fonction de la ville
def getweather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="new")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)
    
    long_lat.config(text=f"{round(location.latitude,4)}°N {round(location.longitude,4)}°E")
    
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    
    api_keys = "ffa3ca4b66665e22748f52ab761c5905"
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_keys}&units=metric"
    json_data = requests.get(api).json()
    
    #current weather from first forecast
    current = json_data['list'][0]
    temp = current['main']['temp']
    humidity = current['main']['humidity']
    pressure = current['main']['pressure']
    wind_speed = current['wind']['speed']
    description = current['weather'][0]['description']
    temperature_data.config(text=f"{temp}°C")
    humidity_data.config(text=f"{humidity}%")
    pressure_data.config(text=f"{pressure}hPa")
    wind_speed_data.config(text=f"{wind_speed}m/s")
    description_data.config(text=f"{description}")
    
    #Daily forecast -pick 12:00pm entries
    daily_data = []
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']:
            daily_data.append(entry)
    
    icons = []
    temps = []
    
    for i in range(5):
        if i >= len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]['icon']
        img = Image.open(f"weather app/icon/{icon_code}@2x.png").resize((50, 50))
        icons.append(ImageTk.PhotoImage(img))
        temps.append((daily_data[i]['main']['temp_max'], daily_data[i]['main']['feels_like']))
        
    day_widget = [
        (firstimage, day1, day1temp),
        (secondimage, day2, day2temp),
        (thirdimage, day3, day3temp),
        (fourthimage, day4, day4temp),
        (fifthimage, day5, day5temp),
    ]
    
    for i,(img_label, day_label, temp_label) in enumerate(day_widget):
        if i >= len(icons):
            break
        img_label.config(image=icons[i])
        img_label.image = icons[i]
        temp_label.config(text=f"Day: {temps[i][0]}\nNight: {temps[i][1]}")
        future_date = datetime.now() + timedelta(days=i)
        day_label.config(text=future_date.strftime("%A"))

#creation de la fenetre 
root = Tk()
root.title("weather app")
root.iconbitmap("weather app/logo.ico")
root.geometry("750x470+300+200")
root.resizable(False, False)
root.config(bg="#202731")

#image de boite ronde
round_box = PhotoImage(file="weather app/Rounded Rectangle 1.png")
Label(root, image=round_box, bg="#202731").place(x=30, y=60)

#l'interieur de l'image de boite ronde
label_temperature = Label(root, text="Temperature", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")
label_temperature.place(x=50, y=120)
label_humidity = Label(root, text="Humidity", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")
label_humidity.place(x=50, y=140)
label_pressure = Label(root, text="Pressure", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")
label_pressure.place(x=50, y=160)
label_wind_speed = Label(root, text="Wind Speed", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")
label_wind_speed.place(x=50, y=180)
label_description = Label(root, text="Description", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")
label_description.place(x=50, y=200)

#search box
search_image = PhotoImage(file="weather app/Rounded Rectangle 3.png")
myimage = Label(root, image=search_image, bg="#202731")
myimage.place(x=270, y=122)
#on vas inserer l'image de la boite recherche
weather_image = PhotoImage(file="weather app/Layer 7.png")
weatherimage = Label(root, image=weather_image, bg="#333c4c")
weatherimage.place(x=295, y=126)
#on vas introduire un espace pour inserer du texte a l'interieur de la search box
textfield = tk.Entry(root, justify="center", width=15, font=("Helvetica", 25, "bold"), bg="#333c4c", fg="white", border=0)
textfield.place(x=364, y=130)
#on vas integrer l'icone pour chercher 
search_icon = PhotoImage(file="weather app/Layer 6.png")
myimage_icon = Button(root, image=search_icon, borderwidth=0, cursor="hand2", bg="#333c4c", command=getweather)
myimage_icon.place(x=655, y=135)

#bottom box 
#creation d'une frame 
frame = Frame(root, width=900, height=180, bg="#7094d4")
frame.pack(side=BOTTOM)
#boxes
first_boxe = PhotoImage(file="weather app/Rounded Rectangle 2.png")
second_boxe = PhotoImage(file="weather app/Rounded Rectangle 2 copy.png")
Label(frame, image=first_boxe, bg="#7094d4").place(x=30, y=20)
Label(frame, image=second_boxe, bg="#7094d4").place(x=300, y=30)
Label(frame, image=second_boxe, bg="#7094d4").place(x=400, y=30)
Label(frame, image=second_boxe, bg="#7094d4").place(x=500, y=30)
Label(frame, image=second_boxe, bg="#7094d4").place(x=600, y=30)
#clock
clock = Label(root, font=("Helvetica", 20), bg="#202731", fg="white")
clock.place(x=30, y=20)
#timezone
timezone = Label(root, font=("Helvetica", 20), bg="#202731", fg="white")
timezone.place(x=500, y=20)

long_lat = Label(root, font=("Helvetica", 10), bg="#202731", fg="white")
long_lat.place(x=500, y=50)

#on vas afficher les donnees qui s'afficheront dans l'image de la boite ronde
temperature_data= Label(root, font=("Helvetica", 10), fg="white", bg="#333c4c")
temperature_data.place(x=150, y=120)

humidity_data = Label(root, font=("Helvetica", 10), fg="white", bg="#333c4c")
humidity_data.place(x=150, y=140)

pressure_data = Label(root, font=("Helvetica", 10), fg="white", bg="#333c4c")
pressure_data.place(x=150, y=160)

wind_speed_data = Label(root, font=("Helvetca", 10), fg="white", bg="#333c4c")
wind_speed_data.place(x=150, y=180)

description_data = Label(root, font=("Helvetica", 10), fg="white", bg="#333c4c")
description_data.place(x=150, y=200)

#l'interieur de la first boxe (on fait les elements qui y seront)
#la premiere cellule
#on fait la frame pour la cellule
firstframe = Frame(root, width=230, height=132, bg="#323661")
firstframe.place(x=35, y=315)
#on insere l'image grace a Label
firstimage = Label(firstframe, image=first_boxe, bg="#323661")
firstimage.place(x=1, y=15)
#on affiche le premier jour
day1 = Label(firstframe, font=("Arial", 20), bg="#323661", fg="white")
day1.place(x=100, y=5) 
#et sa temperature
day1temp = Label(firstframe, font=("Helvetica", 15, "bold"), bg="#323661", fg="white")
day1temp.place(x=100, y=50)

#on fait la deuxieme cellule
secondframe = Frame(root, width=70, height=115, bg="#eeefea")
secondframe.place(x=305, y=325)
#on affiche l'image grace a Label
secondimage = Label(secondframe, bg="#eeefea")
secondimage.place(x=7, y=20)
#on affiche le deuxieme jour
day2 = Label(secondframe, bg="#eeefea", fg="#000")
day2.place(x=10, y=5)
#on affiche la temperature du deuxieme jour
day2temp = Label(secondframe, fg="#000", bg="#eeefea")
day2temp.place(x=2, y=70)

#on fait la troisieme cellule
thirdframe = Frame(root, width=70, height=115, bg="#eeefea")
thirdframe.place(x=405, y=325)
#on affiche l'image grace a Label
thirdimage = Label(thirdframe, bg="#eeefea")
thirdimage.place(x=7, y=20)
#on affiche le troisiem jour
day3 = Label(thirdframe, bg="#eeefea", fg="#000")
day3.place(x=10, y=5)
#on affiche la temperature du troisieme jour
day3temp = Label(thirdframe, fg="#000", bg="#eeefea")
day3temp.place(x=2, y=70)

#on fait la quatrieme cellule
#on cree la frame
fourthframe = Frame(root, width=70, height=115, bg="#eeefea")
fourthframe.place(x=505, y=325)
#on insere l'image grace a Label
fourthimage = Label(fourthframe, bg="#eeefea")
fourthimage.place(x=7, y=20)
#on fait le quatrieme jour
day4 = Label(fourthframe, bg="#eeefea", fg="#000")
day4.place(x=10, y=5)
#on affiche la temperature du quatrieme jour
day4temp = Label(fourthframe, bg="#eeefea", fg="#000")
day4temp.place(x=2, y=70)

#on fait la cinquieme cellule
#on creer la frame pour celle-ci
fifthframe = Frame(root, width=70, height=115, bg="#eeefea")
fifthframe.place(x=605, y=325)
#on vas inserer l'image 
fifthimage = Label(fifthframe, bg="#eeefea")
fifthimage.place(x=10, y=5)
#on fait le cinquieme jour 
day5 = Label(fifthframe, bg="#eeefea", fg="#000")
day5.place(x=10, y=5)
#on fait la temperature du cinquieme jour
day5temp = Label(fifthframe, bg="#eeefea", fg="#000")
day5temp.place(x=2, y=70)

#affichage de la fenetre 
root.mainloop()