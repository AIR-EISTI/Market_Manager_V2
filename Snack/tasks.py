import serial

from celery import shared_task


@shared_task
def badgeuse():
    ser = serial.Serial('/dev/ttyUSB0', timeout=60)
    buff = ""
    for i in range(10):
        s = ser.read(1).decode()
        if s == '\x02':
            print("Debut lecture")
        elif s == '\r':
            print(buff + "")
        elif s == '\n':
            pass
        elif s == '\x07':
            print("bouton")
        elif s == '\x1b':
            print("Fin lecture")
        else:
            buff = buff + s
    return buff
