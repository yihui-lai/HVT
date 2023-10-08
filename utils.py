import os
import numpy as np
import pandas as pd
from model import HVT, get_ch, get_cq

def get_csv_file(Vprime,mass=None,gv=None,gf=None,gh=None):
    dir_ = f'BRs/'
    csv_file = f'BRs_{Vprime}'
    if mass!=None:
        dir_ += f'{Vprime}/'
        csv_file += f'_M{mass}'
    if gv!= None:
        dir_ += f'{mass}/'
        csv_file += f'_gv{gv}'
    if gf!= None: csv_file += f'_gf{gf}'
    if gh!= None: csv_file += f'_gh{gh}'
    csv_file += '.csv'
    return dir_+csv_file

def filterCondition(data, infos):
    condition = None
    for key, value in infos.items():
        if condition is None:
            condition = data[key] == value
        else:
            condition &= data[key] == value
    return condition

def get_minimum_set(mass, gh=None, gf=None, gv=None, ch=None, cq=None):
    if ch==None:
        ch = round(get_ch(gH=gh, gv=gv),5)
    if cq==None:
        cq = round(get_cq(gF=gf, gv=gv),5)
    infos = {'M0': mass, 'g': HVT.g_su2, 'gv': gv, 'ch': ch, 'cl': cq}
    return infos

def get_BRs_from_df(df, mass, gv, gf, gh):
    df_selected = None
    infos = get_minimum_set(mass, gh=gh, gf=gf, gv=gv)
    condition = filterCondition(df, infos)
    if len(df[condition])!=0:
        df_selected = df[condition]
    return df_selected

def BRs_in_df(df_name, mass, gv, gf, gh):
    df_selected = None
    if os.path.exists(df_name):
        df = pd.read_csv(df_name)
        df_selected = get_BRs_from_df(df, mass, gv, gf, gh)
    return df_selected

def do_calculations(mass,gv,ch,cq,Vprime):
    hvt = HVT(MVz= mass, gv= gv, cq= cq, ch= ch)
    hvt.setup()
    if abs(ch)==0 and abs(cq)==0:
        return None
    print(f'Calculating BR for mass: {mass} gv: {gv} cq: {cq} ch: {ch}')
    if Vprime=='Zprime':
        tot = hvt.ZprimeTot.real
    if Vprime=='Wprime':
        tot = hvt.WprimeTot.real
    if tot == 0:
        return None
    if Vprime=='Zprime':
        entry = {
            'M0': mass,
            'g': hvt.g_su2,
            'gv': gv,
            'ch': ch,
            'cl': cq,
            'GammaTot': tot,
            'BRWW':     hvt.ZprimeWW.real/tot,
            'BRhZ':     hvt.ZprimeZH.real/tot,
            'BRee':     hvt.Zprimeee.real/tot,
            'BRmumu':   hvt.Zprimemm.real/tot,
            'BRtautau': hvt.Zprimetautau.real/tot,
            'BRnunu':   hvt.Zprimevv.real/tot,
            'BRuu':     hvt.Zprimeuu.real/tot,
            'BRdd':     hvt.Zprimedd.real/tot,
            'BRcc':     hvt.Zprimecc.real/tot,
            'BRss':     hvt.Zprimess.real/tot,
            'BRbb':     hvt.Zprimebb.real/tot,
            'BRtt':     hvt.Zprimett.real/tot,
            }
        entry['BRll'] = entry['BRee'] + entry['BRmumu']
        entry['BRqq'] = entry['BRuu']+entry['BRdd']+entry['BRcc']+entry['BRss']
        entry['BRjets'] = entry['BRqq'] + entry['BRbb'] + entry['BRtt']
    if Vprime=='Wprime':
        entry = {
            'M0': mass,
            'g': hvt.g_su2,
            'gv': gv,
            'ch': ch,
            'cl': cq,
            'GammaTot':tot,
            'BRWH':    hvt.WprimeHW.real/tot,
            'BRWZ':    hvt.WprimeWZ.real/tot,
            'BReve':   hvt.Wprimeeve.real/tot,
            'BRmvm':   hvt.Wprimemvm.real/tot,
            'BRtauvt': hvt.Wprimetauvt.real/tot,
            'BRud': hvt.Wprimeud.real/tot,
            'BRus': hvt.Wprimeus.real/tot,
            'BRcd': hvt.Wprimecd.real/tot,
            'BRcs': hvt.Wprimecs.real/tot,
            'BRtb': hvt.Wprimetb.real/tot,
            }
        entry['BRlnu'] = entry['BReve'] + entry['BRmvm']
        entry['BRqqbar'] = entry['BRud']+entry['BRus']+entry['BRcd']+entry['BRcs']
        entry['BRjets'] = entry['BRqqbar'] + entry['BRtb']
    return entry

def store_df(df, fname):
    directory = os.path.dirname(fname)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    df = df.astype('float32')
    df.to_csv(fname, index=False)
    print("Created", fname)

def get_masses():
    m_values = [1000, 2000, 3000, 4000]
    # m_values = [4000]
    return m_values

def get_gVs():
    gV_values = [1]
    return gV_values

def get_gFs():
    gF_values = [data['gf'] for data in benchmarks.values()]
    gF_values += list(np.arange(0.0, 1.0+0.01, 0.01))
    gF_values += list(np.arange(1.0, 1.6+0.1,  0.1))
    gF_values = list(sorted(set([round(x,3) for x in gF_values])))
    return gF_values

def get_gHs():
    gH_values = [data['gh'] for data in benchmarks.values()]
    gH_values += list(np.arange(-2.0, 2.0+0.01, 0.01))
    gH_values += list(np.arange(-4.0, 4.0+0.1,  0.1))
    gH_values += list(np.arange(-8.0, 8.0+0.5,  0.5))
    gH_values = list(sorted(set([round(x,3) for x in gH_values])))
    return gH_values


benchmarks = {
    'modelA':  {'ch': -0.556, 'cq': -1.316, 'gv': 1, 'gh':-0.556, 'gf':-0.562},
    'modelB':  {'ch': -0.976, 'cq': 1.024,  'gv': 3, 'gh':-2.928, 'gf':0.146},
    'modelC':  {'ch': 1,      'cq': 0,      'gv': 1, 'gh':1.0,    'gf':0.0},
}

decay_modes = {
    'Zprime': {
        'GammaTot': '#Gamma',
        'BRhZ': 'ZH',
        'BRWW': 'WW',
        'BRll': 'll',
        'BRnunu': '#nu#nu',
        'BRjets': 'qq',
        'BRtt': 'tt',
        },
    'Wprime': {
        'GammaTot': '#Gamma',
        'BRWH': 'WH',
        'BRWZ': 'WZ',
        'BRlnu': 'l#nu',
        'BRjets': 'qq',
        }
}