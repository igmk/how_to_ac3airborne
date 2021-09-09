# Introduction
Welcome to the world of AC3 airborne data! It's a collection of python code examples to get you started with the airborne data. It is a permantently growing and changing document and might never be finished. It follows the concept and ideas of the work done within the [EUREC4A](https://howto.eurec4a.eu/intro.html) community.

## Idea
The book chapters show datasets that are accessible online, i.e., you don’t have to download anything in advance. Most datasets are accessed via the [ac3airborne intake catalog](https://github.com/igmk/ac3airborne-intake), which simply said takes care of the links to datasets in their most recent version. By implemented caching capabilities, it is only necessary to download the data the first time they are used. The scripts typically contain at minimum how to get a specific dataset and some simple plots of basic quantities. Most chapters include additional information from aircraft flight segments or further meta data, sometimes more sophisticated plots, or also a combination of variables from different datasets. In addition, some small tools are included to work with auxilliary data like sea ice coverage or land-mask. 



## Some links
* [AC3 webpage](http://www.ac3-tr.de/)
* The data description papers of ACLOUD {cite}`EhrlichComprehensiveSituRemote2019` and for AFLUX and MOSAiC-ACA {cite}`MechMOSAiCACAAFLUXArctic2021`
* Campaign wikis: [ACLOUD](https://home.uni-leipzig.de/~ehrlich/ACLOUD_wiki_doku/doku.php), [AFLUX](https://home.uni-leipzig.de/~ehrlich/AFLUX_wiki_doku/doku.php?id=start), and [MOSAiC-ACA](https://home.uni-leipzig.de/~ehrlich/MOSAiC_ACA_wiki_doku/doku.php?id=start)
* Master data collections on PANGAEA: ACLOUD {cite}`EhrlichCollectionDataSources2019`, AFLUX {cite}`MechCollectionDataSets2021`, and MOSAiC-ACA {cite}`MechCollectionDataSets2021a`