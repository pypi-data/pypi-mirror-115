
import numpy as np
import numba
from numba import prange , jit , njit
import os
import sys
def sh_b(A):
    t=list(np.asarray(A).shape)
    if len(t)==1:
        return t[0],1
    else:
        return t[0],t[1]
@jit(parallel=True,fastmath=True)
def kroneck(A,B):
    n,m = sh_b(A)
    p,k = sh_b(B)
    return np.array([[A[i,j]*B[s,r] for j in prange(m) for r in prange(k)] for i in prange(n) for s in prange(p)])

@jit(parallel=True,fastmath=True)

def hadamrd(A,B):
    n,m=sh_b(A)
    return np.asarray( [[A[i,j]*B[i,j]  for j in prange(m) ] for i in prange(n) ] )
@jit(parallel=True,fastmath=True)
def khatrirao(a,b):
    return  np.vstack([np.kron(a[:, k], b[:, k]) for k in prange(sh_b(b)[1])]).T
    
@jit(parallel=True, fastmath=True)
def LU(A):
    n=len(A)
    U,L= A.copy(),np.eye(n)
    for i in prange(n):
        for j in prange(i+1,n):
            L[j,i]=U[j,i]/U[i,i]
            U[j]=U[j]-L[j,i]*U[i]
    return L,U 
@jit(parallel=True,fastmath=True)
def Cholesky(A):
    n=len(A)
    H=A.copy()
    for i in prange(n-1):
        H[i,i]=np.sqrt(H[i,i])
        H[i+1:n,i]= H[i+1:n,i]/H[i,i]
        for j in prange(i+1,n):
            H[j:n,j]= H[j:n,j]- H[j:n,i]* H[j,i]
    H[-1,-1]=np.sqrt(H[-1,-1])
    H=np.tril(H).T
    return H


    
from pyccel.decorators import types
from pyccel.epyccel import epyccel

@types('float[:,:](order=F)','float[:,:](order=F)','float[:,:](order=C)')
def matmul_F(x,y,z):
    n,p=x.shape
    m=y.shape[1]

    for i in range(n):
        for j in range(m):
            z[i, j]  = 0.0
            for k in range(p):
                z[i, j] +=x[i, k] * y[k, j]

    return 0
dot_for=epyccel(matmul_F)



