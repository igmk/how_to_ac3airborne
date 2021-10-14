# GPS and INS
Position and orientation of Polar 5 and Polar 6 are recorded by an on-board GPS sensor and the internal navigation system (INS). The following example presents the variables recored by these instruments.

## Data access
* To analyse the data they first have to be loaded by importing the (AC)³airborne meta data catalogue. To do so the pyac3airborne package has to be installed. More information on how to do that and about the catalog can be found [here](https://github.com/igmk/ac3airborne-intake#ac3airborne-intake-catalogue).

## Get data

import ac3airborne

GPS and INS data of Polar 5:

cat = ac3airborne.get_intake_catalog()
list(cat.P5.GPS_INS)

GPS and INS data of Polar 6:

list(cat.P6.GPS_INS)

```{note}
Have a look at the attributes of the xarray dataset `ds_gps_ins` for all relevant information on the dataset, such as author, contact, or citation information.
```

ds_gps_ins = cat['P5']['GPS_INS']['AFLUX_P5_RF10'].to_dask()
ds_gps_ins

The dataset `ds_gps_ins` includes the aircraft's position (`lon`, `lat`, `alt`), attitude (`roll`, `pitch`, `heading`), and the ground speed, vertical speed and true air speed (`gs`, `vs`, `tas`). 

## Load Polar 5 flight phase information
Polar 5 flights are divided into segments to easily access start and end times of flight patterns. For more information have a look at the respective [github](https://github.com/igmk/flight-phase-separation) repository.

At first we want to load the flight segments of (AC)³airborne

meta = ac3airborne.get_flight_segments() 

The following command lists all flight segments into the dictionary `segments`:

segments = {s.get("segment_id"): {**s, "flight_id": flight["flight_id"]}
             for platform in meta.values()
             for flight in platform.values()
             for s in flight["segments"]
            }

In this example, we want to look at a racetrack pattern during `ACLOUD_P5_RF10`.

seg = segments["AFLUX_P5_RF10_rt01"]

Using the start and end times of the segment, we slice the data to this flight section.

ds_gps_ins_rt = ds_gps_ins.sel(time=slice(seg["start"], seg["end"]))

## Plots

%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import numpy as np
import ipyleaflet
from simplification.cutil import simplify_coords_idx
plt.style.use("../mplstyle/book")

### Plot all flights

def simplify_dataset(ds, tolerance):
    indices_to_take = simplify_coords_idx(np.stack([ds.lat.values, ds.lon.values], axis=1), tolerance)
    return ds.isel(time=indices_to_take)

# define colors for the flight tracks
colors = [mcolors.to_hex(c)
          for c in plt.cm.inferno(np.linspace(0, 1, len(cat['P5']['GPS_INS'])))]

m = ipyleaflet.Map(basemap=ipyleaflet.basemaps.Esri.NatGeoWorldMap,
                   center=(80., 6), zoom=3)

for flight_id, color in zip(cat['P5']['GPS_INS'], colors):
    
    # read gps dataset of flight
    ds = cat.P5.GPS_INS[flight_id].to_dask()
    
    # slice to takeoff and landing times
    ds = ds.sel(time=slice(meta['P5'][flight_id]['takeoff'], meta['P5'][flight_id]['landing']))
    
    # reduce dataset for plotting
    ds_reduced = simplify_dataset(ds, tolerance=1e-5)
    
    track = ipyleaflet.Polyline(
        locations=np.stack([ds_reduced.lat.values, 
                            ds_reduced.lon.values], axis=1).tolist(), 
        color=color,
        fill=False,
        weight=2,
        name=flight_id)
    
    m.add_layer(track)
    
m.add_control(ipyleaflet.ScaleControl(position='bottomleft'))
m.add_control(ipyleaflet.LegendControl(dict(zip(cat['P5']['GPS_INS'], colors)),
                                       name="Flights",
                                       position="bottomright"))
m.add_control(ipyleaflet.LayersControl(position='topright'))
m.add_control(ipyleaflet.FullScreenControl())
display(m)

### Plot time series of one flight

fig, ax = plt.subplots(9, 1, sharex=True)

kwargs = dict(s=1, linewidths=0, color='k')

ax[0].scatter(ds_gps_ins.time, ds_gps_ins['alt'], **kwargs)
ax[0].set_ylabel('alt [m]')

ax[1].scatter(ds_gps_ins.time, ds_gps_ins['lon'], **kwargs)
ax[1].set_ylabel('lon [°E]')

ax[2].scatter(ds_gps_ins.time, ds_gps_ins['lat'], **kwargs)
ax[2].set_ylabel('lat [°N]')

ax[3].scatter(ds_gps_ins.time, ds_gps_ins['roll'], **kwargs)
ax[3].set_ylabel('roll [°]')

ax[4].scatter(ds_gps_ins.time, ds_gps_ins['pitch'], **kwargs)
ax[4].set_ylabel('pitch [°]')

ax[5].scatter(ds_gps_ins.time, ds_gps_ins['heading'], **kwargs)
ax[5].set_ylim(-180, 180)
ax[5].set_ylabel('heading [°]')

ax[6].scatter(ds_gps_ins.time, ds_gps_ins['gs'], **kwargs)
ax[6].set_ylabel('gs [kts]')

ax[7].scatter(ds_gps_ins.time, ds_gps_ins['vs'], **kwargs)
ax[7].set_ylabel('vs [m/s]')

ax[8].scatter(ds_gps_ins.time, ds_gps_ins['tas'], **kwargs)
ax[8].set_ylabel('tas [m/s]')


ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()

### Plot time series of racetrack pattern

fig, ax = plt.subplots(9, 1, sharex=True)

kwargs = dict(s=1, linewidths=0, color='k')

ax[0].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['alt'], **kwargs)
ax[0].set_ylabel('alt [m]')

ax[1].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['lon'], **kwargs)
ax[1].set_ylabel('lon [°E]')

ax[2].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['lat'], **kwargs)
ax[2].set_ylabel('lat [°N]')

ax[3].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['roll'], **kwargs)
ax[3].set_ylabel('roll [°]')

ax[4].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['pitch'], **kwargs)
ax[4].set_ylabel('pitch [°]')

ax[5].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['heading'], **kwargs)
ax[5].set_ylim(-180, 180)
ax[5].set_ylabel('heading [°]')

ax[6].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['gs'], **kwargs)
ax[6].set_ylabel('gs [kts]')

ax[7].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['vs'], **kwargs)
ax[7].set_ylabel('vs [m/s]')

ax[8].scatter(ds_gps_ins_rt.time, ds_gps_ins_rt['tas'], **kwargs)
ax[8].set_ylabel('tas [m/s]')


ax[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()

