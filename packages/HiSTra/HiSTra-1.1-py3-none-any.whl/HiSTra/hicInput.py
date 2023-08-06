#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Library for reading all args from the command line.

Obtaining all path: 1..hic file path；2. juice_tool path；3. output path；4. deDoc path

Available functions:
- path_get: From command line, reading all path inf.
- usage: Print usage.
- hic2mat: Dumping .hic file with juice_tool, and save them into the output path/Matrix_from_hic, return the path/Matrix_from_hic.
"""

import sys
import getopt
import argparse
import os
import itertools

def hic2mat(hicfile,matrix_path,juice_path):
    """Transfer the hic file to 276 matrix files.
    Input:
        - hicfile, the abspath of hic file.
        - matrix_path, the output path user set. If empty, use current work directory.
        - juice_path, the juicetools absolute path.
    Output:
        Return Matrix_from_hic dirpath. For example, outputpath(user_set)/Matrix_from_hic/sample_name
    """
    chrname=[str(i) for i in range(1,23)]
    chrname.append("X")    
    juice="nohup java -jar "+juice_path 
    R500="_500k.txt"
    R100="_100k.txt"
    fl = os.path.basename(hicfile).split(".")[0] # get sample name
    print(f"--------- The hic file path is {hicfile}. ---------")
    outdir500k = os.path.join(matrix_path,'Matrix_from_hic',fl,"500k")
    if not os.path.exists(outdir500k):
        os.makedirs(outdir500k)
        print("Create outdir in resuloutin 500k...")
    outdir100k = os.path.join(matrix_path,'Matrix_from_hic',fl,"100k")
    if not os.path.exists(outdir100k):
        os.makedirs(outdir100k)
        print("Create outdir in resuloutin 100k...")
    process, cnt = 0, 0
    for chri,chrj in itertools.combinations_with_replacement(chrname,2):
        if chrj==chri:
            print(f"--------- We are dumpping {fl} sample chromosome pairs {chri,chrj}.")
            print(f"--------- Process is completed {process*100/253}%... ---------") # for process
            process+=22-cnt
            cnt+=1
        
        part1 = ' '.join([juice,'dump observed NONE',hicfile,chri,chrj,'BP 500000',outdir500k])
        part2 = "/chr"+chri+"_chr"+chrj+R500 + ' >>juicer_500k_log.txt 2>&1 &' 
        command_500k = part1 + part2
        
        part1 = ' '.join([juice,'dump observed NONE',hicfile,chri,chrj,'BP 100000',outdir100k])
        part2 = "/chr"+chri+"_chr"+chrj+R100 + ' >>juicer_100k_log.txt 2>&1 &' 
        command_100k = part1 + part2
        # print(command_100k)
        os.system(command_500k)
        os.system(command_100k)
    print('You can check juicer_100k_log.txt and juicer_500k_log.txt in current directory if any error occurs.')
            
    return os.path.join(matrix_path,'Matrix_from_hic',fl)

    part1 = ' '.join(juice,'dump observed NONE',hicfile,chri,chrj,'BP 500000',outdir500k)
    part2 = "/chr"+chri+"_chr"+chrj+R500 + ' >>juicer_500k_log.txt 2>&1 &' 