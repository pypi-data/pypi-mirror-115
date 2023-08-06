TODO 

# Histodata

This repository is a aggregation of pytorch datasets for loading histology datasets.

# installation

```
pip install --upgrade histodata
```

# Usage

Todo for each dataset a own list.

Including:
- Describtion of the dataset
- How to get the dataset
- Dokumentation of the interface
- Example usage of the interface

```
from histodata.datasets import mai, midog, bach, pcam

dataset = mai.mai_patches('path_to_datafolder',
                               transformation=None,
                               subset='train',
                              )
```
