import boto3, sys, os

DOWNDIR = "./Data/"
LEVEL2_BUCKET = "noaa-nesdis-tcprimed-pds"

# Instantiate S3 client
s3 = boto3.resource('s3')
s3cli = boto3.client('s3')
l2_bucket = s3.Bucket(LEVEL2_BUCKET)

def downloadstorm(basin=None, year=None, index=None, start=None, end=None):
	import pandas as pd
	from datetime import datetime
	if year < 2024:
		directory = f"v01r01/final/{year}/{basin}/{index}/"
	else:
		directory = f"v01r01/preliminary/{year}/{basin}/{index}/"

	passes = pd.DataFrame(columns = ['platform', 'instrument', 'dati', 'deltastart', 'deltaend'])
	for object in l2_bucket.objects.filter(Prefix=directory):
		name = object.key
		if 'env' in name:
			continue
		db, ver, tc, platform, instrument, passid, dati = name.split('_')
		dati = datetime.strptime(dati,'%Y%m%d%H%M%S.nc')
		passes.loc[name,:] = pd.Series([platform, instrument, dati, (dati-start).total_seconds(), (dati-end).total_seconds()], ['platform', 'instrument', 'dati', 'deltastart', 'deltaend'])
	if passes.empty:
		sys.exit("No passes found for requested TC")
	#for ii, row in passes.iterrows():
	#	dati = row['dati']
	#	passes.loc[row.index,'deltastart'] = dati - start
	#	passes.loc[row.index,'deltaend'] = dati - end
	#passes['deltastart'] = passes['dati'] - start
	#passes['deltaend'] = passes['dati'] - end
	passes = passes[(passes['deltastart'] >= 0) * (passes['deltaend'] <= 0)].loc[:,'platform':'dati']
	#print(passes)
	for name in passes.index:
		downloadfile(directory, name)
	return passes.sort_values(by='dati')

def downloadfile(directory, name):
	if not os.path.isfile(DOWNDIR+name):
		if not os.path.exists(DOWNDIR+'/'.join(name.split('/')[:-1])):
			os.makedirs(DOWNDIR+'/'.join(name.split('/')[:-1]))
		try:
			with open(DOWNDIR+name, 'wb') as f:
				s3cli.download_fileobj(LEVEL2_BUCKET, name, f)
		except:
			sys.exit(f"Download or parse failed. Exiting. Object: {name}")