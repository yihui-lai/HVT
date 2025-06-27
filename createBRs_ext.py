#!/usr/bin/env python3

import os, argparse
import pandas as pd
from utils import do_calculations_ext, store_df, get_csv_file_ext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Vprime", dest="Vprime", type=str)
    parser.add_argument("--mass", dest="mass", type=int)
    parser.add_argument("--gv", dest="gv", type=float)
    parser.add_argument("--gl", dest="gl", type=float)
    parser.add_argument("--gq12", dest="gq12", type=float)
    parser.add_argument("--gq3", dest="gq3", type=float)
    parser.add_argument("--gh", dest="gh", type=float)
    parser.add_argument("--overwrite", action="store_true", default=False)

    args = parser.parse_args()
    Vprime = args.Vprime
    mass = args.mass
    gv = args.gv #round(args.gv, 3)
    gl = args.gl #round(args.gl, 3)
    gq12 = args.gq12
    gq3 = args.gq3
    gh = args.gh #round(args.gh, 3)
    csv_file = get_csv_file_ext(Vprime=Vprime, mass=mass, gv=gv, gl=gl, gq12=gq12, gq3=gq3, gh=gh)
    if os.path.exists(csv_file) and not args.overwrite:
        return
    #print(csv_file)
    entry = do_calculations_ext(mass, gv, gq3, gq12, gl, gl, gh, Vprime)
    if entry == None:
        return
    df = pd.DataFrame([entry])
    store_df(df=df, fname=csv_file)


if __name__ == "__main__":
    main()
