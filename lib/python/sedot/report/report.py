
from sedot import Package, NoPackageError
from sedot import SEDOT_CONFIG
import os
import time

class Generator:

	def __init__(self, outdir):
		self.outdir = outdir

		global SEDOT_CONFIG
		self.name = SEDOT_CONFIG.get('MIRROR_NAME', None)

	def _make_time(self, tuple=None):
		format = "%d/%m/%Y %H:%M:%S"
		if tuple == None:
			return time.strftime(format)
		else:
			return time.strftime(format, tuple)

	def _make_age(self, tuple):
		t = time.mktime(tuple)
		now = time.mktime(time.localtime())

		delta = now - t

		dday = 86400
		dhour = 3600
		dmin = 60

		res = []
		if delta / dday >= 1:
			res.append("%d day" % int(delta/dday))
			delta = delta % dday

		if delta / dhour >= 1:
			res.append("%d hour" % int(delta/dhour))
			delta = delta % dhour

		if delta / dmin >= 1:
			res.append("%d min" % int(delta/dmin))
			delta = delta % dmin

		if delta >= 1:
			res.append("%d sec" % int(delta))

		return " ".join(res)

	def _print_page_header(self):
		self.f.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html><head>
<title>%s</title>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head><body><div id="c">
""" % (self.name))

	def _print_page_footer(self):
		self.f.write("""
</div></body></html>""")

from sedot.report.sync import SyncGenerator

class Report:
	
	def __init__(self, packages, outdir):
		self.pkgs = packages
		self.outdir = outdir
	
	def generate(self):
		
		#
		# Load data
		#

		packages = {}
		for pkg in self.pkgs:
			try:
				packages[pkg] = Package(pkg)
				packages[pkg].load_status()
			except NoPackageError:
				continue

		#
		# Generate reports
		#

		# Syncronization status

		sync = SyncGenerator(self.outdir)
		sync.set_packages(packages)
		sync.generate()

		#mirror_size = MirrorSizeGenerator(self.outdir)
		#mirror_size.set_packages(packages)
		#mirror_size.generate()
	


