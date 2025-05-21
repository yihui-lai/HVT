#!/usr/bin/env python3
from runJobs import runJobs
from merge_df import merge_df
from createGraphs import createGraphs
from plot_BRs import plot
import argparse


def main(gfstart, gfend, m_values):
    runJobs(runLocal=True, ncores=40, gfstart=gfstart, gfend=gfend, m_values=m_values)
    merge_df(overwrite=False, gfstart=gfstart, gfend=gfend, m_values=m_values)
    #createGraphs(overwrite=False)
    #plot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run jobs with specified parameters.")
    
    # Define arguments
    parser.add_argument("--gfstart", type=float, required=True, help="Start value for gf")
    parser.add_argument("--gfend", type=float, required=True, help="End value for gf")
    parser.add_argument("--m_values", type=str, required=True, help="Comma-separated list of m values (e.g., 100,200,300)")
    
    # Parse arguments
    args = parser.parse_args()
    m_values = [int(value) for value in args.m_values.split(",")]
    main(gfstart=args.gfstart, gfend=args.gfend, m_values=m_values)





