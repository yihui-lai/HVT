#!/usr/bin/env python3

import os
import pandas as pd
from utils import decay_modes, get_csv_file_ext, store_df, get_masses, get_gVs, get_gFs, get_gHs, get_gls, get_gq12s, get_gq3s
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


def merge_df_ext(overwrite, gq12list, gq3list, m_values):
    m_values    = get_masses(m_values)
    gV_values   = get_gVs()
    gl_values   = get_gls()
    gq12_values = get_gq12s(gq12list)
    gq3_values  = get_gq3s(gq3list)
    gH_values   = get_gHs()

    for Vprime in decay_modes.keys():
        files_mass = []
        for mass in m_values:
            files_gv = []
            for gv in gV_values:
                files_gl = []
                for gl in gl_values:
                    files_gq12 = []
                    for gq12 in gq12_values:
                        files_gq3 = []
                        for gq3 in gq3_values:
                            files_gh = []
                            for gh in gH_values:
                                csv_file = get_csv_file_ext(Vprime=Vprime, mass=mass, gv=gv, gl=gl, gq12=gq12, gq3=gq3, gh=gh)
                                if os.path.exists(csv_file):
                                    files_gh.append(csv_file)
                                elif gl == 0 and gq12 ==0 and gq3==0 and gh == 0:
                                    files_gh.append(None)
                            output_gq3 = get_csv_file_ext(Vprime=Vprime, mass=mass, gv=gv, gl=gl, gq12=gq12, gq3=gq3)
                            run_merge(inputs=files_gh, output=output_gq3, reference=gH_values, overwrite=overwrite)
                            if os.path.exists(output_gq3):
                                files_gq3.append(output_gq3)

                        output_gq12 = get_csv_file_ext(Vprime=Vprime, mass=mass, gv=gv, gl=gl, gq12=gq12)
                        run_merge(inputs=files_gq3, output=output_gq12, reference=gq3_values, overwrite=overwrite)
                        if os.path.exists(output_gq12):
                            files_gq12.append(output_gq12)

                    output_gl = get_csv_file_ext(Vprime=Vprime, mass=mass, gv=gv, gl=gl)
                    run_merge(inputs=files_gq12, output=output_gl, reference=gq12_values, overwrite=overwrite)
                    if os.path.exists(output_gl):
                        files_gl.append(output_gl)

                output_gv = get_csv_file_ext(Vprime=Vprime, mass=mass, gv=gv)
                run_merge(inputs=files_gl, output=output_gv, reference=gl_values, overwrite=overwrite)
                if os.path.exists(output_gv):
                    files_gv.append(output_gv)

            output_mass = get_csv_file_ext(Vprime=Vprime, mass=mass)
            run_merge(inputs=files_gv, output=output_mass, reference=gV_values, overwrite=overwrite)
            if os.path.exists(output_mass):
                files_mass.append(output_mass)
        output_vprime = get_csv_file_ext(Vprime=Vprime)
        run_merge(inputs=files_mass, output=output_vprime, reference=m_values, overwrite=overwrite)


def main(overwrite):
    merge_df_ext(overwrite=overwrite)


if __name__ == "__main__":
    main(overwrite=False)
