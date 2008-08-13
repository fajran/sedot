
from sedot import Package, NoPackageError
from sedot import SEDOT_CONFIG
import os
import time

from string import Template

class Generator:

	def __init__(self, outdir):
		self.outdir = outdir

	def set_packages(self, packages):
		self.packages = packages

	def generate(self):
		
		file = os.path.join(self.outdir, "index.html")

		self.f = open(file, "w")

		global SEDOT_CONFIG
		self.name = SEDOT_CONFIG.get('MIRROR_NAME', None)

		self._print_page_header()
		self._print_header()

		self._print_mirror_status()

		self._print_footer()
		self._print_page_footer()

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

	def _print_header(self):
		self.f.write("""
<div id="header">
	<h1>%s</h1>
</div>
<div id="content">
""" % (self.name))

	def _print_footer(self):

		update_time = self._make_time(None)

		self.f.write("""
</div>
<div id="footer">
	<p id="generated">Last update: %s</p>
	<p id="sedot"><a href="https://launchpad.net/sedot">Sedot sampai tua!</a> &trade;</p>
</div>
""" % (update_time))

	def _print_mirror_status(self):
		self.f.write("""
<div id="mirror">
	<h2>Mirror Status</h2>
	<table>
	<tr><th rowspan="2">Mirror</th>
		<th colspan="3">Last synchronization</th>
		<th colspan="2">Last successful synchronization</th>
	</tr>
	<tr><th>Start</th>
		<th>Finish</th>
		<th>Status</th>
		<th>Time</th>
		<th>Age</th>
	</tr>
""")

		template = Template("""
	<tr><td class="name">$mirror</td>
		<td class="date $class_last">$last_start</td>
		<td class="date $class_last">$last_finish</td>
		<td class="status $class_last">$last_status</td>
		<td class="date $class_success">$sync_time</td>
		<td class="age $class_success">$sync_age</td>
	</tr>
""")

		pkgs = self.packages.keys()
		pkgs.sort(lambda a, b: cmp(self.packages[a].name, self.packages[b].name))

		for pkg in pkgs:

			package = self.packages[pkg]

			if not package.status:
				continue

			if package.status.last:
				if package.status.last.start:
					last_start=self._make_time(package.status.last.start)
				else:
					last_start=self._make_time(package.status.last.time)

				if package.status.last.finish:
					last_finish=self._make_time(package.status.last.finish)
					last_status=self._make_status(package.status.last)
				else:
					last_finish = "in progress"
					last_status = ""


			else:
				last_start = "unknown"
				last_finish = "unknown"
				last_status = "unknown"

			if package.status.success:
				sync_time=self._make_time(package.status.success.finish),
				sync_age=self._make_age(package.status.success.finish)
			else:
				sync_time = "Never"
				sync_age = "-"

			class_last=self._make_class_last(package.status.last)
			class_success=self._make_class_success(package.status.success)

			self.f.write(template.substitute(
				mirror=package.name,
				last_start=last_start,
				last_finish=last_finish,
				last_status=last_status,
				sync_time=sync_time,
				sync_age=sync_age,
				class_last=class_last,
				class_success=class_success,
			))

		self.f.write("""
	</table>
</div>
""")

	def _make_time(self, tuple=None):
		format = "%d/%m/%Y %H:%M:%S"
		if tuple == None:
			return time.strftime(format)
		else:
			return time.strftime(format, tuple)

	def _make_status(self, status):
		if status.success:
			msg = "Success"
		else:
			msg = "Fail"

		url = "log/%s/%s/sync.log.gz" % (status.data['pkg'], status.timestamp)

		return '<a href="%s">%s</a>' % (url, msg)

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

	def _make_class_last(self, data):
		if data == None:
			return "unknown"
		elif not data.finish:
			return "inprogress"
		elif data.success:
			return "success"
		else:
			return "fail"

	def _make_class_success(self, data):
		if data == None:
			return "never"
		else:
			t = time.mktime(tuple.finish)
			now = time.mktime(time.localtime())
			delta = now - t

			day = 86400

			if delta > 7 * day:
				return "outdated"
			elif delta > 2 * day:
				return "old"
			else:
				return "uptodate"

class Report:
	
	def __init__(self, packages, outdir):
		self.pkgs = packages
		self.outdir = outdir
	
	def generate(self):
		self._load()
		self._generate()

	def _load(self):
		
		self.packages = {}

		for pkg in self.pkgs:
			try:
				self.packages[pkg] = Package(pkg)
				self.packages[pkg].load_status()
			except NoPackageError:
				continue
	
	def _generate(self):
		
		generator = Generator(self.outdir)
		generator.set_packages(self.packages)
		generator.generate()
	


