# MiRAC-P
The following example presents the nadir passive microwave radiometer MiRAC-P. The Microwave Radar/Radiometer for Arctic Clouds - passive (MiRAC-P) was installed during ACLOUD and AFLUX. During MOSAiC-ACA, passive microwave observations are conducted by the HATPRO instrument.

More information on MiRAC can be found in [Mech et al. (2019)](https://amt.copernicus.org/articles/12/5019/2019/). If you have questions or if you would like to use the data for a publication, please don't hesitate to get in contact with the dataset authors as stated in the dataset attributes `contact` or `author`.

## Data access
* To analyse the data they first have to be loaded by importing the (AC)³airborne meta data catalogue. To do so the pyac3airborne package has to be installed. More information on how to do that and about the catalog can be found [here](https://github.com/igmk/ac3airborne-intake#ac3airborne-intake-catalogue).

## Get data

import ac3airborne

cat = ac3airborne.get_intake_catalog()
list(cat.P5.MIRAC_P)

```{note}
Have a look at the attributes of the xarray dataset `ds_mirac_p` for all relevant information on the dataset, such as author, contact, or citation information.
```

ds_mirac_p = ds_cth = cat['P5']['MIRAC_P']['ACLOUD_P5_RF05'].to_dask()
ds_mirac_p

The dataset includes nadir brightness temperatures (`tb`) observed by MiRAC-P at the 183.31 GHz water vapor absorption line (183±0.6, ±1.5, ±2.5, ±3.5, ±5.0, ±7.5 GHz) and two window channels at 243 and 340 GHz.

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

In this example we want to look at a high-level segment during ACLOUD RF05.

seg = segments["ACLOUD_P5_RF05_hl07"]

Using the start and end times of the segment `ACLOUD_P5_RF05_hl07` stored in `seg`, we slice the MiRAC-P data to the selected flight sections.

ds_mirac_p_sel = ds_mirac_p.sel(time=slice(seg["start"], seg["end"]))

In polar regions, the surface type is helpful for the interpretation of airborne passive microwave observations, especially near the marginal sea ice zone, as generally a higher emissivity is expected over sea ice compared to open ocean. Therefore, we also load AMSR2 sea ice concentration data along the Polar 5 flight track, which is operationally derived by the University of Bremen.

ds_sea_ice = cat['P5']['AMSR2_SIC']['ACLOUD_P5_RF05'].to_dask().sel(
    time=slice(seg["start"], seg["end"]))

## Plots

The flight section during ACLOUD RF05 is flown at about 3 km altitude in west-east direction during a cold-air outbreak event perpendicular to the wind field. Clearly one can identify the roll-cloud structure in the radar reflectivity and the 89 GHz brightness temperature.

import warnings
warnings.filterwarnings("ignore")
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import cm
import numpy as np
plt.style.use("../mplstyle/book")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw=dict(height_ratios=(1, 1, 0.1)))

kwargs = dict(s=10, linewidths=0)
colors = cm.get_cmap('viridis', 6).colors
for i in range(0, 6):
    ax1.scatter(ds_mirac_p_sel.time, ds_mirac_p_sel.tb.sel(channel=i), label='%g GHz'%ds_mirac_p_sel.frequency.sel(channel=i).item(), color=colors[i], **kwargs)

for i in range(6, 8):
    ax2.scatter(ds_mirac_p_sel.time, ds_mirac_p_sel.tb.sel(channel=i), label='%g GHz'%ds_mirac_p_sel.frequency.sel(channel=i).item(), **kwargs)

ax1.legend(frameon=False, bbox_to_anchor=(1.05, 0.5), loc='center left')
ax2.legend(frameon=False, bbox_to_anchor=(1.05, 0.5), loc='center left')

ax1.set_ylabel('$T_b$ [K]')
ax2.set_ylabel('$T_b$ [K]')

# plot AMSR2 sea ice concentration
im = ax3.pcolormesh(np.array([ds_sea_ice.time, ds_sea_ice.time]),
               np.array([0, 1]),
               np.array([ds_sea_ice.sic]), cmap='Blues_r', vmin=0, vmax=100,
               shading='auto')
cax = fig.add_axes([0.87, 0.085, 0.1, ax3.get_position().height])
fig.colorbar(im, cax=cax, orientation='horizontal', label='Sea ice [%]')
ax3.tick_params(axis='y', labelleft=False, left=False)


ax3.set_xlabel('Time (hh:mm) [UTC]')
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()

