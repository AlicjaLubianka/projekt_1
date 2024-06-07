# **Kalkulator geodezyjny**

**OPIS**

Program umożliwia przeliczenie współrzędnych geodezyjnych między układami FLH (współrzędne geodezyjne), XYZ (współrzędne ortokartezjańskie) [metry], PL-1992 (współrzędne płaskie) [metry], PL-2000 (współrzędne płaskie) [metry] oraz NEU (topocentryczne) [metry]. 

Przeliczenia są możliwe tylko dla elipsoid: [GRS80, WGS84, elipsoida Krasowskiego].

**WYMAGANIA**

- Python 3.11.5
- Biblioteki: numpy, argparse, os
  
**SYSTEM OPERACYJNY**

Program napisany jest dla systemu Windows. Został testowany na Windows11.

**INSTRUKCJA OBSŁUGI**

Program umożliwia przekształcanie współrzędnych geodezyjnych między różnymi układami odniesienia: XYZ na FLH (hirvonen), FLH na XYZ, XYZ na NEU FLH na układ PL-1992 oraz FLH na układ PL-2000, przy użyciu wcześniej zdefiniowanych elipsoid referencyjnych.

1. Program operuje w terminalu i korzysta z podawania określonych flag. Każde użycie rozpoczyna się od wpisania polecenia python, a następnie nazwy pliku programu - skrypt.py:

        python skrypt.py
   
3. Następnie użytkownik podaje flagę "-i", która umożliwia pobrać dane z pliku wejściowego zawierającego współrzędne do przekształcenia.

       python skrypt.py -i input_file
   
5. Kolejno należy użyć flagi "-t", która umożliwia wybór transformacji, którą chcemy dokonać.

   
- transformacja ze współrzędnych X,Y,Z do współrzędnych fi, lambda, wysokość(hirvonen):
        python skrypt.py -i input_file -t hirvonen
- transformacja ze współrzędnych fi, lambda, wysokość do wspołrzędnych X,Y,Z:
        python skrypt.py -i input_file -t flh2XYZ
- transformacja ze współrzędnych fi, lambda do układu PL1992:
        python skrypt.py -i input_file -t flh2PL1992
- transformacja ze współrzędnych fi, lambda do układu PL2000:
       python skrypt.py -i input_file -t flh2PL2000
- transformacja ze współrzędnych X,Y,Z do układu N,E,U
        python skrypt.py -i input_file -t xyz2neu


Dane wejściowe i wyjściowe programu są obsługiwane w formacie zmiennoprzecinkowym (float).



**ZNANE BŁĘDY I NIETYPOWE ZACHOWANIA**

•	Program zwraca błąd w przypadku podania niepoprawnego modelu elipsoidy lub systemu współrzędnych.

•	Transformacja FLH -> PL-1992 oraz FLH ->PL-2000 dla elipsoidy Krasowskiego zwraca błędne wyniki, dlatego nie można ich używać (nie jesteśmy pewne, ale działając na kodach z zajęć Geodezja Wyższa I  uzyskujemy inne wyniki).

UWAGA! W końcowym etapie zauważyłyśmy, że nasz plik został błędnie nazwany. Powinien nosić nazwę "kalkulator_blh2reszta.py", a nie "kalkulator_xyz2reszta.py". Taka sytuacja może być myląca.
