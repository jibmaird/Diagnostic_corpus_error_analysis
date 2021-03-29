#!/usr/bin/python
# -*- coding: utf-8 -*-
# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2001, 2019. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# *****************************************************************

'''
Created on Jan 11, 2021

@author: DAVIDMARTINEZIRAOLA

Example: ./brateval_xval.py /aitu-stor/ajimeno/ai4eye/ai4eye-nlp/experiments/ner/current /aitu-stor/ajimeno/ai4eye/ai4eye-nlp/data
'''

import sys
import subprocess
import re

def read_and_add_scores(Eval):
    Scores = {}
    for eval in Eval:
        ELine = eval.split("\n")
        for e in ELine:
            G = e.split("|")
            if (len(G)>1):
                p = re.compile("^[\d\.]+$")
                if p.match(G[1]):
                    if G[0] in Scores:
                        Scores[G[0]]["tp"] += int(G[1])
                        Scores[G[0]]["fp"] += int(G[2])
                        Scores[G[0]]["fn"] += int(G[3])
                    else:
                        Score = {"tp": int(G[1]), "fp": int(G[2]), "fn": int(G[3])}
                        Scores[G[0]] = Score
    return Scores

def compute_and_print_combined(Scores):
    print "Folders combined:"
    Eval_scores = {}
    for type in sorted(Scores):
        p = float(Scores[type]["tp"]) / (float(Scores[type]["tp"]) + float(Scores[type]["fp"]))
        r = float(Scores[type]["tp"]) / (float(Scores[type]["tp"]) + float(Scores[type]["fn"]))
        f = 2 * p * r / (p + r)
        print type + "|" + str(Scores[type]["tp"]) + "|" + str(Scores[type]["fp"]) + "|" + str(Scores[type]["fn"]) + "|" + str(round(p,4)) + "|" + str(round(r,4)) + "|" + str(round(f,4))
        Score = {"p":p, "r":r, "f":f}
        Eval_scores[type] = Score
    return Eval_scores

def compute_sd(Eval,Eval_scores):
    Eval_sd = {}
    for eval in Eval:
        ELine = eval.split("\n")
        for e in ELine:
            G = e.split("|")
            if (len(G)>1):
                p = re.compile("^[\d\.]+$")
                if p.match(G[1]):
                    p_sd = ((float(Eval_scores[G[0]]["p"]) - float(G[4])) ** 2) / 10
                    r_sd = ((float(Eval_scores[G[0]]["r"]) - float(G[5])) ** 2) / 10
                    f_sd = ((float(Eval_scores[G[0]]["f"]) - float(G[6])) ** 2) / 10
                    if G[0] in Eval_sd:
                        Eval_sd[G[0]]["p_sd"] += p_sd
                        Eval_sd[G[0]]["r_sd"] += r_sd
                        Eval_sd[G[0]]["f_sd"] += f_sd
                    else:
                        Score = {"p_sd":p_sd, "r_sd":r_sd, "f_sd":f_sd}
                        Eval_sd[G[0]] = Score
    return Eval_sd

def main():
    pred_d = sys.argv[1]
    gold_d = sys.argv[2]
    exact_match = sys.argv[3]

    Eval = []
    for i in range(10):
        cmd = "java -cp /aitu-stor/tools/brateval/target/BRATEval-1.1.0.jar au.com.nicta.csp.brateval.CompareEntities " 
        cmd += pred_d + "/" + str(i) + "/prediction_only " + gold_d + "/" + str(i) + "/data/testing "
        cmd += exact_match

        Eval.append(subprocess.check_output(cmd, shell=True))

    Scores = read_and_add_scores(Eval)
    Eval_scores = compute_and_print_combined(Scores)
    Eval_sd = compute_sd(Eval,Eval_scores)

    print "Standard deviation:";
    for type in sorted(Eval_sd):
        print type + "|" + str(round(Eval_sd[type]["p_sd"],4)) + "|" + str(round(Eval_sd[type]["r_sd"],4)) + "|" + str(round(Eval_sd[type]["f_sd"],4))

if __name__ == "__main__":
    main()
