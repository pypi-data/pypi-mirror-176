
# Jaesub Hong (jhong@cfa.harvard.edu)

try:
	from cjson		 import color_scheme
except ModuleNotFoundError:
	from cjpy.cjson	 import color_scheme

import pandas as pd
import numpy as np
import astropy
import subprocess

from astropy.io	 import fits, ascii
from collections   import OrderedDict
from astropy.table import Table, QTable
from os		 import path
from colorama      import Fore, Back, Style
from statistics	 import mean, median
from IPython	 import embed
from datetime      import datetime
from pathlib       import Path

import re
import gzip
import csv

from bs4 import BeautifulSoup

cc=color_scheme('dark')

def to_num(candidate):
	"""parse string to number if possible
	work equally well with negative and positive numbers, integers and floats.

	Args:
	  candidate (str): string to convert

	Returns:
	  float | int | None: float or int if possible otherwise None
	"""
	try:
		float_value = float(candidate)
	except ValueError:
		return None

# optional part if you prefer int to float when decimal part is 0 
	if float_value.is_integer():
		return int(float_value)

	return float_value

#----------------------------------------------------------------------------
def panda_to_astropy(table):
#	table=table.convert_dtypes()
	ans=Table.from_pandas(table)
	for each in table:
		stype=str(table[each].dtype)
		if bool(re.match('Float',stype)):
			ans[each]=ans[each].astype(float)
		elif bool(re.match('Int',stype)):
			ans[each]=ans[each].astype(int)
	return ans

# write the table to a fits file
def to_fits(filename, table, overwrite=True, allstring=False):
	filename=str(Path(filename).expanduser())
	ft=table
	if type(table) is pd.core.frame.DataFrame: 
		ft=panda_to_astropy(table)
		if allstring:
			for key in ft.keys():
#			print(key)
				ft[key]=ft[key].astype('str')

#	from IPython import embed; embed()
	if overwrite: ft.write(filename, overwrite=overwrite, format='fits')
	else:	        
		uz_filename=filename
		if bool(re.search('\.gz$',filename)): uz_filename = re.sub('\.gz$','',filename)

		if uz_filename != filename:
			if path.exists(filename):
				output=subprocess.check_output(['gzip -f -d '+filename], shell=True).decode()

		ft.write(uz_filename, append=True, format='fits')

		if uz_filename != filename:
			output=subprocess.check_output(['gzip -f  '+uz_filename], shell=True).decode()

# write the table to a csv or fits file
def to_csv_or_fits(filename, table, overwrite=True, index=False, allstring=False):
	filename=str(Path(filename).expanduser())
	basename=path.basename(filename)
	if bool(re.search('\.csv$',basename)):
		if type(table) is astropy.table.table.Table:
			table = Table.to_pandas(table)
		table.to_csv (filename, index=index)
	elif bool(re.search('\.csv\.gz$',basename)):
		if type(table) is astropy.table.table.Table:
			table = Table.to_pandas(table)
		table.to_csv (filename, index=index)
	elif bool(re.search('\.fits$',basename)):
		to_fits(filename, table, overwrite=overwrite, allstring=allstring)
	elif bool(re.search('\.fits\.gz$',basename)):
		to_fits(filename, table, overwrite=overwrite, allstring=allstring)

# read the table from a csv or fits file
def from_csv_or_fits(filename, index=False, ftype=None, hdu=1, nopandas=False):
	filename=str(Path(filename).expanduser())
	basename=path.basename(filename)

	if ftype != None:
		if ftype == "fits":
			data = Table.read(filename, format='fits', hdu=hdu)
			data.convert_bytestring_to_unicode()
			print(nopandas,'---------')
			if nopandas: return data
			try:
				return data.to_pandas()
			except ValueError:
				# this is when some columns are multi-dimensional
				return data
		elif ftype == "json":
			return pd.read_json(filename)
		elif ftype == "csv":
			return pd.read_csv(filename, index_col=index)

	if bool(re.search('\.csv$',basename)):
		return pd.read_csv(filename, index_col=index)
	elif bool(re.search('\.csv\.gz$',basename)):
		return pd.read_csv(filename, index_col=index)
	elif bool(re.search('\.fits$',basename)) or bool(re.search('\.fits\.gz$',basename)):
		data = Table.read(filename, format='fits', hdu=hdu)
		data.convert_bytestring_to_unicode()
		if nopandas: return data
		try:
			return data.to_pandas()
		except ValueError:
			# this is when some columns are multi-dimensional
			return data
	elif bool(re.search('\.xml$',basename)):
		return pd.read_xml(filename)
	elif bool(re.search('\.xml.gz$',basename)):
		return pd.read_xml(filename)
	elif bool(re.search('\.json$',basename)):
		return pd.read_json(filename)
	elif bool(re.search('\.json.gz$',basename)):
		return pd.read_json(filename)

# read fits as astropy
def readfits(infile, hdu=1, hold=True):
	infile=str(Path(infile).expanduser())
	data = Table.read(infile, format='fits', hdu=hdu)

	if hold: embed()
	return True

# read SAORT output
def from_saort(infile):
	infile=str(Path(infile).expanduser())
	data = ascii.read(infile, delimiter=r'\s', comment='^;')
	header=data.meta['comments']

	mat = re.match(r'^(.+)\((.*)\)_for_(.+)\((.*)\)',header[0])

	ytit   = mat.group(1)
	yunit  = mat.group(2)
	if yunit == 'arcseconds': yunit = 'arcsec'

	coltit = mat.group(3)
	colunit= mat.group(4)

	cols = header[1].split('\t')

	mat = re.match(r'^(.+)\((.*)\)',cols[0])
	xtit = mat.group(1)
	xunit = mat.group(2)

	pdt = []
	for idx, each in enumerate(cols[1:]):
		pdt.append(QTable([data['col1'],data['col'+str(idx+2)]], 
			names=[xtit,ytit], units=[xunit,yunit], 
			meta={'extname':coltit+':'+cols[idx+1].strip()+colunit, 
				'time':str(datetime.now())}))

	return pdt

#----------------------------------------------------------------------------
# list the properties of fits tables
def lsfits(infile, hdu=None, overview=True, full=False, 
		column=None, header=None, stat=None,
		hold=False):
	"""list the properties of fits tables

	% lsfits filename [-full] [-column HDU] [-header HDU] [-stat HDU:column]

	e.g., lsfits example.fits """ 

	if infile == None:
		print("Need an input file. Try with -help")
		return

	hdul=fits.open(infile)
	if overview and column==None and header==None and stat==None:
		hdul.info()
	if full or column != None:
		for each in hdul:
			if each.is_image:  continue
			if type(column) is str:
				if each.name != column: continue
			print(cc.key+each.name,cc.reset)
			print(each.columns)
			for subeach in each.columns:
				print(subeach)
				print(subeach.name)
				print(type(subeach))
	if header != None:
		for each in hdul:
			if type(header) is str:
				if each.name != header: continue
			print(cc.key+each.name,cc.reset)
			hdr=str(each.header)
			for i in range(0, len(hdr), 80):
				line=hdr[i:i+79]
				if line != ''.ljust(79): print(line)
				i=i+80
	if stat != None:
		hdu, column = stat.split(':')
		data=from_csv_or_fits(infile, index=False, ftype='fits', hdu=hdu)
		print(infile, hdu, column,min(data[column]),max(data[column]))

	if hold: from IPython import embed; embed()
	hdul.close()

# list table columns
def list(infile, index=None, ftype=None, hdu=1, list=None, hold=False, 
		maxrow=0, match=None, stat=None, wrap=False, verbose: int=0):
	"""list table vertically, works for fits and csv tables

	% tab2list filename""" 

	if hold: from IPython import embed; embed()
	inp=from_csv_or_fits(infile, index=index, ftype=ftype, hdu=hdu)

	trows = len(inp)
	if match != None:
		match = match.split(';')
		for each in match:
			each=each.strip()
			if verbose>=2:  print(each)
			if   '==' in each:
				column, value = each.split('==')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp=inp[inp[column]== value]
			elif '!=' in each:
				column, value = each.split('!=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp=inp[inp[column]!= value]
			elif '~=' in each:
				column, value = each.split('~=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp=inp[inp[column].str.each(value)]
			elif '>=' in each:
				column, value = each.split('>=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp=inp[inp[column]>= value]
			elif '<=' in each:
				column, value = each.split('<=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp=inp[inp[column]<= value]
			elif '>' in each:
				column, value = each.split('>')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp=inp[inp[column]> value]
			elif '<' in each:
				column, value = each.split('<')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp=inp[inp[column]< value]

	if wrap: sep, rj='\n', 9
	else:	   sep, rj=', ', 0
	if stat != None:
		stat = stat.split(';')
		nrows= len(inp)
		if nrows == 0: print('No data left')
		else:
			for each in stat:
				each=each.strip()
				if inp[each].dtypes != 'object': 
					print('column: '.rjust(rj) + each, 
						'rows: '  .rjust(rj) + str(nrows)+ ' (' + str(trows) + ')', 
						'min: '   .rjust(rj) + '{0:.5}'.format(   min(inp[each])),
						'max: '   .rjust(rj) + '{0:.5}'.format(   max(inp[each])),
						'mean: '  .rjust(rj) + '{0:.5}'.format(  mean(inp[each])),
						'median: '.rjust(rj) + '{0:.5}'.format(median(inp[each])),
						'sum: '   .rjust(rj) + '{0:.5}'.format(   sum(inp[each])),
						sep=sep)
				else:
					print('column: '.rjust(rj) + each, 
						'rows: '  .rjust(rj) + str(nrows)+ ' (' + str(trows) + ')', 
						'min: '   .rjust(rj) + '{0:.20}'.format(   min(inp[each])),
						'max: '   .rjust(rj) + '{0:.20}'.format(   max(inp[each])),
						sep=sep)
		if list != True: return 0

	max_len=0
	maxrow=int(maxrow)
	if type(inp) is pd.core.frame.DataFrame: 
		# this one only for pandas
		new=True
		for idx, row in inp.iterrows():
#			print(row)
			if new:
				new=False
				for key in row.keys():
					clen=len(key)
					if max_len < clen:
						max_len=clen
				max_len+=1

			for key, val in row.items():
				print(f'{key:>{max_len}} | {val:<}')
			print()
			if maxrow > 0:
				if maxrow <= idx+1: break
	else:
		# astropy Table
		for key in inp.colnames:
			clen=len(key)
			if max_len < clen:
				max_len=clen
		max_len +=1
		for  row in inp.iterrows():
#			print(row)
			for key, val in zip(inp.colnames, row):
				if str(type(val)) == "<class 'numpy.ndarray'>": 
					vals=[]
					for each in val:
						if type(each) is bool or \
							str(type(each)) == "<class 'numpy.bool_'>":
								if each: vals.append('T')
								else:    vals.append('F')
						else: vals.append(str(each))
					val=",".join(vals)
#				print(f'{key:>{max_len}} | {val:<}')
				print(key.rjust(max_len),'|',val)
			print()
			if maxrow > 0:
				if maxrow <= idx+1: break


	return 0

# convert csv to fits and vice versa, based on extension
def csv2fits(infile, outfile, ftype=None, hdu=1):
	"""convert csv files to fits files and vice versa

	% csv2fits csv_file  -outfile fits_file
	% fits2csv fits_file -outfile csv_file [-hdu=HDU] 

		-hdu: set HDU id """ 

	inp=from_csv_or_fits(infile, ftype=ftype, hdu=hdu)
	to_csv_or_fits(outfile, inp)

def tdat2csv(infile, outfile, verbose: int=0, sort=None, slice=None):

	if verbose >=2: print(infile)

	names=[]
	dtype=OrderedDict()
	skiprows=0

	# if gz compressed
	if bool(re.search('\.gz$',infile)):
		with gzip.open(infile,'rt') as f:
			for line in f:
				skiprows = skiprows+1
				mat=re.search('^field\[(.*)\][ ]*=[ ]*([a-z]+)[0-9]+',line)
				if bool(mat):
					cdtype=mat.group(2)
					if cdtype == 'char': cdtype='str'
					if verbose >=3: 
						print(mat.group(1),' ',cdtype)
					names.append(mat.group(1))
					dtype[mat.group(1)]=cdtype
				if bool(re.match('^<DATA>$',line)):
					if verbose >=3: print('done!')
					break
	else:
		with open(infile,'rt') as f:
			for line in f:
				skiprows = skiprows+1
				mat=re.search('^field\[(.*)\][ ]*=[ ]*([a-z]+)[0-9]+',line)
				if bool(mat):
					cdtype=mat.group(2)
					if cdtype == 'char': cdtype='str'
					if verbose >=3: 
						print(mat.group(1),' ',cdtype)
					names.append(mat.group(1))
					dtype[mat.group(1)]=cdtype
				if bool(re.match('^<DATA>$',line)):
					if verbose >=3: print('done!')
					break

#	names.append('_')
#	dtype['_']='str'

#	skiprows=skiprows+200000
	print(skiprows)

	if verbose >=3: print(names)
	data=pd.read_csv(infile, names=names, sep='|', 
# 		dtype=dtype, 
		engine='c', 
		index_col=False,
		na_filter=False,
#		nrows=1716511,
#		nrows=711,
#		low_memory=False,
		encoding='cp1252', # to avoid failing after nrows=1716511
		skiprows=skiprows)

	if verbose >=3: 
		print(type(data))
#		print(data)
		print(type(data['name']))
		print(data['name'])

	data=data[data.name != '<END>']

	if sort != None:
		data=data.sort_values(by=sort)

	if slice != None:
		sl=slice
		for key in sl:
			print(key,sl[key])
			data=data[data[key] == sl[key]]

	#data.to_csv(outfile, index=False)
	to_csv_or_fits(outfile, data, allstring=True)

def filter(infile, outfile=None, sl=None, ftype=None, hdu=1, sort=None, nopandas=False,
		hold=False, all=False, overwrite=True):
	"""Usage: filter file [-slice options]

		-hdu: set HDU id """ 

	## need to implement copying the rest of the extensions

	data=from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if sl != None:
		for k, v in sl.items():
			print(k,v)
			if   v[0] == '==': data=data[data[k] == v[1]]
			elif v[0] == '!=': data=data[data[k] != v[1]]
			elif v[0] == '~=': data=data[data[k].str.match(v[1])]
			elif v[0] == '>=': data=data[data[k] >= v[1]]
			elif v[0] == '<=': data=data[data[k] <= v[1]]
			elif v[0] == '>' : data=data[data[k] >  v[1]]
			elif v[0] == '<' : data=data[data[k] <  v[1]]

	if sort != None:
		if   type(data) is pd.core.frame.DataFrame  : data=data.sort_values(by=sort)
		elif type(data) is astropy.table.table.Table: data.sort(sort)

	if hold: embed()
	if outfile != None: to_csv_or_fits(outfile, data, overwrite=overwrite)

#----------------------------------------------------------------------------
def html2csv(infile, outfile=None, header=None, start=0, meta=None,
		overwrite=True, hdu=None, units=None, dtype=None, verbose=0):
   
	# empty list
	data = []
	   
	# for getting the header from
	# the HTML file
	soup = BeautifulSoup(open(infile, encoding="utf-8-sig"),'html.parser')

	if header == None:
		list_header = []
		header = soup.find_all("table")[0].find("tr")
		for items in header:
			try:
				list_header.append(items.get_text().encode('utf-8'))
			except:
				continue
		start=start+1
	else:
		if type(header).__name__ == 'list':
			list_header=header
		else:
			list_header=header.keys()
			units=[]
			dtype_=[]
			for key, val in header.items():
				if type(val).__name__ == 'list': 
					units.append(val[0])
					dtype_.append(val[1])
				else:			     
					units.append(val)

			if dtype == None:
				if len(dtype_) != 0: 
					dtype=dtype_

	
	if units == None:
		list_units = []
		units = soup.find_all("table")[0].find("tr")[start:start+1]
		for items in units:
			try:
				list_units.append(text=items.get_text().encode('utf-8'))
			except:
				continue
		start=start+1
	else:
		list_units=units
	  
	ncol=len(list_header)
	# for getting the data 
#	print(start)
	HTML_data = soup.find_all("table")[0].find_all("tr")[start:]
	for element in HTML_data:
		sub_data = []
		k=0
		for sub_element in element:
			try:
				inp=sub_element.get_text().encode('utf-8')
				if dtype != None:
					if   dtype[k] == "int"  : inp=int(inp)
					elif dtype[k] == "long" : inp=long(inp)
					elif dtype[k] == "float": inp=float(inp)
				sub_data.append(inp)
				k = k+1
			except:
				continue
		if len(sub_data) != ncol: continue
		data.append(sub_data)
#		print(sub_data)
#		embed()
	  
	# Storing the data into Pandas
	# DataFrame 
	#dataFrame = pd.DataFrame(data = data[start:], columns = list_header)

	if meta == None:
		meta=OrderedDict()
	if hdu != None:
		meta['EXTNAME'] = hdu

	dataFrame = Table(rows = data, meta=meta,
			names = list_header, units=list_units)
	   
	# Converting Pandas DataFrame
	# into CSV file
	if outfile !=None:
		to_csv_or_fits(outfile, dataFrame, overwrite=overwrite)

