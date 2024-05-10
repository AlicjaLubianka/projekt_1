# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:22:23 2024

@author: Magda
"""

from argparse import ArgumentParser
import skrypt 
from skrypt import Transformacje

parser = ArgumentParser()
parser.add_argument('-m', '--m', type=str, help="Wskaż elipsoidę GRS80, WGS84, Krasowski")
parser.add_argument('-xyz', '--xyz', type=str, help="Podaj nazwe pliku wynikiowego dla kalkulatora z rozszerzeniem txt")
parser.add_argument('-f', '--f', type=float)
parser.add_argument('-l', '--l', type=float)
parser.add_argument('-ha', '--ha', type=float)
parser.add_argument('-output', '--output', type=str, help="Podaj rodzaj jednostki")

args = parser.parse_args()

mod = Transformacje(model = args.m)

print("")
print("")
print("Elipsoida:", args.m)
x, y, z = mod.flh2XYZ(args.f, args.l, args.ha)
print(f"Wyniki dla transformacji flh2xyz: X = {x:^.3f} [m], Y = {y:^.3f} [m], Z = {z:^.3f} [m]")
if args.l >= 13.5 and args.l <= 25.5 and args.f <= 55.0 and args.f >= 48.9:
    x92, y92 = mod.flh2PL1992(args.f,args.l)
    x00, y00 = mod.flh2PL2000(args.f,args.l)
    print(f"Wyniki dla transformacji flh2PL92 i flh2PL00: X1992 = {x92:^.3f} [m], Y1992 = {y92:^.3f} [m], X2000 = {x00:^.3f} [m], Y2000 = {y00:^.3f} [m]")
else:
    x92 = " '-' " 
    y92 = " '-' " 
    x00 = " '-' " 
    y00 = " '-' " 
    print(f"Wyniki z transformacji flh2PL92 i flh2PL20: X1992 = {x92} [m], Y1992 = {y92} [m], X2000 = {x00} [m], Y2000 = {y00} [m]")
    print("To położenie nie jest obsługiwane przez układy współrzędnych płaskich PL1992 i PL2000")

print("Nazwa pliku głównego:", skrypt.__name__)
print("")
print("")

mod.zapis_danych_v2(args.xyz, x, y, z, output = args.output)
