
# Jaesub Hong (jhong@cfa.harvard.edu)
# to do 
#	- log scale tick labeling 
#	- multiplot for modeling fitting

try:
	import cjson
	import tabletool as tt
except ModuleNotFoundError:
	from cjpy import cjson
	from cjpy import tabletool as tt

from collections import OrderedDict

import pandas
import astropy
from astropy.table import Table, QTable
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize, LogNorm
import matplotlib.cm	 as cm
import matplotlib		 as mpl
from matplotlib.patches		import Circle
from matplotlib			import rc,rcParams
from matplotlib.ticker		import LogLocator
#from mpl_toolkits.axes_grid1  import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import numpy as np
import math
import healpy	as hp

from astropy.io import fits

from scipy import optimize as opt
from scipy import ndimage

from os		import path
from functools	import wraps

from IPython	import embed
import subprocess
from scipy.signal import savgol_filter
import re
from pathlib	import Path

def help_rcParams():
	text=OrderedDict()
	text["figure.figsize"       ] ="changes the figure size; keeps the font size the same"
	text["figure.dpi"		    ] ="changes the figure size; keep relative size of font to figure the same"
	text["font.size"		    ] ="change the font size; keeps the figure size the same"

	text["axes.labelsize"	    ] ="Fontsize of the x and y labels"
	text["axes.titlesize"	    ] ="Fontsize of the axes title"
	text["figure.titlesize"	    ] ="Size of the figure title (Figure.suptitle())"
	text["xtick.labelsize"	    ] ="Fontsize of the tick labels"
	text["ytick.labelsize"	    ] ="Fontsize of the tick labels"

	text["legend.fontsize"	    ] ="Fontsize for legends (plt.legend(), fig.legend())"
	text["legend.title_fontsize"] ="Fontsize for legend titles, None sets to the same as the default axes."
	text["legend.facecolor"	    ]	="Background color for legend"
	text["legend.edgecolor"	    ]	="Edge color for legend"
	text["legend.framealpha"    ]	="Background alpha for legend: 0.5"
	text["legend.labelspacing"  ]	="Vertical spacing for legend: 0.5"
	text["legend.frameon"       ]	="Legend frame: true"
	text["legend.loc"		    ] ="Location for legend: best"

	text["axes.grid"] ="Grid True or False"
	text["grid.alpha"] ="Grid transparency"
	text["grid.color"] ="Grid color"

	text["xtick.direction"] ="xtick direction"
	text["ytick.direction"] ="ytick direction"
	return text

def help_text(param):
	if param != None:
		if param == "basics":
			print("rcParams:")
			cjson.show(help_rcParams(),  notype=True)
			print("e.g., -*#rcParams:figure.figsize '12,10'")
			print
			print("See also",mpl.matplotlib_fname())
		else:
			print("available help words: basics")
		exit()

#----------------------------------------------------------------------------------------
class LogNorm_mid(LogNorm):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		LogNorm.__init__(self,vmin=vmin, vmax=vmax, clip=clip)
		self.mid=mid
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [np.log(self.vmin), np.log(self.mid), np.log(self.vmax)], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(np.log(value), x, y))

class Norm_mid(Normalize):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		Normalize.__init__(self,vmin=vmin, vmax=vmax, clip=clip)
		self.mid=mid
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.mid, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

#----------------------------------------------------------------------------------------
def read(infile, x=None, y=None, hdu=1, data=None,
		xlabel=None, ylabel=None,
		ftype=None, nopandas=True):
	if type(data).__name__ == "NoneType":
		if infile == None: 
			print("input data or file is required.")
			return None, None, None, None, None 

		if not path.isfile(infile):
			print("cannot read the file:", infile)
			return None, None, None, None, None

		data=tt.from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if x == None or y == None:
		if   type(data) is pandas.core.frame.DataFrame: colnames=data.columns.values.tolist()
		elif type(data) is   astropy.table.table.Table: colnames=data.colnames
		else: print('need to know column names or provide -x and -y')

#		colnames=data.colnames
		if x == None: 
			if len(colnames) == 1: x='_auto_'
			else:			     x=colnames[0]
		if y == None: 
			if len(colnames) == 1: y=colnames[0]
			else:			     y=colnames[1]
	
	# default label
	if xlabel == None:
		if x != '_auto_':
			xlabel = x 
			if hasattr(data[x],'info'):
				if hasattr(data[x].info,'unit'):
					xunit=data[x].info.unit
					if xunit != None: xlabel = xlabel +' ('+str(xunit)+')'

	if ylabel == None:
		ylabel = y 
		if hasattr(data[y],'info'):
			if hasattr(data[y].info,'unit'):
				yunit=data[y].info.unit
				if yunit != None: ylabel = ylabel +' ('+str(yunit)+')'

	return data, x, y, xlabel, ylabel
	
def minmax(data, nonzero=False):
	if nonzero: 
		data=np.array(data)
		return [np.min(data[np.nonzero(data)]), np.max(data)]
	else:       return [np.min(data), np.max(data)]

def set_range(data, margin=None, 
		dr=None, # data range
		dmin=None, dmax=None,
		scale='linear', drawdown=None):

	if type(dr) is list: 
		if dr[0] == None: dr = None
	
	if type(dr).__name__ == 'NoneType': dr= minmax(data, nonzero= scale != 'linear')

	if dmin != None: dr[0] = dmin
	if dmax != None: dr[1] = dmax

	if margin != None:
		dr = add_margin(dr, margin=margin, scale=scale, drawdown=drawdown)

	return dr

def set_range_2D(xdata, ydata, margin=None, xr=None, yr=None, 
		xmin=None, xmax=None, ymin=None, ymax=None,
		xlowdata=None, xhighdata=None, xerrdata=None,
		ylowdata=None, yhighdata=None, yerrdata=None,
		xscale='linear', yscale='linear', drawdown=None):

	if type(xr) is list: 
		if xr[0] == None: xr = None
	if type(yr) is list: 
		if yr[0] == None: yr = None
	
	if type(xr).__name__ == 'NoneType': 
		if type(xlowdata).__name__ != 'NoneType':
			xr= cjson.minmax(np.concatenate((np.array(xlowdata),np.array(xhighdata))), nonzero= xscale != 'linear')
		elif type(xerrdata).__name__ != 'NoneType':
			xr= cjson.minmax(np.concatenate((np.array(xdata-xerrdata),np.array(xdata+xerrdata))), nonzero= xscale != 'linear')
		else:
			xr= cjson.minmax(xdata, nonzero= xscale != 'linear')

	if type(yr).__name__ == 'NoneType': 
		if type(ylowdata).__name__ != 'NoneType':
			yr= cjson.minmax(np.concatenate((np.array(ylowdata),np.array(yhighdata))), nonzero= yscale != 'linear')
		elif type(yerrdata).__name__ != 'NoneType':
			yr= cjson.minmax(np.concatenate((np.array(ydata-yerrdata),np.array(ydata+yerrdata))), nonzero= yscale != 'linear')
		else:
			yr= cjson.minmax(ydata, nonzero= yscale != 'linear')

	if xmin != None: xr[0] = xmin
	if xmax != None: xr[1] = xmax
	if ymin != None: yr[0] = ymin
	if ymax != None: yr[1] = ymax

	if margin != None:
		if type(margin) is not list:
			xr = add_margin(xr, margin=margin, scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin, scale=yscale, drawdown=drawdown)
		elif len(margin) == 2:
			xr = add_margin(xr, margin=margin[0], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[1], scale=yscale, drawdown=drawdown)
		elif len(margin) == 4:
			xr = add_margin(xr, margin=margin[0:1], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[2:3], scale=yscale, drawdown=drawdown)

	return xr, yr

def get_log_edges(vr, nbin):
	logvr = [math.log(vr[0],10), math.log(vr[1],10)]
	logslope = logvr[1] - logvr[0]
	return [10.0**(logslope*v/nbin+logvr[0]) for v in range(0,nbin+1)]

def get_edges(vr, nbin, log=False):
	if log:
		logvr = [math.log(vr[0],10), math.log(vr[1],10)]
		logslope = logvr[1] - logvr[0]
		return [10.0**(logslope*v/nbin+logvr[0]) for v in range(0,nbin+1)]
	else:
		step = (vr[1] - vr[0])/nbin
		return [v*step+vr[0] for v in range(0,nbin+1)]

def add_margin(prange, margin=None, scale='linear', drawdown=None):

	if   margin == None     : margin=[0.2,0.2]
	elif np.isscalar(margin): margin=[margin, margin]
	if scale == 'linear':
		diff=prange[1]-prange[0]
		prange=[prange[0]-margin[0]*diff,prange[1]+margin[1]*diff]
	else:
		if prange[0] <= 0.0:
			if drawdown == None: drawdown = 1.e-5
			prange[0]=prange[1]*drawdown

		logpr = [math.log(v,10) for v in prange]
		diff = logpr[1]-logpr[0]
		logpr=[logpr[0]-margin[0]*diff,logpr[1]+margin[1]*diff]
		prange=[10.0**v for v in logpr]

	return prange

def filter_by_range(xdata, ydata, xr, yr, weights=None):
#	embed()
#	xdata=np.array(xdata)
#	ydata=np.array(ydata)
	mask = (xdata >= xr[0]) & (xdata <= xr[1]) & (ydata >= yr[0]) & (ydata <= yr[1]) 
	xdata=xdata[mask]
	ydata=ydata[mask]

	if type(weights).__name__ != 'NoneType':
		weights=weights[mask]
#	if filter:
#		 data=data[data[x] >= xr[0]]
#		 data=data[data[x] <= xr[1]]
#		 data=data[data[y] >= yr[0]]
#		 data=data[data[y] <= yr[1]]

	return xdata, ydata, weights

def val2pix(val, vr=None, pr=None):
	# value to pixel
	slope=(pr[1]-pr[0])/(vr[1]-vr[0])
	if type(val) is not list:
		return int(slope*(val-vr[1])+pr[0])
	return [int(slope*(v-vr[1])+pr[0]) for v in val]

def pix2val(pix, vr=None, pr=None):
	# pixel to value
	slope=(vr[1]-vr[0])/(pr[1]-pr[0])
	if type(pix) is not list:
		return slope*(pix-pr[0])+vr[0]
	return [slope*(p-pr[0])+vr[0] for p in pix]

#----------------------------------------------------------------------------------------
# obsolete
# set this in matplotlib.matplotlib_fname()
def default_rcParams(rcParams=None):
	defaults=OrderedDict()
	defaults["figure.dpi"		]= 150
	defaults["axes.grid"		]= True
	defaults["xtick.top"		]= True
	defaults["legend.framealpha"	]= 0.7
	defaults["legend.facecolor"	]= "white"
	defaults["legend.edgecolor"	]= "None"
	defaults["legend.frameon"	]= True
	defaults["legend.fancybox"	]= False
	defaults["legend.labelspacing"]= 0.3
	defaults["legend.loc"		]= "best"

	if rcParams != None: 
		for key in defaults.keys() - rcParams.keys():
			rcParams[key] = defaults[key]
		return rcParams
	else: return defaults

def set_rcParams(rcParams=None, verbose=0, force=False, name=None):
	# run only once unless forced
	if not force:
		if hasattr(set_rcParams,'new'): return
	set_rcParams.new=False

	defaults = OrderedDict()
	if rcParams == None: 
		if name == None: return
		elif name == "dplot":
			defaults["xtick.top"		]= False
			defaults["ytick.right"		]= False
			defaults["axes.grid"		]= False
			defaults["xtick.direction"	]= "out"
			defaults["ytick.direction"	]= "out"
		else: return
		rcParams= OrderedDict()

	for key, val in rcParams.items():
		if verbose >=2: print(key,val)
		plt.rcParams[key] = val

	for key in defaults.keys() - rcParams.keys():
		if verbose >=2: print(key,defaults[key])
		plt.rcParams[key] = defaults[key]
	
# obsolete, just use set_rcParams
def set_fig_basics(figsize=None, dpi=None, fontsize=None, 
		legendsize=None, titlesize=None):
	# changes the figure size; keeps the font size the same
	if figsize != None: 
		plt.rcParams["figure.figsize"] = (float(figsize[0]), float(figsize[1]))

	# changes the figure size; keep relative size of font to figure the same
	if dpi != None: 
		plt.rcParams["figure.dpi"] = int(dpi)

	# change the font size; keeps the figure size the same
	if fontsize != None:
		plt.rcParams["font.size"] = float(fontsize)

	# xx-small, x-small, small, medium, large, x-large, xx-large, smaller, larger.

	if legendsize != None:
		plt.rcParams["legend.fontsize"] = legendsize

	if titlesize != None:
		plt.rcParams["axes.titlesize"] = titlesize

#----------------------------------------------------------------------------------------
def wrap(plt, xr=None, yr=None, xlabel=None, ylabel=None, 
		title="", xscale='linear', yscale='linear', outfile=None, 
		y_title=1.0, rect=[0,0,1,1],
		ax2=None, ay2=None, ax=None, 
		xlabel2=None, ylabel2=None, 
		xr2=None, yr2=None, tight=True,
		xticks=None, yticks=None,
		xtickv=None, ytickv=None, grid=None,
		label=True, display=True, ion=False):

	if label:
		if xlabel != None: ax.set_xlabel(xlabel)
		if ax2 != None: 
			if xlabel2 != None: 
				# print(ax2, xlabel2)
				ax2.set_xlabel(xlabel2)

		if ylabel != None: ax.set_ylabel(ylabel)
		if ay2 != None: 
			if ylabel2 != None: 
#				print(ay2, ylabel2)
				ay2.set_ylabel(ylabel2)
#		print('rect',rect)
		# this needs a clean up
		plt.title(title, y=y_title)

	if type(xr).__name__ != "NoneType":
		ax.set_xlim(xr)

	if ax2 != None: 
		if type(xr2).__name__ != "NoneType":
			ax2.set_xlim(xr2)

	if type(yr).__name__ != "NoneType":
		ax.set_ylim(yr)
	if ay2 != None: 
		if type(yr2).__name__ != "NoneType":
			ay2.set_ylim(yr2)

	# if xscale != None: plt.xscale(xscale)
	# if yscale != None: plt.yscale(yscale)
	aux_xtick=False
	if xscale != None: 
		ax.set_xscale(xscale)
		if xscale == "log":
			xr=ax.get_xlim()
			if xr[1]/xr[0] < 100:
				aux_xtick=True
	aux_ytick=False
	if yscale != None: 
		ax.set_yscale(yscale)
		if yscale == "log":
			yr=ax.get_ylim()
			if yr[1]/yr[0] < 100:
				aux_ytick=True

	# locs, labels = plt.xticks()
	# embed()

	if type(xticks).__name__ != "NoneType":
		if type(xtickv).__name__ == "NoneType":
			xtickv=[float(v) for v in xticks]
		ax.set_xticks(xtickv, xticks)
		# ax.set_xticks(xtickv)
	if type(yticks).__name__ != "NoneType":
		if type(ytickv).__name__ == "NoneType":
			ytickv=[float(v) for v in yticks]
		ax.set_yticks(ytickv, yticks)

	if tight:
		plt.tight_layout(rect=rect)
	if grid != None:
		if grid == True:
			plt.grid()

	if not ion: 
		if outfile != None: 
			plt.savefig(Path(outfile).expanduser())
			plt.close("all")
		else: 
			if display: plt.show()

def colorbar(cbar, im, ax, fig, orientation=None, ticks_position=None):
	cax = ax.inset_axes(cbar) #, transform=ax.transAxes)
	fig.colorbar(im, 
			orientation=orientation,
			cax=cax)
	if ticks_position != None:
		if ticks_position == 'left' or ticks_position == 'right':
			cax.yaxis.set_ticks_position(ticks_position)
		if ticks_position == 'bottom' or ticks_position == 'top':
			cax.xaxis.set_ticks_position(ticks_position)

def colorbar_set(cbar, im, ax, fig, 
		xlabel=None, ylabel=None, title=None,
		off=None, width=None, length=None, rect=[0.,0.,1.,1.],
		orientation=None, outside=False):

	if not outside:
		if off    == None: off    = 0.03
		if width  == None: width  = 0.03
		if length == None: length = 0.5-off
		loff = 1.0-length-off
		woff = 1.0-width-off
		if orientation == 'vertical':
			if cbar == 'lower,left':
				rect=[off,off,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
			elif cbar == 'upper,left':
				rect=[off,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
			elif cbar == 'lower,right':
				rect=[woff,off,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
			elif cbar == 'upper,right':
				rect=[woff,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
		elif orientation == 'horizontal':
			if cbar == 'lower,left':
				rect=[off,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'upper,left':
				rect=[off,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'lower,right':
				rect=[loff,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'upper,right':
				rect=[loff,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
	else:
		if width  == None: width  = 0.03
		if length == None: length = 0.5
		if off    == None: off    = -0.10 - width
		loff = 0.5
		woff = 1.02
		y=rect[3]+(rect[3]-1)*20.
		if orientation == 'vertical':
			if cbar == 'lower,left':
				rect=[off,0,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel, loc='top')
			elif cbar == 'upper,left':
				rect=[off,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel, loc='bottom')
			elif cbar == 'lower,right':
				rect=[woff,0,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel)
			elif cbar == 'upper,right':
				rect=[woff,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel)
			ax.set_title(title, y=y)
		elif orientation == 'horizontal':
			if cbar == 'lower,left':
				ax.set_xlabel(xlabel,loc='right')
				ax.set_title(title, y=y)
				rect=[0,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'upper,left':
				ax.set_xlabel(xlabel)
				ax.set_title(title, y=y, loc='right')
				rect=[0,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'lower,right':
				ax.set_xlabel(xlabel, loc='left')
				ax.set_title(title,y=y)
				rect=[loff,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'upper,right':
				ax.set_xlabel(xlabel)
				ax.set_title(title, y=y, loc='left')
				rect=[loff,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			ax.set_ylabel(ylabel)

def despine_axes(ax, despine):
	if despine == None: despine = False
	if type(despine) is bool:
		if despine:
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
	else:
		for each in despine.split(','):
			ax.spines[each].set_visible(False)

#----------------------------------------------------------------------------------------
def hist2line(edges, values):
	edges = np.array(edges)
	values = np.array(values)
	x, y = [edges[0]], [values[0]]
	c = []
	for i in range(1, len(values)):
		x.append(edges[i])
		x.append(edges[i])
		y.append(values[i-1])
		y.append(values[i])
		c.append((edges[i-1]+edges[i])*0.5)
	x.append(edges[-1])
	y.append(values[-1])
	c.append((edges[-2]+edges[-1])*0.5)
	return x, y, c

#----------------------------------------------------------------------------------------
def prep_data_deco(func):

	def xdexpr(expr, x, y):
		if expr !=None: return eval(expr)
		else: return x

	def ydexpr(expr, x, y):
		if expr !=None: return eval(expr)
		else: return y

	def errexpr(expr, err, x, y):
		if expr !=None: return eval(expr)
		else: return err

	@wraps(func)
	def prep_data(*args, xdata=None, ydata=None, weights=None,
			xexpr=None, yexpr=None, 
			xerrdata=None, yerrdata=None, xerr=None, yerr=None, xeexpr=None, yeexpr=None, 
			xhighdata=None, xlowdata=None, xhigh=None, xlow=None,
			yhighdata=None, ylowdata=None, yhigh=None, ylow=None,
			data=None, image=None, infile=None, x=None, y=None, 
			xlabel=None, ylabel=None, xr=None, yr=None, 
			xmin=None, xmax=None, ymin=None, ymax=None,
			margin=0.0, drawdown=None, filter=False,
			xscale=None, yscale=None, xlog=False, ylog=False, 
			rcParams=None, clip=None,  # pixel coordinates
			verbose: int=0, ftype=None, hdu=None, help=None, **kwargs):

		help_text(help)

		loaded = None

		# try loading an image
		if type(image) is bool:
			if image:
				# read image
				# assume fits image for now
				hdul=fits.open(infile)
				if hdu == None: hdu=0
#				image=np.transpose(hdul[hdu].data)
				image=hdul[hdu].data
				loaded='image'
		elif type(image).__name__ != "NoneType":
			loaded='image'

		# make sure 2-d image and clip if requested
		if loaded == "image":
			ndim = image.ndim
			if ndim == 3: 
				image = image.sum(axis=0)
			image=np.transpose(image)
			#print(image.shape)

			if type(clip) is list:
				# x and y seem to be swapped
				#image=image[clip[2]:clip[3],clip[0]:clip[1]]
				image=image[clip[0]:clip[1],clip[2]:clip[3]]

			nbinx, nbiny=image.shape
			#print(nbinx,nbiny)
			if type(clip) is not list:
				if xr == None: xr=[0,nbinx]
				if yr == None: yr=[0,nbiny]
			else:
				if xr == None: xr=[clip[0],clip[1]]
				if yr == None: yr=[clip[2],clip[3]]

		# if there is no image then try loading a table
		if type(xdata).__name__ == "NoneType" and loaded == None:
			if hdu == None: hdu=1
			data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data, 
					xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu)
			if type(data).__name__ == "NoneType": return False

			ydata=data[y]
			if x == '_auto_': xdata=np.arange(0, len(ydata))
			else: xdata=data[x]

			if xerr  != None: xerrdata=data[xerr]
			if yerr  != None: yerrdata=data[yerr]
			if xlow  != None: xlowdata =data[xlow]
			if xhigh != None: xhighdata=data[xhigh]
			if ylow  != None: ylowdata =data[ylow]
			if yhigh != None: yhighdata=data[yhigh]
			loaded='table'

		if xscale == None: 
			xscale = 'log' if xlog else 'linear'
		if yscale == None: 
			yscale = 'log' if ylog else 'linear'

		# change xdata and ydata by expr
		xdata = xdexpr(xexpr, xdata, ydata)
		ydata = ydexpr(yexpr, xdata, ydata)
		xerrdata = errexpr(xeexpr, xerrdata, xdata, ydata)
		yerrdata = errexpr(yeexpr, yerrdata, xdata, ydata)

		xr, yr =  set_range_2D(xdata, ydata, xr=xr, yr=yr, 
				xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
				margin=margin, drawdown=drawdown,
				xlowdata=xlowdata, xhighdata=xhighdata, xerrdata=xerrdata,
				ylowdata=ylowdata, yhighdata=yhighdata, yerrdata=yerrdata,
				xscale=xscale, yscale=yscale)

		if filter:
#			if loaded == 'table':
			if type(xdata).__name__ != 'NoneType':
				xdata, ydata, weights = filter_by_range(xdata, ydata, xr, yr, weights=weights)
				# need to clip the image

		set_rcParams(rcParams, verbose=verbose, name=func.__name__)

		if type(infile   ).__name__ != 'NoneType': kwargs['infile'     ] = infile
		if type(ftype    ).__name__ != 'NoneType': kwargs['ftype'      ] = ftype
		if type(hdu      ).__name__ != 'NoneType': kwargs['hdu'        ] = hdu
		if type(xerrdata ).__name__ != 'NoneType': kwargs['xerrdata'   ] = xerrdata
		if type(yerrdata ).__name__ != 'NoneType': kwargs['yerrdata'   ] = yerrdata
		if type(xlowdata ).__name__ != 'NoneType': kwargs['xlowdata'   ] = xlowdata
		if type(ylowdata ).__name__ != 'NoneType': kwargs['ylowdata'   ] = ylowdata
		if type(xhighdata).__name__ != 'NoneType': kwargs['xhighdata'  ] = xhighdata
		if type(yhighdata).__name__ != 'NoneType': kwargs['yhighdata'  ] = yhighdata

		return func(*args, xdata=xdata, ydata=ydata, weights=weights,
			data=data, image=image, 
			xlabel=xlabel, ylabel=ylabel, xr=xr, yr=yr, 
			xscale=xscale, yscale=yscale, 
			margin=margin, drawdown=drawdown,
			verbose=verbose, help=None, 
			**kwargs)

	return prep_data

# two part reading
# combined model matching the regular data point to set up residual
# combined model and its components with high x-axis scaling
# the latter could be in a different HDU, while the former can be in the same HDU as the data
def prep_model_deco(func):

	def mdexpr(expr, m, x, y):
		if expr !=None: return eval(expr)
		else: return m

	def rdexpr(expr,  r, m, x, y):
		if expr !=None: return eval(expr)
		else: return r

	@wraps(func)
	def prep_data(*args, x=None, m=None, r=None,
			infile=None, ftype=None, hdu=None, 
			xdata=None, ydata=None, mdata=None, 
			rexpr=None, mexpr=None,
			rlabel=None, rr=None, rscale='linear',
			mlabel=None,
			xlabel=None, ylabel=None, xr=None, yr=None, 
			xscale=None, yscale=None, 
			margin=None, drawdown=None,
			rmin=None, rmax=None, 
			rmargin=0.0, data=None,
			xerrdata=None, yerrdata=None, 
			xlowdata=None, xhighdata=None,
			ylowdata=None, yhighdata=None,
			verbose: int=0, 
			mhdu=None, phdu=None,
			help=None, **kwargs):

		help_text(help)

		loaded = None

		# if there is no image then try loading a table
		if type(mdata).__name__ == "NoneType" and loaded == None:
			if hdu == None: hdu=1
			data_, m_, r_, mlabel, rlabel = read(infile, x=m, y=r, data=data, 
					xlabel=None, ylabel=rlabel, ftype=ftype, hdu=hdu)
			if type(data).__name__ == "NoneType": return False

			if m != None: mdata=data[m]
			else:         mdata=None
			if r != None: rdata=data[r]
			else:         rdata=None

			loaded='table'

		# change xdata and ydata by expr
		mdata = mdexpr(mexpr, mdata, xdata, ydata)
		rdata = rdexpr(rexpr, rdata, mdata, xdata, ydata)

		rr =  set_range(rdata, dr=rr, 
				dmin=rmin, dmax=rmax,
				margin=rmargin, drawdown=None,
				scale=rscale)

		# if mhdu is present replace mdata
		if type(mhdu).__name__ != 'NoneType':
			toUnpack = read(infile, ftype=ftype, hdu=mhdu)
			mdata = toUnpack[0]

		# if phdu is present read parameter data
		if type(phdu).__name__ != 'NoneType':
			toUnpack = read(infile, ftype=ftype, hdu=phdu)
			pdata = toUnpack[0]
		else:
			pdata=None

		return func(*args, xdata=xdata, ydata=ydata, 
			mdata=mdata, rdata=rdata, pdata=pdata,
			xlabel=xlabel, ylabel=ylabel, xr=xr, yr=yr, 
			xscale=xscale, yscale=yscale, 
			margin=margin, drawdown=drawdown,
			data=data, rlabel=rlabel, rr=rr, mlabel=mlabel,
			xerrdata=xerrdata, yerrdata=yerrdata, 
			xlowdata=xlowdata, xhighdata=xhighdata,
			ylowdata=ylowdata, yhighdata=yhighdata,
			rmargin=rmargin, 
			verbose=verbose, help=None, **kwargs)

	return prep_data
#----------------------------------------------------------------------------------------
# 1-D plots from a single data set
@prep_data_deco
def plot1d(xdata=None, ydata=None, data=None, 
		xr=None, yr=None, xlabel=None, ylabel=None,  
		xr2=None, yr2=None, xlabel2=None, ylabel2=None,  
		outfile=None, attr='', alpha=None,
		xscale='linear', yscale='linear',
		marker='.', linestyle='None', color=None, linewidth=None,
		display=True, savgol=None, ion=False, grid=None,
		help=None, hold=False, verbose: int= 0, **kwargs):
	"""Plot 1-D from input table
	"""

	def show(ion=True):
		if ion: plt.ion()

		nonlocal xdata, ydata, marker
		fig, ax = plt.subplots()

		attrs = attr.split(',')
		if 'hist' in attrs:
			# we assume this is for histogram
			xdata=np.array(xdata)
			ydata=np.array(ydata)
			if len(xdata) == len(ydata)+1:
				xh, yh, xc = hist2line(xdata, ydata)
			elif len(xdata) == len(ydata):
				extend=np.concatenate([xdata[0]*2-xdata[1],xdata,xdata[-1]*2-xdata[-2]], axis=None)
				roll =np.roll(extend, 1)
				edges = (extend+roll)/2
				xh, yh, xc = hist2line(edges[1:], ydata)
				xc=xdata

			plt.plot(xh, yh,
				color=color, alpha=alpha,
				marker=None, linestyle=linestyle, linewidth=linewidth)
			plt.plot(xc, ydata,
				color=color,  alpha=alpha,
				marker=marker, linestyle='none')
			xdata=xc
		else:
			plt.plot(xdata, ydata,
				color=color, alpha=alpha,
				marker=marker, linestyle=linestyle)

		if 'poisson_error' in attrs:
			for exc, ey in zip(xdata, ydata):
				err= math.sqrt(ey)
				plt.plot([exc,exc], [ey-err,ey+err],
					color=color,  alpha=alpha,
					marker=None, linestyle='solid')

		# smoothing?
		if type(savgol).__name__ != 'NoneType':
			print(savgol)
			ydata = savgol_filter(ydata, savgol[0], savgol[1])
			plt.plot(xdata, ydata,
				color='red', label='savgol smooth',
				linestyle='solid')

		wrap(plt, xr, yr, xlabel, ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, 
				ax=ax,
				display=display, ion=ion, grid=grid)

	show(ion=ion)
	if hold: embed()

	return plt

# 2-D plots from a single data set
@prep_data_deco
def dplot(xdata=None, ydata=None, image=None, data=None,
		xr=None, yr=None, zr=None,
		zmin=None, zmax=None, zoff=None,
		zmid=None,
		zlthresh=None, zlscale=None,
		outfile=None, 
		xscale=None, yscale=None,
		xedges=None, yedges=None,
		xlabel=None, ylabel=None, title=None,
		xr2=None, yr2=None, xlabel2=None, ylabel2=None,  
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, cmap='Blues', aspect='auto',
		interpolation=None, display=True, weights=None,
		cbar=True, cb_orientation='vertical', cb_ticks_position='right', cb_outside=False,
		cb_off=None, cb_width=None, cb_length=None, zclip=False,
		xhist=False, xh_height=0.15, xh_scale=None, 
		yhist=False, yh_height=0.15, yh_scale=None, 
		xslice=None, yslice=None, # data coordinateslike xr or yr (not necessarily pixels)
		halpha=0.3, hcolor="darkblue", hgap=0.04, hheight: float=0.15,
		despine=None, margin=0.0, drawdown=None,
		noplot=False,
		help=None, hold=False, verbose:int= 0):
	""" 2-d density plot 
	"""

	if type(image).__name__ == 'NoneType':
		# data points
		if binsize != None:  binx,  biny = binsize, binsize
		if nbin    != None: nbinx, nbiny = nbin,    nbin

		if binx==None:  binx = (xr[1]-xr[0])/nbinx
		else:          nbinx = int((xr[1]-xr[0])/binx)

		if biny==None:  biny = (yr[1]-yr[0])/nbiny
		else:          nbiny = int((yr[1]-yr[0])/biny)
		doimage=False
	else:
		# image input
		# assume xr, and yr is given, and probably no log scale for x and y axes?
		nbinx, nbiny = image.shape
#		ndim = image.ndim
#		if   ndim == 2: nbinx, nbiny = image.shape
#		elif ndim == 3: 
#			nbinz, nbinx, nbiny = image.shape
#			image = image.sum(axis=0)
		if zmax == None: zmax = np.max(image)
		if zmin == None: zmin = np.min(image)
		binx = (xr[1]-xr[0])/nbinx
		biny = (yr[1]-yr[0])/nbiny
		doimage=True


	if type(xedges).__name__ == 'NoneType':
#		xedges = nbinx
#		if xscale == 'log': xedges = get_log_edges(xr, nbinx)
		# now force xedges to be array regardless of log or linear scale
		# otherwise, numpy.histogram2d seems to limit the image range by the data
		xedges = get_edges(xr, nbinx, log= xscale =='log')

	if type(yedges).__name__ == 'NoneType':
#		yedges = nbiny
#		if yscale == 'log': yedges = get_log_edges(yr, nbiny)
		# now force xedges to be array regardless of log or linear scale
		yedges = get_edges(yr, nbiny, log= yscale =='log')

	bins = [xedges, yedges]

	if not doimage:
		# to get zmax
		heatmap, *_ = np.histogram2d(xdata, ydata, bins=bins, weights=weights)
		if zmax == None: zmax=np.max(heatmap.T)
		if zmin == None: zmin=np.min(heatmap.T)

		if noplot: return heatmap.T, xedges, yedges
		weights = np.ones(len(xdata))
	else:
		if type(xedges) is not list:
			xedges_ = [ii*binx+xr[0]+binx*0.5 for ii in range(0,nbinx)]
		else:
			xedges_ = [(v+w)*0.5 for v, w in zip(xedges[:-1:], xedges[1::])]

#		xdata   = xedges_ * nbiny
		xdata   = [[v]  * nbiny for v in xedges_]
		xdata   = np.array(xdata).flatten()

		if type(xedges) is not list:
			yedges_ = [ii*binx+yr[0]+binx*0.5 for ii in range(0,nbiny)]
		else:
			yedges_ = [(v+w)*0.5 for v, w in zip(yedges[:-1:], yedges[1::])]
#		ydata   = [[v]  * nbinx for v in yedges_]
#		ydata   = np.array(ydata).flatten()
		ydata   = yedges_ * nbinx

		weights = image.flatten()
		if zmax == None: zmax=np.max(weights)
		if zmin == None: zmin=np.min(weights)


	def show(ion=True):

		nonlocal zmin,zmax, zoff
		nonlocal zmid
		nonlocal zlthresh, zlscale
		nonlocal zclip
		nonlocal xr, yr
		fig, ax = plt.subplots()

		if ion: plt.ion()
		if not zlog:
			if zr != None: 
				zmin =zr[0]
				zmax =zr[1]

			if zmid != None:
#				norm=colors.TwoSlopeNorm(zmid, vmin=zmin, vmax=zmax)
#				print(zmin)
#				norm=Norm_mid(zmid, vmin=zmin, vmax=zmax)
				norm=colors.CenteredNorm(zmid) #, vmin=zmin, vmax=zmax)
			else:
				norm=colors.Normalize(vmin=zmin, vmax=zmax)

			image, xedges, yedges, im = ax.hist2d(xdata, ydata, bins=bins, 
					norm=norm,
					cmap=cmap, weights=weights)
			ax.set_aspect(aspect)
		else:
			# log, with negative

			if zr != None: 
				zmin =zr[0]
				zmax =zr[1]

			zclip=True
			if zmin > 0:
				norm=colors.LogNorm(vmin=zmin, vmax=zmax, clip=zclip)
			elif zmin < 0:
				if zlthresh == None: zlthresh=-zmin
				if zlscale  == None: zlscale=-zmin/zmax
				norm=colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
				# lognorm=colors.PiecewiseNorm(flist=['linear','log'],refpoints_cm=[0.1], refpoints_data=[0.0], vmin=zmin, vmax=zmax, clip=zclip)
				# print(zoff,zmin,zmax)
				# if zoff  == None: zoff=zmax/1.e3
				# lognorm=colors.FuncNorm((lambda x: np.log10(x-zmin+zoff)-np.log10(zoff),
				# 		lambda x: zoff*(10.**x-1)+zmin), vmin=zmin, vmax=zmax, clip=zclip)
			else:
				if zlthresh == None: zlthresh=zmax/1.e3
				if zlscale  == None: zlscale=0.2
				norm=colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
				# lognorm=LogNorm_mid_offset(vmin=zmin, vmax=zmax, clip=clip, mid=zmid, offset=zoff)
				# print('zmin',zmin)
				# print('zmax',zmax)
				# print('zoff',zoff)
				# print('zmid',zmid)

			image, xedges, yedges, im = ax.hist2d(xdata, ydata, weights=weights,
					norm=norm,
					bins=bins,  cmap=cmap)
			ax.set_aspect(aspect)
#			cm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

		if noplot: return image

		nonlocal cbar, despine, cb_outside, margin, xslice, yslice

		if xhist or yhist:
			if despine == None: despine=True
		despine_axes(ax, despine)

		y_title=1.0
		if xhist:
			nonlocal xh_height, xh_scale
			xax= ax.inset_axes([0,1.+hgap,1,hheight] , transform=ax.transAxes, sharex=ax)
			if yslice != None:
				if type(yslice) is not list: 
					p2v=pix2val([0,1], vr=yr, pr=[0,nbiny])
					p2v=p2v[1]-p2v[0]
					yslice=[yslice,yslice+p2v]
				pix_yslice=val2pix(yslice, vr=yr, pr=[0,nbiny])
				if pix_yslice[0] == pix_yslice[1]: pix_yslice[1]=pix_yslice[1]+1
#				ax.plot([xr[0],xr[0]],yslice, marker='D', clip_on=True, color='black')
#				ax.plot([xr[1],xr[1]],yslice, marker='D', clip_on=True, color='black')
				ax.plot(xr,[yslice[0],yslice[0]], linestyle='solid', clip_on=True, color='white', alpha=0.5)
				ax.plot(xr,[yslice[1],yslice[1]], linestyle='solid', clip_on=True, color='white', alpha=0.5)
				xh = image[:,pix_yslice[0]:pix_yslice[1]].sum(axis=1)
				if not doimage:
					pick = (ydata >= yslice[0]) & (ydata <= yslice[1])
					xdata_=xdata[pick]
					weights_=weights[pick]
					# something is wrong here
				#	xh = np.histogram(xdata_, bins=xedges)
				else:
					xdata_=xdata
					weights_=weights
			else:
				xh = image.sum(axis=1)
				xdata_=xdata
				weights_=weights

			xl, yl, _ = hist2line(xedges, xh)
#			xax.plot(xl, yl,
			if not doimage:
				# can this be done in one shot?
				xh, xedges, _ = xax.hist(xdata_, bins=xedges, histtype='stepfilled', 
						facecolor=hcolor, 
						weights=weights_,
						alpha=halpha)
				xh, xedges, _ = xax.hist(xdata_, bins=xedges, histtype='step', 
						weights=weights_,
						edgecolor=hcolor)
			else:
				xh, xedges, _ = xax.hist(xdata[::nbiny], bins=xedges, histtype='stepfilled', 
						facecolor=hcolor, weights=xh,
						alpha=halpha)
				xh, xedges, _ = xax.hist(xdata[::nbiny], bins=xedges, histtype='step', 
						weights=xh,
						edgecolor=hcolor)


			xax.set_xlim(xr)
			xax.set_xscale(xscale)
#			xax.set_xticklabels([])
			plt.setp(xax.get_xticklabels(), visible=False)
			plt.setp(xax.get_xlabel(), visible=False)

			if xh_scale == None:
				if zlog: 
					xax.set_yscale('log')
					xh_scale='log'
			else:
				xax.set_yscale(xh_scale)

#			print('margin',margin)
#			print('xh_height',xh_height)
#			xh_yr =  set_range(xh, 
#				margin=margin/pow(xh_height,0.3), drawdown=drawdown,
#				scale=xh_scale)
#			xax.set_ylim(xh_yr)

			despine_axes(xax, despine)

		if yhist:
			nonlocal yh_height, yh_scale
			if yh_height == None: yh_height=0.15
			yax= ax.inset_axes([1.+hgap,0.0,hheight,1] , transform=ax.transAxes, sharey=ax)
			yh = image.sum(axis=0)
			if xslice != None:
				if type(xslice) is not list: 
					p2v=pix2val([0,1], vr=xr, pr=[0,nbinx])
					p2v=p2v[1]-p2v[0]
					xslice=[xslice,xslice+p2v]
				pix_xslice=val2pix(xslice, vr=xr, pr=[0,nbinx])
				if pix_xslice[0] == pix_xslice[1]: pix_xslice[1]=pix_xslice[1]+1
				yh = image[pix_xslice[0]:pix_xslice[1],:].sum(axis=0)
#				ax.plot(xslice,[yr[0],yr[0]], marker='D', clip_on=True, color='black')
#				ax.plot(xslice,[yr[1],yr[1]], marker='D', clip_on=True, color='black')
				ax.plot([xslice[0],xslice[0]],yr, linestyle='solid', clip_on=True, color='white', alpha=0.5)
				ax.plot([xslice[1],xslice[1]],yr, linestyle='solid', clip_on=True, color='white', alpha=0.5)
				if not doimage:
					pick = (xdata >= xslice[0]) & (xdata <= xslice[1])
					ydata_=ydata[pick]
					weights_=weights[pick]
				else:
					ydata_=ydata
					weights_=weights
			else:
				yh = image.sum(axis=0)
				ydata_=ydata
				weights_=weights

			xl, yl, _ = hist2line(yedges, yh)
#			yax.plot(xl,yl,
			if not doimage:
				yh, yedges, _ = yax.hist(ydata_, bins=yedges, 
						weights=weights_,
						align='mid',
						orientation='horizontal',
						facecolor=hcolor,
						histtype='stepfilled',
						alpha=halpha)
				yh, yedges, _ = yax.hist(ydata_, bins=yedges, 
						weights=weights_,
						align='mid',
						orientation='horizontal',
						edgecolor=hcolor,
						histtype='step')
			else:
				yh, yedges, _ = yax.hist(ydata[0:nbiny], bins=yedges, 
						weights=yh,
						align='mid',
						orientation='horizontal',
						facecolor=hcolor,
						histtype='stepfilled',
						alpha=halpha)
				yh, yedges, _ = yax.hist(ydata[0:nbiny], bins=yedges, 
						weights=yh,
						align='mid',
						orientation='horizontal',
						edgecolor=hcolor,
						histtype='step')

			yax.set_ylim(yr)
			yax.set_yscale(yscale)
			plt.setp(yax.get_yticklabels(), visible=False)
			if yh_scale == None:
				if zlog: 
					yax.set_xscale('log')
					yh_scale='log'
			else:
				yax.set_xscale(yh_scale)

#			yh_yr =  set_range(yh, 
#				margin=margin/pow(yh_height,0.3), drawdown=drawdown,
#				scale=yh_scale)

#			yax.set_xlim(yh_yr)
#			xax.axes.xaxis.set_visible(False)
#			xax.plot(xedges[1:], xh)
			despine_axes(yax, despine)

			if type(cbar) is bool:
				if cbar: 
#					if xhist or (title != None and title != ''):
					if xhist:
						cbar='lower,left'
						cb_orientation = 'vertical'
						cb_outside=True
					else:
						cbar = [0.0, 1.01, 1.0, 0.05]
#						cb_outside=True
						cb_orientation = 'horizontal'
						cb_ticks_position = 'top'
						y_title = 1.15


		hsize=hheight+hgap
		if xhist: 
			yhsize=0.05*hsize
			y_title=1.0+hsize
		else: yhsize=0.0
		if yhist: xhsize=0.05*hsize
		else: xhsize=0.0
		rect=[0,0,1.+xhsize, 1.0+yhsize]
		

		if type(cbar) is bool:
			if cbar: 
				if zlog:
					if zmin <=0:
#						lloc=LogLocator(subs=range(10))
#						lloc.tick_values(vmin=zlthresh,vmax=zmax)
						cb=fig.colorbar(im, pad=0.01)
#						cb.ax.yaxis.set_minor_locator(lloc)
					else:
						cb=fig.colorbar(im, pad=0.01)
				else:
					cb=fig.colorbar(im, pad=0.01)
#			cb.ax.minorticks_on()
#			print('here')
		elif type(cbar) is list:
			cbar=[float(v) for v in cbar]
			colorbar(cbar, im, ax, fig, 
					orientation=cb_orientation, 
					ticks_position=cb_ticks_position)
		elif type(cbar) is str:
			colorbar_set(cbar, im, ax, fig, 
					off=cb_off, width=cb_width, length=cb_length,
					xlabel=xlabel, ylabel=ylabel, title=title, rect=rect,
					orientation=cb_orientation, outside=cb_outside)
	
		wrap(plt, xr, yr, xlabel, ylabel, title=title, label=not cb_outside,
				rect=rect, y_title=y_title,
				xscale=xscale, yscale=yscale, 
				outfile=outfile, 
				ax=ax,
				ion=ion, display=display)
		return image

	image = show(ion=False)
	if hold: embed()

	return image, xedges, yedges

#----------------------------------------------------------------------------------------
def annotate(data=None, common_kwargs={}):
	if data == None: return

	for kwargs in data:
		t = kwargs.pop('t')
		x = kwargs.pop('x')
		y = kwargs.pop('y')
		for key in common_kwargs:
			if key not in kwargs:
				kwargs[key] = common_kwargs[key]
		plt.text(x, y, t, **kwargs)

#----------------------------------------------------------------------------------------
def hp2mollview(infile=None, hdu=1, outfile=None, xsize=800, title="",
		nest=False, min=None, max=None, cmap=None, gridcolor="white",
		hold=False, display=False, ion=False, **kwargs):
	map = hp.read_map(infile, hdu=hdu)
	print("title",title)
	hp.mollview(map, xsize=xsize, title=title, nest=nest, cmap=cmap, 
			min=min, max=max, **kwargs)
	hp.graticule(color=gridcolor)
	wrap(plt, outfile=outfile,  title=title,
		display=display, ion=ion, tight=False)
	if hold: embed()

#----------------------------------------------------------------------------------------
# multiple data set using a class
class plottool:
	
	key = 0

	# data set: one for each
	xdata,     ydata     = OrderedDict(), OrderedDict()
	rexpr		         = OrderedDict()
	xr,        yr	   = OrderedDict(), OrderedDict()
	label,     marker    = OrderedDict(), OrderedDict()
	linestyle, linewidth = OrderedDict(), OrderedDict()
	alpha,     color     = OrderedDict(), OrderedDict()
	altx,      alty	   = OrderedDict(), OrderedDict()
	attr			   = OrderedDict()

	# common options
	xlabel  = ylabel  = plabel = None
	xscale  = yscale  = 'linear'
	title   = outfile = None
	display = ion     = hold     = False
	verbose = 1
	datfile = None
	xcol    = 'x'
	ycol    = 'y'
	xunit   = yunit   = ''
	xlabel2 = ylabel2 = ''
	xr2     = yr2	= None
	bbox_to_anchor    = None
	grid    = None

	plabel_kw = {}

	def __init__(self, **kwpars):
		self.set_kwpars(kwpars)
		self.xdata = OrderedDict()
		self.ydata = OrderedDict()

	def set_kwpars(self, kwargs):

		for key, val in kwargs.items(): 
			if hasattr(self, key): setattr(self, key, val)

		return 1

	@prep_data_deco
	def collect_data(self, xdata=None, ydata=None, 
			xr=None, yr=None, label=None, 
			marker='.', linestyle='None', color=None, alpha=None, linewidth=1.5,
			altx=False, alty=False, rexpr=None, grid=None, attr='',
#			rcParams=None,
			help=None, hold=False, verbose: int= 0, **kwargs):
		"""for multiple data set
		"""

		key = self.key

		self.xdata		[key] = xdata
		self.ydata		[key] = ydata
		self.xr		[key] = xr
		self.yr		[key] = yr
		self.label		[key] = label
		self.marker		[key] = marker
		self.linestyle	[key] = linestyle
		self.linewidth	[key] = linewidth
		self.color		[key] = color
		self.alpha		[key] = alpha
		self.altx		[key] = altx
		self.alty		[key] = alty
		self.rexpr		[key] = rexpr
		self.attr		[key] = attr

		self.key = key + 1
	
		# in order to set options any time
		# in this way one time options can be set in the -main options
		# but it becomes redundantly repeated when collect_data is
		# repeatedly called as -main
		# should go either class initialization or 
		# the -post routine, but that would make the -option setting a bit deeper
		if self.key == 1:
			self.set_kwpars(kwargs)
			self.verbose = kwargs.get('verbose', verbose)
#			set_rcParams(rcParams, verbose=verbose)
		#print(self.verbose)

		if self.verbose > 2:
			print(xdata)
			print(ydata)
		return 1

	def mplot1d(self):
		"""Multiple Plot 1-D from input table
		"""

		pcolor = ["black","red","green","blue","purple","magenta","brown","orange","cyan"]
		icolor = 0
		lcolor = len(pcolor)
		
		for key in self.xdata:
			if 'xrf' not in locals(): xrf=self.xr[key]
			if 'yrf' not in locals(): yrf=self.yr[key]

#		if verbose >2: print(key, icolor)
			if xrf[0] > self.xr[key][0]: xrf[0] = self.xr[key][0]
			if xrf[1] < self.xr[key][1]: xrf[1] = self.xr[key][1]
			if yrf[0] > self.yr[key][0]: yrf[0] = self.yr[key][0]
			if yrf[1] < self.yr[key][1]: yrf[1] = self.yr[key][1]

			if self.color[key] == None:
				self.color[key] = pcolor[icolor]
				icolor = (icolor+1) % lcolor

#		print(key, len(xdata[key]), xr[key], yr[key], 
#				title[key], marker[key], linestyle[key], color[key])

		if self.verbose >1: print("range:",xrf, yrf)

		def show(ion=True):
			if self.ion: plt.ion()

			fig, ax=plt.subplots()
			ax2    =None
			ay2    =None

			nonlocal xrf, yrf

			pids=[]
			for key in self.xdata:
				x=self.xdata[key]
				y=self.ydata[key]

				if self.alty[key]:
					if ay2 == None: 
						ay2 = ax.twinx()
						ay2.yaxis.label.set_color(self.color[key])
						ay2.tick_params(axis='y', colors=self.color[key])
						ay2.tick_params(axis='y', colors=self.color[key], which='minor')
						ay2.spines['right'].set_color(self.color[key])
					at=ay2
					
				elif self.altx[key]:
					if ax2 == None: 
						ax2 = ax.twiny()
						ax2.xaxis.label.set_color(self.color[key])
						ax2.tick_params(axis='x', colors=self.color[key])
						ax2.tick_params(axis='x', colors=self.color[key], which='minor')
						ax2.spines['top'].set_color(self.color[key])
					at=ax2
				else: at=ax

				# if len(x) == len(y) +1:
				attrs = self.attr[key].split(',')
				if 'hist' in attrs:
					# we assume this is for histogram
					if len(x) == len(y)+1:
						xh, yh, xc = hist2line(x, y)
						x=xc
					elif len(x) == len(y):
						extend=np.concatenate([x[0]*2-x[1],x,x[-1]*2-x[-2]], axis=None)
						roll =np.roll(extend, 1)
						edges = (extend+roll)/2
						xh, yh, xc = hist2line(edges[1:], y)
					pid, = at.plot(xh, yh,
						color=self.color[key], label=self.label[key], alpha=self.alpha[key],
						marker=None, linestyle=self.linestyle[key], linewidth=self.linewidth[key])
					pid_, = at.plot(x, y,
						color=self.color[key],  alpha=self.alpha[key],
						marker=self.marker[key], linestyle='none')
					# print('here', len(x), len(y), len(xc), len(xh), len(yh))
				else:
					pid, = at.plot(x, y,
						color=self.color[key], label=self.label[key], alpha=self.alpha[key],
						marker=self.marker[key], linestyle=self.linestyle[key], linewidth=self.linewidth[key])

				if 'poisson_error' in attrs:
					for exc, ey in zip(x, y):
						err= math.sqrt(ey)
						pid_, = at.plot([exc,exc], [ey-err,ey+err],
							color=self.color[key],  alpha=self.alpha[key],
							marker=None, linestyle='solid')

				if self.label[key] != "": pids.append(pid)
				
			plt.legend(labelcolor='linecolor', 
#				frameon=False, 
					bbox_to_anchor=self.bbox_to_anchor,
					ncol=1, handles=pids)
			annotate(data=self.plabel, common_kwargs=self.plabel_kw)

			if self.verbose >1: print('outfile',self.outfile)
			wrap(plt, xrf, yrf, self.xlabel, self.ylabel,  title=self.title,
					xscale=self.xscale, yscale=self.yscale, outfile=self.outfile, 
					xlabel2=self.xlabel2, ylabel2=self.ylabel2, xr2=self.xr2, yr2=self.yr2,
					ax2=ax2, ay2=ay2, ax=ax, grid=self.grid,
					display=self.display, ion=self.ion)

		show(ion=False)
		if self.hold: embed()

		return plt

	def rplot1d(self):
		"""Reference Plot 1-D from input table
		"""

		pcolor = ["black","red","green","blue","purple","magenta","brown"]
		icolor = 0
		lcolor = len(pcolor)
		
		keys = self.xdata.keys()
		ref = list(keys)[0]

		xref=self.xdata.pop(ref)
		yref=self.ydata.pop(ref)
		xr=self.xr[ref]
		yr=self.yr[ref]

		for key in self.xdata:
			if self.color[key] == None:
				self.color[key] = pcolor[icolor]
				icolor = (icolor+1) % lcolor

		if self.datfile != None: pdt=OrderedDict()

		def show(ion=True):

			nonlocal xref, yref

			if self.datfile != None: nonlocal pdt
			if self.ion: plt.ion()

			fig, ax=plt.subplots()
			ax2    =None
			ay2    =None

			pids=[]
			for key in self.xdata:

				x=self.xdata[key]
				y=self.ydata[key]

				if self.rexpr[key] != None: x, y=eval(self.rexpr[key])

				if self.alty[key]:
					if ay2 == None: 
						ay2 = ax.twinx()
						ay2.yaxis.label.set_color(self.color[key])
						ay2.tick_params(axis='y', colors=self.color[key])
						ay2.tick_params(axis='y', colors=self.color[key], which='minor')
						ay2.spines['right'].set_color(self.color[key])
					pid, = ay2.plot(x, y,
						color=self.color[key], label=self.label[key], alpha=self.alpha[key],
						marker=self.marker[key], linestyle=self.linestyle[key], linewidth=self.linewidth[key])
					
				elif self.altx[key]:
					if ax2 == None: 
						ax2 = ax.twiny()
						ax2.xaxis.label.set_color(self.color[key])
						ax2.tick_params(axis='x', colors=self.color[key])
						ax2.tick_params(axis='x', colors=self.color[key], which='minor')
						ax2.spines['top'].set_color(self.color[key])
					pid, = ax2.plot(self.xdata[key],self.ydata[key],
						color=self.color[key], label=self.label[key], alpha=self.alpha[key],
						marker=self.marker[key], linestyle=self.linestyle[key], linewidth=self.linewidth[key])
				else:
					pid, = ax.plot(x,y,
						color=self.color[key], label=self.label[key], alpha=self.alpha[key],
						marker=self.marker[key], linestyle=self.linestyle[key], linewidth=self.linewidth[key])
				pids.append(pid)

				if self.datfile != None:
					pdt[key]=QTable([x,y],
						names=[self.xcol,self.ycol], units=[self.xunit,self.yunit], 
						meta={'extname':self.label[key]})

			plt.legend(labelcolor='linecolor', 
					bbox_to_anchor=self.bbox_to_anchor,
					ncol=1, handles=pids)

			if self.verbose >1: print('outfile',self.outfile)
			wrap(plt, xr, yr, self.xlabel, self.ylabel,  title=self.title,
					xscale=self.xscale, yscale=self.yscale, outfile=self.outfile, 
					xlabel2=self.xlabel2, ylabel2=self.ylabel2, xr2=self.xr2, yr2=self.yr2,
					ax2=ax2, ay2=ay2, ax=ax,
					display=self.display, ion=self.ion)

		show(ion=False)

		if self.hold: embed()
		if self.datfile != None:
			overwrite=True
			for each in pdt:
				tt.to_fits(self.datfile,pdt[each], overwrite=overwrite)
				overwrite=False

		return plt

	def scan_fitsfile_moot(self, infile=None, hdu="", x=None):
		if infile == None:
			return None
		hdul=fits.open(infile)
		tasks=OrderedDict()
		loops=[]
		for each in hdul:
			if hdu !="":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new=False
				if bool(re.search('A',str(subeach.format))):
					continue
				if x != None:
					if x != subeach.name: 
						if hdu !="":
							loopid = subeach.name
						else:
							loopid = each.name + ' '+ subeach.name
						new=True
				else:
					x = subeach.name
				if new:
					loops.append(loopid)
					task=OrderedDict()
					task['infile']	=infile
					task['hdu']		=each.name
					task['x']		=x
					task['y']		=subeach.name
					task['label']	=loopid

					tasks['-loop=='+loopid] = task

		tasks['-loop'] = loops
		return tasks

	def scan_fits_cols(self, infile=None, hdu="", x=None):
		if infile == None:
			return None
		hdul=fits.open(infile)
		tasks=OrderedDict()
		for each in hdul:
			if hdu !="":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new=False
				if bool(re.search('A',str(subeach.format))):
					continue
				if x != None:
					if x != subeach.name: 
						if hdu !="":
							loopid = subeach.name
						else:
							loopid = each.name + ' '+ subeach.name
						new=True
				else:
					x = subeach.name
				if new:
					task=OrderedDict()
					task['infile']	=infile
					task['hdu']		=each.name
					task['x']		=x
					task['y']		=subeach.name
					task['label']	=loopid

					tasks[loopid] = task
		return tasks

	def scan_fits_hdus(self, infile=None, x=None, y=None, hdu="", verbose=0):
		if infile == None:
			return None

		infile=str(Path(infile).expanduser())
		hdul=fits.open(infile)
		tasks=OrderedDict()
		for each in hdul:

			if not hasattr(each, 'columns'): continue

			if hdu != "":
				if not bool(re.search(hdu,each.name)): continue
			if int(verbose)>0: print(each.name)

			ind=[]
			for idx, subeach in enumerate(each.columns):
				if bool(re.search('A',str(subeach.format))): continue
				ind.append(idx)
			if x == None: x=each.columns[ind[0]].name
			if y == None: y=each.columns[ind[1]].name

			x_bingo = False
			y_bingo = False
			for subeach in each.columns:
				if x == subeach.name: x_bingo=True
				if y == subeach.name: y_bingo=True

			if x_bingo*y_bingo:
				task=OrderedDict()
				task['infile']	=infile
				task['hdu']		=each.name
				task['x']		=x
				task['y']		=y
				task['label']	=each.name

				tasks[each.name] = task
		return tasks

#----------------------------------------------------------------------------------------
# plot Data Model Residual; e.g., spectral fit
@prep_data_deco
@prep_model_deco
def plotDMR(xdata=None, ydata=None, mdata=None, rdata=None, pdata=None,
		mcxdata=None, mcdata=None, mcdeco=None,		# module component x, data
		xr=None, yr=None, xlabel=None, ylabel=None,  ylabel2=None,
		rr=None, rlabel=None,					# redidual range, redidual label
		ratio=[3,1],						# data portion, error portion = 1.- data portion
		outfile=None, 
		xscale='log', yscale='log',				# often used for spectral analysis
		marker ='None',  linestyle='None',   color='black', # for data
		emarker='None', elinestyle='solid', ecolor='black', # for data error or range
		mmarker='None', mlinestyle='solid', mcolor='red',   # for model
		rmarker='None', rlinestyle='None',  rcolor='black', # for residual
		smarker='None', slinestyle='solid', scolor='black', # for residual error or range
		rtype  ='relative',
		pfontsize=8, pfontfamily="monospace",
		display=True, 
		xerrdata=None, yerrdata=None, 
		xlowdata=None, xhighdata=None,
		ylowdata=None, yhighdata=None,
		mx=None, my=None, mc=None,
		xticks=None, yticks=None,
		xtickv=None, ytickv=None,
		data=None,
		help=None, hold=False, verbose: int= 0, **kwargs):

	pcolor = ["green","blue","purple","magenta","brown","orange"]
	icolor = 0
	lcolor = len(pcolor)
		
	def show(ion=True):
		if ion: plt.ion()

		nonlocal xdata, ydata, mdata, rdata, data
		nonlocal xerrdata, xlowdata, xhighdata
		nonlocal yerrdata, ylowdata, yhighdata
		nonlocal pcolor, icolor, lcolor
		fig = plt.figure()
		gs  = fig.add_gridspec(2, hspace=0, height_ratios=ratio)
		axs = gs.subplots(sharex=True)
		ax = axs[0]

		label_statistic = ""
		if hasattr(data,'meta'):
			header = data.meta
			if "RCHI2" in header:
				label_statistic = label_statistic + "$\chi_r^2$ = %.2f" % (header["RCHI2"])
			if "DOF" in header:
				label_statistic = label_statistic + "  DoF = %d" % (header["DOF"])

		else:
			header = {}


		# plot models
		if type(mdata).__name__ == 'Table':
			ncols=len(mdata.columns)
		else:
			ncols= len(mdata.shape)

		if ncols == 1:
			ax.plot(xdata, mdata,
					color=mcolor,
					marker=mmarker, linestyle=mlinestyle)
		else:
			if (mx != None) and (my !=None):
				ax.plot(mdata[mx], mdata[my],
						color=mcolor,
						marker=mmarker, linestyle=mlinestyle)
				idx=1
				while True:
					try:
						mcdata = mdata[mc+str(idx)]
					except:
						break
					ax.plot(mdata[mx], mcdata,
						color=pcolor[icolor],
						marker=mmarker, linestyle=mlinestyle)
					icolor = (icolor +1) % lcolor
					idx = idx +1


		# plot data 
		ax.plot(xdata, ydata,
				color=color,
				marker=marker, linestyle=linestyle)

		# plot x and y error bars
		if type(xlowdata).__name__ == 'NoneType':
			xlowdata = xdata - xerrdata
			xhighdata= xdata + xerrdata
		if type(ylowdata).__name__ == 'NoneType':
			ylowdata = ydata - yerrdata
			yhighdata= ydata + yerrdata

		for ex, ey, exlow, exhigh in zip(xdata, ydata, xlowdata, xhighdata):
			ax.plot([exlow, exhigh],[ey,ey], 
				color=ecolor,
				marker=emarker, linestyle=elinestyle)
		for ex, ey, eylow, eyhigh in zip(xdata, ydata, ylowdata, yhighdata):
			ax.plot([ex,ex],[eylow, eyhigh],
				color=ecolor,
				marker=emarker, linestyle=elinestyle)

		# add fit parameter labels
		# will add more options
		if type(pdata).__name__ != 'NoneType':
			lineno=0
			for row in pdata:
				if row['frozen']: continue
				color_=mcolor
				if 'addcompno' in row.colnames:
					if row['addcompno'] >0:
						color_=pcolor[ (row['addcompno'] -1) % lcolor]
				t=ax.text(0.88,0.95-lineno*0.04, 
					row['aka'] + '.'+row['parameter']+': ',
					fontsize=pfontsize,
					fontfamily=pfontfamily,
					color=color_,
					horizontalalignment='right',
					transform=ax.transAxes)
				t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))
				lineno=lineno+1
			lineno=0
			addidx=0
			for row in pdata:
				if row['frozen']: continue
				color_=mcolor
				if 'addcompno' in row.colnames:
					if row['addcompno'] >0:
						color_=pcolor[ (row['addcompno'] -1) % lcolor]
				t=ax.text(0.88,0.95-lineno*0.04, 
					"%.2e" % (row['value']),
					fontsize=pfontsize,
					fontfamily=pfontfamily,
					color=color_,
					horizontalalignment='left',
					transform=ax.transAxes)
				t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))
				lineno=lineno+1
#			embed()

		# plot residuals
		axs[1].plot(xdata, rdata,
				color=rcolor,
				marker=rmarker, linestyle=rlinestyle)

		# plot residual x range
		for ex, ey, exlow, exhigh in zip(xdata, rdata, xlowdata, xhighdata):
			axs[1].plot([exlow, exhigh],[ey,ey], 
				color=scolor,
				marker=smarker, linestyle=slinestyle)

		# plot residual y error range
		if rtype =='relative':
			for ex, ey in zip(xdata, rdata):
				axs[1].plot([ex, ex],[-1+ey,1+ey], 
					color=scolor,
					marker=smarker, linestyle=slinestyle)
		elif rtype =='absolute':
			for ex, eylow, eyhigh in zip(xdata, ylowdata-ydata+rdata, yhighdata-ydata+rdata):
				axs[1].plot([ex, ex],[eylow,eyhigh], 
					color=scolor,
					marker=smarker, linestyle=slinestyle)

		t=axs[1].text(0.03,0.1, label_statistic, 
				horizontalalignment='left',
				transform=axs[1].transAxes)
		t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))

		wrap(plt, xr, yr, xlabel2=xlabel, ylabel=ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, 
				ax=ax, ax2=axs[1], ay2=axs[1], ylabel2=ylabel2,
				xticks=xticks, yticks=yticks,
				xtickv=xtickv, ytickv=ytickv,
				display=display, ion=ion)

	show(ion=False)
	if hold: embed()
