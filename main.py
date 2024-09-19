import xarray as xr

DOWNDIR = "./Data/"

def plot(passds, passrow, basin, year, index):
	import matplotlib.pyplot as plt
	import cartopy.crs as ccrs
	import cartopy.feature as cfeature

	fig, ax = plt.subplots(2,2, gridspec_kw={'wspace': 0.1, 'hspace': 0.1, 'left': 0.05, 'right': 0.95, 'bottom': 0.05, 'top': 0.95}, subplot_kw={'projection': ccrs.PlateCarree()})
	ax0, ax1 = ax[0]
	ax2, ax3 = ax[1]
	plt.suptitle(f"{year} {basin}{index} {passrow.instrument} {passrow.platform} {passrow.dati}")

	if passrow.platform == "GMI":
		data37 = [passds.passive_microwave.S1['TB_36.64H'], passds.passive_microwave.S1['TB_36.64V']]
		coords37 = [passds.passive_microwave.S1.latitude, passds.passive_microwave.S1.longitude]
		data89 = [passds.passive_microwave.S1['TB_89.0H'], passds.passive_microwave.S1['TB_89.0V']]
		coords89 = [passds.passive_microwave.S1.latitude, passds.passive_microwave.S1.longitude]
		dataradar = passds.radar_radiometer.KuGMI.correctedReflectFactor_Ku
		coordsradar = [passds.radar_radiometer.KuGMI.latitude, passds.radar_radiometer.KuGMI.longitude, passds.radar_radiometer.KuGMI.binHeight]
	elif passrow.platform == "TMI":
		data37 = [passds.passive_microwave.S2['TB_37.0H'], passds.passive_microwave.S2['TB_37.0V']]
		coords37 = [passds.passive_microwave.S2.latitude, passds.passive_microwave.S2.longitude]
		data89 = [passds.passive_microwave.S3['TB_85.5H'], passds.passive_microwave.S3['TB_85.5V']]
		coords89 = [passds.passive_microwave.S3.latitude, passds.passive_microwave.S3.longitude]
		dataradar = passds.radar_radiometer.KuTMI.correctedReflectFactor_Ku
		coordsradar = [passds.radar_radiometer.KuTMI.latitude, passds.radar_radiometer.KuTMI.longitude, passds.radar_radiometer.KuTMI.binHeight]
	elif passrow.platform == "ATMS":
		data37 = [passds.passive_microwave.S2['TB_31.4QV']]
		coords37 = [passds.passive_microwave.S2.latitude, passds.passive_microwave.S2.longitude]
		data89 = [passds.passive_microwave.S3['TB_88.2QV']]
		coords89 = [passds.passive_microwave.S3.latitude, passds.passive_microwave.S3.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "MHS":
		data37 = None
		coords37 = None
		data89 = [passds.passive_microwave.S1['TB_89.0V']]
		coords89 = [passds.passive_microwave.S1.latitude, passds.passive_microwave.S1.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "SSMIS":
		data37 = [passds.passive_microwave.S2['TB_37.0H'], passds.passive_microwave.S2['TB_37.0V']]
		coords37 = [passds.passive_microwave.S2.latitude, passds.passive_microwave.S2.longitude]
		data89 = [passds.passive_microwave.S4['TB_91.665H'], passds.passive_microwave.S4['TB_91.665V']]
		coords89 = [passds.passive_microwave.S4.latitude, passds.passive_microwave.S4.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "SSMI":
		data37 = [passds.passive_microwave.S1['TB_37.0H'], passds.passive_microwave.S1['TB_37.0V']]
		coords37 = [passds.passive_microwave.S1.latitude, passds.passive_microwave.S1.longitude]
		data89 = [passds.passive_microwave.S2['TB_85.5H'], passds.passive_microwave.S2['TB_85.5V']]
		coords89 = [passds.passive_microwave.S2.latitude, passds.passive_microwave.S2.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "AMSR2":
		data37 = [passds.passive_microwave.S4['TB_36.5H'], passds.passive_microwave.S4['TB_36.5V']]
		coords37 = [passds.passive_microwave.S4.latitude, passds.passive_microwave.S4.longitude]
		data89 = [passds.passive_microwave.S6['TB_B89.0H'], passds.passive_microwave.S6['TB_B89.0V']]
		coords89 = [passds.passive_microwave.S6.latitude, passds.passive_microwave.S6.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "AMSRE":
		data37 = [passds.passive_microwave.S4['TB_36.5H'], passds.passive_microwave.S4['TB_36.5V']]
		coords37 = [passds.passive_microwave.S4.latitude, passds.passive_microwave.S4.longitude]
		data89 = [passds.passive_microwave.S6['TB_B89.0H'], passds.passive_microwave.S6['TB_B89.0V']]
		coords89 = [passds.passive_microwave.S6.latitude, passds.passive_microwave.S6.longitude]
		dataradar = None
		coordsradar = None
	elif passrow.platform == "AMSUB":
		data37 = None
		coords37 = None
		data89 = [passds.passive_microwave.S1['TB_89.0_0.9QV']]
		coords89 = [passds.passive_microwave.S1.latitude, passds.passive_microwave.S1.longitude]
		dataradar = None
		coordsradar = None

	try:
		datair = passds.infrared.IRWIN
		coordsir = [passds.infrared.latitude, passds.infrared.longitude]
	except:
		datair = None
		coordsir = None

	# TODO: ADD COASTLINES TO PLOTS

	if data37 is None or coords37 is None:
		ax0.set_visible(False)
	else:
		# TODO: ADD 37GHZ COLOR PLOTS
		ax0.pcolormesh()
	
	if data89 is None or coords89 is None:
		ax1.set_visible(False)
	else:
		# TODO: ADD 89GHZ PLOTS
		ax1.
	
	if datair is None or coordsir is None:
		ax2.set_visible(False)
	else:
		# TODO: ADD IR TO PLOTS
		ax2.
	
	if dataradar is None or coordsradar is None:
		ax3.set_visible(False)
	else:
		# TODO: ADD TMI/GMI RADAR PLOTS
	
	
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
		plot(xr.open_dataset(DOWNDIR+passrow.name), passrow, args.basin, year, index)