#!/usr/bin/env python3

import os, argparse
import pandas as pd
from utils import do_calculations, store_df, get_csv_file


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
    gv = round(args.gv, 3)
    gf = round(args.gf, 3)
    gh = round(args.gh, 3)
    csv_file = get_csv_file(Vprime=Vprime, mass=mass, gv=gv, gf=gf, gh=gh)
    if os.path.exists(csv_file) and not args.overwrite:
        return

    entry = do_calculations(mass, gv, gf, gh, Vprime)
    if entry == None:
        return
    df = pd.DataFrame([entry])
    store_df(df=df, fname=csv_file)


if __name__ == "__main__":
    main()
