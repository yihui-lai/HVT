#!/usr/bin/env python3
import numpy as np
import os
from utils import BRs_in_df, get_csv_file, decay_modes, get_masses, get_gVs, get_gFs, get_gHs
from parallelize import parallelize
import glob

debug = True

def runJobs(runLocal, ncores, gfstart, gfend, m_values):
    m_values = get_masses(m_values)
    gV_values = get_gVs()
    gF_values = get_gFs(gfstart, gfend)
    gH_values = get_gHs()
    m_values = m_values
    print("m_values", len(m_values))
    print("gV_values", len(gV_values))
    print("gF_values", len(gF_values))
    print("gH_values", len(gH_values))
    print("Max", len(decay_modes.keys()) * len(m_values) * len(gV_values) * len(gF_values) * len(gH_values))
    jobArgs = []
    tot = 0
    for Vprime in decay_modes.keys():
        print(f"Looking for {Vprime}")
        for mass in m_values:
            print(f"  Looking for {mass}")
            for gv in gV_values:
                for gf in gF_values:
                    for gh in gH_values:
                        if gf == 0 and gh == 0:
                            continue
                        csv_file = get_csv_file(Vprime=Vprime, mass=mass, gv=gv, gf=gf, gh=gh)
                        tot += 1
                        if os.path.exists(csv_file):
                            continue
                        # if BRs_in_df(get_csv_file(Vprime=Vprime), mass, gv, gf, gh) is not None:
                        #     continue
                        # if BRs_in_df(get_csv_file(Vprime=Vprime,mass=mass), mass, gv, gf, gh) is not None:
                        #     continue
                        # if BRs_in_df(get_csv_file(Vprime=Vprime,mass=mass,gv=gv), mass, gv, gf, gh) is not None:
                        #     continue
                        # if BRs_in_df(get_csv_file(Vprime=Vprime,mass=mass,gv=gv,gf=gf), mass, gv, gf, gh) is not None:
                        #     continue
                        runCommand = f"--Vprime {Vprime} --mass {mass} --gv {gv} --gf {gf} --gh {gh}"
                        jobArgs.append(runCommand)

    jobExec = f"{os.getcwd()}/createBRs.py"
    if runLocal:
        commands = [f"{jobExec} {args}" for args in jobArgs]
        print(f"Running locally {len(commands)} commands out of {tot}")
        if len(commands) != 0:
            _ = parallelize(commands, ncores=ncores)


def main(runLocal, ncores):
    runJobs(runLocal, ncores=ncores)


if __name__ == "__main__":
    main(runLocal=True, ncores=30)
    # main(runLocal=False, ncores=40)
