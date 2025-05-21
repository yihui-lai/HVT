#!/usr/bin/env python3

import os
import pandas as pd
from utils import decay_modes, get_csv_file, store_df, get_masses, get_gVs, get_gFs, get_gHs
import numpy as np

def merge(files, output, overwrite):
    if os.path.exists(output) and not overwrite:
        return
    print(f"Merging {len(files)} files into {output}")
    df_list = []
    for fname in files:
        if fname == None:
            continue
        df_list.append(pd.read_csv(fname))
    df = pd.concat(df_list)
    store_df(df=df, fname=output)


def run_merge(inputs, output, reference, overwrite):
    if len(reference) == len(inputs):
        merge(inputs, output, overwrite=overwrite)
    else:
        if len(reference) < 300:
            print("skipping", output, len(inputs), len(reference))


def merge_df(overwrite, gfstart, gfend, m_values):
    m_values = get_masses(m_values)
    gV_values = get_gVs()
    gF_values = get_gFs(gfstart, gfend)
    gH_values = get_gHs()
    for Vprime in decay_modes.keys():
        files_mass = []
        for mass in m_values:
            files_gv = []
            for gv in gV_values:
                files_gf = []
                for gf in gF_values:
                    files_gh = []
                    for gh in gH_values:
                        csv_file = get_csv_file(Vprime=Vprime, mass=mass, gv=gv, gf=gf, gh=gh)
                        if os.path.exists(csv_file):
                            files_gh.append(csv_file)
                        elif gf == 0 and gh == 0:
                            files_gh.append(None)
                    output_gf = get_csv_file(Vprime=Vprime, mass=mass, gv=gv, gf=gf)
                    run_merge(inputs=files_gh, output=output_gf, reference=gH_values, overwrite=overwrite)
                    if os.path.exists(output_gf):
                        files_gf.append(output_gf)
                output_gv = get_csv_file(Vprime=Vprime, mass=mass, gv=gv)
                run_merge(inputs=files_gf, output=output_gv, reference=gF_values, overwrite=overwrite)
                if os.path.exists(output_gv):
                    files_gv.append(output_gv)
            output_mass = get_csv_file(Vprime=Vprime, mass=mass)
            run_merge(inputs=files_gv, output=output_mass, reference=gV_values, overwrite=overwrite)
            if os.path.exists(output_mass):
                files_mass.append(output_mass)
        output_vprime = get_csv_file(Vprime=Vprime)
        run_merge(inputs=files_mass, output=output_vprime, reference=m_values, overwrite=overwrite)


def main(overwrite):
    merge_df(overwrite=overwrite)


if __name__ == "__main__":
    main(overwrite=False)
