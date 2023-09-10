#!/usr/bin/env python3

import os, math
from array import array
from collections import OrderedDict
import pandas as pd
import ROOT as rt
import model as HVT
from utils import filterCondition, decay_modes, get_masses, get_gVs, get_gFs, get_gHs, benchmarks

def createGraphs(overwrite=False):
    m_values = get_masses()
    gV_values = get_gVs()
    gF_values = get_gFs()
    gH_values = get_gHs()
    expected = sum([len(decays) for decays in decay_modes.values()])*len(m_values)*(len(gV_values)*len(gF_values)+len(benchmarks))
    graphs = OrderedDict()
    f_stored = rt.TFile('graphs.root', "READ")
    for Vprime, decays in decay_modes.items():
        fname = f'BRs/BRs_{Vprime}.csv'
        if not os.path.exists(fname):
            continue
        df = pd.read_csv(fname)
        for mass in m_values:
            for gv in gV_values:
                for decay in decays:
                    for gf in gF_values:
                        gname = f'{Vprime}_{mass}_{gv}_{decay}_{gf}'
                        if gname in graphs:
                            raise ValueError(f'graph already exists: {gname}')
                        graphs[gname] = f_stored.Get(gname)
                        if graphs[gname] and not overwrite:
                            continue
                        x_values = []
                        brs = []
                        for gh in gH_values:
                            ch = round(HVT.get_ch(gH=gh, gv=gv),5)
                            cq = round(HVT.get_cq(gF=gf, gv=gv),5)
                            infos = {'M0': mass, 'g': HVT.g_su2, 'gv': gv, 'ch': ch, 'cl': cq}
                            condition = filterCondition(df, infos)
                            if len(df[condition])!=0:
                                filtered_df = df[condition]
                            else:
                                fname = f'BRs/BRs_{Vprime}_M{mass}_gv{gv}_gf{gf}_gh{gh}.csv'
                                if not os.path.exists(fname):
                                    continue
                                df_model = pd.read_csv(fname)
                                condition = filterCondition(df_model, infos)
                                if len(df_model[condition])!=0:
                                    filtered_df = df[condition]
                                else:
                                    continue
                            br = filtered_df[decay].iloc[0]
                            x_values.append(gh*math.copysign(1, gf))
                            brs.append(br)
                        graphs[gname] = rt.TGraph(len(x_values), array('d',x_values), array('d',brs))
                        print(f"Created graph: {gname}")
            
            for model, benchmark in benchmarks.items():
                gv, gf, gh = 1, benchmark['gf'], benchmark['gh']
                for decay in decays:
                    gname = f'{Vprime}_{mass}_{model}_{decay}'
                    if gname in graphs and not overwrite:
                        continue
                    gname_ref = f'{Vprime}_{mass}_{gv}_{decay}_{gf}'
                    if not gname_ref in graphs:
                        continue
                    graph = graphs[gname_ref]
                    x = gh*math.copysign(1, gf)
                    for i in range(graph.GetN()):
                        x_ = graph.GetX()[i]
                        if x_ == x:
                            y = graph.Eval(x)
                    graphs[gname] = rt.TGraph(1, array('d',[x]), array('d',[y]))
    f_stored.Close()
    print(f'Created {len(graphs)}/{expected} graphs')
    f_ = rt.TFile('graphs.root', "RECREATE")
    for name, graph in graphs.items():
        graph.Write(name)
    f_.Close()

def main(overwrite):
    createGraphs(overwrite)

if __name__ == "__main__":
    main(overwrite=False)
    # main(overwrite=True)
