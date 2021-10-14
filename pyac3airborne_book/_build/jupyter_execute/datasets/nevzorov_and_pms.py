# PMS probes and Nevzorov
The following example presents the data collected by the PMS and Nevzorov probes on Polar 5 during the MOSAiC-ACA campaign. The PMS probes where attached to the wings of the aircraft and operated by the group at DLR e.V. and JGU Mainz namely: C. Voigt, M. Moser, and V. Hahn. If you have questions or if you would like to use the data for a publication, please get in contact with the dataset authors as stated above and in the dataset attributes `contact` or `author`.

## Data access
* To analyse the data they first have to be loaded by importing the (AC)³airborne meta data catalogue. To do so the pyac3airborne package has to be installed. More information on how to do that and about the catalog can be found [here](https://github.com/igmk/ac3airborne-intake#ac3airborne-intake-catalogue).

## Get data

import ac3airborne
cat = ac3airborne.get_intake_catalog()

### Nevzorov

First, we load the data collected by the Nevzorov.

list(cat.P5.NEVZOROV)

```{note}
Have a look at the attributes of the xarray dataset `ds_nevzorov` for all relevant information on the dataset, such as author, contact, or citation information.
```

flight_id = 'MOSAiC-ACA_P5_RF11' # id of flight we work on
ds_nevzorov = cat['P5']['NEVZOROV'][flight_id].to_dask()
ds_nevzorov

The dataset includes the liquid water content (`lwc`) and total water content (`twc`).

### PMS
Next, we load the data from the different instruments of the PMS to determine total number concentration, particle size distributions and water contents.

- Cloud Droplet Probe (CDP) with 2 to 50 microns
- Cloud Imaging Probe (CIP) with 7.5 to 967.5 microns
- Precipitation Imaging Probe (PIP) with 51.5 to 6643.5 microns

ds_cdp = cat.P5.CDP[flight_id].to_dask()
ds_cip = cat.P5.CIP[flight_id].to_dask()
ds_pip = cat.P5.PIP[flight_id].to_dask()

ds_pms_combined = cat.P5.PMS_COMBINED[flight_id].to_dask()
ds_pms_combined

The dataset `ds_pms_combined` combines the measurements from the different instruments of the PMS and hence includes
total number concentration (`N`),
median volume diameter (`MVD`), liquid water content (`LWC`), ice water content (`IWC`) and particle number concentration (`dNdD`).

## Load Polar 5 flight phase information
Polar 5 flights are divided into segments to easily access start and end times of flight patterns. For more information have a look at the respective [github](https://github.com/igmk/flight-phase-separation) repository.

At first we want to load the flight segments of (AC)³airborne

meta = ac3airborne.get_flight_segments()
flight = meta['P5'][flight_id]

Here, we want to have a look on the size distributions measured during different legs of a `racetrack_pattern`. In order to simplify things we can import the module `flightphase` from the `ac3airborne.tools`.

from ac3airborne.tools import flightphase

We can now select only the `racetrack_pattern`. This kind of pattern is available two times.

flight_query = flightphase.FlightPhaseFile(flight)
queried = flight_query.selectKind(['racetrack_pattern'])
len(queried)

## Plots

%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.style.use("../mplstyle/book")

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, gridspec_kw=dict(height_ratios=(1, 1, 1, 1)))
ax1.semilogy(ds_cdp.time, ds_cdp.N, color='k')
ax1.set_title('CDP')
ax2.semilogy(ds_cip.time, ds_cip.N, color='b')
ax2.set_title('CIP')
ax3.semilogy(ds_pip.time, ds_pip.N, color='g')
ax3.set_title('PIP')
ax4.plot(ds_nevzorov.time, ds_nevzorov.lwc, '--', color='g', label='LWC')
ax4.plot(ds_nevzorov.time, ds_nevzorov.twc, '--', color='b', label='TWC')
ax4.set_title('Nevzorov')

ax1.set_ylabel('N [$1/m^3$]')
ax2.set_ylabel('N [$1/m^3$]')
ax3.set_ylabel('N [$1/m^3$]')

ax4.set_ylabel('water content [kg/m^3]')

ax4.legend(frameon=False, loc='upper right')

ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()

from matplotlib import cm
import numpy as np
def colors(n):
    """Creates set of random colors of length n"""
    
    cmap = cm.get_cmap('gist_rainbow')
    rnd = np.random.uniform(low=0, high=1, size=n)
    cols = cmap(rnd)
    
    return cols

titles = ['ice','ocean']
fig, axs = plt.subplots(1, 2, gridspec_kw=dict())
for i, rtp in enumerate(queried):
    col_segments = colors(len(rtp['parts']))
    for j,part in enumerate(rtp['parts']):
        if 'leg' in part['name']:
            ds_sel = ds_pms_combined.sel(time=slice(part['start'],part['end']))
            axs[i].loglog(ds_sel.bin_mid, ds_sel.dNdD.mean(dim='time'), 'o',color=col_segments[j],label=part['levels'][0])
    axs[i].legend(frameon=False)
    axs[i].set_xlabel('D[$\mu m$]')
    axs[i].set_ylabel('N[$m^{-4}$]')
    axs[i].set_title('Over '+titles[i])

