#!/usr/bin/env python3

import os
import pandas as pd
import model as HVT
from utils import decay_modes, get_masses, get_gVs, get_gFs, get_gHs, filterCondition
from parallelize import parallelize
from ClusterSubmission.CondorBase import SubmitListToCondor

def runJobs(runLocal, ncores):
    m_values = get_masses()
    gV_values = get_gVs()
    gF_values = get_gFs()
    gH_values = get_gHs()
    
    jobArgs = []
    for Vprime in decay_modes.keys():
        for mass in m_values:
            for gv in gV_values:
                for gf in gF_values:
                    for gh in gH_values:
                        if gf == 0 and gh ==0:
                            continue
                        csv_file = f'BRs/BRs_{Vprime}_M{mass}_gv{gv}_gf{gf}_gh{gh}.csv'
                        if os.path.exists(csv_file):
                            continue
                        csv_file_merged = f'BRs/BRs_{Vprime}_M{mass}_gv{gv}_gf{gf}.csv'
                        if os.path.exists(csv_file_merged):
                            df = pd.read_csv(csv_file_merged)
                            ch = round(HVT.get_ch(gH=gh, gv=gv),5)
                            cq = round(HVT.get_cq(gF=gf, gv=gv),5)
                            infos = {'M0': mass, 'g': HVT.g_su2, 'gv': gv, 'ch': ch, 'cl': cq}
                            condition = filterCondition(df, infos)
                            if len(df[condition])!=0:
                                continue
                        runCommand = f"--Vprime {Vprime} --mass {mass} --gv {gv} --gf {gf} --gh {gh}"
                        jobArgs.append(runCommand)
    
    if False:
        jobArgs = []
        Vprime = 'Zprime'
        mass = 2000
        gv = 1
        gf = 0.01
        gh = 0.01
        runCommand = f"--Vprime {Vprime} --mass {mass} --gv {gv} --gf {gf} --gh {gh}"
        jobArgs.append(runCommand)

    jobExec = f"{os.getcwd()}/createBRs.py"
    if runLocal:
        commands = [f'{jobExec} {args}' for args in jobArgs]
        # print(commands)
        print(f'Running locally {len(commands)} commands')
        if len(commands)!=0:
            parallelize(commands, ncores=ncores)
    else:
        JsonInfo = {
            'MY.SendCredential': 'True',
            'environment': f"PYTHON3PATH={os.environ.get('PYTHON3PATH', '')}"
            }
        SubmitListToCondor(jobArgs, jobExec, JsonInfo=JsonInfo, JobName='HVT', debug=True)
        # SubmitListToCondor(jobArgs, jobExec, JsonInfo=JsonInfo, JobName='HVT')

def main(runLocal, ncores):
    runJobs(runLocal, ncores=ncores)

if __name__ == "__main__":
    main(runLocal=True, ncores=30)
    # main(runLocal=False, ncores=40)
