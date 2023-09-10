#!/usr/bin/env python3

import os, argparse
import pandas as pd
import model as HVT
from utils import do_calculations, store_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Vprime", dest="Vprime", type=str)
    parser.add_argument("--mass", dest="mass", type=int)
    parser.add_argument("--gv", dest="gv", type=int)
    parser.add_argument("--gf", dest="gf", type=float)
    parser.add_argument("--gh", dest="gh", type=float)
    parser.add_argument("--overwrite", action="store_true", default=False)

    args = parser.parse_args()
    Vprime = args.Vprime
    mass = args.mass
    gv = round(args.gv,3)
    gf = round(args.gf,3)
    gh = round(args.gh,3)
    csv_file = f'BRs/BRs_{Vprime}_M{mass}_gv{gv}_gf{gf}_gh{gh}.csv'
    if os.path.exists(csv_file) and not args.overwrite:
        return
    
    ch = round(HVT.get_ch(gH=gh, gv=gv),5)
    cq = round(HVT.get_cq(gF=gf, gv=gv),5)
    entry = do_calculations(mass,gv,ch,cq,Vprime)
    if entry == None:
        return
    df = pd.DataFrame([entry])
    store_df(df=df, fname=csv_file)

if __name__ == "__main__":
    main()