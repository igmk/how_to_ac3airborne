import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np

import ac3airborne

import os

# local caching
try:
    from dotenv import load_dotenv

    load_dotenv('/home/mech/projects/ac3/ac3airborne/.env')

    local_storage = os.environ['INTAKE_CACHE']
except ImportError:
    local_storage = '/tmp/'

kwds = {'simplecache': dict(
    cache_storage=local_storage, 
    same_names=True
)}

cat = ac3airborne.get_intake_catalog()

flight_id = 'COMPEX_P5_RF11'
campaign, platform, rf = flight_id.split('_')

ds_sic = cat[campaign][platform]['AMSR2_SIC'][flight_id].to_dask()


fig = plt.figure()
ax1 = fig.add_axes([0.1,0.2,0.9,0.8], projection=ccrs.NorthPolarStereo(central_longitude=10))
        
im = ax1.scatter(ds_sic.lon, ds_sic.lat, c=ds_sic.sic, vmin=0, vmax=100, transform=ccrs.PlateCarree(), cmap='Blues_r', s=1, lw=0)
ax1.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=["left", "bottom"],
    xlocs=mticker.FixedLocator(np.arange(-10, 20, 1)),
    ylocs=mticker.FixedLocator(np.arange(75, 85, 1)),
    x_inline=False,
    y_inline=False,
    rotate_labels=False,
    linewidth=0.25,
    color="#F5F5F5",
    alpha=0.5,
    zorder=5,
)
ax1.coastlines(color='white')
ax1.set_facecolor('k')

fig.colorbar(im, ax=ax1, label="Sea ice concentration [%]")

ax2 = fig.add_axes([0.4,0.0,0.6,0.1])

ax2.plot(ds_sic.time,ds_sic.sic/100.)

ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.set_xlabel('Time (hh:mm) [UTC]')





