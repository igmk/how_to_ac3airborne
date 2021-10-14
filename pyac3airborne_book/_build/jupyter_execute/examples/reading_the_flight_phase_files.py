# Querying the *flight phase files*
We introduce here some new methods to select the flight segments, querying for different criteria.

## Data access
* To analyse the data they first have to be loaded by importing the (AC)³airborne meta data catalogue. To do so the pyac3airborne package has to be installed. More information on how to do that and about the catalog can be found [here](https://github.com/igmk/ac3airborne-intake#ac3airborne-intake-catalogue).

## Get data

import ac3airborne

cat = ac3airborne.get_intake_catalog()
list(cat.P5.GPS_INS)

```{note}
Have a look at the attributes of the xarray dataset `ds_gps` for all relevant information on the dataset, such as author, contact, or citation information.
```

In this example we want to look at `ACLOUD_P5_RF14`. First we read the GPS information:

ds_gps = cat['P5']['GPS_INS']['ACLOUD_P5_RF14'].to_dask()
ds_gps

## Load Polar 5 flight phase information
Polar 5 flights are divided into segments to easily access start and end times of flight patterns. For more information have a look at the respective [github](https://github.com/igmk/flight-phase-separation) repository.

At first we want to load the flight segments of (AC)³airborne

meta = ac3airborne.get_flight_segments() 

In order to simplify things we can import the module `flightphase` from the `ac3airborne.tools`.

from ac3airborne.tools import flightphase

The next step is to select the flight segments of our flight:

flight = meta['P5']['ACLOUD_P5_RF14']

flight_query = flightphase.FlightPhaseFile(flight)

## Plots
First, the entire flight is plotted:

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
plt.style.use("../mplstyle/book")

proj = ccrs.NorthPolarStereo()
extent = (-5.0, 24.0, 78.0, 83.0)

fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection=proj)
ax.set_extent(extent)

ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAND)
ax.gridlines()
ax.coastlines()

nya_lat = 78.924444
nya_lon = 11.928611

ax.plot(nya_lon, nya_lat, 'ro', transform=ccrs.PlateCarree())
ax.text(nya_lon, nya_lat+0.05, 'Ny-Ålesund', transform=ccrs.PlateCarree())

line_all = ax.plot(ds_gps.lon, ds_gps.lat, transform=ccrs.PlateCarree())

plt.show()

### Query all segments of a specific kind

As an example only `high_level` flights are plotted in the following (only one kind of pattern):

queried = flight_query.selectKind(['high_level'])
queried

Plot the selected segments:

ll = line_all.pop(0)
ll.remove()

lines = []
for q in queried:
    start = q['start']
    end   = q['end']
    
    line = ax.plot(ds_gps.lon.sel(time=slice(start, end)),
                   ds_gps.lat.sel(time=slice(start, end)),
                   transform=ccrs.PlateCarree())
    lines.append(line)
    
fig

 Of course, also more than one kind of pattern can be selected:

kinds = ['a-train_underflight', 'nya_overflight', 'polarstern_overflight']

queried = flight_query.selectKind(kinds)
queried

Plot the selected segments:

for l in lines:
    ll = l.pop(0)
    ll.remove()
    
lines = []
for q in queried:
    start = q['start']
    end   = q['end']
    
    line = ax.plot(ds_gps.lon.sel(time=slice(start, end)),
                   ds_gps.lat.sel(time=slice(start, end)),
                   transform=ccrs.PlateCarree())
    lines.append(line)
    
fig

### Sorting out all segments given a list of kinds

sort_out = ['short_turn', 'holding_pattern', 'major_ascend', 'major_descend', 'high_level']

queried = flight_query.selectKind(sort_out, invertSelection=True)
queried

Plot the selected segments:

for l in lines:
    ll = l.pop(0)
    ll.remove()
    
lines = []
for q in queried:
    start = q['start']
    end   = q['end']
    
    line = ax.plot(ds_gps.lon.sel(time=slice(start, end)),
                   ds_gps.lat.sel(time=slice(start, end)),
                   transform=ccrs.PlateCarree())
    lines.append(line)
    
fig

### Query a segment with a specific value in a specific attribute

#### Example 1: Select element with specific name

attribute = 'name'
value = 'racetrack pattern 1'

queried = flight_query.select(attribute, value) 
queried

Plot the selected elements:

for l in lines:
    ll = l.pop(0)
    ll.remove()
    
lines = []
for q in queried:
    start = q['start']
    end   = q['end']
    
    line = ax.plot(ds_gps.lon.sel(time=slice(start, end)),
                   ds_gps.lat.sel(time=slice(start, end)),
                   transform=ccrs.PlateCarree())
    lines.append(line)
    
fig

Also with inverted selection:

queried = flight_query.select(attribute, value, invertSelection=True) 
queried

Plot the selected elements:

for l in lines:
    ll = l.pop(0)
    ll.remove()
    
lines = []
for q in queried:
    start = q['start']
    end   = q['end']
    
    line = ax.plot(ds_gps.lon.sel(time=slice(start, end)),
                   ds_gps.lat.sel(time=slice(start, end)),
                   transform=ccrs.PlateCarree())
    lines.append(line)
    
fig

#### Example 2: Specific level

attribute = 'levels'
value = 9800

queried = flight_query.select(attribute, value)
queried

Plot the selected elements:

for l in lines:
    ll = l.pop(0)
    ll.remove()
    
lines = []
for q in queried:
    start = q['start']
    end   = q['end']
    
    line = ax.plot(ds_gps.lon.sel(time=slice(start, end)),
                   ds_gps.lat.sel(time=slice(start, end)),
                   transform=ccrs.PlateCarree())
    lines.append(line)
    
fig

But what if we want only a specific level without ascend and descend? We can require that the attribute value is strictly equal to the one, that we give, i.e. there are no other values:

queried = flight_query.select(attribute, value, strict=True)
queried

This functions only if the attribute has more values, as for level or kind. Now plot the selected elements:

for l in lines:
    ll = l.pop(0)
    ll.remove()
    
lines = []
for q in queried:
    start = q['start']
    end   = q['end']
    
    line = ax.plot(ds_gps.lon.sel(time=slice(start, end)),
                   ds_gps.lat.sel(time=slice(start, end)),
                   transform=ccrs.PlateCarree())
    lines.append(line)
    
fig

