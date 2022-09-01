#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 11:15:52 2022

@author: lillycummins

Motive: given an abricate summary file, reformat file with highest hit per gene for phandango visualisation
"""

import argparse
import os
import time
import pandas as pd

parser = argparse.ArgumentParser(description = 'Format ABRicate summary for phandango visualisation.')
parser.add_argument("--input", "-i", type=str, required=True) #abricate summary.tsv file
parser.add_argument("--output", "-o", type=str, required=True) #output file name
parser.add_argument("--cutoff", "-c", type=int, required=True) #cut off value to binarise data
args = parser.parse_args()

#check user input
if not os.path.isfile(args.input):
    print('Cannot find input summary file.')
    print('Exiting')

#if output is left empty make file name with time stamp
if args.output == None:
    args.output = os.path.join(os.getcwd(),'ABRicate2Phandango_'+time.strftime('%Y%m%d_%H%M')) + os.sep
elif not os.path.isdir(args.output):
    os.makedirs(args.output)

with open(args.input) as sumfile:
    df = pd.read_csv(sumfile, sep='\t') #load summary file as a dataframe
    df = df.replace('.',0) #replace entries where no match was found with 0
    df.drop('NUM_FOUND', inplace=True, axis=1) #remove number found column
    headings = df.columns.values.tolist() #take column headers 
    genes = headings[1:] #create list of genes to iterate through
    for gene in genes: #for each gene  in column headings
        gene_coverage_list = df[gene].tolist() #take a list of observed coverage of gene per assembly
        final_coverage_list=[]
        for coverage in gene_coverage_list: #need to check if there is one entry per coverage reported
            if type(coverage) == str: #this means there are multiple hits reported in one assembly
                new_coverage_list=[]
                split_coverages=coverage.split(";")
                new_coverages = [float(i) for i in split_coverages]
                highest_coverage = max(new_coverages) #take highest hit per gene
                final_coverage_list.append(highest_coverage)
            else:
                final_coverage_list.append(coverage)     
        for i in range(0,len(final_coverage_list)): #binarise data
            if (final_coverage_list[i] >= args.cutoff) == True:
                final_coverage_list[i] = 1 
            else:
                final_coverage_list[i] = 0
                continue
        df[gene]= final_coverage_list #replace column with list that has processed hits
      
df.to_csv(args.output+".tsv", sep="\t", index=False)