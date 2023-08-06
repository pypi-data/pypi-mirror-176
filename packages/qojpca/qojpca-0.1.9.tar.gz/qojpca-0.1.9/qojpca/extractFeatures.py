# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import os
import igl
import numpy as np
import pandas as pd
from pathlib import Path
#%%
def findObjPaths(directory):
    list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if(file.endswith(".obj")):
                list.append(os.path.join(root, file))
    return list

def computeMean(pathToFolder : str):
    listPath = findObjPaths(pathToFolder)
    return computeMean(listPath)

def computeMean(listPath : list):
    v_bar, f_bar = igl.read_triangle_mesh(listPath[0])
    N = len(v_bar)
    M = len(listPath)
    print(M)
    i = 0
    for obj in listPath:
        v_i, f_i = igl.read_triangle_mesh(obj)
        v_bar = v_bar + v_i
        if( i%10 ==0):
            print(i%M)
        i= i+1
    v_bar = v_bar / M
    return v_bar,f_bar

def computeMean(arrays :np.array):
    v_bar = np.array(arrays[0])
    M = np.shape(arrays)[0]
    print(M)
    for v_i in arrays:
        v_bar = v_bar + v_i
    v_bar = v_bar / M
    return v_bar

def readPositions(listPath: list):
    print("readPositions()")
    v_bar, f_bar = igl.read_triangle_mesh(listPath[0])
    N = len(v_bar)
    M = len(listPath)
    print(M)
    i = 0
    df = pd.DataFrame()
    print(df)
    for obj in listPath:
        objPath = Path(obj)
        v_i, f_i = igl.read_triangle_mesh(obj)
        expressionID = str(os.path.basename(objPath)).split(".")[0]
        if not expressionID in df.columns:
            df[expressionID] = ""
            df[expressionID] = df[expressionID].astype(object)
        df.at[str(os.path.basename(objPath.parents[1])),expressionID]=[v_i]
        if( i%10 ==0):
            print(i%M)
        i= i+1
    return df
    
    
def computeUis(pathToFolder):
    listPath = findObjPaths(pathToFolder)
    u_is = np.zeros(shape=(0,N*3))
    v_bar,f_bar = computeMean(listPath)
    for obj in listPath:
        v_i, f_i = igl.read_triangle_mesh(obj)
        ui = v_bar - v_i
        ui = ui.flatten(order='F').reshape(1,-1)
        u_is = np.append(u_is , ui, axis = 0 )
    return u_is

#%%

def computeKdirs(pathToFolder):
    
    k_dirs = np.zeros(shape=(0,N*12))
    
    for obj in listPath:
        v_i, f_i = igl.read_triangle_mesh(obj)
        v1, v2, k1, k2 = igl.principal_curvature(v_i, f_i)
        v1v1t = np.zeros((np.shape(v1)[0],6))
        v2v2t = np.zeros((np.shape(v1)[0],6))
        for i in range(0, np.shape(v1)[0]):
            tmp = v1[i].reshape(3,1)
            vivit = tmp.dot(tmp.transpose())
            vivit = vivit[np.triu_indices(3)] 
            v1v1t[i] = vivit
        for i in range(0, np.shape(v2)[0]): 
            tmp = v2[i].reshape(3,1)
            vivit = tmp.dot(tmp.transpose())
            vivit = vivit[np.triu_indices(3)] 
            v2v2t[i] = vivit
            
        
        vs = np.append(v1v1t , v2v2t, axis = 1 )
        vs = vs.flatten(order='F').reshape((1,-1))
    
        k_dirs = np.append(k_dirs , vs, axis = 0 )
        
    return k_dirs


def computeK1K2s(pathToFolder):

    k1k2s = np.zeros(shape=(0,N*2))
    
    for obj in listPath:
        v_i, f_i = igl.read_triangle_mesh(obj)
        v1, v2, k1, k2 = igl.principal_curvature(v_i, f_i)
        k1 = np.reshape(k1,(-1,1))
        k2 = np.reshape(k2,(-1,1))
        k1k2 = np.append(k1 , k2, axis = 1 )
        k1k2 = k1k2.flatten(order='F').reshape((1,-1))
        k1k2s = np.append(k1k2s , k1k2, axis = 0 )
        
    return k1k2s


