#!/usr/bin/env python3
from runJobs import runJobs
from runJobs_ext import runJobs_ext
from merge_df import merge_df
from merge_df_ext import merge_df_ext
from createGraphs import createGraphs
from plot_BRs import plot
import argparse


def main(gflist, m_values):
    runJobs(runLocal=True, ncores=40, gflist=gflist, m_values=m_values)
    merge_df(overwrite=False, gflist=gflist, m_values=m_values)

def main_ext(gq12list, gq3list, m_values):
    runJobs_ext(runLocal=True, ncores=40, gq12list=gq12list, gq3list=gq3list, m_values=m_values)
    merge_df_ext(overwrite=False, gq12list=gq12list, gq3list=gq3list, m_values=m_values)
    #createGraphs(overwrite=False)
    #plot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run jobs with specified parameters.")
    
    # Define arguments
    parser.add_argument("--m_values", type=str, required=True, help="Comma-separated list of m values (e.g., 100,200,300)")
    parser.add_argument("--gf_range", type=str, required=False, help="Comma-separated list of gf range (e.g., 0,0.5)")
    parser.add_argument("--gq12_range", type=str, required=False, help="Comma-separated list of gf range (e.g., 0,0.5)")
    parser.add_argument("--gq3_range", type=str, required=False, help="Comma-separated list of gf range (e.g., 0,0.5)")

    # Parse arguments
    args = parser.parse_args()
    m_values = [int(value) for value in args.m_values.split(",")]
    if args.gf_range != None:
        gflist = [float(value) for value in args.gf_range.split(",")]
        main(gflist=gflist, m_values=m_values)
    elif args.gq12_range != None:
        gq12list = [float(value) for value in args.gq12_range.split(",")]
        gq3list = [float(value) for value in args.gq3_range.split(",")]
        main_ext(gq12list=gq12list, gq3list=gq3list, m_values=m_values)





