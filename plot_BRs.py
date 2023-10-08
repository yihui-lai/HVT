#!/usr/bin/env python3

import math
import ROOT as rt
from collections import OrderedDict
from array import array
from utils import decay_modes, get_masses, get_gVs, get_gFs, benchmarks

from tdrstyle import *
import tdrstyle as TDR

rt.gROOT.SetBatch(rt.kTRUE)
rt.gStyle.SetOptStat(0)
rt.gStyle.SetOptFit(0)

TDR.cmsTextSize = 0.6
TDR.cmsTextFont = 42
# TDR.cmsText='Private work'
TDR.cmsText='HVT model'
TDR.extraText=''
TDR.extraText2=''
TDR.cms_energy = ""
TDR.cms_lumi = ""

# colors = {
#     0.0: rt.kRed+1,
#     0.2: rt.kOrange+1,
#     0.4: rt.kOrange-2,
#     0.6: rt.kGreen+1,
#     0.8: rt.kGreen+2,
#     1.0: rt.kAzure+7,
#     1.2: rt.kAzure+2,
#     1.4: rt.kViolet+7,
#     1.6: 880,
#     -0.562: rt.kBlack,

#     'BRll': rt.kRed+1,
#     'BRnunu': rt.kOrange+1,
#     'BRjets': rt.kGreen+2,
#     'BRhZ': rt.kAzure+2,
#     'BRWW': rt.kMagenta+1,

#     'BRWH': rt.kAzure+2,
#     'BRWZ': rt.kMagenta+1,
#     'BRlnu': rt.kRed+1,
#     # rt.kPink
#     # rt.kAzure+10,
#     # rt.kBlue+1,
#     # rt.kGray,
#     # rt.kGreen+1, rt.kGreen,
#     }

def createCanvas(cname, isBR, decayName, Vprime, mass, nEntries, nEntries2, y_min = 2*1e-6, extra_info=[]):
    if isBR:
        canv = tdrCanvas(cname, -3.5, 3.5, y_min, 2, "g_{H} #times sign(g_{F})", f"BR({Vprime}'#rightarrow {decayName})", square=True, iPos =0)
    else:
        canv = tdrCanvas(cname, -3.5, 3.5, 1*1e-3, 1e4, "g_{H} #times sign(g_{F})", f"{decayName}({Vprime}'#rightarrow 2X) [GeV]", square=True, iPos =0)
    canv.SetLogy(True)
    leg = tdrLeg(0.63,0.18,0.95,0.18+(2+nEntries)*0.05)
    if nEntries>5:
        leg = tdrLeg(0.60,0.18,0.95,0.18+(1+nEntries/2)*0.05)
        leg.SetNColumns(2)
    leg2 = tdrLeg(0.25,0.18,0.50,0.18+(1+nEntries2)*0.045)
    
    tdrHeader(leg, f"M({Vprime}') = {mass} GeV")
    # latex = rt.TLatex()
    # latex.SetNDC()
    # latex.SetTextAngle(0)
    # latex.SetTextColor(rt.kBlack)
    # latex.SetTextFont(TDR.extraTextFont3)
    # # latex.SetTextAlign(align_)
    # latex.SetTextSize(0.035)
    # latex.DrawLatex(0.25, 0.35, f"M({Vprime}') = {mass} GeV")
    # for ind,info in enumerate(extra_info):
    #     latex.DrawLatex(0.2, 0.35-0.05*(ind+1), info)
    return canv, leg, leg2


def plot_BR_per_model(graphs, mass, model):
    gv, gf = 1, benchmarks[model]['gf']
    cname = f'BRs_M{mass}_{model}'

    decays = OrderedDict([
        ('BRhZ',   {'color': rt.kViolet+2, 'leg': 'VH/VV'}),
        ('BRjets', {'color': rt.kAzure+2,  'leg': "qq/qq'"}),
        ('BRnunu', {'color': rt.kGreen+2,  'leg': '#nu#nu'}),
        ('BRlnu',  {'color': rt.kOrange+1, 'leg': 'l#nu'}),
        ('BRll',   {'color': rt.kRed+1,    'leg': 'll'}),
        ]) 
    y_min=1*1e-5
    gh, gf = benchmarks[model]['gh'], benchmarks[model]['gf']
    x_model = gh*math.copysign(1, gf)
    line = rt.TLine(x_model, y_min, x_model, 2)
    canv, leg, leg2 = createCanvas(cname, True, "XY", 'V', mass, nEntries=len(decays)-2, nEntries2=3, y_min=y_min)
    for decay, info in decays.items():
        color = info['color']
        lstyle = rt.kSolid
        Vprime = 'Zprime' if decay != 'BRlnu' else 'Wprime'
        gname = f'{Vprime}_{mass}_{gv}_{decay}_{gf}'
        if not gname in graphs:
            print(f'Missing {gname}')
            continue
        graph = graphs[gname]
        graph.SetLineWidth(2)
        tdrDraw(graph, "C", lcolor=color, lstyle=lstyle)
        leg.AddEntry(graph, info['leg'], 'l')
        marker = rt.kFullCircle
        gname = f'{Vprime}_{mass}_{model}_{decay}'
        graph_model = graphs[gname]
        tdrDraw(graph_model, "P", mcolor=color, marker=marker)
    lstyle = rt.kDashed
    tdrDrawLine(line,lcolor=rt.kBlack, lstyle=lstyle, lwidth=2)
    graphs['reference_'+model].SetLineWidth(2)
    tdrDraw(graphs['reference_'+model], "C", mcolor=rt.kBlack, lstyle=lstyle)
    leg2.AddEntry(graphs['reference_'+model], f'Model {model[-1]}', 'lp')
    ref_obj = rt.TLine()
    leg2.AddEntry(ref_obj, 'g_{F} = '+f'{gf}', '')
    leg2.AddEntry(ref_obj, 'g_{H} = '+f'{gh}', '')
    canv.SaveAs(f'pdfs/{cname}.pdf')


def plot_gf_graphs(graphs, Vprime, mass, gv, decay, decayName):
    cname = f"{decay}_M{mass}_gv{gv}_{Vprime}"

    gF_values = {
        0.0:  rt.kViolet+7,
        0.02: rt.kAzure+2,
        0.05: rt.kAzure+7,
        0.1:  rt.kGreen+2,
        0.2:  rt.kGreen+1,
        0.6:  rt.kOrange-2,
        1.0:  rt.kOrange+1,
        1.4:  rt.kRed+1,
    }
    isVV = any([x in decay for x in ['W','Z','H','h']])
    canv, leg, _ = createCanvas(cname, 'BR' in decay, decayName, Vprime.replace('prime',''), mass, len(gF_values), 0, y_min=1e-08)
    for gf, color in gF_values.items():
        if not isVV and gf==0:
            gf= get_gFs()[2]
        gname = f'{Vprime}_{mass}_{gv}_{decay}_{gf}'
        graph = graphs[gname]
        if not graph:
            print(f'Missing {gname}')
            continue
        graph.SetLineWidth(2)
        tdrDraw(graph, "C", lcolor=color, lstyle=rt.kSolid)
        leg.AddEntry(graph, 'g_{F}='+str(gf), 'l')
    canv.SaveAs(f'pdfs/{cname}.pdf')

def plot():
    m_values = get_masses()
    gV_values = get_gVs()
    gF_values = get_gFs()
    f_ = rt.TFile(f'graphs.root')

    graphs = {}
    graphs['reference'] = rt.TGraph(1, array('d',[100]), array('d',[100]))
    for model in benchmarks.keys():
        graphs['reference_'+model] = rt.TGraph(1, array('d',[100]), array('d',[100]))
    
    for Vprime, decays in decay_modes.items():
        for mass in m_values:
            for gv in gV_values:
                for decay in decays:
                    for gf in gF_values:
                        gname = f'{Vprime}_{mass}_{gv}_{decay}_{gf}'
                        graphs[gname] = f_.Get(gname)
            for model in benchmarks:
                for decay in decays:
                    gname = f'{Vprime}_{mass}_{model}_{decay}'
                    graphs[gname] = f_.Get(gname)
    f_.Close()

    tdrDraw(graphs['reference'], "C", mcolor=rt.kBlack, lstyle=rt.kDashed)

    for model in benchmarks.keys():
        for mass in m_values:
            plot_BR_per_model(graphs, mass, model)

    for Vprime, decays in decay_modes.items():
        for mass in m_values:
            for gv in gV_values:
                for decay,decayName in decays.items():
                    plot_gf_graphs(graphs, Vprime, mass, gv, decay, decayName)

def main():
    plot()

if __name__ == "__main__":
    main()