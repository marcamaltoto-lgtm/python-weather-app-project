from tkinter import *
from PIL import Image, ImageTk
import pytz
import tkinter as tk
from datetime import datetime, timedelta 
from timezonefinder import TimezoneFinder
import requests
from geopy.geocoders import Nominatim 
from tkinter import messagebox

#on fait la fonction pour le search_button
def gettheweather():
        city = search_bar_entry.get()
        #on vas gerer les erreurs
        if not city:
            messagebox.showwarning("Error", "Entrer une ville valide")
            return
        geolocator = Nominatim(user_agent="my_weather_app")
        location = geolocator.geocode(city)
        if not location:
            messagebox.showwarning("Error", "Ville introuvable")
            return
        obj = TimezoneFinder()
        result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
        zone.config(text=result)
        
        long_lat.config(text=f"{round(location.latitude,4)}°N {round(location.longitude,4)}°E")
        
        #on affiche l'heure
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        
        #on vas utiliser une api key pour demander a une api de nous permettre d'acceder aux donnees de la meteo 
        api_key = "4b8317b770dcb7721018974e4eec87c7"
        api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        json_data = requests.get(api).json()
        
        #on vas recuperer renvoyer par l'api et les afficher
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
        
        #pour l'affichage des cinqs autres jour on prend pour 12:00:00pm
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
            img = Image.open(f"weather app/icon/{icon_code}@2x.png").resize((50,50))
            icons.append(ImageTk.PhotoImage(img))
            temps.append((daily_data[i]['main']['temp_max'], daily_data[i]['main']['feels_like']))
            
        day_widget = [
            (first_image, first_day, first_temperature),
            (second_image, second_day, second_temperature),
            (third_image, third_day, third_temperature), 
            (fourth_image, fourth_day, fourth_temperature),
            (fifth_image, fifth_day, fifth_temperature)
        ]
        
        for i,(img_label, day_label, temp_label) in enumerate(day_widget):
            if i >= len(icons):
                break
            img_label.config(image=icons[i])
            img_label.image = icons[i]
            temp_label.config(text=f"Day: {temps[i][0]}\nNight: {temps[i][1]}")
            future_date = datetime.now() + timedelta(days=i)
            day_label.config(text=future_date.strftime("%A"))
    

#creation de la fenetre tkinter 
root = Tk()
root.title("My weather app")
root.geometry("750x470+300+200")
root.config(bg="#353B45")
root.resizable(False, False)
root.iconbitmap("weather app/logo.ico")

#on fait l'interface en general
#on insere une image qui servirat de conteneur pour les elements de la meteo du jour j
box = PhotoImage(file="weather app/box.png").subsample(5,5)
label_daily_weather = Label(root, image=box, bg="#353B45", font=("Helvetica", 14))
label_daily_weather.place(x=10, y=60)

#on fait l'interieur du containeur
label_title = Label(root, text="Today's forecast", bg="#282E7B", fg="#C99379", font=("Helvetica", 12, "bold"))
label_title.place(x=70, y=90)
label_temperature = Label(root, text="Temperature", bg="#282E7B", fg="white", font=("Helvetica", 12))
label_temperature.place(x=30, y=120)
label_humidity = Label(root, text="Humidity", bg="#282E7B", fg="white", font=("Helvetica", 12))
label_humidity.place(x=30, y=140)
label_pressure = Label(root, text="Pressure", bg="#282E7B", fg="white", font=("Helvetica", 12))
label_pressure.place(x=30, y=160)
label_wind_speed = Label(root, text="Wind Speed", bg="#282E7B", fg="white", font=("Helvetica", 12))
label_wind_speed.place(x=30, y=180)
label_description = Label(root, text="Description", bg="#282E7B", fg="white", font=("Helvetica", 12))
label_description.place(x=30, y=200)

#on fait la barre de recherche
search_bar_image = PhotoImage(file="weather app/search bar.png").subsample(4,4)
search_bar_label = Label(root, image=search_bar_image, bg="#353B45")
search_bar_label.place(x=290, y=95)
#on fait une entry pour enter les villes
search_bar_entry = Entry(root, bg="#e8e8e8", font=("Helvetica", 15), fg="#282E7B", width=23, border=0, justify="center")
search_bar_entry.place(x=415, y=175)
#on fait le bouton pour rechercher
search_button_image = PhotoImage(file="weather app/search.png").subsample(15,15)
search_button = Button(root, image=search_button_image, cursor="hand2", bg="#e8e8e8", border=0, command=gettheweather)
search_button.place(x=685, y=171)

#on fait un espace dans lequel sera les previsions quotidiennes sur 5 jours 
bottom_frame = Frame(root, bg="#FBB45E", width=900, height=180)
bottom_frame.pack(side="bottom")
#on insere les images dans lesquels il y aura les previsions 
first_boxe = PhotoImage(file="weather app/Rounded Rectangle 2.png")
second_boxe = PhotoImage(file="weather app/Rounded Rectangle 2 copy.png")
#et on affiche ceux-ci
Label(bottom_frame, image=first_boxe, bg="#FBB45E").place(x=30, y=20)
Label(bottom_frame, image=second_boxe, bg="#FBB45E").place(x=300, y=30)
Label(bottom_frame, image=second_boxe, bg="#FBB45E").place(x=400, y=30)
Label(bottom_frame, image=second_boxe, bg="#FBB45E").place(x=500, y=30)
Label(bottom_frame, image=second_boxe, bg="#FBB45E").place(x=600, y=30)

#on vas faire des labels pour afficher la position du la recherche, sa geolocalisation en long et lat et son heure locale
clock = Label(root, bg="#353B45", fg="#251211", font=("Helvetica", 20))
clock.place(x=70, y=10)
zone = Label(root, bg="#353B45", fg="#251211", font=("Helvetica", 20))
zone.place(x=500, y=10)
long_lat = Label(root, bg="#353B45",fg="#251211", font=("Helvetica", 15))
long_lat.place(x=500, y=50)

#on vas inserer des frames dans les 5 boites de predictions quotidiennes et faire l'interieur
#pour la premiere
first_frame = Frame(root, bg="#323661", width=230, height=132)
first_frame.place(x=35,y=315)
first_image = Label(first_frame, bg="#323661", image=first_boxe)
first_image.place(x=1, y=15)
first_day = Label(first_frame, bg="#323661", fg="white", font=("Arial", 14))
first_day.place(x=100,y=5)
first_temperature = Label(first_frame, bg="#323661", fg="white", font=("Helvetica", 12, "bold"))
first_temperature.place(x=100, y=50)
#pour la deuxieme
second_frame = Frame(root, bg="#eeefea", width=70, height=115)
second_frame.place(x=305,y=325)
second_image = Label(second_frame, bg="#eeefea")
second_image.place(x=7, y=20)
second_day = Label(second_frame, fg="#7D7585", bg="#eeefea", font=("Arial", 10))
second_day.place(x=10,y=5)
second_temperature = Label(second_frame, fg="#7D7585", bg="#eeefea", font=("Helvetica", 8, "bold"))
second_temperature.place(x=2, y=70)
#pour la troisieme
third_frame = Frame(root, bg="#eeefea", width=70, height=115)
third_frame.place(x=405,y=325)
third_image = Label(third_frame, bg="#eeefea")
third_image.place(x=7, y=20)
third_day = Label(third_frame, fg="#7D7585", bg="#eeefea", font=("Arial", 12))
third_day.place(x=10,y=5)
third_temperature = Label(third_frame, fg="#7D7585", bg="#eeefea", font=("Helvetica", 8, "bold"))
third_temperature.place(x=2, y=70)
#pour la quatrieme
fourth_frame = Frame(root, bg="#eeefea", width=70, height=115)
fourth_frame.place(x=505,y=325)
fourth_image = Label(fourth_frame, bg="#eeefea")
fourth_image.place(x=7, y=20)
fourth_day = Label(fourth_frame, fg="#7D7585", bg="#eeefea", font=("Arial", 10))
fourth_day.place(x=10,y=5)
fourth_temperature = Label(fourth_frame, fg="#7D7585", bg="#eeefea", font=("Helvetica", 8, "bold"))
fourth_temperature.place(x=2, y=70)
#pour la cinquieme
fifth_frame = Frame(root, bg="#eeefea", width=70, height=115)
fifth_frame.place(x=605,y=325)
fifth_image = Label(fifth_frame, bg="#eeefea" )
fifth_image.place(x=7, y=20)
fifth_day = Label(fifth_frame, bg="#eeefea", fg="#7D7585", font=("Arial", 12))
fifth_day.place(x=10,y=5)
fifth_temperature = Label(fifth_frame, bg="#eeefea", fg="#7D7585", font=("Helvetica", 8, "bold"))
fifth_temperature.place(x=2, y=70)

#on vas mettre des labels a l'interieur du container pour afficher des donnees
temperature_data = Label(root, bg="#333c4c", font=("Helvetica", 11), fg="white")
temperature_data.place(x=150, y=120)
humidity_data = Label(root, bg="#333c4c", font=("Helvetica", 11), fg="white")
humidity_data.place(x=150, y=140)
pressure_data = Label(root, bg="#333c4c", font=("Helvetica", 11), fg="white")
pressure_data.place(x=150, y=160)
wind_speed_data = Label(root, bg="#333c4c", font=("Helvetica", 11), fg="white")
wind_speed_data.place(x=150, y=180)
description_data = Label(root, bg="#333c4c", font=("Helvetica", 11), fg="white")
description_data.place(x=150, y=200)

#affichage de cette fenetre
root.mainloop()