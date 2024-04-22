import math
import numpy as np
import sys
python skrypt input.txt output.txt
class skoordynowane_transformacje:
    def __init__(self):
        pass
# self- instancja klasy, input-plik wejsciowy, output-wyjsciowy plik
def process_coordinates_file(self, input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    output_lines = []
    for line in lines:
        coordinates = line.strip().split()
        if len(coordinates) != 3:
            print("Niepoprawna liczba współrzędnych w linii:", line)
            continue
        try:
            X, Y, Z = map(float, coordinates)
        except ValueError:
            print("Niepoprawny format współrzędnych w linii:", line)
            continue
        fi, lon, h = self.XYZ2flh(X, Y, Z)
        output_lines.append(f"{fi} {lon} {h}\n")

    with open(output_file, 'w') as f:
        f.writelines(output_lines)

        
def XYZ2flh(X, Y, Z, a = 6378137,e2 = 0.00669438002290):
    """
    
    Funkcja służy do przeliczenia współrzędnych kartezjańskich
    na współrzędne geocentryczne(długosć, szerokosć, wysokosć)
    Parameters
    ----------
    X : float
        Wspórzędna X w metrach.
    Y : float
        Wspórzędna Y w metrach.
    Z : float
        Wspórzędna Z w metrach.
    a : int
        Stała o wartosci 6378137.
    e2 : float
        Stała o wartosci 0.00669438002290.

    Returns:
        tuple: Krotka zawierające współrzędne
        geocentryczne ( długosć, szerokosć, wysokosć)

    """
    l = np.arctan2(Y,X)
    p = np.sqrt(X**2 + Y**2)
    f = np.arctan(Z/ (p*(1-e2)))
    while True:
        def Np(f,a,e2):
            N = a / np.sqrt((1- e2 * np.sin(f)**2))
            return(N)
        N = Np(f, a, e2)
        h = p/ np.cos(f) - N
        fs = f #f stare
        f = np.arctan(Z/ (p*(1-(e2*(N/(N+h))))))
        if np.abs(fs-f)<(0.000001/206265):
            break
    return(f,l,h)

if __name__ == "__main__":
    transformer = skoordynowane_transformacje()
    
    if len(sys.argv) != 3:
        print("źle")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    transformer.process_coordinates_file(input_file,output_file)