import xarray as xr
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

DOWNDIR = "./Data/"

bd = LinearSegmentedColormap.from_list("", [
    (0/120, "#a8d1ff"),
    (11/120, "#011a36"), 
    (12/120, "#000000"),
    (12/120, "#1d1d1d"),
    (21/120, "#fafafa"),
    (21/120, "#3a3a3a"),
    (60/120, "#d2d2d2"),
    (60/120, "#5b5b5b"),
    (71/120, "#5b5b5b"),
    (71/120, "#9a9a9a"),
    (83/120, "#9a9a9a"),
    (83/120, "#b7b7b7"),
    (93/120, "#b7b7b7"),
    (93/120, "#000000"),
    (99/120, "#000000"),
    (99/120, "#f9f9f9"),
    (105/120, "#f9f9f9"),
    (105/120, "#9e9e9e"),
    (110/120, "#9e9e9e"),
    (110/120, "#424242"),
    (120/120, "#424242")]).reversed()
vmax_bd = 303.15
vmin_bd = 183.15

def read_cmap(fname):
	import numpy as np

	cpt_file_path = fname
	colormap_data = np.loadtxt(cpt_file_path, skiprows=3, usecols=(1, 2, 3)) / 255.0  
	data_values = np.loadtxt(cpt_file_path, skiprows=3, usecols=0) 
	normalized_data_values = (data_values - np.nanmin(data_values)) / (np.nanmax(data_values) - np.nanmin(data_values))
	colormap_data_points = list(zip(normalized_data_values, colormap_data))
	if colormap_data_points[0][0] != 0.0:
		colormap_data_points.insert(0, (0.0, colormap_data[0]))
	if colormap_data_points[-1][0] != 1.0:
		colormap_data_points.append((1.0, colormap_data[-1]))
	return LinearSegmentedColormap.from_list('custom_cmap', colormap_data_points)

def plot(passfname, passrow, basin, year, index, zoom=None):
	import matplotlib.pyplot as plt
	import cartopy.crs as ccrs
	import cartopy.feature as cfeature
	from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
	#import matplotlib as mpl
	
	plt.rcParams.update({'font.size': 14})

	# Load data
	passds = {}
	#passds['passive_microwave'] = xr.open_dataset(passfname, group='/passive_microwave')
	try:
		S1 = xr.open_dataset(passfname, group='/passive_microwave/S1')
	except:
		pass
	try:
		S2 = xr.open_dataset(passfname, group='/passive_microwave/S2')
	except:
		pass
	try:
		S3 = xr.open_dataset(passfname, group='/passive_microwave/S3')
	except:
		pass
	try:
		S4 = xr.open_dataset(passfname, group='/passive_microwave/S4')
	except:
		pass
	try:
		S5 = xr.open_dataset(passfname, group='/passive_microwave/S5')
	except:
		pass
	try:
		S6 = xr.open_dataset(passfname, group='/passive_microwave/S6')
	except:
		pass
	try:
		KuTMI = xr.open_dataset(passfname, group='/radar_radiometer/KuTMI')
	except:
		pass
	try:
		KuGMI = xr.open_dataset(passfname, group='/radar_radiometer/KuGMI')
	except:
		pass
	passds['infrared'] = xr.open_dataset(passfname, group='/infrared')

	states_provinces = cfeature.NaturalEarthFeature(category='cultural',name='admin_1_states_provinces_lines',scale='50m',facecolor='none')
	cmap_89 = read_cmap('./nrl89H.ct')
	cmap_37 = read_cmap('./nrl37.ct')

	fig, ax = plt.subplots(2,2, gridspec_kw={'wspace': 0.1, 'hspace': 0.1, 'left': 0.05, 'right': 0.95, 'bottom': 0.05, 'top': 0.95}, subplot_kw={'projection': ccrs.PlateCarree()})
	ax0, ax1 = ax[0]
	ax2, ax3 = ax[1]
	plt.suptitle(f"{year} {basin}{index} {passrow.instrument} {passrow.platform} {passrow.dati}")

	if passrow.platform == "GMI":
		data37 = [S1['TB_36.64H'], S1['TB_36.64V']]
		coords37 = [S1.latitude, S1.longitude]
		data89 = [S1['TB_89.0H'], S1['TB_89.0V']]
		coords89 = [S1.latitude, S1.longitude]
		dataradar = KuGMI.correctedReflectFactor_Ku
		coordsradar = [KuGMI.latitude, KuGMI.longitude, KuGMI.binHeight]
	elif passrow.platform == "TMI":
		data37 = [S2['TB_37.0H'], S2['TB_37.0V']]
		coords37 = [S2.latitude, S2.longitude]
		data89 = [S3['TB_85.5H'], S3['TB_85.5V']]
		coords89 = [S3.latitude, S3.longitude]
		dataradar = KuTMI.correctedReflectFactor_Ku
		coordsradar = [KuTMI.latitude, KuTMI.longitude, KuTMI.binHeight]
	elif passrow.platform == "ATMS":
		data37 = [S2['TB_31.4QV']]
		coords37 = [S2.latitude, S2.longitude]
		data89 = [S3['TB_88.2QV']]
		coords89 = [S3.latitude, S3.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "MHS":
		data37 = None
		coords37 = None
		data89 = [S1['TB_89.0V']]
		coords89 = [S1.latitude, S1.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "SSMIS":
		data37 = [S2['TB_37.0H'], S2['TB_37.0V']]
		coords37 = [S2.latitude, S2.longitude]
		data89 = [S4['TB_91.665H'], S4['TB_91.665V']]
		coords89 = [S4.latitude, S4.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "SSMI":
		data37 = [S1['TB_37.0H'], S1['TB_37.0V']]
		coords37 = [S1.latitude, S1.longitude]
		data89 = [S2['TB_85.5H'], S2['TB_85.5V']]
		coords89 = [S2.latitude, S2.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "AMSR2":
		data37 = [S4['TB_36.5H'], S4['TB_36.5V']]
		coords37 = [S4.latitude, S4.longitude]
		data89 = [S6['TB_B89.0H'], S6['TB_B89.0V']]
		coords89 = [S6.latitude, S6.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "AMSRE":
		data37 = [S4['TB_36.5H'], S4['TB_36.5V']]
		coords37 = [S4.latitude, S4.longitude]
		data89 = [S6['TB_B89.0H'], S6['TB_B89.0V']]
		coords89 = [S6.latitude, S6.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "AMSUB":
		data37 = None
		coords37 = None
		data89 = [S1['TB_89.0_0.9QV']]
		coords89 = [S1.latitude, S1.longitude]
		dataradar = None
		coordsradar = None

	try:
		datair = passds['infrared'].IRWIN
		coordsir = [passds['infrared'].latitude, passds['infrared'].longitude]
	except:
		datair = None
		coordsir = None

	if datair is None or coordsir is None:
		ax2.set_visible(False)
	else:
		ax2.add_feature(cfeature.LAND)
		ax2.add_feature(cfeature.COASTLINE)
		ax2.add_feature(states_provinces, edgecolor='gray')
		pcm = ax2.pcolormesh(coordsir[1], coordsir[0], datair, cmap=bd, vmin=vmin_bd, vmax=vmax_bd)
		divider = make_axes_locatable(ax2)
		cax = divider.append_axes("right", size="5%", pad=0.05, axes_class=plt.Axes)
		plt.colorbar(pcm, cax=cax, label='Brightness Temperature (K)')
		ax2.set_title("Infrared Brightness Temperature")

	xlim = ax2.get_xlim()
	ylim = ax2.get_ylim()

	if data37 is None or coords37 is None:
		ax0.set_visible(False)
	else:
		ax0.add_feature(cfeature.LAND)
		ax0.add_feature(cfeature.COASTLINE)
		ax0.add_feature(states_provinces, edgecolor='gray')
		pcm = ax0.pcolormesh(coords37[1], coords37[0], data37[0], cmap=cmap_37, vmin=125, vmax=300)
		divider = make_axes_locatable(ax0)
		cax = divider.append_axes("right", size="5%", pad=0.05, axes_class=plt.Axes)
		plt.colorbar(pcm, cax=cax, label='Brightness Temperature (K)')
		ax0.set_title(data37[0].attrs['frequency'])
		ax0.set_xlim(xlim[0],xlim[1])
		ax0.set_ylim(ylim[0],ylim[1])
	
	if data89 is None or coords89 is None:
		ax1.set_visible(False)
	else:
		ax1.add_feature(cfeature.LAND)
		ax1.add_feature(cfeature.COASTLINE)
		ax1.add_feature(states_provinces, edgecolor='gray')
		pcm = ax1.pcolormesh(coords89[1], coords89[0], data89[0], cmap=cmap_89, vmin=105, vmax=305)
		divider = make_axes_locatable(ax1)
		cax = divider.append_axes("right", size="5%", pad=0.05, axes_class=plt.Axes)
		plt.colorbar(pcm, cax=cax, label='Brightness Temperature (K)')
		ax1.set_title(data89[0].attrs['frequency'])
		ax1.set_xlim(xlim[0],xlim[1])
		ax1.set_ylim(ylim[0],ylim[1])

		cax.set_title("Inspiration & Colortables, Data:\n@CocoasCola & Deelan Jariwala, TC-PRIMED\nPlot: @JWThiesing", loc='center', fontsize=8)
	
	if dataradar is None or coordsradar is None:
		ax3.set_visible(False)
	else:
		#hgtkm = 2.4
		#print(coordsradar[2].mean(['scan','beam']))
		#rangeindex = np.where(coordsradar[2])
		rangeindex = 10

		ax3.add_feature(cfeature.LAND)
		ax3.add_feature(cfeature.COASTLINE)
		ax3.add_feature(states_provinces, edgecolor='gray')
		pcm = ax3.pcolormesh(coordsradar[1], coordsradar[0], dataradar[rangeindex,:,:], cmap='Spectral_r', vmin=0, vmax=60)
		divider = make_axes_locatable(ax3)
		cax = divider.append_axes("right", size="5%", pad=0.05, axes_class=plt.Axes)
		plt.colorbar(pcm, cax=cax, label='Reflectivity (dBZ)')
		ax3.set_title(f'Ku Reflectivity at 2.4 km')
		ax3.set_xlim(xlim[0],xlim[1])
		ax3.set_ylim(ylim[0],ylim[1])

	if not zoom is None:
		zoom = float(zoom)
		storm_metadata = xr.open_dataset(passfname, group='/overpass_storm_metadata')
		lat = storm_metadata.storm_latitude
		lon = np.where(storm_metadata.storm_longitude > 180, (storm_metadata.storm_longitude)-360, storm_metadata.storm_longitude)
		#print(storm_metadata.storm_longitude, lon)
		bottom = (lat-zoom).values
		top = (lat+zoom).values
		left = (lon-zoom)
		right = (lon+zoom)
		#print(bottom, top, left, right)

		ax0.set_xlim(left, right)
		ax0.set_ylim(bottom, top)
		ax1.set_xlim(left, right)
		ax1.set_ylim(bottom, top)
		ax2.set_xlim(left, right)
		ax2.set_ylim(bottom, top)
		ax3.set_xlim(left, right)
		ax3.set_ylim(bottom, top)

	plt.tight_layout()
	plt.show()
	return

if __name__ == "__main__":
	import argparse, sys
	from datetime import datetime
	import download
	
	# Parse arguments!!
	parser = argparse.ArgumentParser(
						prog='main.py',
						description='Download and plot all microwave data from the selected datetime window for a given TC',
						epilog='')
	parser.add_argument('basin', choices=['AL','EP','CP','IO','SH','WP'])
	parser.add_argument('year')
	parser.add_argument('index')
	parser.add_argument('startdate')
	parser.add_argument('enddate')
	#parser.add_argument('-restrict_instrument', action='store_true')
	parser.add_argument('--restrict_instrument', default=None)
	parser.add_argument('--zoom', default=None)
	args = parser.parse_args(sys.argv[1:])
	year = int(args.year)
	index = str(args.index).rjust(2, '0')
	try:
		startdati = datetime.strptime(args.startdate,'%Y%m%d%H')
		enddati = datetime.strptime(args.enddate,'%Y%m%d%H')
	except:
		sys.exit("Datetime parsing failed. Try writing it in descending order of significance - YYYYMMDDHH")

	passes = download.downloadstorm(basin=args.basin, year=year, index=index, start=startdati, end=enddati)
	for ii, passrow in passes.iterrows():
		if not args.restrict_instrument is None and (not args.restrict_instrument == passrow.platform):
			continue
		plot(DOWNDIR+passrow.name, passrow, args.basin, year, index, zoom=args.zoom)