# Dropsondes
Dropsondes were launched from Polar 5 providing profiles of air temperature, humidity, pressure, and the horizontal wind vector between flight altitude (3-4 km) and the surface. The full dataset is available on PANGAEA for [ACLOUD](https://doi.pangaea.de/10.1594/PANGAEA.900204), [AFLUX](https://doi.pangaea.de/10.1594/PANGAEA.921996), and [MOSAiC-ACA](https://doi.pangaea.de/10.1594/PANGAEA.933581). Each NetCDF file contains dropsondes of a single flight ordered into groups.

## Data access
* To analyse the data they first have to be loaded by importing the (AC)³airborne meta data catalogue. To do so the pyac3airborne package has to be installed. More information on how to do that and about the catalog can be found [here](https://github.com/igmk/ac3airborne-intake#ac3airborne-intake-catalogue).

## Get data

import ac3airborne

List of flights, where dropsondes are available:

cat = ac3airborne.get_intake_catalog()
list(cat.P5.DROPSONDES)

## Dataset
To get an overview of the variables recorded by the dropsondes, we load the first dropsonde released during `ACLOUD_P5_RF05`.

ds_dsd = cat['P5']['DROPSONDES']['ACLOUD_P5_RF05'](i_sonde=1).to_dask()
ds_dsd

### View variables
Below are vertical profiles of temperature, relative humidity, wind velocity and wind direction of that dropsonde shown.

%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.style.use("../mplstyle/book")

fig, ax = plt.subplots(1, 4, sharey=True)

var_names = ['Temp_recon', 'RHum_recon', 'Wind_vel', 'Wind_dir']
labels = ['T [°C]', 'RH [%]', 'U [m/s]', 'D [°]']

kwargs = dict(s=1, color='k')
for i, var_name in enumerate(var_names):
    
    ax[i].scatter(ds_dsd[var_name], ds_dsd.GPS_Alt, **kwargs)
    
    ax[i].set_xlabel(labels[i])

ax[0].set_ylabel('GPS altitude [m]')
    
plt.show()

## Load Polar 5 flight phase information
Polar 5 flights are divided into segments to easily access start and end times of flight patterns. For more information have a look at the respective [github](https://github.com/igmk/flight-phase-separation) repository.

At first we want to load the flight segments of (AC)³airborne

meta = ac3airborne.get_flight_segments() 

Create a list with all dropsondes during the campaigns:

ds_dict = {'ACLOUD': {}, 'AFLUX': {}, 'MOSAiC-ACA': {}}
for platform in meta.values():
    for flight in platform.values():
        for segment in flight['segments']:
            if 'dropsondes' in segment.keys():
                for sonde in segment['dropsondes']:
                    params = {'segment_id': segment['segment_id'],
                              'flight_id': flight['flight_id'],
                              'date': flight['date'],
                              'name': flight['name'],
                             }
                    ds_dict[flight['mission']][sonde] = params

Get total number of dropsondes during the campaigns:

for mission, sondes in ds_dict.items():
    n = len(sondes.values())
    print('{n} dropsondes are available from {mission}.'.format(
        n=n, mission=mission))

## Plots
The next sections present the entire dataset by loading all dropsondes of the three campaigns and plotting vertical profiles of temperature, humidity and horizontal wind velocity.
### Temperature profile

fig, axes = plt.subplots(1, 3, sharey=True, sharex=True)

ax = {'ACLOUD': axes[0], 'AFLUX': axes[1], 'MOSAiC-ACA': axes[2]}

kwargs = dict(s=1, color='red', alpha=0.4)
for mission, sondes in ds_dict.items():
    
    ax[mission].set_title(mission)
    
    for sonde_id, params in ds_dict[mission].items():

        # read dropsonde data
        i_sonde = int(sonde_id[-2:])
        ds = cat['P5']['DROPSONDES'][params['flight_id']](i_sonde=i_sonde).to_dask()

        ax[mission].scatter(ds.Temp_recon, ds.GPS_Alt, **kwargs)

axes[0].set_ylabel('Altitude [m]')
axes[0].set_xlabel('Temperature [°C]')
   
plt.show()

### Humidity profile

fig, axes = plt.subplots(1, 3, sharey=True, sharex=True)

ax = {'ACLOUD': axes[0], 'AFLUX': axes[1], 'MOSAiC-ACA': axes[2]}

kwargs = dict(s=1, color='blue', alpha=0.4)
for mission, sondes in ds_dict.items():
    
    ax[mission].set_title(mission)
    
    for sonde_id, params in ds_dict[mission].items():

        # read dropsonde data
        i_sonde = int(sonde_id[-2:])
        ds = cat['P5']['DROPSONDES'][params['flight_id']](i_sonde=i_sonde).to_dask()

        ax[mission].scatter(ds.RHum_recon, ds.GPS_Alt, **kwargs)

axes[0].set_ylabel('Altitude [m]')
axes[0].set_xlabel('Relative humidity [%]')

plt.show()

### Wind profile

fig, axes = plt.subplots(1, 3, sharey=True)

ax = {'ACLOUD': axes[0], 'AFLUX': axes[1], 'MOSAiC-ACA': axes[2]}

kwargs = dict(s=1, color='green', alpha=0.4)
for mission, sondes in ds_dict.items():
    
    ax[mission].set_title(mission)
    ax[mission].set_xlim(0, 25)
    
    for sonde_id, params in ds_dict[mission].items():

        # read dropsonde data
        i_sonde = int(sonde_id[-2:])
        ds = cat['P5']['DROPSONDES'][params['flight_id']](i_sonde=i_sonde).to_dask()

        ax[mission].scatter(ds.Wind_vel, ds.GPS_Alt, **kwargs)

axes[0].set_ylabel('Altitude [m]')
axes[0].set_xlabel('Wind velocity [m/s]')

plt.show()

