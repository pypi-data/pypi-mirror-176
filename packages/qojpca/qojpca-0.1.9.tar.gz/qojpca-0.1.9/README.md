
# qojpca

[![codecov](https://codecov.io/gh/cryckx/qojpca/branch/main/graph/badge.svg?token=qojpca_token_here)](https://codecov.io/gh/cryckx/qojpca)
[![CI](https://github.com/cryckx/qojpca/actions/workflows/main.yml/badge.svg)](https://github.com/cryckx/qojpca/actions/workflows/main.yml)

QOJPCA (Quasi-orthogonal Joint Principal Component Analysis) package allows for improving the orthogonality between linear bases computed through Principal Component Analysis.  

## Install it from PyPI

The package has been released on PyPip and can be installed through. 

```bash
pip install qojpca
```

## Requirements

Numpy, Scikit

## Usage

The package can be used by importing the "base" module into your python script as:

```py
from qojpca import base
""" 
QOJPCA can be computed using the qojpca static function
l_p (resp. l_q): number of latent variables for P (resp. Q)
l: regularization parameter. Note that it is multiplied by the largest eigenvalue of XX^T
"""
P_vals,Q_vals,P,Q = base.qojpca(X,Y,l_p,l_q,l)
```

Or by using the command line interface. For example 

```bash
$ python -m qojpca X.npy Y.npy --l_x 10 --l_y 10 --output_directory output --regularization 100
```
where:
l_p (resp. l_q) are the number of latent variables for linear basis P (resp. Q).
