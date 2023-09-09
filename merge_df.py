#!/usr/bin/env python3

import os
import pandas as pd
from utils import decay_modes, store_df, get_masses, get_gVs, get_gFs, get_gHs


def merge(files, output, overwrite):
    if os.path.exists(output) and not overwrite:
        return
    print(f'Merging {len(files)} files into {output}')
    df_list = []
    for fname in files:
        if fname == None:
            continue
        df_list.append(pd.read_csv(fname))
    df = pd.concat(df_list)
    store_df(df=df, fname=output)

def merge_df(overwrite):
    
    m_values = get_masses()
    gV_values = get_gVs()
    gF_values = get_gFs()
    gH_values = get_gHs()

    for Vprime in decay_modes.keys():
        for mass in m_values:
            files_gv = []
            for gv in gV_values:
                files_gf = []
                for gf in gF_values:
                    files_gh = []
                    for gh in gH_values:
                        csv_file = f'BRs/BRs_{Vprime}prime_M{mass}_gv{gv}_gf{gf}_gh{gh}.csv'
                        if os.path.exists(csv_file):
                            files_gh.append(csv_file)
                        elif gf == 0 and gh ==0:
                            files_gh.append(None)
                    output_gf = f'BRs/BRs_{Vprime}prime_M{mass}_gv{gv}_gf{gf}.csv'
                    if len(gH_values) == len(files_gh):
                        merge(files_gh, output_gf, overwrite=overwrite)
                    else:
                        print("skipping", output_gf, len(files_gh), len(gH_values))
                    if os.path.exists(output_gf):
                        files_gf.append(output_gf)
                output_gv = f'BRs/BRs_{Vprime}prime_M{mass}_gv{gv}.csv'
                if len(gF_values) == len(files_gf):
                    merge(files_gf, output_gv, overwrite=overwrite)
                else:
                    print("skipping", output_gv, len(files_gf), len(gF_values))
                if os.path.exists(output_gv):
                    files_gv.append(output_gv)
            output = f'BRs/BRs_{Vprime}prime_M{mass}_gv{gv}.csv'
            if len(gV_values) == len(files_gv):
                merge(files_gv, output, overwrite=overwrite)
                
def main(overwrite):
    merge_df(overwrite=overwrite)
    

if __name__ == "__main__":
    main(overwrite=False)