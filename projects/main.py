#python Alarm clock
import time
import datetime
import pygame

def set_alarm(alarm_time):
    print(f"Alarm set for {alarm_time} ")
    sound_file = "C:/Users/USER/OneDrive/Desktop/studying/python/py/Baby_Cry_Long.mp3"
    is_runnig = True

    while is_runnig:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)

        if current_time == alarm_time:
            print("WAKE UP 💤")
            is_runnig = False

        time.sleep(1)



if __name__ =="__main__":
    alarm_time = input ("Enter the alarm time (HH:MM:SS): ")
    set_alarm(alarm_time)
