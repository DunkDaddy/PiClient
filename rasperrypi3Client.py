import grovepi
import math
from time import sleep
import datetime
from multiprocessing import Process
import requests

sensor = 4  # The Sensor goes on digital port 4.
sound_sensor = 0

blue = 0  # The Blue colored sensor.
minutes = 10
sleeptimer = 60 * minutes
mintemp = 17
maxtemp = 28
minhum = 30
maxhum = 50

maxsound = 800

celcius = True

current_time = datetime.datetime.now()
hour = current_time.hour + 1

starttime = 8
endtime = 14

url = 'http://192.168.1.114:8000/data/opretmaalinger/'
head = {'Authorization': 'Token d2b6345c35b8d0a8b7116e5109076832012e760b'}


def get_sound():
    soundwarning = ''
    while True:
        sound_level = grovepi.analogRead(sound_sensor)
        sleep(0.5)
        print(sound_level)
        if (sound_level > maxsound and hour >= endtime or sound_level > maxsound and hour <= starttime):
            [temp, humidity] = grovepi.dht(sensor, blue)
            soundwarning = 'to loud outisde office hours'
            r = requests.post(url, headers=head,
                              json={"tempratur": temp, "luftfugtighed": humidity, "advarsel": soundwarning,
                                    "alarm": True})
            print(temp, humidity)
            break
        elif (sound_level > maxsound):
            [temp, humidity] = grovepi.dht(sensor, blue)
            soundwarning = 'to noisy'
            print(soundwarning)
            soundwarning = ''
            r = requests.post(url, headers=head,
                              json={"tempratur": temp, "luftfugtighed": humidity, "advarsel": soundwarning,
                                    "alarm": False})


def everything_else():
    tempwarning = ""
    humwarning = ""
    while True:
        if (starttime <= hour and endtime >= hour):
            try:
                # This example uses the blue colored sensor.
                # The first parameter is the port, the second parameter is the type of sensor.
                [temp, humidity] = grovepi.dht(sensor, blue)
                if (temp > maxtemp):
                    tempwarning = "temperature is too high "
                if (temp < mintemp):
                    tempwarning = "temperature is to low "
                if (humidity > maxhum):
                    humwarning = " humidity is too high"
                if (humidity < minhum):
                    humwarning = " humidity is too low"
                if (celcius == False):
                    fahrenheit = temp * 1.8 + 32
                    print("temp = %.02f F humidity =%.02f%%" % (fahrenheit, humidity))
                    print(tempwarning + " " + humwarning)
                    x = tempwarning + " " + humwarning + "."
                    r = requests.post(url, headers=head,
                                      json={"tempratur": temp, "luftfugtighed": humidity, "advarsel": x,
                                            "alarm": False})

                else:
                    print("temp = %.02f C humidity =%.02f%%" % (temp, humidity))
                    x = tempwarning + " " + humwarning + "."
                    print(x)
                    r = requests.post(url, headers=head,
                                      json={"tempratur": temp, "luftfugtighed": humidity, "advarsel": x,
                                            "alarm": False})
                    print(r.text)

                humwarning = ""
                tempwarning = ""
                sleep(sleeptimer)

            except IOError:
                print("Error")
        else:
            print('hi')
            sleep(sleeptimer)


if __name__ == '__main__':
    proc1 = Process(target=get_sound)
    proc1.start()

    proc2 = Process(target=everything_else)
    proc2.start()