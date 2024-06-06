# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 21:53:02 2024

@author: Ala
"""

from argparse import ArgumentParser
import skrypt 
from skrypt import Transformacje

parser = ArgumentParser()


parser.add_argument('mode', choices=['hirvonen', 'FLH2XYZ', 'flh2PL1992','xyz2neu', 'flh2PL2000'], help="Wybierz tryb 'hirvonen' lub 'FLH2XYZ'")
parser.add_argument('-m', '--m', type=str, help="Wskaż elipsoidę GRS80, WGS84, Krasowski")

group_a = parser.add_argument_group('hirvonen', 'Argumenty dla trybu hirvonen')
group_a.add_argument('-x', type=float, help="Argument x dla trybu hirvonen")
group_a.add_argument('-y', type=float, help="Argument y dla trybu hirvonen")
group_a.add_argument('-z', type=float, help="Argument z dla trybu hirvonen")


group_b = parser.add_argument_group('FLH2XYZ', 'Argumenty dla trybu FLH2XYZ')
group_b.add_argument('-f', type=float, help="Argument f dla trybu FLH2XYZ")
group_b.add_argument('-l', type=float, help="Argument l dla trybu FLH2XYZ")
group_b.add_argument('-ha', type=float, help="Argument h dla trybu FLH2XYZ")


group_c = parser.add_argument_group('flh2PL1992', 'Argumenty dla trybu flh2PL1992')
group_c.add_argument('-fa', type=float, help="Argument fa dla trybu flh2PL1992")
group_c.add_argument('-la', type=float, help="Argument la dla trybu flh2PL1992")

group_d = parser.add_argument_group('flh2PL2000', 'Argumenty dla trybu flh2PL2000')
group_d.add_argument('-fb', type=float, help="Argument fb dla trybu flh2PL2000")
group_d.add_argument('-lb', type=float, help="Argument lb dla trybu flh2PL2000")

group_e = parser.add_argument_group('xyz2neu', 'Argumenty dla trybu xyz2neu')
group_e.add_argument('-xa', type=float, help="Argument xa dla trybu xyz2neu")
group_e.add_argument('-ya', type=float, help="Argument ya dla trybu xyz2neu")
group_e.add_argument('-za', type=float, help="Argument za dla trybu xyz2neu")
group_e.add_argument('-xb', type=float, help="Argument xb dla trybu xyz2neu")
group_e.add_argument('-yb', type=float, help="Argument yb dla trybu xyz2neu")
group_e.add_argument('-zb', type=float, help="Argument zb dla trybu xyz2neu")
args = parser.parse_args()

if args.mode == 'hirvonen':

    geo = Transformacje(model = args.m)
    f, l, h = geo.hirvonen(args.x, args.y, args.z)
    print("")
    print("")
    print("Elipsida:", args.m)
    print(f"Wyniki_z_algorytmu_hirvonen'a; f = {f}, l = {l}, h = {h:^.3f}[m]")
    
    print("Nazwa pliku głównego:", skrypt.__name__)
    print("")
    print("")

if args.mode == 'flh2PL1992':
    
    geo = Transformacje(model = args.m)
    if args.la >= 13.5 and args.la <= 25.5 and args.fa <= 55.0 and args.fa >= 48.9:
        x92, y92 = geo.flh2PL1992(args.fa,args.la)
        print(f"Wyniki_z_transformacji_flh2PL92; X1992 = {x92:^.3f}[m], Y1992 = {y92:^.3f}[m]")
    else:
        x92 = " '-' " 
        y92 = " '-' " 
        print(f"Wyniki_z_transformacji_flh2PL92; X1992 = {x92}[m], Y1992 = {y92}[m]")
        print("To położenie nie jest obsługiwane przez układy współrzędnych płaskich PL1992")

if args.mode == 'flh2PL2000':
    geo = Transformacje(model = args.m)
    if args.lb >= 13.5 and args.lb <= 25.5 and args.fb <= 55.0 and args.fb >= 48.9:
        x20, y20 = geo.flh2PL2000(args.fb,args.lb)
        print(f"Wyniki_z_transformacji_flh2PL2000; X2000 = {x20:^.3f}[m], Y2000 = {y20:^.3f}[m]")
    else:
        x20 = " '-' " 
        y20 = " '-' " 
        print(f"Wyniki_z_transformacji_flh2PL2000; X2000 = {x20}[m], Y2000 = {y20}[m]")
        print("To położenie nie jest obsługiwane przez układy współrzędnych płaskich PL2000")
if args.mode == 'xyz2neu':
    geo = Transformacje(model = args.m)
    f, l, h = geo.hirvonen(args.xa, args.ya, args.za)
    n, e, u = geo.xyz2neu(f, l, args.xa, args.ya, args.za, args.xb, args.yb, args.zb)

    n = float(n)
    e = float(e)
    u = float(u)
    
    
    print("")
    print("")
    print("")
    print("")
    print("Elipsida:", args.m)
    print(f"Wyniki_z_xyz2neu; n = {n}, e = {e}, u = {u}")
    print("Nazwa pliku głównego:", skrypt.__name__)
    print("")
    print("")
    print("")
    print("")

if args.mode == 'FLH2XYZ':
    mod = Transformacje(model = args.m)
    
    print("")
    print("")
    print("Elipsoida:", args.m)
    x, y, z = mod.flh2XYZ(args.f, args.l, args.ha)
    print(f"Wyniki dla transformacji flh2xyz: X = {x:^.3f} [m], Y = {y:^.3f} [m], Z = {z:^.3f} [m]")
    print("Nazwa pliku głównego:", skrypt.__name__)
    print("")
    print("")