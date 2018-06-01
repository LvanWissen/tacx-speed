import RPi.GPIO as GPIO
import time
import collections

GPIO.setmode(GPIO.BCM)  # gpio pin numbering
SENSOR_PIN = 14

# Bike Settings
tire_circumference = 2.133  # in meter
resistance_level = 1

# Globals
rpm = 0
lastreading = 0.0
rev_readings = collections.deque(maxlen=10)

GPIO.setup(SENSOR_PIN, GPIO.IN)


def readState():
    return int(GPIO.input(SENSOR_PIN))


def countRPM(channel):
    global rpm
    global lastreading
    global rev_readings

    if int(GPIO.input(SENSOR_PIN)):

        reading = time.time()

        revtime = reading - lastreading
        rev_readings.append(revtime)

        lastreading = reading


def getSpeed():
    avg_rev = sum(rev_readings) / 10

    if avg_rev:  # return 0 if lastreading is 5 seconds ago
        if lastreading < (time.time() - 5):
            return 0

        speed = (tire_circumference / avg_rev) * 3.6

        rpm = int(60 / avg_rev)

        print("{speed} km/h ({rpm} RPM)".format(speed=round(speed, 2), rpm=rpm))

        return round(speed, 2)

    return 0


def calcPower(speed, resistance_level):
    """
    Power (watts) = slope x speed (km/h) + intercept

    Level   1       2       3       4       5       6       7       8       9       10
    Slope   3.73    5.33    6.87    8.27    10.07   11.4    13.13   14.4    15.93   17.73
    Intcpt  -28.67  -36.67  -43.33  -47.33  -66.33  -67.00  -83.67  -82.00  -89.67  -114.67


    """
    satoridata = [
        {
            'level': 1,
            'slope': 3.73,
            'intercept': -28.67
        },
        {
            'level': 2,
            'slope': 5.33,
            'intercept': -36.67
        },
        {
            'level': 3,
            'slope': 6.87,
            'intercept': -43.33
        },
        {
            'level': 4,
            'slope': 8.27,
            'intercept': -47.33
        },
        {
            'level': 5,
            'slope': 10.07,
            'intercept': -66.33
        },
        {
            'level': 6,
            'slope': 11.4,
            'intercept': -67.00
        },
        {
            'level': 7,
            'slope': 13.13,
            'intercept': -83.67
        },
        {
            'level': 8,
            'slope': 14.4,
            'intercept': -82.00
        },
        {
            'level': 9,
            'slope': 15.93,
            'intercept': -89.67
        },
        {
            'level': 10,
            'slope': 17.73,
            'intercept': -114.67
        }
    ]

    power = satoridata[resistance_level-1]['slope'] * speed + satoridata[resistance_level-1]['intercept']
    print(resistance_level, power)
    return max((0, round(power)))


if __name__ == "__main__":
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=countRPM, bouncetime=100)

    while True:
        getSpeed()
        time.sleep(1)
