#!/usr/bin/env python3

import os, math
import ROOT as rt
from collections import OrderedDict
from array import array
from utils import decay_modes, get_masses, get_gVs, get_gFs, get_gHs, benchmarks

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

colors = {
    0.0: rt.kRed+1,
    0.2: rt.kOrange+1,
    0.4: rt.kOrange-2,
    0.6: rt.kGreen+1,
    0.8: rt.kGreen+2,
    1.0: rt.kAzure+7,
    1.2: rt.kAzure+2,
    1.4: rt.kViolet+7,
    1.6: 880,

    'BRll': rt.kRed+1,
    'BRnunu': rt.kOrange+1,
    'BRjets': rt.kGreen+2,
    'BRhZ': rt.kAzure+2,
    'BRWW': rt.kMagenta+1,

    'BRWH': rt.kAzure+2,
    'BRWZ': rt.kMagenta+1,
    'BRlnu': rt.kRed+1,
    # rt.kPink
    # rt.kAzure+10,
    # rt.kBlue+1,
    # rt.kGray,
    # rt.kGreen+1, rt.kGreen,
    }

def createCanvas(cname, isBR, decayName, Vprime, mass, nEntries, nEntries2, y_min = 2*1e-6, extra_info=[]):
    if isBR:
        canv = tdrCanvas(cname, -3.5, 3.5, y_min, 2, "g_{H} #times sign(g_{F})", f"BR({Vprime}'#rightarrow {decayName})", square=True, iPos =0)
    else:
        canv = tdrCanvas(cname, -3.5, 3.5, 1*1e-1, 1e4, "g_{H} #times sign(g_{F})", f"{decayName}({Vprime}'#rightarrow 2X) [GeV]", square=True, iPos =0)
    canv.SetLogy(True)
    leg = tdrLeg(0.63,0.15,0.95,0.15+(2+nEntries)*0.05)
    if nEntries>5:
        leg = tdrLeg(0.60,0.15,0.95,0.15+(1+nEntries/2)*0.05)
        leg.SetNColumns(2)
    leg2 = tdrLeg(0.25,0.18,0.50,0.18+(1+nEntries2)*0.045)
    leg3 = tdrLeg(0.37,0.18,0.55,0.18+(1+nEntries2)*0.045)
    # leg3 = tdrLeg(0.75,0.18,0.95,0.18+(3)*0.045)
    
    tdrHeader(leg, f"M({Vprime}') = {mass} GeV")
    latex = rt.TLatex()
    # latex.SetNDC()
    # latex.SetTextAngle(0)
    # latex.SetTextColor(rt.kBlack)
    # latex.SetTextFont(TDR.extraTextFont3)
    # # latex.SetTextAlign(align_)
    # latex.SetTextSize(0.035)
    # latex.DrawLatex(0.25, 0.35, f"M({Vprime}') = {mass} GeV")
    # for ind,info in enumerate(extra_info):
    #     latex.DrawLatex(0.2, 0.35-0.05*(ind+1), info)
    return canv, leg, leg2, leg3, latex


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
    canv, leg, leg2, leg3, latex = createCanvas(cname, True, "XY", 'V', mass, nEntries=len(decays)-2, nEntries2=3, y_min=y_min)
    for decay, info in decays.items():
        color = info['color']
        lstyle = rt.kSolid
        Vprime = 'Zprime' if decay != 'BRlnu' else 'Wprime'
        gname = f'{Vprime}_{mass}_{gv}_{decay}_{gf}'
        graph = graphs[gname]
        if not graph:
            print(f'Missing {gname}')
            continue
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


def plot():
    m_values = get_masses()
    gV_values = get_gVs()
    gF_values = get_gFs()
    gH_values = get_gHs()
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

    # for mode, decayName in modes.items():
        # for mass in m_values:
            # for gv in gv_values:
                # 
                # cname = f"{mode}_M{mass}_gv{gv}_{Vprime}prime"
                # canv, leg, leg2, leg3, latex = createCanvas(cname, 'BR' in mode, decayName, Vprime, mass, len(gF_values), 0)
    # 
                # for gF in gF_values:
                    # gname = f"{mode}_{mass}_{gv}_{gF}"
                    # graph = graphs[gname]
                    # pos = gF>=0
                    # color = colors[abs(gF)]
                    # marker = rt.kFullCircle if pos else rt.kFullTriangleUp
                    # lstyle = rt.kSolid if pos else rt.kDashed
                    # graph.SetLineWidth(2)
                    # tdrDraw(graph, "C", mcolor=color, marker=marker, msize=0.3, lstyle=lstyle)
                    # if pos:
                        # leg.AddEntry(graph, 'g_{F}='+str(abs(gF)), 'l')
                # if any([x<0 for x in gF_values]):
                    # leg.AddEntry(ref_graph, 'g_{F}<0', 'l')
                # canv.SaveAs(f'pdfs/{cname}.pdf')
                # canv.SaveAs(f'{cname}.pdf')
    
    # for mass in m_values:
    #     for gv in gv_values:
    #         cname = f"BRs_M{mass}_gv{gv}_{Vprime}prime"
    #         canv, leg, leg2, leg3, latex = createCanvas(cname, True, "XY", Vprime, mass, len(modes)-2, 2, y_min=1*1e-5)
    #         lines = {}
    #         for mode, decayName in modes.items():
    #             if 'GammaTot' in mode: continue
    #             if 'BRtt' in mode: continue
    #             is_VV = any([x in mode for x in ['W','Z','H','h']])
    #             color = colors[mode]
    #             # for gF in [0.6, 0.2, 0.0]:
    #             for gF in [0.6]:
    #                 if gF==0.0 and not is_VV:
    #                     continue
    #                 lstyle = rt.kSolid if gF==0.2 else (rt.kDotted if gF==0.6 else 6)
    #                 gname = f"{mode}_{mass}_{gv}_{gF}"
    #                 graph = graphs[gname]
    #                 graph.SetLineWidth(2)
    #                 tdrDraw(graph, "C", lcolor=color, lstyle=lstyle)
    #                 if gF==0.2:
    #                     leg.AddEntry(graph, decayName, 'l')
    #                 if mode == list(modes.keys())[1]:
    #                     graphs[f'reference_{gF}'] = rt.TGraph(1, array('d',[100]), array('d',[100]))
    #                     tdrDraw(graphs[f'reference_{gF}'], "C", lcolor=rt.kBlack, lstyle=lstyle)
    #                     leg3.AddEntry(graphs[f'reference_{gF}'], 'g_{F} = '+str(gF), 'l')
    #                 # if any([x<0 for x in gF_values]):
    #                 #     leg.AddEntry(ref_graph, 'g_{F}<0', 'l')
    #             for model, benchmark in benchmarks.items():
    #                 if not 'A' in model:
    #                     continue
    #                 if 'C' in model and not is_VV:
    #                     continue
    #                 marker = rt.kFullCircle if 'A' in model else (rt.kFullTriangleUp if 'B' in model else rt.kFullSquare)
    #                 gname = f"{mode}_{mass}_{model}"
    #                 graph_model = graphs[gname]
    #                 tdrDraw(graph_model, "P", mcolor=color, marker=marker)
    #                 if mode == list(modes.keys())[1]:
    #                     graph_model_ref = graphs['reference_'+model]
    #                     tdrDraw(graph_model_ref, "C", mcolor=rt.kBlack, marker=marker)
    #                     leg2.AddEntry(graph_model_ref, f'model {model[-1]}', 'p')
    #         # canv.SaveAs(f'pdfs/{cname}.pdf')
    #         canv.SaveAs(f'{cname}_modelA.pdf')

def main():
    plot()

if __name__ == "__main__":
    main()