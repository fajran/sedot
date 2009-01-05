
from sedot.report.report import Generator

from sedot import SEDOT_CONFIG

import os
import glob
import time
from string import Template


class SyncGenerator(Generator):

	def __init__(self, outdir):
		Generator.__init__(self, outdir)

		self.report_name_short = "Status"
		self.report_name = "Synchronization Status"
		self.output_file = "sync.html"

	def _print_report(self, out):
		out.write("""
<div id="mirror-status">
	<table>
	<tr><th rowspan="2">Mirror</th>
		<th colspan="3">Last synchronization</th>
		<th colspan="2">Last successful synchronization</th>
		<th rowspan="2">&nbsp;</th>
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
		<td>$locked</td>
	</tr>
""")

		pkgs = self.packages.keys()
		pkgs.sort(lambda a, b: cmp(self.packages[a].name.lower(), self.packages[b].name.lower()))

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
				sync_time=self._make_time(package.status.success.finish)
				sync_age=self._make_age(package.status.success.finish)
			else:
				sync_time = "Never"
				sync_age = "-"

			class_last=self._make_class_last(package.status.last)
			class_success=self._make_class_success(package.status.success)

			locked = ""
			if glob.glob(os.path.join(package.target, '.SYNC-in-Progress-*')):
				locked = """<img class="lock" alt="locked" src="img/lock.png"/>"""

			out.write(template.substitute(
				mirror=package.name,
				last_start=last_start,
				last_finish=last_finish,
				last_status=last_status,
				sync_time=sync_time,
				sync_age=sync_age,
				class_last=class_last,
				class_success=class_success,
				locked=locked,
			))

		out.write("""
	</table>
</div>
""")

	def _make_status(self, status):
		if status.success:
			msg = "Success"
		else:
			msg = "Fail"

		url = "log/%s/%s/sync.log.gz" % (status.data['pkg'], status.timestamp)

		return '<a href="%s">%s</a>' % (url, msg)

	def _make_class_last(self, data):
		if data == None:
			return "unknown"
		elif not data.finish:
			return "inprogress"
		elif data.success:
			return "success"
		else:
			return "fail"

