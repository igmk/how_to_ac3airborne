# Flight-phase separation
The idea behind `flight-phase-separation` is to easily select segments of research flights based on their properties as required for the user's research. The selection can be done using any combination of attributes. In the following sections, the stored attributes and the structure of files under `flight_phase_files` is presented.

## Interactive map of flight segments
This example displays the Polar 5 flight segments from `ACLOUD_P5_RF14` on an interactive map.

flight_id = 'ACLOUD_P5_RF14'

import ac3airborne
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from matplotlib import cm
import ipyleaflet
from ipyleaflet import Polyline, Map, basemaps, basemap_to_tiles
from simplification.cutil import simplify_coords_idx
plt.style.use("mplstyle/book")


def colors(n):
    """Creates set of random colors of length n"""
    
    cmap = cm.get_cmap('gist_rainbow')
    rnd = np.random.uniform(low=0, high=1, size=n)
    cols = cmap(rnd)
    
    return cols


def simplify_dataset(ds, tolerance):
    indices_to_take = simplify_coords_idx(np.stack([ds.lat.values, ds.lon.values], axis=1), tolerance)
    return ds.isel(time=indices_to_take)

# load intake catalog and flight segments
cat = ac3airborne.get_intake_catalog()
meta = ac3airborne.get_flight_segments()

# read gps data of one flight
ds_gps_ins = cat['P5']['GPS_INS'][flight_id].to_dask()
flight = meta['P5'][flight_id]

# plot map
m = Map(basemap=basemap_to_tiles(basemaps.NASAGIBS.ModisTerraTrueColorCR, str(flight['date'])),
        center=(80, 10),
        zoom=4,
        scroll_wheel_zoom=True)

col_segments = colors(len(flight['segments']))

for i, segment in enumerate(flight['segments']):
    
    # reduce flight segment
    ds_reduced = simplify_dataset(ds_gps_ins.sel(time=slice(segment['start'], 
                                                            segment['end'])), 
                                  1e-5)
    
    # plot flight segment
    line = Polyline(locations=np.stack([ds_reduced.lat.values, ds_reduced.lon.values], axis=1).tolist(),
                    color=to_hex(col_segments[i]),
                    fill=False,
                    weight=2,
                    name=str(i) + ': ' + segment['name'])
    m.add_layer(line)

m.add_control(ipyleaflet.ScaleControl())
m.add_control(ipyleaflet.LayersControl(position='topright'))
m.add_control(ipyleaflet.FullScreenControl())

display(m)

## Flight keywords
`name`: research flight number within campaign (e.g. *RF10*)

`mission`: name of campaign (*ACLOUD*, *AFLUX*, *MOSAiC-ACA*)

`platform`: aircraft short name (*P5*, *P6*)

`flight_id`: unique identifier for flight (*campaign_platform_name*)

`contacts`: information on mission PI and creator of `.yaml` file (name and email contact)

`date`: date of flight (will be read as python `datetime.date` object)

`flight_report`: link to the online flight report with detailed information on the flight (flight objectives, quicklooks, photos)

`takeoff`: flight takeoff at the airport (will be read as python `datetime.datetime` object)

`landing`: flight landing at the airport (will be read as python `datetime.datetime` object)

`events`: planned flight features, such as patterns, joint flights between aircraft, satellite overpasses, or instrument calibration

`remarks`: information on atmospheric conditions and instrument status

`segments`: list of flight segments

## Keyword `segments`
The following section provides an overview of the flight `segments` and their properties. They are ordered chronologically in a list, with the first segment starting at flight `takeoff` and the last segment ending at flight `landing`. The given `start` and `end` times of each segment are included.

### Segment keywords
`kinds`: list of properties, which describe the flight segment (see next section)

`name`: name of segment, that is unique within the flight

`irregularities`: list of irregularities in the flight track or caused by other factors, such as icing

`segment_id`: unique id of flight segment

`start`: start of segment (will be read as python `datetime.datetime` object)

`end`: end of segment (will be read as python `datetime.datetime` object)

`levels`: median flight level(s) or highest and lowest flight level for ascends/descends [in feet]

`dropsondes`: list of dropsondes released during that segment

`parts`: list of sub-segments (parts), which belong to a flight pattern (see next section)

### Keyword `kinds`
Making `flight-phase-separation` a useful tool for various communities, either working on in-situ or remotely sensed data, the various flight maneuvers are classified and separated. The following section provides an overview of the `kinds` used to describe the flight segments. Multiple keywords can be used for one flight segment. In total, 33 `kinds` are defined to classify the segments.

#### Takeoff and landing maneuvers
The takeoff and landing maneuvers are labelled as `major_ascend` (takeoff) and `major_descend` (landing). Their `start` and `end` times correspond to the flight `takeoff` and `landing` keyword, respectively.

| Name           | Description                                                              | Ending of `segment_id` |
| --------------- | ------------------------------------------------------------------------ |-----------|
| `major_ascend`    | takeoff from the airport until a constant flight level is reached        | `ma`   |
| `major_descend`   | last descend from a constant flight level before landing at the airport   | `md`   |
 
#### Straight segment with constant flight altitude
Straight flight segments with constant flight altitude are classified into three height levels.
| Name         | Description                                     | Ending of `segment_id` |
| ------------- | ----------------------------------------------- |-----------|
| `low_level`     | Constant flight level at < 1 km altitude        | `ll` |
| `mid_level`     | Constant flight level at 1-2 km altitude        | `ml` |
| `high_level`    | Constant flight level at > 2 km altitude        | `hl` |


#### Ascends and descends
Ascends and descends are classified by two properties: (1) the height difference between lowest and highest point, and (2) the vertical velocity. Note that sometimes ascends or descends may be flown within curves.

| Name         | Description                                     | Ending of `segment_id` |
| --------------- | ------------------------------------------------------------------------ |-----------|
| `small_ascend`    | Ascend with height difference < 1 km   | `sa` |
| `small_descend`   | Descend with height difference < 1 km  | `sd` |
| `medium_ascend`    | Ascend with height difference of 1-2 km   | `ma` |
| `medium_descend`   | Descend with height difference of 1-2 km  | `md` |
| `large_ascend`    | Ascend with height difference > 2 km   | `la` |
| `large_descend`   | Descend with height difference > 2 km  | `ld` |
| `profiling`       | Ascend or descend with vertical speed mostly between 5-10 m/s            |       |

#### Overflights, underflights and co-locations
During many research flights, the research station in Ny-Alesund and the research vessel Polarstern are overflown, or the satellite constellation A-train is underflown. These segments are marked and easily accessible. Additionally, co-locations between aircraft are marked.

| Name         | Description                                     | Ending of `segment_id` |
| --------------- | ------------------------------------------------------------------------ |-----------|
| `nya_overflight`      | Overflight over the Ny-Alesund research station within 15 km. Might be combined with `cross_pattern` or `high_level`|
| `polarstern_overflight`       | Overflight over RV Polarstern within 15 km. Might be combined with `cross_pattern` |
| `a-train_underflight` | Underflight of the A-Train satellite constellation. For Polar 5, it is usually combined with `high_level`. For Polar 6 it might be any profiling pattern        |
| `sveabreen_glacier_overflight`       | Overflight over the Sveabreen glacier, Svalbard, mostly during `major_ascend` |
| `p6_co-location`  | Co-location of Polar 5 with Polar 6 | 
| `p5_co-location`  | Co-location of Polar 6 with Polar 5 | 

#### Instrument calibration and testing
Especially in the beginning of campaigns, maneuvers are flown to test or calibrate instrumentation. The keywords for these segments are listed in the table below. 
| Name         | Description                                     | Ending of `segment_id` |
| --------------- | ------------------------------------------------------------------------ |-----------|
| `radiometer_calibration`      | Segment dedicated for radiometer calibration |
| `instrument_testing`      | Segment for instrument testing, usually at the beginning of campaigns, where various maneuvers are flown | `it` |

#### Curves and circles
Different curves and circles are flown, depending on the angle or flight direction. These segments are not described by further keywords. Note, that segments, which are only curves (without ascend or descend), do not have the keywords `irregularities`, `segment_id`, `levels`, and `dropsondes`.

| Name         | Description                                     | Ending of `segment_id` |
| --------------- | ------------------------------------------------------------------------ |-----------|
| `short_turn`     | Turn directly to another flight direction (cutting corner) | |
| `long_turn`      | Turn on the long way to another flight direction (without cutting corner) | |
| `procedure_turn` | Turn of 180° to be directly on track again in opposite direction | |
| `cirle` | 360° circle, which is not part of a specific pattern | |
| `cross_pattern_turn` | Transfer leg during `cross_pattern` | |

#### Patterns
Different flight patterns with each specific properties were flown during the campaigns. Each pattern segment consists of sub-segments, which are listed under the keyword `parts`.  Every part can be one of the above mentioned segments.
| Name         | Description                                     | Ending of `segment_id` |
| --------------- | ------------------------------------------------------------------------ |-----------|
| `cross_pattern`         | Rectangular crosses with transfer legs in between, usually flown over Ny-Alesund or Polarstern | `cr` | 
| `racetrack_pattern`     | Back and forth on the same track, with possible height changes | `rt` |
| `holding_pattern`       | Time spending or waiting | `ho` |
| `stairstep_pattern`     | Step wise ascending or descending along a straight line | `ss` |
| `sawtooth_pattern`      | Alternating ascends and descends along a straight line| `st` |
| `radiation_square`      | Square pattern at high altitude for radiation measurements | `rs` |
| `noseboom_calibration_pattern`       | Pattern dedicated to calibrate the nose boom | `np` |

## Template of `.yaml` file
Below, a template of a `flight-phase-separation` `.yaml` file is shown. A description of the keywords is presented in the previous sections.
```
name: RF04
mission: ACLOUD
platform: P5
flight_id: ACLOUD_P5_RF04
contacts:
- name:
  email:
  tags:
  - pi  # PI of flight
- name:
  email:
  tags:
  - lc  # list creator
date: 2017-05-23
flight_report: null
takeoff: 2017-05-23 09:11:47
landing: 2017-05-23 14:23:40
events: []
remarks: []
segments:
- kinds:
  - major_ascend
  name: major ascend 1
  irregularities: []
  segment_id: ACLOUD_P5_RF04_ma
  start: 2017-05-23 09:11:47
  end: null
  levels: []
  dropsondes: []
- kinds:
  - add_new_segments_here
  name: null
  irregularities: []
  segment_id: null
  start: null
  end: null
  levels: []
  dropsondes: []
- kinds:
  - major_descend
  name: major descend 1
  irregularities: []
  segment_id: ACLOUD_P5_RF04_md
  start: null
  end: 2017-05-23 14:23:40
  levels: []
  dropsondes: []
```

