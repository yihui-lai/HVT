#!/usr/bin/env python3

import os, math
from array import array
from collections import OrderedDict
import pandas as pd
import ROOT as rt
from utils import get_csv_file, filterCondition, get_BRs_from_df, decay_modes, get_masses, get_gVs, get_gFs, get_gHs, benchmarks


def createGraphs(overwrite=False):
    m_values = get_masses()
    gV_values = get_gVs()
    gF_values = get_gFs()
    gH_values = get_gHs()
    expected = sum([len(decays) for decays in decay_modes.values()]) * len(m_values) * (len(gV_values) * len(gF_values) + len(benchmarks))
    graphs = OrderedDict()
    f_stored = rt.TFile("graphs.root", "READ") if os.path.exists("graphs.root") else None
    for Vprime, decays in decay_modes.items():
        fname = get_csv_file(Vprime=Vprime)
        if not os.path.exists(fname):
            continue
        df = pd.read_csv(fname)
        for mass in m_values:
            for gv in gV_values:
                for decay in decays:
                    for gf in gF_values:
                        gname = f"{Vprime}_{mass}_{gv}_{decay}_{gf}"
                        if gname in graphs:
                            raise ValueError(f"graph already exists: {gname}")
                        graphs[gname] = f_stored.Get(gname) if f_stored else None
                        if graphs[gname] and not overwrite:
                            continue
                        x_values = []
                        brs = []
                        for gh in gH_values:
                            filtered_df = get_BRs_from_df(df, mass, gv, gf, gh)
                            if filtered_df is None:
                                fname = get_csv_file(Vprime=Vprime, mass=mass, gv=gv, gf=gf, gh=gh)
                                print(f"Model not in central df. Checking in {fname}")
                                if not os.path.exists(fname):
                                    continue
                                df_model = pd.read_csv(fname)
                                filtered_df = get_BRs_from_df(df_model, mass, gv, gf, gh)
                                if filtered_df is None:
                                    continue
                            br = filtered_df[decay].iloc[0]
                            x_values.append(gh * math.copysign(1, gf))
                            brs.append(br)
                        graphs[gname] = rt.TGraph(len(x_values), array("d", x_values), array("d", brs))
                        print(f"Created graph: {gname}")

            for model, benchmark in benchmarks.items():
                gv, gf, gh = 1, benchmark["gf"], benchmark["gh"]
                for decay in decays:
                    gname = f"{Vprime}_{mass}_{model}_{decay}"
                    if gname in graphs and not overwrite:
                        continue
                    gname_ref = f"{Vprime}_{mass}_{gv}_{decay}_{gf}"
                    if not gname_ref in graphs:
                        continue
                    graph = graphs[gname_ref]
                    x = gh * math.copysign(1, gf)
                    for i in range(graph.GetN()):
                        x_ = graph.GetX()[i]
                        if x_ == x:
                            y = graph.Eval(x)
                    graphs[gname] = rt.TGraph(1, array("d", [x]), array("d", [y]))
                    print(f"Created graph: {gname}")
    if f_stored:
        f_stored.Close()
    print(f"Created {len(graphs)}/{expected} graphs")
    f_ = rt.TFile("graphs.root", "RECREATE")
    for name, graph in graphs.items():
        graph.Write(name)
    f_.Close()


def main(overwrite):
    createGraphs(overwrite)


if __name__ == "__main__":
    main(overwrite=False)
    # main(overwrite=True)
