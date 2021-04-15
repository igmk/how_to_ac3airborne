# description of the flight yaml files
```
name: RF04 # number of research flight within campaign
mission: ACLOUD # name of campaign [ACLOUD|AFLUX|MOSAiC-ACA]
platform: P5 # platform short name [P5|P6|HALO]
flight_id: ACLOUD_P5_RF04 # campaign_platform_name
contacts:
- name: null # PI o flight
  email: null
- name: null # creator of yaml
  email: null
date: 2017-05-23 # date of flight (take off day)
flight_report: null # url of public flight report
takeoff: &id001 2017-05-23 09:11:47 # datetime object of take off
landing: &id002 2017-05-23 14:23:40 # datetime object of landing
events: []
remarks:
- Clouds above open water and sea ice
segments:
- kinds:
  - major_ascend
  name: major ascend 1
  irregularities: []
  segment_id: ACLOUD_P5_RF04_ma1
  start: *id001
  end: null
  dropsondes:
    GOOD: []
    BAD: []
    UGLY: []
- kinds:
  - add_new_segments_here
  name: null
  irregularities: []
  segment_id: null
  start: null
  end: null
  dropsondes:
    GOOD: []
    BAD: []
    UGLY: []
- kinds:
  - major_descend
  name: major descend 1
  irregularities: []
  segment_id: ACLOUD_P5_RF04_md1
  start: null
  end: *id002
  dropsondes:
    GOOD: []
    BAD: []
    UGLY: []
```

import numpy as np
import matplotlib.pyplot as plt
plt.ion()

data = np.random.randn(2, 100)
fig, ax = plt.subplots()
ax.scatter(*data, c=data[1], s=100*np.abs(data[0]));