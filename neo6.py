#/usr/bin/python3
#-*- coding: utf-8 -*-

import serial
try:
    from geopy.geocoders import Nominatim
    geo=True
except:
    geo=False


class GpsNeo6():
    """
        class de gestion du soc NEO 6M
        """

    
    def __init__(self,port,debit=9600,diff=1):
        """
            on initialise les variables a partir de:
            port: port com
            debit: vitesse en bauds
            diff: differece heure local et utc
            """
        self.port=serial.Serial(port,debit)
        self.diff=diff
        self.tabCode=["GPVTG","GPGGA","GPGSA","GPGLL","GPRMC","GPGSV"]
        self.vitesse=""
        self.latitude=""
        self.longitude=""
        self.latitudeDeg=""
        self.longitudeDeg=""
        self.time=""
        self.altitude=""
        self.precision=""
        self.satellite=""
        self.geoloc=Nominatim()
        
    def __del__(self):
        """
            on ferme le port a la destruction de l'objet
            """
        self.port.close()
        
    def __repr__(self):
        """
            on affiche les info
            """
        rep="heure: "+str(self.time)+"\rlatitude: "+str(self.latitude) \
            +"\rlongitude: "+str(self.longitude)+"\rvitesse: "+str(self.vitesse)+" km/h" \
            +"\raltitude: "+str(self.altitude)+" metre(s)"+"\rprecision: "+str(self.precision)+" metre(s)" \
            +"\rNombre de satelites vue: "+str(self.satellite)
        if geo:
            rep+="\rlieu : "+self.geolocation()
        return rep
    
    
    
    def recupData(self):
        """
            on recupere les datas sur le port serie
            """
        l='->'
        ligne=""
        tab={}
        gp=[]
        while len(tab)<6:
            l=self.port.read(2)
            if b'\r' in l or b'\n' in l:
                l=''
                for i in self.tabCode:
                    if i in ligne:
                        if i=="GPGSV": 
                            gp.append(ligne)
                            tab["GPGSV"]=gp
                        else:                     
                            tab[i]=ligne
                            gp=[]
                ligne=""
            else: 
                try:
                    ligne+=str(l.decode().strip())
                except: pass
        return tab
    
    def degToDec(self,deg):
        """
            fonction de tronsformation des coordonees en degre vers les degre decimals
            """
        dec=int(deg[0:deg.find(".")-2])
        min=int(deg[deg.find(".")-2:deg.find(".")])/60
        sec=float("0."+deg[deg.find(".")+1:])/36
        return round(dec+min+sec,10)
    
    
    def traite(self):
        """
            on traite les donnes pour les mettres en formes
            """
        donnees=self.recupData()
        data=donnees["GPGGA"]
        data=data.split(',')
        temps=str(int(data[1][0:2])+self.diff)+"h"+data[1][2:4]+"m"+data[1][4:6]+"s" #mets en forme la date avec le decalage de l'heure        
        self.time=temps
        self.latitude=self.degToDec(data[2]) #mets au format decimale xx.yyyyyy
        self.latitudeDeg=float(data[2])/100#+data[3]
        self.longitude=self.degToDec(data[4]) #mets au format decimale xx.yyyyyy
        self.longitudeDeg=float(data[4])/100#+data[5]
        self.altitude=data[9]
        self.precision=data[6]
        self.vitesse=self.traiteGPVTG(donnees["GPVTG"]) #recupere que la vitesse de deplacement
        self.satellite=int(donnees["GPGSV"][0].split(',')[3]) #recupere le nombre de satellite vue
        
        
        
    def traiteGPVTG(self,data):
        """
            on traite les donnees pour la vitesse
            """
        data=data.split(',')
        return data[7]
    
    def geolocation(self):
        """
            si on peut on geolocalise les coordonnees
            """
        if geo:
            try:
                
                location = self.geoloc.reverse(str(self.latitude)+", "+str(self.longitude))
                return str(location)
            except: return "Le Néant"
        else: return "le Néant"
        
    
    
if __name__=="__main__":
    #on definit le port la vitesse et la diferrence d'heure utc et locale
    gps=GpsNeo6(port="com5",debit=9600,diff=2)
    
    while True:
        #on appel un traitement gps
        gps.traite()
        #on affiche les infos
        print(gps)
        #print(gps.time)
        
