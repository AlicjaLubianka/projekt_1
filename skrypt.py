import math
import numpy as np
import sys
class skoordynowane_transformacje:
    def __init__(self):
        pass
def process_coordinates_file(self, input_file, output_file):
    try:
        with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
            for line in f_input:
                # Rozdziel linię na poszczególne wartości
                coordinates = line.strip().split()
                
                # Przelicz współrzędne XYZ na BLH
                X, Y, Z = map(float, coordinates)
                fi, lon, h = XYZ2flh(X, Y, Z)
                
                # Zapisz wyniki do pliku wyjściowego
                f_output.write(f"{fi} {lon} {h}\n")
        print("Pomyślnie przetworzono i zapisano wyniki do pliku:", output_file)
    except FileNotFoundError:
        print("Nie można odnaleźć pliku wejściowego:", input_file)
    except Exception as e:
        print("Wystąpił błąd podczas przetwarzania pliku:", str(e))
        
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
    # Przykładowe wywołanie transformacji XYZ -> BLH
    transformer = skoordynowane_transformacje()
    X = 4070605.089
    Y = 931621.785
    Z = 4801509.052
    fi, lon, h = XYZ2flh(X, Y, Z)
    print("Współrzędne geograficzne (fi, lambda, h):", fi, lon, h)

    if len(sys.argv) != 3:
        print("Sposób użycia: python main.py plik_wejsciowy.txt plik_wyjsciowy.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    transformer.process_coordinates_file(input_file, output_file)