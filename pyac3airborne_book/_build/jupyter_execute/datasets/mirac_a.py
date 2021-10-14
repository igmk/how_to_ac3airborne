# MiRAC-A
The following example demonstrates the use of MiRAC-A data collected during ACLOUD, AFLUX and MOSAiC-ACA. The Microwave Radar/Radiometer for Arctic Clouds (MiRAC) consists of an active component, a 94 GHz Frequency Modulated Continuous Wave (FMCW) cloud radar, and a passive 89 GHz microwave radiometer. MiRAC-A is mounted on Polar 5 with a fixed viewing angle of 25° against flight direction.

More information on the instrument can be found in [Mech et al. (2019)](https://amt.copernicus.org/articles/12/5019/2019/). If you have questions or if you would like to use the data for a publication, please don't hesitate to get in contact with the dataset authors as stated in the dataset attributes `contact` or `author`.

## Data access
* To analyse the data they first have to be loaded by importing the (AC)³airborne meta data catalogue. To do so the pyac3airborne package has to be installed. More information on how to do that and about the catalog can be found [here](https://github.com/igmk/ac3airborne-intake#ac3airborne-intake-catalogue).

## Get data

import ac3airborne

cat = ac3airborne.get_intake_catalog()
list(cat.P5.MIRAC_A)

```{note}
Have a look at the attributes of the xarray dataset `ds_mirac_a` for all relevant information on the dataset, such as author, contact, or citation information.
```

ds_mirac_a = cat['P5']['MIRAC_A']['ACLOUD_P5_RF05'].to_dask()
ds_mirac_a

The dataset includes the radar reflectivity (`Ze`, `Ze_unfiltered`), the radar reflectivity filter mask (`Ze_flag`), the 89 GHz brightness temperature (`TB_89`) as well as information on the aircraft's flight altitude (`altitude`). The radar reflectivity is defined on a regular `time`-`height` grid with corresponding target positions (`lat`, `lon`). The full dataset is available on PANGAEA.

## Load Polar 5 flight phase information
Polar 5 flights are divided into segments to easily access start and end times of flight patterns. For more information have a look at the respective [github](https://github.com/igmk/flight-phase-separation) repository.

At first we want to load the flight segments of (AC)³airborne

meta = ac3airborne.get_flight_segments() 

The following command lists all flight segments into the dictionary `segments`

segments = {s.get("segment_id"): {**s, "flight_id": flight["flight_id"]}
             for platform in meta.values()
             for flight in platform.values()
             for s in flight["segments"]
            }

In this example we want to look at a high-level segment during ACLOUD RF05

seg = segments["ACLOUD_P5_RF05_hl09"]

Using the start and end times of the segment `ACLOUD_P5_RF05_hl09` stored in `seg`, we slice the MiRAC data to this flight section.

ds_mirac_a_sel = ds_mirac_a.sel(time=slice(seg["start"], seg["end"]))

## Plots

The flight section during ACLOUD RF05 is flown at about 3 km altitude in west-east direction during a cold-air outbreak event perpendicular to the wind field. Clearly one can identify the roll-cloud structure in the radar reflectivity and the 89 GHz brightness temperature.

%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from numpy import log10
plt.style.use("../mplstyle/book")

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# 1st: plot flight altitude and radar reflectivity
ax1.plot(ds_mirac_a_sel.time, ds_mirac_a_sel.altitude*1e-3, label='Flight altitude', color='k')

im = ax1.pcolormesh(ds_mirac_a_sel.time, ds_mirac_a_sel.height*1e-3, 10*log10(ds_mirac_a_sel.Ze).T, vmin=-40, vmax=30, cmap='jet', shading='nearest')
fig.colorbar(im, ax=ax1, label='Radar reflectivity [dBz]')
ax1.set_ylim(-0.25, 3.5)
ax1.set_ylabel('Height [km]')
ax1.legend(frameon=False, loc='upper left')

# 2nd: plot 89 GHz TB
ax2.plot(ds_mirac_a_sel.time, ds_mirac_a_sel.TB_89, label='Tb(89 GHz)', color='k')
ax2.set_ylim(177, 195)
ax2.set_ylabel('$T_b$ [K]')
ax2.set_xlabel('Time (hh:mm) [UTC]')
ax2.legend(frameon=False, loc='upper left')

ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()

