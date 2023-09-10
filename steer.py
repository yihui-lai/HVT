#!/usr/bin/env python3
from runJobs import runJobs
from merge_df import merge_df
from createGraphs import createGraphs
from plot_BRs import plot

def main():
    runJobs(runLocal=True, ncores=40)
    merge_df(overwrite=False)
    createGraphs(overwrite=False)
    plot()

if __name__ == "__main__":
    main()
