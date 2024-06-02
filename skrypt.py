import numpy as np
from argparse import ArgumentParser
import os as os
import tkinter as tk


class Transformacje:
    
    
    def __init__(self, model: str="WGS84"):
        """
        Parameters
        ----------
        Parametry elipsoidy:
            a - duża półoś elipsoidy
            e2 - mimośród -((kwadrat promienia równikowego + kwadrat promienia południkowego)/kwadrat promienia równikowego) 
        """
            
        if model == "WGS84":
            self.a = 6378137.000
            self.e2 = 0.00669437999013
        elif model == "GRS80":
            self.a = 6378137.000
            self.e2 = 0.00669438002290
        elif model == "Krasowski":
            self.a = 6378245.000
            self.e2 = 0.00669342162296
        else:
            raise NotImplementedError(f"{model}  jest nieobsługiwalną elipsoidą - przykładowe elipsoidy WGS84, GRS80, Krasowski.")
    
    def dms(self, x):
        """
        Funkcja dms pozwala zamienić daną -FLOAT- z radianów na daną -STRING- w stopniach, minutach sekundach.
        Parameters
        ----------
        x : FLOAT
        [radiany.]
    
        Returns
        x: STR
        [dms] - stopnir, minuty, sekundy
        -------
    
        """
    
        sig = ' '
        if x < 0:
            sig = '-'
            x = abs(x)
        x = x * 180/np.pi
        d = int(x)
        m = int(60 * (x - d))
        s = (x - d - m/60)*3600
        if s > 59.999995:
            s = 0
            m = m + 1
        if m == 60:
            m = 0
            d = d + 1
        
        d = str(d)
        if len(d) == 1:
            d = "  " + d
        elif len(d) == 2:
            d = " " + d
        elif len(d) == 3:
            d = d
            
        if m < 10:
            m = str(m)
            m = "0" + m
            
        if s < 10:
            s = "%.5f"%s
            s = str(s)
            s= "0" + s
        else:
            s = ("%.5f"%s)
            
        x1=(f'{d}°{m}′{s}″')  
        return(x1)
            
    def Np(self, f):
        """
        Funkcja oblicz promień przekroju w pierwszym wertykale. Jest niezbędna do wykonania się algorytmu hirvonena 
        oraz funkcji: flh2XYZ, flh2PL92, flh2PL00
        
        Parameters
        ----------
        f : FLOAT
        [radiany] - szerokość geodezyjna
        
        Returns
        -------
        N : float
        [metry] - promień przekroju w pierwszym wertykale
        
        -------
        """
    
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        return(N)
        
        
    def hirvonen(self, X, Y, Z, output="dec_degree"):
        """
        Algorytm Hirvonena - algorytm służy do transformacji współrzędnych prostokątnych (ortokartezjańskich)
        x, y, z na współrzędne geodezyjne phi, lambda, h. Podczas tej procedury iteracyjnej możnna przeliczyć współrzędne
        do 1 mm dokładności
        Parameters
        ----------
        X : FLOAT
            Współrzędna w układzie ortokartezjańskim.
        Y : FLOAT
            Współrzędna w układzie ortokartezjańskim.
        Z : FLOAT
            Współrzędna w układzie ortokartezjańskim.
    
        Returns
        -------
        fi : FLOAT
             [stopnie dziesiętne] - szerokość geodezyjna.
        lam : FLOAT
             [stopnie dziesiętne] - długość geodezyjna.
         h : FLOAT
             [metry] - wysokość elipsoidalna
     
        """
            
    
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p * (1 - self.e2)))
        while True:
            N = Transformacje.Np(self, f)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - self.e2 * (N / (N+h)))))
            if np.abs(fp - f) < (0.000001/206265):
                break
        l = np.arctan2(Y, X)
        if output == "dec_degree":
            fi=(f*180/np.pi)
            lam=(l*180/np.pi)
            return (fi, lam, h)
        elif output == "dms":
            fi = Transformacje.dms(self, f)
            lam = Transformacje.dms(self, l)
            return (fi,lam,h) 
        elif output == 'radiany':
            fi=f
            lam=l
            return(f,l,h)
        else:
            raise NotImplementedError(f"{output} - output format not defined")
    
        
        
    def flh2XYZ(self, f, l, h):
        """
        Algorytm odwrotny do algorytmu Hirvonena - służy do transformacji współrzędnych geodezyjnych B, L, H na współrzędne 
        ortokartezjańskie x,y,z.
    
        Parameters
        ----------
        f : FLOAT
           [stopnie dziesiętne] - szerokość geodezyjna.
        l : FLOAT
           [stopnie dziesiętne] - długośc geodezyjna.
        h : FLOAT
           [metry] - wysokość elipsoidalna
    
        Returns
        -------
        X : FLOAT
            Współrzędna w układzie ortokartezjańskim.
        Y : FLOAT
            Współrzędna w układzie ortokartezjańskim.
        Z : FLOAT
            Współrzędna w układzie ortokartezjańskim.
        -------
    
        """
        
        f=np.radians(f)
        l=np.radians(l)
        N = Transformacje.Np(self, f)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f)
        return(X,Y,Z)
        
        
    def flh2PL1992(self, f, l):
        """
        Algorytm do przeliczania współrzędnych geodezyjnych do układu współrzędnych 1992. Jest to układ wsp. płaskich
        prostokątnych oparty na odwzorowaniu Gaussa-Krügera dla elipsoidy GRS80 w jednej dziesięciostopniowej strefie.
    
        Parameters
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna..
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.
    
        Returns
        -------
        X1992, Y1992 : FLOAT
            [metry] - współrzędne w układzie 1992
        """
    
        
            
        if l > 25.5 or l < 13.5:
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(l))} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
                
        if f > 55 or f < 48.9:
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(f))} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
                
        f = np.radians(f)
        l = np.radians(l)
        a2 = self.a**2
        b2 = a2 * (1 - self.e2)
        e_2 = (a2 - b2)/b2
        l0 = np.radians(19)
        dl = l - l0
        dl2 = dl**2
        dl4 = dl**4
        t = np.tan(f)
        t2 = t**2
        t4 = t**4
        n2 = e_2 * (np.cos(f)**2)
        n4 = n2 ** 2
        N = Transformacje.Np(self, f)
        e4 = self.e2**2
        e6 = self.e2**3
        A0 = 1 - (self.e2/4) - ((3*e4)/64) - ((5*e6)/256)
        A2 = (3/8) * (self.e2 + e4/4 + (15*e6)/128)
        A4 = (15/256) * (e4 + (3*e6)/4)
        A6 = (35*e6)/3072
        sigma = self.a * ((A0 * f) - A2 * np.sin(2*f) + A4 * np.sin(4*f) - A6 * np.sin(6*f))
        xgk = sigma + ((dl**2)/2) * N * np.sin(f) * np.cos(f) * (1 + ((dl**2)/12)*(np.cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (np.cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
        ygk = dl * N * np.cos(f) * (1 + (dl2/6) * (np.cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (np.cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
        x92 = xgk * 0.9993 - 5300000
        y92 = ygk * 0.9993 + 500000
        return(x92,y92)
        
        
    def flh2PL2000(self, f, l):
        """
        Algorytm do przeliczania współrzędnych geodezyjnych do układu współrzędnych 2000. Układ współrzędnych 2000 
        to układ współrzędnych płaskich prostokątnych, który powstał w wyniku odwzorowania Gaussa-Krügera dla elipsoidy 
        GRS80 w czterech trzystopniowych strefach o południkach osiowych 15°E, 18°E, 21°E i 24°E, 
        oznaczone odpowiednio numerami – 5, 6, 7 i 8.
        
        Parameters
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna.
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.
    
        Returns
        -------
        X2000, Y2000 : FLOAT
             [metry] - współrzędne w układzie 2000
    
        """
        
              
        if l >= 13.5 and l < 16.5:
            l0 = np.radians(15)
        elif l >= 16.5 and l < 19.5:
            l0 = np.radians(18)
        elif l >= 19.5 and l < 22.5:
            l0 = np.radians(21)
        elif l >= 22.5 and l <= 25.5:
            l0 = np.radians(24)
        else:
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(l))} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
            
        if f > 55 or f < 48.9:
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(f))} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
                
        f = np.radians(f)
        l = np.radians(l)
        a2 = self.a**2
        b2 = a2 * (1 - self.e2)
        e_2 = (a2 - b2)/b2
        dl = l - l0
        dl2 = dl**2
        dl4 = dl**4
        t = np.tan(f)
        t2 = t**2
        t4 = t**4
        n2 = e_2 * (np.cos(f)**2)
        n4 = n2 ** 2
        N = Transformacje.Np(self, f)
        e4 = self.e2**2
        e6 = self.e2**3
        A0 = 1 - (self.e2/4) - ((3*e4)/64) - ((5*e6)/256)
        A2 = (3/8) * (self.e2 + e4/4 + (15*e6)/128)
        A4 = (15/256) * (e4 + (3*e6)/4)
        A6 = (35*e6)/3072
        sigma = self.a * ((A0 * f) - A2 * np.sin(2*f) + A4 * np.sin(4*f) - A6 * np.sin(6*f))
        xgk = sigma + ((dl**2)/2) * N * np.sin(f) * np.cos(f) * (1 + ((dl**2)/12)*(np.cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (np.cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
        ygk = dl * N * np.cos(f) * (1 + (dl2/6) * (np.cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (np.cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
        strefa = round(l0 * 180/np.pi)/3
        x00 = xgk * 0.999923
        y00 = ygk * 0.999923 + strefa * 1000000 + 500000
        return(x00,y00)
    
        
    def dXYZ(self, xa, ya, za, xb, yb, zb):
        
        """
        Definicja ta oblicza macierz różnicy współrzędnych punktów A i B, która jest wymagana do wyliczenia macierzy neu
    
        Parameters
        ----------
        xa : FLOAT
            współrzędna w układzie ortokartezjańskim
        ya : FLOAT
            współrzędna w układzie ortokartezjańskim
        za : FLOAT
            współrzędna w układzie ortokartezjańskim
        xb : FLOAT
            współrzędna w układzie ortokartezjańskim
        yb : FLOAT
            współrzędna w układzie ortokartezjańskim
        zb : FLOAT
            współrzędna w układzie ortokartezjańskim
    
        Returns
        -------
        dXYZ : ARRAY
            macierz różnicy współrzędnych
    
        """
    
        dXYZ = np.array([xb-xa, yb-ya, zb-za])
        return(dXYZ)
        
        
    def Rneu(self, f, l):
        """
        Definicja ta tworzy macierz obrotu R, która wymagana jest do wyliczenia macierzy neu.
    
        Parameters
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna.
        l : FLOAT
            [stopnie dziesiętne] - długość geodezyjna.
    
        Returns
        -------
        R ARRAY
            macierz obrotu R
    
        """
        f=np.radians(f)
        l=np.radians(l)
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l),  np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f),             0,         np.sin(f)          ]])
        return(R)
        
        
    def xyz2neu(self, f, l, xa, ya, za, xb, yb, zb):
        
        """
        Algorytm służy do przeliczania współrzednych ortokartezjańskich do układu współrzędnych horyzontalnych.
        Układ współrzędnych horyzontalnych (neu), to układ wsp. astronomicznych, w którym główna oś to lokalny 
        kierunek pionu, a płaszczyzna podstawowa to płaszczyzna horyzontu astronomicznego. Zenit i nadir to bieguny układu.
        Ich położenie na sferze niebieskiej zależy od wsp geograficznych położenia obserwatora oraz momentu obserwacji 
        przez niego. Układ współrzędnych horyzontalnych to opis wyłącznie chwilowego położenia ciała.
    
        Parameters
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna.
        l : FLOAT
            [stopnie dziesiętne] - długość geodezyjna.
        xa : FLOAT 
            współrzędna w układzie ortokartezjańskim.
        ya : FLOAT 
            współrzędna w układzie ortokartezjańskim.
        za : FLOAT 
            współrzędna w układzie ortokartezjańskim.
        xb : FLOAT 
            współrzędna w układzie ortokartezjańskim.
        yb : FLOAT 
            współrzędna w układzie ortokartezjańskim.
        zb : FLOAT 
            współrzędna w układzie ortokartezjańskim.
    
        Returns
        -------
        n , e, u : STR
            współrzędne horyzontalne
    
        """
                  
        dX = Transformacje.dXYZ(self, xa, ya, za, xb, yb, zb)
        R = Transformacje.Rneu(self, f,l)
        neu = R.T @ dX
        n = neu[0];   e = neu[1];   u = neu[2]
        n = "%.16f"%n; e = "%.16f"%e; u="%.16f"%u
        dlugosc = []
        xx = len(n); dlugosc.append(xx)
        yy = len(e); dlugosc.append(yy)
        zz = len(u); dlugosc.append(zz)
        P = 50
        
        while xx < P:
            n = str(" ") + n
            xx += 1
        while yy < P:
            e = str(" ") + e
            yy += 1
                    
        while zz < P:
            u = str(" ") + u
            zz +=1
        return(n, e, u) 
    
    def wczytanie_pliku_z_zapisem(self, dane, output='dms', xyz_txt = 'wyniki_xyz.txt', flh_txt = 'wyniki_flh.txt', x1992_y1992_txt = 'wyniki_x1992_y1992.txt', x2000_y2000_txt = 'wyniki_x2000_y2000.txt', neu_txt= 'wyniki_neu.txt'):
        '''
        Funkcja wczytuje plik z Danymi X,Y,Z, a następnie tworzy listę posegregowanych X,Y,Z wykorzystując wyjsciowe dane.
        Następnie funkcja zapisuje wyniki obliczeń XYZ,FLH, X1992_Y1992, X2000_Y2000 tworząc z nich tabele w różnych plikach tekstowych.

        Parameters
        ----------
        dane : TYPE
            DESCRIPTION.
        output : str
            Sposób, w którym funkcja ma zapisywać współrzęde f oraz l [dms, radiany, dec_degree]. 
        xyz_txt : str
           Nazwa pliku z wynikami dla xyz.
        flh_txt : str
           Nazwa pliku z wynikami dla flh.
        x1992_y1992_txt : str
           Nazwa pliku z wynikami dla PL1992.    
        x2000_y2000_txt : str
           Nazwa pliku z wynikami dla PL2000.
        neu_txt : str
            Nazwa pliku z wynikami dla neu.
        Returns
        -------
        Plik txt

        '''
        with open(dane, "r") as plik:
            tab=np.genfromtxt(plik, delimiter=",", dtype = '<U20', skip_header = 4)
            X=[]
            Y=[]
            Z=[]
            for i in tab:
                x=i[0]
                X.append(float(x))
                y=i[1]
                Y.append(float(y))
                z=i[2]
                Z.append(float(z))
            ilosc_wierszy = len(X)
            F=[]
            L=[]
            H=[]
            X92=[]
            Y92=[]
            X00=[]
            Y00=[]
            N=[]
            E=[]
            U=[]    
        for x,y,z in zip (X,Y,Z):
            f,l,h = Transformacje.hirvonen(self, x, y, z, output = output)
            if output == "dms":
                F.append(f)
                L.append(l)
            elif output == "radiany":
                f=Transformacje.f2s_rad(self,f)
                l=Transformacje.f2s_rad(self,l)
                F.append(f)
                L.append(l)
            else:
                f=Transformacje.f2s_fl(self,f)
                l=Transformacje.f2s_fl(self,l)
                F.append(f)
                L.append(l)
            H.append(Transformacje.f2s(self, h))
            f,l,h = Transformacje.hirvonen(self, x, y, z)
            
            if l >= 13.5 and l <= 25.5 and f <= 55.0 and f >= 48.9:
                x92, y92 = Transformacje.flh2PL1992(self, f,l)
                X92.append(Transformacje.f2s(self, x92))
                Y92.append(Transformacje.f2s(self, y92))
                x00, y00 = Transformacje.flh2PL2000(self, f,l)
                X00.append(Transformacje.f2s(self, x00))
                Y00.append(Transformacje.f2s(self, y00))
            else:
                x92 = "         '-'         " ; X92.append(x92)
                y92 = "         '-'         " ; Y92.append(y92)
                x00 = "         '-'         " ; X00.append(x00)
                y00 = "         '-'         " ; Y00.append(y00)
                
        f1, l1, h1 = Transformacje.hirvonen(self, X[0], Y[0], Z[0])
        n1, e1, u1 = Transformacje.xyz2neu(self, f1, l1, X[0], Y[0], Z[0], X[-1], Y[-1], Z[-1])
        N.append(n1)
        E.append(e1)
        U.append(u1)
        
        i=0
        while i<(ilosc_wierszy-1):
            f, l, h = Transformacje.hirvonen(self, X[i], Y[i], Z[i])
            n, e, u = Transformacje.xyz2neu(self, f, l, X[i], Y[i], Z[i], X[i+1], Y[i+1], Z[i+1])
            N.append(n)
            E.append(e)
            U.append(u)
            i+=1 
            
        for i in range(len(X)):
            X[i] = Transformacje.f2s(self, X[i])
            Y[i] = Transformacje.f2s(self, Y[i])
            Z[i] = Transformacje.f2s(self, Z[i])
        
        with open(xyz_txt , "w",  encoding="utf-8") as plik:
            plik.write(f"Zestawienie wyników obliczeń geodezyjnych: X, Y, Z\n")
            plik.write("-"*67)
            plik.write(f"\n")
            plik.write(f"|         X          |          Y          |          Z          |")
            plik.write(f"\n")
            plik.write("-"*67)
            plik.write(f"\n")
            for x, y, z in zip(X, Y, Z):
                plik.write(f"|{x}|{y}|{z}|")
                plik.write(f"\n")
            plik.write("-"*67)
            
        with open(flh_txt , "w",  encoding="utf-8") as plik:
            plik.write(f"Zestawienie wyników obliczeń geodezyjnych:  f, l, h\n")
            plik.write("-"*67)
            plik.write(f"\n")
            plik.write(f"|          fi         |        lambda       |          h          |")
            plik.write(f"\n")
            plik.write("-"*67)
            plik.write(f"\n")
            for  f, l, h in zip(F, L, H):
                plik.write(f"|     {f}|     {l}|{h}|")
                plik.write(f"\n")
            plik.write("-"*67)
            
        with open(x1992_y1992_txt , "w",  encoding="utf-8") as plik:
            plik.write(f"Zestawienie wyników obliczeń geodezyjnych: x1992, y1992\n")
            plik.write(f"Znak '-' w zestawieniu współrzędnych geodezyjnych (X1992, Y1992) oznacza to, że dla podanych X, Y, Z po obliczeniu współrzędnych geodezyjnych fi oraz lambda nie są akceptowalne w standardowych układach współrzędnych geodezyjnych układów PL1992.\n")
            plik.write("-"*45)
            plik.write(f"\n")
            plik.write(f"|        x1992        |        y1992        |")
            plik.write(f"\n")
            plik.write("-"*45)
            plik.write(f"\n")
            for x92, y92 in zip(X92, Y92):
                plik.write(f"|{x92}|{y92}|")
                plik.write(f"\n")
            plik.write("-"*45)
        
        with open(x2000_y2000_txt , "w",  encoding="utf-8") as plik:
            plik.write(f"Zestawienie wyników obliczeń geodezyjnych:x2000, y2000.\n")
            plik.write(f"Znak '-' w zestawieniu współrzędnych geodezyjnych (X2000, Y2000) oznacza to, że dla podanych X, Y, Z po obliczeniu współrzędnych geodezyjnych fi oraz lambda nie są akceptowalne w standardowych układach współrzędnych geodezyjnych układów PL2000.\n")
            plik.write("-"*45)
            plik.write(f"\n")
            plik.write(f"|        x2000        |        y2000        |")
            plik.write(f"\n")
            plik.write("-"*45)
            plik.write(f"\n")
            for x00, y00 in zip(X00, Y00):
                plik.write(f"|{x00}|{y00}|")
                plik.write(f"\n")
            plik.write("-"*45)
            
        
        with open(neu_txt , "w", encoding="utf-8") as plik1:
            plik1.write(f"Wyniki n, e, u:.\n")
            plik1.write("-"*154)
            plik1.write(f"\n")
            plik1.write(f"|                        n                         |                        e                         |                        u                         |")
            plik1.write(f"\n")
            plik1.write("-"*154)
            plik1.write(f"\n")
            for n, e, u in zip(N, E, U):
                plik1.write(f"|{n}|{e}|{u}|")
                plik1.write(f"\n")
            plik1.write("-"*154)
            
    def f2s_rad(self, liczba):
        '''
        Konwertuje liczby zmiennoprzecinkowe [float] na ciągi znaków [string], zachowując precyzję 
        odpowiednią dla jednostki radianów. Celem jest estetyczne zapisanie wyników w pliku wyjściowym.

        Parameters
        ----------
        liczba : FLOAT
            Liczba w radianach.

        Returns
        -------
        liczba : STR
            string z okreloną stała iloscia znaków

        '''
        zm_liczba = "%.12f"%liczba
        P = 16
        xx = len(zm_liczba)
        while xx < P:
            zm_liczba = str(" ") + zm_liczba
            xx += 1
        return(zm_liczba)  

    
    def f2s_fl(self, liczba):
        '''
        Przekształca liczby zmiennoprzecinkowe [float] na ciągi znaków [string] z odpowiednią precyzją, 
        zgodną z formatem stopni dziesiętnych. Cel jest taki, aby wyniki były czytelnie zapisane w pliku wynikowym.

        Parameters
        ----------
        liczba : FLOAT
            Liczba w stopniach dziesiętnych.

        Returns
        -------
        liczba : STR
            string z okreloną stała iloscia znaków

        '''
        zm_liczba = "%.10f"%liczba
        P = 16
        xx = len(zm_liczba)
        while xx < P:
            zm_liczba = str(" ") + zm_liczba
            xx += 1
        return(zm_liczba)        
    
    
    def f2s(self, liczba):
        '''
        Konwersja z liczb zmiennoprzecinkowych [float] na ciągi znaków [string] z dokładnością odpowiadającą 
        wymogom formatu stopni, minut i sekund (dms). Proces ten ma na celu estetyczne zapisanie 
        wyników w pliku wyjściowym.

        Parameters
        ----------
        liczba : FLOAT
            Liczba w dms.

        Returns
        -------
        liczbe : STR
            string z okreloną stała ilością znaków


        '''
        zm_liczba = "%.3f"%liczba
        P = 21
        xx = len(zm_liczba)
        while xx < P:
            zm_liczba = str(" ") + zm_liczba
            xx += 1
        return(zm_liczba)
    
    def zapis_danych_v2(self, xyz_txt, x, y, z, output = "dms"):
        '''
        Generowanie pliku tekstowego z danymi wprowadzanymi do narzędzia Kalkulatora, 
        które przekształcają te dane na współrzędne geodezyjne w układach PL2000, PL1992, oraz formaty xyz i flh

        Parameters
        ----------
        xyz_txt : STR
            PLIK TXT
        X, Y, Z : FLOAT
             [metry] - współrzędne w układzie ortokartezjańskim,
        f : FLOAT
             [stopnie dziesiętne] - szerokość geodezyjna.
        l : FLOAT
             [stopnie dziesiętne] - długość geodezyjna.
        h : FLOAT
             [metry] - wysokość elipsoidalna
        X1992, Y1992 : FLOAT
             [metry] - współrzędne w układzie 1992
        X2000, Y2000 : FLOAT
             [metry] - współrzędne w układzie 2000
        output : TYPE, optional
            DESCRIPTION. The default is "dms".

        Returns
        -------
        Plik txt

        '''
        f,l,h = Transformacje.hirvonen(self, x, y, z, output = output)
            
        if output == "dms":
            f=f
            l=l
        elif output == "radiany":
            f=Transformacje.f2s_rad(self,f)
            l=Transformacje.f2s_rad(self,l)
        else:
            f=Transformacje.f2s_fl(self,f)
            l=Transformacje.f2s_fl(self,l)
        h = Transformacje.f2s(self, h)
        F,L,H = Transformacje.hirvonen(self, x, y, z)
        
        if L >= 13.5 and L <= 25.5 and F <= 55.0 and F >= 48.9:
            x92, y92 = Transformacje.flh2PL1992(self, F,L)
            x92 = Transformacje.f2s(self, x92)
            y92 = Transformacje.f2s(self, y92)
            x00, y00 = Transformacje.flh2PL2000(self, F,L)
            x00 = Transformacje.f2s(self, x00)
            y00 = Transformacje.f2s(self, y00)
        else:
            x92 = "         '-'         " 
            y92 = "         '-'         " 
            x00 = "         '-'         "
            y00 = "         '-'         "
        x = Transformacje.f2s(self, x)
        y = Transformacje.f2s(self, y)
        z = Transformacje.f2s(self, z)
        
        if not os.path.exists(xyz_txt):
            with open(xyz_txt, "w", encoding="utf-8") as plik:
                plik.write(f"Zestawienie wyników obliczeń geodezyjnych: X, Y, Z, fi, lambda, h, X1992, Y1992, X2000, Y2000.\n")
                plik.write(f"Znak '-' w zestawieniu współrzędnych geodezyjnych (X1992, Y1992, X2000, Y2000) oznacza to, że dla podanych X, Y, Z po obliczeniu współrzędnych geodezyjnych fi oraz lambda nie są akceptowalne w standardowych układach współrzędnych geodezyjnych układów PL1992, PL2000.\n")
                plik.write("-"*221)
                plik.write(f"\n")
                plik.write(f"||          X          |          Y          |          Z          |          fi         |        lambda       |          h          |        x1992        |        y1992        |        x2000        |        y2000        |")
                plik.write(f"\n")
                plik.write("-"*221)
                plik.write(f"\n")
                plik.write(f"||{x}|{y}|{z}|     {f}|     {l}|{h}|{x92}|{y92}|{x00}|{y00}|")
                plik.write(f"\n")
                plik.write("-"*221)
                plik.write(f"\n")
        else:
            with open(xyz_txt, "a", encoding="utf-8") as plik:
                plik.write(f"||{x}|{y}|{z}|     {f}|     {l}|{h}|{x92}|{y92}|{x00}|{y00}|")
                plik.write(f"\n")
                plik.write("-"*221)
                plik.write(f"\n")
    
if __name__ == "__main__":
    mod =Transformacje("WGS84")
    mod.wczytanie_pliku_z_zapisem("input_file.txt")
  
        
