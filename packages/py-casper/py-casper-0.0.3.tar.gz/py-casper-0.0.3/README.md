# CASPER (Concentration And Shape Parameter Estimation Routine)

Casper is a python package aimed at predicting the concentration and shape parameter of dark matter haloes as a function of mass and redshift for a specified cosmology.

### Installation

The easiest way to install Casper is using pip:

```
pip install py-casper [--user]
```

The --user flag may be required if you do not have root privileges. Alternatively for a more involved 'installation' that is also editable you can simply  clone the github repository:

```
git clone https://github.com/Shaun-T-Brown/CASPER.git
```

and add the folder (specifically src) to your python path. This method will also require scipy and numpy to be installed. Using pip will automatically install all dependencies.

To use the main functionality of the package (i.e. to predict c and alpha) you will need to be able to generate the linear power spectra for a given cosmology. In principle this can be done using any accurate method. However, we recommend installing and using [CAMB](https://camb.readthedocs.io/en/latest/).

### Usage

The best way to demonstrate how Casper can be used is with a few examples. A static jupyter notebook can be found here, while an interactive version hosted by binder can be found here.

### Acknowledgements
