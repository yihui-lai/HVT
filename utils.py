import os
import numpy as np
import pandas as pd
from model import HVT
from model_extend import HVT_ext

def get_csv_file(Vprime, mass=None, gv=None, gf=None, gh=None):
    dir_ = f"BRs/"
    csv_file = f"BRs_{Vprime}"
    if mass != None:
        dir_ += f"{Vprime}/"
        csv_file += f"_M{mass}"
    if gv != None:
        dir_ += f"mass_{mass}/"
        csv_file += f"_gv{gv:.12f}"
    if gf != None:
        dir_ += f"gv_{gv:.12f}/"
        csv_file += f"_gf{gf:.12f}"
    if gh != None:
        dir_ += f"gf_{gf:.12f}/"
        csv_file += f"_gh{gh:.12f}"
    csv_file += ".csv"
    return dir_ + csv_file

def get_csv_file_ext(Vprime, mass=None, gv=None, gl=None, gq12=None, gq3=None, gh=None):
    dir_ = f"BRs/"
    csv_file = f"BRs_{Vprime}"
    if mass != None:
        dir_ += f"{Vprime}/"
        csv_file += f"_M{mass}"
    if gv != None:
        dir_ += f"mass_{mass}/"
        csv_file += f"_gv{gv:.12f}"
    if gl != None:
        dir_ += f"gv_{gv:.12f}/"
        csv_file += f"_gl{gl:.12f}"
    if gq12 != None:
        dir_ += f"gl_{gl:.12f}/"
        csv_file += f"_gq12{gq12:.12f}"
    if gq3 != None:
        dir_ += f"gq12_{gq12:.12f}/"
        csv_file += f"_gq3{gq3:.12f}"
    if gh != None:
        dir_ += f"gq3_{gq3:.12f}/"
        csv_file += f"_gh{gh:.12f}"
    csv_file += ".csv"
    return dir_ + csv_file

def filterCondition(data, infos):
    condition = None
    for key, value in infos.items():
        if condition is None:
            condition = data[key] == value
        else:
            condition &= data[key] == value
    return condition


def get_BRs_from_df(df, mass, gv, gf, gh):
    df_selected = None
    infos = {"M0": mass, "gh": gh, "gf": gf, "gv": gv}
    condition = filterCondition(df, infos)
    if len(df[condition]) != 0:
        df_selected = df[condition]
    return df_selected


def BRs_in_df(df_name, mass, gv, gf, gh):
    df_selected = None
    if os.path.exists(df_name):
        df = pd.read_csv(df_name)
        df_selected = get_BRs_from_df(df, mass, gv, gf, gh)
    return df_selected


def get_BRs_from_df_ext(df, mass, gv, gq3, gq12, gl3, gl12, gh):
    df_selected = None
    infos = {"M0": mass, "gh": gh, "gq3": gq3, "gq12": gq12, "gl3": gl3, "gl12": gl12, "gv": gv}
    condition = filterCondition(df, infos)
    if len(df[condition]) != 0:
        df_selected = df[condition]
    return df_selected


def BRs_in_df_ext(df_name, mass, gv, gq3, gq12, gl3, gl12, gh):
    df_selected = None
    if os.path.exists(df_name):
        df = pd.read_csv(df_name)
        df_selected = get_BRs_from_df(df, mass, gv,  gq3, gq12, gl3, gl12, gh)
    return df_selected


def do_calculations_ext(mass, gv, gq3, gq12, gl3, gl12, gh, Vprime):
    hvt = HVT_ext(MVz=mass, gv=gv, gh=gh, gq3=gq3, gq12=gq12, gl3=gl3, gl12=gl12)
    hvt.setup()
    if abs(gq3) == 0 and abs(gq12) == 0 and abs(gl3) == 0 and abs(gl12) == 0 and abs(gh) == 0:
        return None
    print(f"Calculating BR for mass: {mass} gv: {gv} gq3: {gq3} gq12: {gq12} gl3: {gl3} gl12: {gl12} gh: {gh}")
    if Vprime == "Zprime":
        tot = hvt.ZprimeTot.real
    if Vprime == "Wprime":
        tot = hvt.WprimeTot.real
    if tot == 0:
        return None
    if Vprime == "Zprime":
        entry = {
            "M0": mass,
            "g": hvt.g_su2,
            "gv": hvt.gv,
            "gh": hvt.gh,
            "gq3": hvt.gq3,
            "gq12": hvt.gq12,
            "gl3": hvt.gl3,
            "gl12": hvt.gl12,
            "ch": hvt.ch,
            "cl": hvt.cl,
            "gw": hvt.gw,
            "GammaTot": tot,
            "BRWW": hvt.ZprimeWW.real / tot,
            "BRhZ": hvt.ZprimeZH.real / tot,
            "BRee": hvt.Zprimeee.real / tot,
            "BRmumu": hvt.Zprimemm.real / tot,
            "BRtautau": hvt.Zprimetautau.real / tot,
            "BRnunu": hvt.Zprimevv.real / tot,
            "BRuu": hvt.Zprimeuu.real / tot,
            "BRdd": hvt.Zprimedd.real / tot,
            "BRcc": hvt.Zprimecc.real / tot,
            "BRss": hvt.Zprimess.real / tot,
            "BRbb": hvt.Zprimebb.real / tot,
            "BRtt": hvt.Zprimett.real / tot,
        }
        entry["BRll"] = entry["BRee"] + entry["BRmumu"]
        entry["BRqq"] = entry["BRuu"] + entry["BRdd"] + entry["BRcc"] + entry["BRss"]
        entry["BRjets"] = entry["BRqq"] + entry["BRbb"] + entry["BRtt"]
    if Vprime == "Wprime":
        entry = {
            "M0": mass,
            "g": hvt.g_su2,
            "gv": hvt.gv,
            "gh": hvt.gh,
            "gq3": hvt.gq3,
            "gq12": hvt.gq12,
            "gl3": hvt.gl3,
            "gl12": hvt.gl12,
            "ch": hvt.ch,
            "cl": hvt.cl,
            "gw": hvt.gw,
            "GammaTot": tot,
            "BRWH": hvt.WprimeHW.real / tot,
            "BRWZ": hvt.WprimeWZ.real / tot,
            "BReve": hvt.Wprimeeve.real / tot,
            "BRmvm": hvt.Wprimemvm.real / tot,
            "BRtauvt": hvt.Wprimetauvt.real / tot,
            "BRud": hvt.Wprimeud.real / tot,
            "BRus": hvt.Wprimeus.real / tot,
            "BRcd": hvt.Wprimecd.real / tot,
            "BRcs": hvt.Wprimecs.real / tot,
            "BRtb": hvt.Wprimetb.real / tot,
        }
        entry["BRlnu"] = entry["BReve"] + entry["BRmvm"]
        entry["BRqqbar"] = entry["BRud"] + entry["BRus"] + entry["BRcd"] + entry["BRcs"]
        entry["BRjets"] = entry["BRqqbar"] + entry["BRtb"]
    return entry


def do_calculations(mass, gv, gf, gh, Vprime):
    hvt = HVT(MVz=mass, gv=gv, gf=gf, gh=gh)
    hvt.setup()
    if abs(gf) == 0 and abs(gh) == 0:
        return None
    print(f"Calculating BR for mass: {mass} gv: {gv} gf: {gf} gh: {gh}")
    if Vprime == "Zprime":
        tot = hvt.ZprimeTot.real
    if Vprime == "Wprime":
        tot = hvt.WprimeTot.real
    if tot == 0:
        return None
    if Vprime == "Zprime":
        entry = {
            "M0": mass,
            "g": hvt.g_su2,
            "gv": hvt.gv,
            "gh": hvt.gh,
            "gf": hvt.gf,
            "ch": hvt.ch,
            "cl": hvt.cq,
            "GammaTot": tot,
            "BRWW": hvt.ZprimeWW.real / tot,
            "BRhZ": hvt.ZprimeZH.real / tot,
            "BRee": hvt.Zprimeee.real / tot,
            "BRmumu": hvt.Zprimemm.real / tot,
            "BRtautau": hvt.Zprimetautau.real / tot,
            "BRnunu": hvt.Zprimevv.real / tot,
            "BRuu": hvt.Zprimeuu.real / tot,
            "BRdd": hvt.Zprimedd.real / tot,
            "BRcc": hvt.Zprimecc.real / tot,
            "BRss": hvt.Zprimess.real / tot,
            "BRbb": hvt.Zprimebb.real / tot,
            "BRtt": hvt.Zprimett.real / tot,
        }
        entry["BRll"] = entry["BRee"] + entry["BRmumu"]
        entry["BRqq"] = entry["BRuu"] + entry["BRdd"] + entry["BRcc"] + entry["BRss"]
        entry["BRjets"] = entry["BRqq"] + entry["BRbb"] + entry["BRtt"]
    if Vprime == "Wprime":
        entry = {
            "M0": mass,
            "g": hvt.g_su2,
            "gv": hvt.gv,
            "gh": hvt.gh,
            "gf": hvt.gf,
            "ch": hvt.ch,
            "cl": hvt.cq,
            "GammaTot": tot,
            "BRWH": hvt.WprimeHW.real / tot,
            "BRWZ": hvt.WprimeWZ.real / tot,
            "BReve": hvt.Wprimeeve.real / tot,
            "BRmvm": hvt.Wprimemvm.real / tot,
            "BRtauvt": hvt.Wprimetauvt.real / tot,
            "BRud": hvt.Wprimeud.real / tot,
            "BRus": hvt.Wprimeus.real / tot,
            "BRcd": hvt.Wprimecd.real / tot,
            "BRcs": hvt.Wprimecs.real / tot,
            "BRtb": hvt.Wprimetb.real / tot,
        }
        entry["BRlnu"] = entry["BReve"] + entry["BRmvm"]
        entry["BRqqbar"] = entry["BRud"] + entry["BRus"] + entry["BRcd"] + entry["BRcs"]
        entry["BRjets"] = entry["BRqqbar"] + entry["BRtb"]
    return entry


def store_df(df, fname):
    print("make ",os.path.dirname(fname))
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    df = df.astype("float64")
    df.to_csv(fname, index=False)
    print("Created", fname)


def get_masses(m_values):
    m_value_int = []
    for i in m_values:
        m_value_int.append(int(i))
    return m_value_int


def get_gVs():
    gV_values = [1]
    return gV_values


def get_gFs(gflist):
    gF_values = [(data["gf"]) for data in benchmarks.values()]
    #gF_values = list(np.logspace(np.log10(0.0005), np.log10(5), 160))
    #gF_values += list(np.linspace(0.0005, 3.5, 160))
    #gF_values = list(sorted(set([round(x, 12) for x in gF_values])))
    ## for testing
    #gF_values = list(np.logspace(np.log10(0.05), np.log10(1), 41))
    #gF_values += list(np.linspace(0.06, 1.1, 40))
    #gF_values = list(sorted(set([round(x, 12) for x in gF_values])))
    #gf_leng=len(gF_values)
    #gfstart=int(gf_leng*gflist[0])
    #gfend=int(gf_leng*gflist[1])
    #if gfstart<=0:
    #    gfstart=0
    #if gfend>=gf_leng:
    #    gfend=gf_leng
    #gF_values = gF_values[gfstart:gfend]
    #print("gF", gF_values, len(gF_values))
    return gF_values

def get_gls():
    gl_values = [(data["gf"]) for data in benchmarks.values()]
    gl_values = list(sorted(set([round(x, 12) for x in gl_values])))
    return gl_values

def get_gq12s(gq12list):
    gq12_values = []
    for i in gq12list:
        gq12_values.append(float(i))
    #gq12_values = [(data["gf"]) for data in benchmarks.values()]
    gq12_values = list(sorted(set([round(x, 12) for x in gq12_values])))
    return gq12_values

def get_gq3s(gq3list):
    gq3_values = []
    for i in gq3list:
        gq3_values.append(float(i))
    # 
    ntotal_point = 160
    ntotal_point = 10
    gq3_values = list(np.logspace(np.log10(0.001), np.log10(2.5), ntotal_point))
    gq3_values += list(-np.logspace(np.log10(0.001), np.log10(2.5), ntotal_point))
    gq3_values += list(np.linspace(0.001, 2.5, ntotal_point))
    gq3_values += list(-np.linspace(0.001, 2.5, ntotal_point))
    #gq3_values = [(data["gf"]) for data in benchmarks.values()]
    gq3_values = list(sorted(set([round(x, 12) for x in gq3_values])))
    return gq3_values

def get_gHs():
    gH_values = [(data["gh"]) for data in benchmarks.values()]
    ntotal_point = 160
    ntotal_point = 10
    gH_values = list(np.logspace(np.log10(0.001), np.log10(3.5), ntotal_point))
    gH_values += list(-np.logspace(np.log10(0.001), np.log10(3.5), ntotal_point))
    gH_values += list(np.linspace(0.001, 3.5, ntotal_point))
    gH_values += list(-np.linspace(0.001, 3.5, ntotal_point))
    gH_values = list(sorted(set([round(x, 12) for x in gH_values])))
    #print("gH", gH_values, len(gH_values))
    return gH_values

benchmarks = {
    "modelA":  {"ch": -0.556, "cq": -1.316, "gv": 1.0, "gh": -0.556, "gf": -0.562},
#    "modelB":  {"ch": -0.976, "cq": 1.024,  "gv": 3.0, "gh": -2.928, "gf": 0.146},
#    "modelC1": {"ch": 1,      "cq": 0,      "gv": 1.0, "gh": 1.0,    "gf": 0.0},
#    "modelC3": {"ch": 3,      "cq": 0,      "gv": 1.0, "gh": 3.0,    "gf": 0.0},
}

decay_modes = {
    "Zprime": {
        "GammaTot": "#Gamma",
        "BRhZ": "ZH",
        "BRWW": "WW",
        "BRll": "ll",
        "BRnunu": "#nu#nu",
        "BRjets": "qq",
        "BRtt": "tt",
    },
    "Wprime": {
        "GammaTot": "#Gamma",
        "BRWH": "WH",
        "BRWZ": "WZ",
        "BRlnu": "l#nu",
        "BRjets": "qq",
    },
}
