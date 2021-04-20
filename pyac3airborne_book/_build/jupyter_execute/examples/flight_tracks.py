## Flight tracks from segment files

%pylab inline
import ac3airborne
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import ipyleaflet

cat = ac3airborne.get_intake_catalog()

meta = ac3airborne.get_flight_segments()

tracks = list(cat.Polar5.GPS_INS)

def track2layer(track, color="green", name=""):
    return ipyleaflet.Polyline(
        locations=np.stack([track.lat.values, track.lon.values], axis=1).tolist(), 
        color=color,
        fill=False,
        weight=2,
        name=name
    )

from simplification.cutil import simplify_coords_idx
def simplify_dataset(ds, tolerance):
    indices_to_take = simplify_coords_idx(np.stack([ds.lat.values, ds.lon.values], axis=1), tolerance)
    return ds.isel(time=indices_to_take)

colors = [matplotlib.colors.to_hex(c)
          for c in plt.cm.inferno(np.linspace(0, 1, len(tracks)))]

m = ipyleaflet.Map(
    basemap=ipyleaflet.basemaps.Esri.NatGeoWorldMap,
    center=(79, 6), zoom=4
)

print(tracks)

for flight_id,color in zip(tracks,colors):
    ds = cat.Polar5.GPS_INS[flight_id].to_dask()
    dsreduced = simplify_dataset(
        ds.sel(time=slice(meta['P5'][flight_id]['takeoff'],meta['P5'][flight_id]['landing'])), 1e-5)
    m.add_layer(track2layer(dsreduced,color))

m.add_control(ipyleaflet.ScaleControl(position='bottomleft'))
m.add_control(ipyleaflet.LegendControl(dict(zip(tracks, colors)),
                                       name="Flights",
                                       position="bottomright"))
m.add_control(ipyleaflet.LayersControl(position='topright'))
m.add_control(ipyleaflet.FullScreenControl())
display(m)

