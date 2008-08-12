
import os
from . import SEDOT_BASE
from status import PackageStatus

__all__ = ['Package', 'NoPackageError']


class NoPackageError(Exception):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		print repr(self.value)
	

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
	
	def _read(self, file):
		f = open(os.path.join(self.dir, file))
		
		for line in f.readlines():
			line = line.strip()
			if line[0] != '#':
				return line
			return None

	def load_status(self):
		
		self.status = PackageStatus(self.package)

			
