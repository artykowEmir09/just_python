#python threading
import threading
import time

def walk_dog():
    time.sleep(8)
    print("You finish walking the dog ")

def take_out_trash():
    time.sleep(2)
    print("You take out the trash")

def get_mail():
    time.sleep(4)
    print("You get the mail")

walk_dog() 
take_out_trash()
get_mail()