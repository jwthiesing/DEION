import xarray as xr

DOWNDIR = "./Data/"

def plot(passds, passrow, basin, year, index):
	import matplotlib.pyplot as plt
	import cartopy.crs as ccrs

	fig, ax = plt.subplots(2,2, gridspec_kw={'wspace': 0.1, 'hspace': 0.1, 'left': 0.05, 'right': 0.95, 'bottom': 0.05, 'top': 0.95}, subplot_kw={'projection': ccrs.PlateCarree()})
	ax0, ax1 = ax[0]
	ax2, ax3 = ax[1]
	plt.suptitle(f"{year} {basin}{index} {passrow.instrument} {passrow.platform} {passrow.dati}")

	# TODO: ADD PLOTTING CAPABILITIES
	# TODO: ADD COASTLINES TO PLOTS
	# TODO: ADD IR TO PLOTS
	# TODO: ADD 89GHZ PLOTS
	# TODO: ADD 37GHZ COLOR PLOTS
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