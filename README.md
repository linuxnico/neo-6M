# neo-6M

Python 3 class for neo-6M GPS

# required:

geopy library if you want geolocalize your gps point

https://github.com/geopy/geopy

# use:

        from neo6 import GpsNeo6

        gps=GpsNeo6(port="/dev/ttyUSB0",debit=9600,diff=2) #diff is difference between utc time en local time    

        while True:

            gps.traite()
  
            print(gps) # print all info
  
            print(gps.latitude,gps.longitude)
  
