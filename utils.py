import numpy as np

def filterCondition(data, infos):
    condition = None
    for key, value in infos.items():
        if condition is None:
            condition = data[key] == value
        else:
            condition &= data[key] == value
    return condition

def do_calculations(mass,gv,ch,cq,Vprime):
    import model as HVT
    HVT.MVz = mass
    HVT.gv = gv
    HVT.ch = ch
    HVT.cq = cq
    HVT.cl = HVT.cq
    HVT.c3 = HVT.cq
    HVT.gst = HVT.gv
    if abs(ch)==0 and abs(cq)==0:
        return None
    print(f'Calculating BR for mass: {mass} gv: {gv} cq: {cq} ch: {ch}')
    if Vprime=='Zprime':
        tot = HVT.ZprimeTot().real
    if Vprime=='Wprime':
        tot = HVT.WprimeTot().real
    if tot == 0:
        return None
    if Vprime=='Zprime':
        entry = {
            'M0': mass,
            'g': HVT.g_su2,
            'gv': gv,
            'ch': ch,
            'cl': cq,
            'GammaTot': tot,
            'BRWW':     HVT.ZprimeWW().real/tot,
            'BRhZ':     HVT.ZprimeZH().real/tot,
            'BRee':     HVT.Zprimeee().real/tot,
            'BRmumu':   HVT.Zprimemm().real/tot,
            'BRtautau': HVT.Zprimetautau().real/tot,
            'BRnunu':   HVT.Zprimevv().real/tot,
            'BRuu':     HVT.Zprimeuu().real/tot,
            'BRdd':     HVT.Zprimedd().real/tot,
            'BRcc':     HVT.Zprimecc().real/tot,
            'BRss':     HVT.Zprimess().real/tot,
            'BRbb':     HVT.Zprimebb().real/tot,
            'BRtt':     HVT.Zprimett().real/tot,
            }
        entry['BRll'] = entry['BRee'] + entry['BRmumu']
        entry['BRqq'] = entry['BRuu']+entry['BRdd']+entry['BRcc']+entry['BRss']
        entry['BRjets'] = entry['BRqq'] + entry['BRbb'] + entry['BRtt']
    if Vprime=='Wprime':
        entry = {
            'M0': mass,
            'g': HVT.g_su2,
            'gv': gv,
            'ch': ch,
            'cl': cq,
            'GammaTot':tot,
            'BRWH':    HVT.WprimeHW().real/tot,
            'BRWZ':    HVT.WprimeWZ().real/tot,
            'BReve':   HVT.Wprimeeve().real/tot,
            'BRmvm':   HVT.Wprimemvm().real/tot,
            'BRtauvt': HVT.Wprimetauvt().real/tot,
            'BRud': HVT.Wprimeud().real/tot,
            'BRus': HVT.Wprimeus().real/tot,
            'BRcd': HVT.Wprimecd().real/tot,
            'BRcs': HVT.Wprimecs().real/tot,
            'BRtb': HVT.Wprimetb().real/tot,
            }
        entry['BRlnu'] = entry['BReve'] + entry['BRmvm']
        entry['BRqqbar'] = entry['BRud']+entry['BRus']+entry['BRcd']+entry['BRcs']
        entry['BRjets'] = entry['BRqqbar'] + entry['BRtb']
    return entry

def store_df(df, fname):
    df = df.astype('float32')
    df.to_csv(fname, index=False)
    print("Created", fname)

def get_masses():
    m_values = [1000, 2000, 3000, 4000]
    # m_values = [2000]
    return m_values

def get_gVs():
    gV_values = [1]
    return gV_values

def get_gFs():
    gF_values = []
    gF_values += list(np.arange(0.0, 0.1+0.01, 0.01))
    gF_values += list(np.arange(0.1, 1.6+0.1,  0.1))
    gF_values = np.array(sorted(set(gF_values + [-0.562, 0.146])))
    gF_values = [round(x,3) for x in gF_values]
    return gF_values

def get_gHs():
    gH_values = []
    gH_values += list(np.arange(-1.0, 1.0+0.01, 0.01))
    gH_values += list(np.arange(-4.0, 4.0+0.1,  0.1))
    gH_values += list(np.arange(-8.0, 8.0+0.5,  0.5))
    gH_values = np.array(sorted(set(gH_values + [-0.556, -2.928])))
    gH_values = [round(x,3) for x in gH_values]
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