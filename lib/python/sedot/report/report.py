
from sedot import Package, NoPackageError
from sedot import SEDOT_CONFIG
import os
import time
import shutil

class Generator:

	def __init__(self, outdir):
		self.outdir = outdir
		self.report_name = "Status"
		self.output_file = "index.html"

		global SEDOT_CONFIG
		self.name = SEDOT_CONFIG.get('MIRROR_NAME', None)

		self.day_old = 2
		self.day_outdated = 7

	def set_packages(self, packages):
		self.packages = packages

	def set_all_generators(self, generators):
		self.generators = generators

	def generate(self):
		tmp = ".%s.tmp" % self.output_file
		file = os.path.join(self.outdir, tmp)
		f = open(file, "w")
		self._print_page_header(f)
		self._print_report(f)
		self._print_page_footer(f)

		file_orig = os.path.join(self.outdir, self.output_file)
		shutil.move(file, file_orig)

	def _print_report(self, f):
		pass

	def _make_time(self, tuple=None):
		format = "%d/%m/%y %H:%M"
		if tuple == None:
			return time.strftime(format)
		else:
			return time.strftime(format, tuple)

	def _make_size(self, size):
		size = float(size)
		ms = ["KB", "MB", "GB", "TB"]

		for m in ms:
			if size < 1024:
				return "%.2f %s" % (size, m)
				break
			size = size / 1024.0
		
		return "%.2f %s" % (size, m)

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
		
		reports_link = ""
		for gen in self.generators:
			reports_link += '<li><a href="%s">%s</a></li>' % (gen.output_file, gen.report_name_short)
		if reports_link:
			reports_link = '<ul>' + reports_link + '</ul>'

		out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html><head>
<title>%s</title>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head><body><div id="c">

<div id="header">
	<h1>%s</h1>
</div>
<div id="reports">%s</div>
<div id="content">
<h2>%s</h2>
""" % (self.name, self.name, reports_link, self.report_name))

	def _print_page_footer(self, out):
		update_time = self._make_time(None)
		out.write("""
</div>
<div id="footer">
	<p id="generated">Last update: %s</p>
	<p id="sedot"><a href="https://launchpad.net/sedot">Sedot sampai tua!</a> &trade;</p>
</div>
</div></body></html>""" % (update_time))

	def _make_class_success(self, data):
		if data == None:
			return "never"
		else:
			t = time.mktime(data.finish)
			now = time.mktime(time.localtime())
			delta = now - t

			day = 86400

			if delta > self.day_outdated * day:
				return "outdated"
			elif delta > self.day_old * day:
				return "old"
			else:
				return "uptodate"


from sedot.report.summary import SummaryGenerator
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

		generators = [SummaryGenerator, SyncGenerator, MirrorSizeGenerator]

		obj_list = []
		for gen in generators:
			obj = gen(self.outdir)
			obj.set_packages(packages)

			obj_list.append(obj)

		for obj in obj_list:
			obj.set_all_generators(obj_list)
			obj.generate()

