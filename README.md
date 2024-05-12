**OPIS**

Program umożliwia przeliczenie współrzędnych geodezyjnych między układami BLH (współrzędne geodezyjne), XYZ (współrzędne ortokartezjańskie) [metry] oraz PL-1992 (współrzędne płaskie) [metry] i PL-2000 (współrzędne płaskie) [metry]. 

Przeliczenia są możliwe tylko dla elipsoid: [GRS80, WGS84, elipsoida Krasowskiego].

**WYMAGANIA**

- Python 3.11.5
- Biblioteki: numpy, argparse, os
  
**SYSTEM OPERACYJNY**

Program napisany jest dla systemu Windows. Został testowany na Windows11.

**INSTRUKCJA OBSŁUGI**

Program umożliwia  transformację FLH -> XYZ, FLH->PL1992, FLH->PL2000 dla wcześniej podanych elipsoid. Dane wejściowe i wyjściowe programu są obsługiwane w formacie zmiennoprzecinkowym (float).
Należy skorzystać z opcji wprowadzania ręcznego (input txt) dla wprowadzenia współrzędnych.

Aby uzyskać współrzędne przeliczone na wybrany przez nas układ odniesienia, musimy otworzyć w wierszu poleceń (cmd) ścieżkę do folderu zawierającego nasz plik (przykładowa ścieżka: C:\Users\user \Pulpit\informatyka\projekt1), a następnie wpisać słowo „python” oraz nazwę naszego pliku (w tym przypadku plik: „wyniki.txt”).

W następnym kroku, kontynuując zapis w tej samej linijce możemy wpisywać współrzędne FLH (wartości F oraz L wprowadzamy w stopniach dziesiętnych, natomiast H w metrach).

**PRZYKŁAD**

python kalkulator_xyz2reszta.py -m GRS80 -xyz wyniki.txt -f 40 -l 50 -ha 54 -output dms

- [-m] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
  
- [-xyz] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozszerzenia pliku - tak zostanie zapisany plik wynikowy.
  
- [-f, -l, -ha] - [stopnie dziesietne] - współrzędne geodezyjne elipsoidalne punktu, wysokość [metry].
  
- [-output] - [dms/dec_degree/radiany] - wybieramy w jakich jednostkach chcemy mieć wyniki.
  
Wyniki: Współrzędne ortokartezjańskie geocentryczne [metry], współrzędne płaskie PL1992 [metry], współrzędne płaskie PL2000 [metry]. [x, y, z, h, x1992, y1992, x2000, y2000].

**ZNANE BŁĘDY I NIETYPOWE ZACHOWANIA**

•	Program zwraca błąd w przypadku podania niepoprawnego modelu elipsoidy lub systemu współrzędnych.

•	Transformacja FLH -> PL-1992 oraz FLH ->PL-2000 dla elipsoidy Krasowskiego zwraca błędne wyniki, dlatego nie można ich używać (nie jesteśmy pewne, ale działając na kodach z zajęć Geodezja Wyższa I  uzyskujemy inne wyniki).

UWAGA! W końcowym etapie zauważyłyśmy, że nasz plik został błędnie nazwany. Powinien nosić nazwę "kalkulator_blh2reszta.py", a nie "kalkulator_xyz2reszta.py". Taka sytuacja może być myląca.
