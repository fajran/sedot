
from sedot.report.report import Generator

from sedot import SEDOT_CONFIG

import os
import glob
import time
from string import Template

class SummaryGenerator(Generator):

	def __init__(self, outdir):
		Generator.__init__(self, outdir)

		self.report_name_short = "Summary"
		self.report_name = "Mirror Status"
		self.output_file = "index.html"

	def _print_report(self, out):
		
		pkgs = self.packages.keys()
		pkgs.sort(lambda a, b: cmp(self.packages[a].name, self.packages[b].name))

		total_packages = len(pkgs)
		total_size = 0
		for pkg in pkgs:
			if self.packages[pkg].size.size:
				total_size += self.packages[pkg].size.size

		out.write("""
<div id="mirror-summary">
	<table class="overview">
	<tr><th>Monitored packages:</th>
		<td>%d</td>
	</tr>
	<tr><th>Total size:</th>
		<td>%s</td>
	</tr>
	</table>

	<table class="packages">
	<tr><th rowspan="2">Mirror</th>
		<th colspan="2">Syncronization</th>
		<th rowspan="2">Size</th>
		<th rowspan="2">&nbsp;</th>
	</tr>
	<tr><th>Last</th>
		<th>Age</th>
	</tr>
""" % (total_packages, self._make_size(total_size)))

		template = Template("""
	<tr><td class="name">$mirror_link $other_link</td>
		<td class="date $class_last"><img src="$last_img" alt="$class_last"/> $last_link</td>
		<td class="age $class_success">$sync_age</td>
		<td class="size">$size</td>
		<td>$locked</td>
	</tr>
""")

		for pkg in pkgs:
			
			package = self.packages[pkg]

			if not package.status:
				continue

			# Mirror link
			
			mirror_link = None
			other_link = []

			for i in ['http', 'ftp', 'rsync']:
				if package.urls[i] and mirror_link == None:
					mirror_link = '<a href="%s">%s</a>' % (package.urls[i], package.name)
				elif package.urls[i]:
					other_link.append('<span class="other">[<a href="%s">%s</a>]</span>' % (package.urls[i], i))

			if not mirror_link:
				mirror_link = package.name

			# Status

			if package.status.last:
				if package.status.last.start:
					last_time=self._make_time(package.status.last.start)
				else:
					last_time=self._make_time(package.status.last.time)
				last_link = '<span title="In Progress">%s</span>' % last_time
				class_last = "inprogress"
				last_img = "img/hourglass.png"

				if package.status.last.finish:
					last_time = self._make_time(package.status.last.finish)

					log_url = "log/%s/%s/sync.log.gz" % (package.status.last.data['pkg'], package.status.last.timestamp)

					if package.status.last.success:
						last_link = '<span title="Success"><a href="%s">%s</a></span>' % (log_url, last_time)
						class_last = "success"
						last_img = "img/tick.png"
					else:
						last_link = '<span title="Fail"><a href="%s">%s</a></span>' % (log_url, last_time)
						class_last = "fail"
						last_img = "img/cross.png"

			
			if package.status.success:
				sync_time=self._make_time(package.status.success.finish)
				sync_age=self._make_age(package.status.success.finish)
			else:
				sync_time = "Never"
				sync_age = "-"

			class_success=self._make_class_success(package.status.success)

			if package.size.size:
				size = self._make_size(package.size.size)
			else:
				size = "unknown"

			locked = ""
			if glob.glob(os.path.join(package.target, '.SYNC-in-Progress-*')):
				locked = """<img class="lock" alt="locked" src="img/lock.png"/>"""

			out.write(template.substitute(
				mirror_link=mirror_link,
				other_link=" ".join(other_link),
				class_last=class_last,
				last_link=last_link,
				class_success=class_success,
				sync_age=sync_age,
				last_img=last_img,
				size=size,
				locked=locked
			))

		out.write("""
	</table>
</div>
""")

	def _make_class_success(self, data):
		if data == None:
			return "never"
		else:
			t = time.mktime(data.finish)
			now = time.mktime(time.localtime())
			delta = now - t

			day = 86400

			if delta > 7 * day:
				return "outdated"
			elif delta > 2 * day:
				return "old"
			else:
				return "uptodate"

