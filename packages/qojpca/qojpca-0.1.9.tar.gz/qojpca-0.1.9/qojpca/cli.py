"""CLI interface for qojpca project.
"""
import argparse
#import cupy as np
import numpy as np
from qojpca import base
from pathlib import Path
import os 

def run_qojpca(args):
    P= np.array([])
    Q= np.array([])
    if(len(args.matrices) == 2):
        X,Y = load_matrices(args)
    if(len(args.matrices) == 4):
        X,Y,P,Q = load_matrices(args)
    if args.l_x is None:
        print("INFO: computing "+str(X.shape[1])+" latent variable for the first matrix.")
        l_p = X.shape[1]
    if args.l_y is None:
        print("INFO: computing "+str(Y.shape[1])+" latent variable for the second matrix.")
        l_q = Y.shape[1]
    if(args.l_x is not None):
        l_p = int(args.l_x)
    if(args.l_y is not None):
        l_q = int(args.l_y)
    l = 1.0
    if(args.penalization is not None):
        l = float(args.penalization)
    P_vals,Q_vals,P,Q = base.qojpca(X,Y,l_p,l_q,P,Q,l)
    if(not os.path.isdir(args.output_folder)):
        os.makedirs(args.output_folder)
    np.save(args.output_folder+"/P.npy",P)
    np.save(args.output_folder+"/P_vals.npy",P_vals)
    np.save(args.output_folder+"/Q.npy",Q)
    np.save(args.output_folder+"/Q_vals.npy",Q_vals)

    
def run_jpca(args):
    X,Y =load_matrices(args)
    if args.l_x is None:
        print("INFO: computing "+str(X.shape[1])+" latent variable for the first matrix.")
        l_x = X.shape[1]
    if args.l_y is None:
        print("INFO: computing "+str(Y.shape[1])+" latent variable for the second matrix.")
        l_y = Y.shape[1]
    if(args.l_x is not None):
        l_x = int(args.l_x)
    if(args.l_y is not None):
        l_y = int(args.l_y)
        
    P_vals,Q_vals,P,Q = base.jpca(X,Y,l_x,l_y)
    if(not os.path.isdir(args.output_folder)):
        os.makedirs(args.output_folder)
    np.save(args.output_folder+"/P.npy",P)
    np.save(args.output_folder+"/P_vals.npy",P_vals)
    np.save(args.output_folder+"/Q.npy",Q)
    np.save(args.output_folder+"/Q_vals.npy",Q_vals)
    
def load_matrices(args):
    matrices = args.matrices
    if(len(matrices) == 2):
        X = np.load(matrices[0])
        Y = np.load(matrices[1])
        print("INFO: matrices successfully loaded")
        return X,Y
    if(len(matrices) == 4):
        X = np.load(matrices[0])
        Y = np.load(matrices[1])
        P = np.load(matrices[2])
        Q = np.load(matrices[3])
        print("INFO: matrices successfully loaded")
        return X,Y,P,Q
    print("ERROR: wrong number of matrices provided")
    return 0

def add_learning_arguments(parser):
    parser.add_argument('matrices', metavar='M', type=str, nargs="+",
                    help='matrices to be processed')
    parser.add_argument('--l_x', 
                    help='number of latent variables to compute for the first matrix, default is 50')
    parser.add_argument('--l_y',
                    help='number of latent variables to compute for the second matrix, default is 50')
    parser.add_argument('--output_folder',required=True,
                    help='output directory')
    parser.add_argument('--penalization',
                    help='penalization value, that is lambda in the paper')              
    args = parser.parse_args()
    return args

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m qojpca` and `$ qojpca `.
    """
    parser = argparse.ArgumentParser(description='QOJPCA command line interface.')
    parser.add_argument('command', choices=['qojpca', 'jpca', 'extractFeatures'])
    
    args = parser.parse_args()
    
    if(args.command == "qojpca"):
        args= add_learning_arguments(parser)
        run_qojpca(args)
        
    if(args.command == "qojpca"):
        args=add_learning_arguments(parser)
        run_jpca(args)
        


    
