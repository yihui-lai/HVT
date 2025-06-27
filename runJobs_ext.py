#!/usr/bin/env python3
import numpy as np
import os
from utils import BRs_in_df, get_csv_file, get_csv_file_ext, decay_modes, get_masses, get_gVs, get_gFs, get_gHs, get_gls, get_gq12s, get_gq3s
from parallelize import parallelize
import glob

debug = True

def runJobs_ext(runLocal, ncores, gq12list, gq3list, m_values):
    m_values    = get_masses(m_values)
    gV_values   = get_gVs()
    gl_values   = get_gls()
    gq12_values = get_gq12s(gq12list)
    gq3_values  = get_gq3s(gq3list)
    gH_values   = get_gHs()
    m_values    = m_values
    print("---> runJobs ")
    print("m_values", len(m_values), m_values)
    print("gV_values", len(gV_values), gV_values)
    print("gl_values", len(gl_values), gl_values)
    print("gq12_values", len(gq12_values), gq12_values)
    print("gq3_values", len(gq3_values), gq3_values)
    print("gH_values", len(gH_values), gH_values)
    print("Max", len(decay_modes.keys()) * len(m_values) * len(gV_values) * len(gl_values) * len(gq12_values) * len(gq3_values) * len(gH_values))
    input()
    jobArgs = []
    tot = 0
    for Vprime in decay_modes.keys():
        print(f"Looking for {Vprime}")
        for mass in m_values:
            print(f"  Looking for {mass}")
            for gv in gV_values:
                for gl in gl_values:
                    for gq12 in gq12_values:
                        for gq3 in gq3_values:
                            for gh in gH_values:
                                if gl == 0 and gq12 == 0 and gq3 == 0 and gh == 0:
                                    continue
                                csv_file = get_csv_file_ext(Vprime=Vprime, mass=mass, gv=gv, gl=gl, gq12=gq12, gq3=gq3,gh=gh)
                                tot += 1
                                if os.path.exists(csv_file):
                                    continue
                                runCommand = f"--Vprime {Vprime} --mass {mass} --gv {gv} --gl {gl} --gq12 {gq12} --gq3 {gq3} --gh {gh}"
                                jobArgs.append(runCommand)
    jobExec = f"{os.getcwd()}/createBRs_ext.py"
    if runLocal:
        commands = [f"{jobExec} {args}" for args in jobArgs]
        print(f"Running locally {len(commands)} commands out of {tot}")
        if len(commands) != 0:
            _ = parallelize(commands, ncores=ncores)


def main(runLocal, ncores):
    runJobs_ext(runLocal, ncores=ncores)

if __name__ == "__main__":
    main(runLocal=True, ncores=30)
    # main(runLocal=False, ncores=40)
