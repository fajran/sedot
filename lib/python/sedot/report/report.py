
from sedot import Package, NoPackageError
from sedot import SEDOT_CONFIG
import os
import time

class Generator:

	def __init__(self, outdir):
		self.outdir = outdir
		self.report_name = "Status"
		self.output_file = "index.html"

		global SEDOT_CONFIG
		self.name = SEDOT_CONFIG.get('MIRROR_NAME', None)

	def set_packages(self, packages):
		self.packages = packages

	def generate(self):
		file = os.path.join(self.outdir, self.output_file)
		f = open(file, "w")
		self._print_page_header(f)
		self._print_report(f)
		self._print_page_footer(f)

	def _print_report(self, f):
		pass

	def _make_time(self, tuple=None):
		format = "%d/%m/%y %H:%M"
		if tuple == None:
			return time.strftime(format)
		else:
			return time.strftime(format, tuple)

	def _make_age(self, tuple):
		t = time.mktime(tuple)
		now = time.mktime(time.localtime())

		simple = True

		delta = now - t

		dday = 86400
		dhour = 3600
		dmin = 60

		age = [0, 0, 0, 0]
		age_string = [
			("day", "days", "d"),
			("hour", "hours", "h"), 
			("min", "mins", "m"),
			("sec", "secs", "s")
		]

		age[0] = int(delta/dday)
		if age[0] > 0:
			delta = delta % dday

		age[1] = int(delta/dhour)
		if age[1] > 0:
			delta = delta % dhour

		age[2] = int(delta/dmin)
		if age[2] > 0:
			delta = delta % dmin

		age[3] = int(delta)

		res = []
		for i in [0, 1, 2]:
			str = None

			if simple and age[i] > 0:
				str = "%d%s" % (age[i], age_string[i][2])
			elif age[i] == 1:
				str = "%d %s" % (age[i], age_string[i][0])
			elif age[i] > 1:
				str = "%d %s" % (age[i], age_string[i][1])

			if str:
				res.append("<span>%s</span>" % str)

		if not res:
			res.append("a moment ago")

		if simple:
			return "<span class='age simple'>%s</span>" % (" ".join(res))
		else:
			return "<span class='age'>%s</span>" % (" ".join(res))

	def _print_page_header(self, out):
		out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html><head>
<title>%s</title>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head><body><div id="c">

<div id="header">
	<h1>%s</h1>
</div>
<div id="content">
<h2>%s</h2>
""" % (self.name, self.name, self.report_name))

	def _print_page_footer(self, out):
		update_time = self._make_time(None)
		out.write("""
</div>
<div id="footer">
	<p id="generated">Last update: %s</p>
	<p id="sedot"><a href="https://launchpad.net/sedot">Sedot sampai tua!</a> &trade;</p>
</div>
</div></body></html>""" % (update_time))

from sedot.report.sync import SyncGenerator
from sedot.report.size import MirrorSizeGenerator

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

		mirror_size = MirrorSizeGenerator(self.outdir)
		mirror_size.set_packages(packages)
		mirror_size.generate()

