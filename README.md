# **Kalkulator geodezyjny**

**OPIS**

Program umożliwia przeliczenie współrzędnych geodezyjnych między układami BLH (współrzędne geodezyjne), XYZ (współrzędne ortokartezjańskie) [metry] oraz PL-1992 (współrzędne płaskie) [metry] i PL-2000 (współrzędne płaskie) [metry]. 

Przeliczenia są możliwe tylko dla elipsoid: [GRS80, WGS84, elipsoida Krasowskiego].

**WYMAGANIA**

- Python 3.11.5
- Biblioteki: numpy, argparse, os
  
**SYSTEM OPERACYJNY**

Program napisany jest dla systemu Windows. Został testowany na Windows11.

**INSTRUKCJA OBSŁUGI**

Program umożliwia przekształcanie współrzędnych geodezyjnych między różnymi układami odniesienia: XYZ na FLH, FLH na XYZ, FLH na układ PL-1992 oraz FLH na układ PL-2000, przy użyciu wcześniej zdefiniowanych elipsoid referencyjnych. Dane wejściowe i wyjściowe programu są obsługiwane w formacie zmiennoprzecinkowym (float).
Program pozwala na wczytanie współrzędnych z pliku tekstowego (input_file.txt), gdzie dane wejściowe to współrzędne X, Y, Z. Przetwarzanie tych danych generuje cztery pliki wynikowe zawierające odpowiednio współrzędne w układach XYZ, FLH, X1992Y1992 oraz X2000Y2000. Użytkownik ma możliwość wyboru interesującego go rezultatu i otwarcia odpowiedniego pliku tekstowego.

Sposób wprowadzenia współrzędnych: wprowadzanie ręczne (--input cmd). Aby uzyskać współrzędne przeliczone na wybrany przez nas układ musimy otworzyć w oknie cmd ścieżkę do folderu z naszym plikiem (przykład ścieżki: C:\Users\user\OneDrive\Pulpit\informatyka\projekt1) a następnie wpisać słowo „python” oraz nazwę naszego pliku (w tym przypadku plik: „kalkulator_xyz2reszta.py").

W następnym kroku, kontynuując zapis w tej samej linijce możemy wpisywać współrzędne FLH (wartości F oraz L wprowadzamy w stopniach dziesiętnych, natomiast H w metrach) dla transformacji BLH -> XYZ, BLH -> PL1992 oraz BLH -> PL2000.

**PRZYKŁAD**

Mamy także możliwość wyboru układu wprowadzanych przez nas współrzędnych, docelowego układu do którego chcemy przeliczyć nasze współrzędne oraz wyboru elipsoidy (spośród trzech wyżej wymienionych), a także wybrania pliku docelowego, do którego chcemy zapisać otrzymane wyniki.

- [-m] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
  
- [-xyz] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozszerzenia pliku - tak zostanie zapisany plik wynikowy.
  
- [-f, -l, -ha] - [stopnie dziesietne] - współrzędne geodezyjne elipsoidalne punktu, wysokość [metry].
  
- [-output] - [dms/dec_degree/radiany] - wybieramy w jakich jednostkach chcemy mieć wyniki.

Przykład:

python kalkulator_xyz2reszta.py -m GRS80 -xyz wyniki.txt -f 40 -l 50 -ha 54 -output dms

Wyniki: 

Współrzędne ortokartezjańskie geocentryczne [metry], współrzędne płaskie PL1992 [metry], współrzędne płaskie PL2000 [metry]. [x, y, z, h, x1992, y1992, x2000, y2000].

Otrzymujemy:

Elipsoida: GRS80

Wyniki dla transformacji flh2xyz: X = 3144998.413 [m], Y = 3748063.157 [m], Z = 4078020.283 [m]

Wyniki z transformacji flh2PL92 i flh2PL20: X1992 =  '-'  [m], Y1992 =  '-'  [m], X2000 =  '-'  [m], Y2000 =  '-'  [m]

To położenie nie jest obsługiwane przez układy współrzędnych płaskich PL1992 i PL2000

Nazwa pliku głównego: skrypt

Nasze wyniki zapisują się w pliku o nazwie "wyniki.txt".

**ZNANE BŁĘDY I NIETYPOWE ZACHOWANIA**

•	Program zwraca błąd w przypadku podania niepoprawnego modelu elipsoidy lub systemu współrzędnych.

•	Transformacja FLH -> PL-1992 oraz FLH ->PL-2000 dla elipsoidy Krasowskiego zwraca błędne wyniki, dlatego nie można ich używać (nie jesteśmy pewne, ale działając na kodach z zajęć Geodezja Wyższa I  uzyskujemy inne wyniki).

UWAGA! W końcowym etapie zauważyłyśmy, że nasz plik został błędnie nazwany. Powinien nosić nazwę "kalkulator_blh2reszta.py", a nie "kalkulator_xyz2reszta.py". Taka sytuacja może być myląca.
