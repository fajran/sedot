
import os
from sedot import SEDOT_BASE
from status import PackageStatus, NoStatusError

__all__ = ['Package', 'NoPackageError']


class NoPackageError(Exception):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		print repr(self.value)
	
class MirrorSize:

	def __init__(self, package):
		self.package = package
		self._load()

		self.size = None
		self.time = None
	
	def _load(self):
		global SEDOT_BASE
		dir = os.path.join(SEDOT_BASE, "log", "mirror-size")

		logname = os.path.join(dir, "%s.log" % self.package)

		if not os.path.isfile(logname):
			return
		
		lines = open(logname).readlines()[-1]
		(self.time, self.size) = lines.split(" ")

	def __str__(self):
		return str(self.size)

class Package:

	def __init__(self, package):
		self.package = package

		self.status = None

		self._load()

	def _load(self):
		global SEDOT_BASE
		self.dir = os.path.join(SEDOT_BASE, "pkgs", self.package)

		if not os.path.isdir(self.dir):
			raise NoPackageError(self.package)

		self.source = self._read("source")
		self.target = self._read("target")
		self.method = self._read("method")
		self.name = self._read("name")
		self.cron = self._read("cron")
		self.color = self._read_color("color")

		self.size = MirrorSize(self.package)
	
	def _read(self, file):
		fname = os.path.join(self.dir, file)

		if os.path.isfile(fname):
			f = open(fname)
			for line in f.readlines():
				line = line.strip()
				if line[0] != '#':
					return line
		
		return None
	
	def _read_color(self, file):
		fname = os.path.join(self.dir, file)

		if os.path.isfile(fname):
			f = open(fname)
			for line in f.readlines():
				line = line.strip()
				if line[0] != '':
					return line
		
		return "#FF0000"

	def load_status(self):
		
		try:
			self.status = PackageStatus(self.package)
		except NoStatusError:
			self.status = None

			
