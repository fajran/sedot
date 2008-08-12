
from . import SEDOT_BASE
import os
import time
import rfc822

class NoStatusError(Exception):
	def __init__(self, package, timestamp=None):
		self.value = package
		self.package = package
		self.timestamp = timestamp
	
	def __str__(self):
		print repr(self.value)

class SyncStatus:

	def __init__(self, package, timestamp):
		self.package = package
		self.timestamp = timestamp

		self.data = {}
		self.success = False
		self.done = True
		self.code = -1
		self.time = None
		self.start = None
		self.finish = None

		self._load()
	
	def _load(self):
		global SEDOT_BASE
		self.dir = os.path.join(SEDOT_BASE, "log", "sync", self.package, self.timestamp)

		if not os.path.isdir(self.dir):
			raise NoStatusError(self.package, self.timestamp)

		try:
			f = open(os.path.join(self.dir, "status.txt"))
		except IOError:
			raise NoStatusError(self.package, self.timestamp)

		for line in f.readlines():
			line = line.strip()
			pos = line.find(" ")

			key = line[:pos]
			val = line[pos+1:]

			self.data[key] = val

			if key == "status":
				if val == "200":
					self.success = True
				elif val == "100":
					self.done = False
			if key in 'time':
				self.time = self._parse_time(val)
			if key == 'start':
				self.start = self._parse_time(val)
			if key == 'finish':
				self.finish = self._parse_time(val)
			if key == 'code':
				self.code = int(val)

		# Backward compatibility
		if not self.time and self.finish:
			self.time = self.finish

	def _parse_time(self, txt):
		return rfc822.parsedate(txt)

class PackageStatus:

	def __init__(self, package):
		self.package = package

		self.success = None
		self.last = None

		self._load()

	def _load(self):
		global SEDOT_BASE
		self.dir = os.path.join(SEDOT_BASE, "log", "sync", self.package)

		if not os.path.isdir(self.dir):
			raise NoStatusError(self.package)

		dirs = os.listdir(self.dir)
		dirs.sort(reverse=True)

		for timestamp in dirs:

			try:
				status = SyncStatus(self.package, timestamp)
			except NoStatusError:
				continue

			if status.code == 301:  # Unable to gain lock
				continue

			if self.last == None:
				self.last = status

			if status.success:
				self.success = status
				break

