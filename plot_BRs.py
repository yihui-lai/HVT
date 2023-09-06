import math, json, argparse
import numpy as np
import pandas as pd
from array import array
from model import *
import model as HVT

from tdrstyle import *
import tdrstyle as TDR

rt.gROOT.SetBatch(rt.kTRUE)
rt.gStyle.SetOptStat(0)
rt.gStyle.SetOptFit(0)

TDR.cmsTextSize = 0.6
TDR.cmsTextFont = 52
TDR.cmsText='Private work'
TDR.extraText=''
TDR.extraText2=''
TDR.cms_energy = ""
TDR.cms_lumi = ""

def filterCondition(data, infos):
    condition = None
    for key, value in infos.items():
        if condition is None:
            condition = data[key] == value
        else:
            condition &= data[key] == value
    return condition

def do_calculations(mass,gv,ch,cq,Vprime):
    HVT.MVz = mass
    HVT.gv = gv
    HVT.ch = ch
    HVT.cq = cq
    HVT.cl = HVT.cq
    HVT.c3 = HVT.cq
    HVT.gst = HVT.gv
    print(f'Calculating BR for mass: {mass} gv: {gv} cq: {cq} ch: {ch}')
    if Vprime=='Z':
        tot = HVT.ZprimeTot().real
    if Vprime=='W':
        tot = HVT.WprimeTot().real
    if tot == 0:
        return None
    if Vprime=='Z':
        entry = {
            'M0': mass,
            'g': HVT.g_su2,
            'gv': gv,
            'ch': ch,
            'cl': cq,
            'GammaTot':tot,
            'BRWW': HVT.ZprimeWW().real/tot,
            'BRhZ': HVT.ZprimeZH().real/tot,
            'BRll': (HVT.Zprimeee()+HVT.Zprimemm()).real/tot,
            'BRnunu': HVT.Zprimevv().real/tot,
            'BRtt': HVT.Zprimett().real/tot,
            'BRjets': (HVT.Zprimeuu()+HVT.Zprimedd()+HVT.Zprimecc()+HVT.Zprimess()+HVT.Zprimebb()+HVT.Zprimett()).real/tot,
            }
    if Vprime=='W':
        entry = {
            'M0': mass,
            'g': HVT.g_su2,
            'gv': gv,
            'ch': ch,
            'cl': cq,
            'GammaTot':tot,
            'BRWH': HVT.WprimeHW().real/tot,
            'BRWZ': HVT.WprimeWZ().real/tot,
            'BRlnu': (HVT.Wprimeeve()+HVT.Wprimemvm()).real/tot,
            'BRjets': (HVT.Wprimeud()+HVT.Wprimeus()+HVT.Wprimecd()+HVT.Wprimecs()+HVT.Wprimetb()).real/tot,
            }

    return entry

Vprime = 'Z'
modes = {
    'GammaTot': '#Gamma',
    'BRhZ': 'ZH',
    'BRWW': 'WW',
    'BRll': 'l#bar{l}',
    'BRnunu': '#nu#bar{#nu}',
    'BRjets': 'q#bar{q}',
    'BRtt': 't#bar{t}',
    }


Vprime = 'W'
modes = {
    'GammaTot': '#Gamma',
    'BRWH': 'WH',
    'BRWZ': 'WZ',
    'BRlnu': 'l#bar{#nu}',
    'BRjets': 'q#bar{q}',
    }

csv_file = f'BRs_{Vprime}prime.csv'
df = pd.read_csv(csv_file)


df_list = []
m_values = [1000, 2000, 3000, 4000]
gv_values = [1, 3]
gF_values = np.arange(-1.6, 1.7, 0.2)
gH_values = np.arange(-7.5, 7.6, 0.25)

# m_values = [1000]
# gv_values = [3]
# gF_values = np.arange(0, 1.7, 0.8)
# gH_values = np.arange(-7.5, 7.6, 1)

gF_values = [round(x,3) for x in gF_values]
gH_values = [round(x,3) for x in gH_values]

print(gF_values)
print(gH_values)

for mass in m_values:
    for gv in gv_values:
        for gF in gF_values:
            for gH in gH_values:
                ch = round(get_ch(gH=gH, gv=gv),5)
                cq = round(get_cq(gF=gF, gv=gv),5)
                infos = {'M0': mass, 'g': HVT.g_su2, 'gv': gv, 'ch': ch, 'cl': cq}
                condition = filterCondition(df, infos)
                if len(df[condition])!=0:
                    continue
                entry = do_calculations(mass,gv,ch,cq,Vprime)
                if entry == None:
                    continue
                df_list.append(pd.DataFrame([entry]))

df = pd.concat([df]+df_list, ignore_index=True)
df = df.astype('float32')
df.to_csv(csv_file, index=False)


ref_graph = rt.TGraph(1, array('d',[100]), array('d',[100]))
tdrDraw(ref_graph, "C", mcolor=rt.kBlack, lstyle=rt.kDashed)

for mode, name in modes.items():
    for mass in m_values:
        for gv in gv_values:
            graphs = {}
            for gF in gF_values:
                x_values = []
                brs = []
                for gH in gH_values:
                    ch = round(get_ch(gH=gH, gv=gv),5)
                    cq = round(get_cq(gF=gF, gv=gv),5)
                    infos = {'M0': mass, 'g': HVT.g_su2, 'gv': gv, 'ch': ch, 'cl': cq}
                    condition = filterCondition(df, infos)
                    if len(df[condition])==0:
                        continue
                    br = df[condition][mode].iloc[0]
                    # if gH
                    # x_values.append(gH*math.copysign(1, gF))
                    x_values.append(gH)
                    brs.append(br)
                graphs[gF] = rt.TGraph(len(x_values), array('d',x_values), array('d',brs))

            cname = f"{mode}_M{mass}_gv{gv}_{Vprime}prime"
            if 'BR' in mode:
                canv = tdrCanvas(cname, -8, 8, 1*1e-5, 2, "g_{H}", f"BR({Vprime}'#rightarrow {name})", square=True, iPos =0)
                canv.SetLogy(True)
                # leg = tdrLeg(0.7,0.65-(2+len(graphs)/2)*0.045,0.89,0.65)
                leg = tdrLeg(0.60,0.18,0.95,0.18+(1+len(graphs)/4)*0.045)
                leg.SetNColumns(2)
            else:
                canv = tdrCanvas(cname, -8, 8, 1*1e-1, 1e4, "g_{H}", f"{name}({Vprime}'#rightarrow 2X) [GeV]", square=True, iPos =0)
                canv.SetLogy(True)
                # leg = tdrLeg(0.7,0.65-(2+len(graphs)/2)*0.045,0.89,0.65)
                leg = tdrLeg(0.60,0.18,0.95,0.18+(1+len(graphs)/4)*0.045)
                leg.SetNColumns(2)
            
            latex = rt.TLatex()
            latex.SetNDC()
            latex.SetTextAngle(0)
            latex.SetTextColor(rt.kBlack)
            latex.SetTextFont(TDR.extraTextFont3)
            # latex.SetTextAlign(align_)
            latex.SetTextSize(0.035)
            latex.DrawLatex(0.2, 0.35, f"M({Vprime}') = {mass} GeV")
            latex.DrawLatex(0.2, 0.30, "g_{V} = "+str(gv))


            colors = {
                # rt.kPink
                # rt.kAzure+10,
                # rt.kBlue+1,
                # rt.kGray,
                # rt.kGreen+1, rt.kGreen,
                0.0: rt.kRed+1,
                0.2: rt.kOrange+1,
                0.4: rt.kOrange-2,
                0.6: rt.kGreen+1,
                0.8: rt.kGreen+2,
                1.0: rt.kAzure+7,
                1.2: rt.kAzure+2,
                1.4: rt.kViolet+7,
                1.6: 880,

            }

            ind = -1
            for gF, graph in graphs.items():
                pos = gF>=0
                ind += 1
                # color = colors[ind]
                color = colors[abs(gF)]
                marker = rt.kFullCircle if pos else rt.kFullTriangleUp
                lstyle = rt.kSolid if pos else rt.kDashed
                graph.SetLineWidth(2)
                tdrDraw(graph, "C", mcolor=color, marker=marker, msize=0.3, lstyle=lstyle)
                if pos:
                    leg.AddEntry(graph, 'g_{F}='+str(abs(gF)), 'l')
            leg.AddEntry(ref_graph, 'g_{F}<0', 'l')
            canv.SaveAs(cname+'.pdf')