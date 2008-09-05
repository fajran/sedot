

from os import path

SEDOT_LIBDIR = path.abspath(path.join(path.dirname(__file__), '..'))
SEDOT_BASE = path.abspath(path.join(SEDOT_LIBDIR, '..', '..'))

SEDOT_CONFIG = {}

def get_config():
	global SEDOT_CONFIG

	file = path.join(SEDOT_BASE, 'etc', 'config.sh')

	f = open(file)
	for line in f.readlines():
		line = line.strip()

		if len(line) == 0:
			continue

		if line[0] == '#':
			continue

		pos = line.find('=')
		if pos < 0:
			continue

		key = line[:pos].strip()
		val = line[pos+1:].strip()

		if val[0] == '"' and val[-1] == '"':
			val = val[1:-1]
		elif val[0] == "'" and val[-1] == "'":
			val = val[1:-1]

		SEDOT_CONFIG[key] = val

get_config()

if SEDOT_CONFIG.get('BASE', None):
	SEDOT_BASE = SEDOT_CONFIG['BASE']

from package import *

