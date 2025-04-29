# Introduction

Welcome to the world of AC<sup>3</sup> airborne data! It is a collection of python code examples that should get you started with the airborne data collected during the various airborne campaigns within the German DFG project - TRR 172, "ArctiC Amplification: Climate Relevant Atmospheric and SurfaCe Processes, and Feedback Mechanisms (AC<sup>3</sup>) (*Wendisch et al., 2019*, *Wendisch et al., 2022*), a joint research initiative of the Universities Leipzig (Leipzig Institute of Meteorology, LIM), Cologne (Institute of Geophysics and Meteorology, IGM), University of Bremen (Environmental Physics, IUP) and of the research institutes TROPOS (Leipzig) and Alfred Wegener Institute a Helmholtz Centre for Polar and Marine Research (AWI Bremerhaven and Potsdam). The document is permanently growing and changing and might never be finished. It follows the concept and ideas of the work done within the [EUREC4A](https://howto.eurec4a.eu/intro.html) community.

## Idea
The datasets presented here are accessible online, i.e., you don’t have to download anything in advance. Most datasets are accessed via the [ac3airborne intake catalog](https://github.com/igmk/ac3airborne-intake), which simply said takes care of the links to datasets in their most recent version. Many of the datasets are publicly available, are located on the [PANGAEA](https://www.pangaea.de/) database, and have a digital object identifier (DOI). Data from more recent campaigns are either on the [Nextcloud server of the AC<sup>3</sup> project](https://cloud.ac3-tr.de) and only accessible with username and password. These data are still preliminary, never planed to be published on PANGAEA, or still under moratorium. Some of the data has been post-processed to fit the needs and is publicly available from a server at University of Cologne. 

By implemented caching capabilities, it is only required to download the data the first time they are used. The scripts typically contain at minimum a description on how to get a specific dataset and some simple plots of basic quantities. Most chapters include additional information from aircraft flight segments or further metadata, sometimes more sophisticated plots, or also a combination of variables from different datasets. In addition, some small tools are included to work with auxiliary data like sea ice coverage or land-mask. 

## Platforms
Three airborne platforms have been operated during the various (AC<sup>3</sup>) campaigns: the two Basler Turbo-67 (BT-67) [P5 and P6](https://halo-ac3.de/halo-ac3/p5-p6/) from the AWI and operated by Kenn Borek Air and the Gulfstream G-550 [HALO](https://halo-ac3.de/halo-ac3/halo/) operated by DLR. 

## Campaigns
Six airborne campaigns have been conducted in the Arctic have been conducted in the framework of (AC)<sup>3</sup>: ACLOUD, PAMARCMiP, AFLUX, MOSAiC-ACA, HALO-AC3, and COMPEX-EC. These campaigns are covered by ac3airborne, including the HAMAG campaign, that strictly speaking isn't an (AC)<sup>3</sup> campaign. An exception is PAMARCMiP where only the gps tracks are included.

```{figure} img/all_tracks.png
---
height: 250px
name: directive-fig
---
Flight tracks of the campaigns covered by ac3airborne.
```

## Some links
* [ac3airborne](https://github.com/igmk/ac3airborne/) on github
* [AC<sup>3</sup>](http://www.ac3-tr.de/) project page
* [HALO-(AC)<sup>3</sup>](https://halo-ac3.de/) campaign and publication (*Wendisch et al., 2024*) 
* The data description papers for ACLOUD (*Ehrlich et al., 2019a*), for AFLUX and MOSAiC-ACA (*Mech et al., 2022*), and for HALO-(AC)<sup>3</sup> (*Ehrlich et al., 2025*)
* Campaign wikis/blogs: [ACLOUD](https://home.uni-leipzig.de/~ehrlich/ACLOUD_wiki_doku/doku.php), [AFLUX](https://home.uni-leipzig.de/~ehrlich/AFLUX_wiki_doku/doku.php), [MOSAiC-ACA](https://home.uni-leipzig.de/~ehrlich/MOSAiC_ACA_wiki_doku/doku.php), [HALO-(AC)<sup>3</sup>](https://home.uni-leipzig.de/~ehrlich/HALO_AC3_wiki_doku/doku.php), [HAMAG](https://blog.uni-koeln.de/awares/category/campaigns-conf/hamag/), and [COMPEX-EC](https://blog.uni-koeln.de/awares/category/campaigns-conf/compex-ec/) 
* Master data collections on PANGAEA: ACLOUD (*Ehrlich et al., 2019b*), AFLUX (*Mech et al., 2021a*), MOSAiC-ACA (*Mech et al., 2021b*), and HALO-(AC)<sup>3</sup> Polar 5 (*Mech et al., 2024*), Polar 6 (*Herber et al., 2024*), and HALO (*Ehrlich et al., 2024*)



