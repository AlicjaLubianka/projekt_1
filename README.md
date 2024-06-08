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
   
2. Następnie użytkownik podaje flagę "-i", która umożliwia pobrać dane z pliku wejściowego zawierającego współrzędne do przekształcenia.

       python skrypt.py -i input_file.txt
   
3. Kolejno należy użyć flagi "-t", która umożliwia wybór transformacji, którą chcemy dokonać.

   
- transformacja ze współrzędnych X,Y,Z do współrzędnych fi, lambda, wysokość(hirvonen):

       python skrypt.py -i input_file.txt -t hirvonen
  
- transformacja ze współrzędnych fi, lambda, wysokość do wspołrzędnych X,Y,Z:

       python skrypt.py -i input_file.txt -t flh2XYZ
  
- transformacja ze współrzędnych fi, lambda do układu PL1992:

       python skrypt.py -i input_file.txt -t flh2PL1992
  
- transformacja ze współrzędnych fi, lambda do układu PL2000:

        python skrypt.py -i input_file.txt -t flh2PL2000
  
- transformacja ze współrzędnych X,Y,Z do układu NEU:
  
        python skrypt.py -i input_file.txt -t xyz2neu

4. Kolejnym krokiem jest użycie flagi "-o", w której uwzględniamy plik wejściowy o formacie .txt ze współrzędnymi. Plik ten powinien znajdować się na komputerze w folderze z plikiem skrypt.py.

        python skrypt.py -i input_file.txt -t flh2PL1992 -o output_file.txt

5. Na koniec użytkownik jest proszony o podanie powierzchni odniesienia za pomocą flagi "-m" - do wyboru są: elipsoida WGS84, GRS80 i Krasowskiego.

        python skrypt.py -i input_file.txt -t flh2PL1992 -o output_file.txt -m GRS80

        python skrypt.py -i input_file.txt -t flh2PL1992 -o output_file.txt -m WRS84

        python skrypt.py -i input_file.txt -t flh2PL1992 -o output_file.txt -m Krasowski

UWAGA!
Aby przeprowadzić transformację xyz2neu, należy podać współrzędne orto-kartezjańskie punktu referencyjnego (xa, ya, za) oraz punktu, który ma zostać przekształcony (xb, yb, zb). Format pliku tekstowego powinien wyglądać następująco:

9876543.210,1234567.890,2345678.910,9876544.211,1234568.891,2345679.911

Współrzędne muszą być rozdzielone przecinkami, a plik nie powinien zawierać żadnych innych danych. Aby dodać kolejny punkt do obliczeń, należy umieścić go w nowym wierszu. Zarówno dane wejściowe, jak i wyjściowe programu powinny być w formacie zmiennoprzecinkowym (float).

Przykład danych wejściowych w pliku tekstowym:

3664940.500,1409153.590,5009571.170
3664940.510,1409153.580,5009571.167
3664940.520,1409153.570,5009571.167
3664940.530,1409153.560,5009571.168
3664940.520,1409153.590,5009571.170
3664940.514,1409153.584,5009571.166
3664940.525,1409153.575,5009571.166
3664940.533,1409153.564,5009571.169
3664940.515,1409153.590,5009571.170
3664940.514,1409153.584,5009571.169
3664940.515,1409153.595,5009571.169
3664940.513,1409153.584,5009571.171

W przypadku transformacji FLH na PL-2000 lub PL-1992 należy podać jedynie wartości F i L.

Jednostki:

-Współrzędne XYZ: w metrach

-Współrzędne elipsoidalne FL: w stopniach dziesiętnych
-H: w metrach

Po transformacji uzyskujemy wyniki w postaci:

-Współrzędnych XYZ: w metrach

-Współrzędnych elipsoidalnych FL: w stopniach, minutach i sekundach

-H: w metrach

**ZNANE BŁĘDY I NIETYPOWE ZACHOWANIA**

•	Program zwraca błąd w przypadku podania niepoprawnego modelu elipsoidy lub systemu współrzędnych. Model elipsoidy Krasowskiego nie działa poprawnie. 

•	Transformacja FLH -> PL-1992 oraz FLH ->PL-2000 zwraca błędne wyniki, dlatego nie można ich używać (nie jesteśmy pewne, ale działając na kodach z zajęć Geodezja Wyższa I  uzyskujemy inne wyniki).

•	Błąd w przypadku transformacji XYZ -> BLH: Program zwraca błąd dla transformacji XYZ -> BLH w przypadku podania współrzędnych X=0 Y=0, dla których nie jest możliwe jednoznaczne określenie współrzędnych w układzie BLH.
