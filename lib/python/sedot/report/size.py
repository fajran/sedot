
from sedot.report.report import Generator

from sedot import SEDOT_CONFIG

from string import Template

class MirrorSizeGenerator(Generator):
	
	def __init__(self, outdir):
		Generator.__init__(self, outdir)

		self.report_name = "Mirror Size"
		self.output_file = "size.html"
	
	def _print_report(self, out):
		out.write("""
<div id="mirror-size">
	<h2>Mirror Size</h2>
	<table>
	<tr><th>Mirror</th>
		<th>Size</th>
		<th>&nbsp;</th>
	</tr>
""")

		template = Template("""
	<tr><td class="name">$mirror</td>
		<td class="size">$size</td>
		<td class="graph"><img src="mirror-size/$pkg.month.png" alt="$mirror"/></td>
	</tr>
""")

		pkgs = self.packages.keys()
		pkgs.sort(lambda a, b: cmp(self.packages[a].name, self.packages[b].name))

		for pkg in pkgs:

			package = self.packages[pkg]

			if not package.size.size:
				continue

			out.write(template.substitute(
				mirror=package.name,
				size=self._make_size(package.size.size),
				pkg=package.package
			))

		out.write("""
	</table>
</div>
""")
	
	def _make_size(self, size):
		size = float(size)
		ms = ["KB", "MB", "GB"]

		for m in ms:
			if size < 1024:
				return "%.2f %s" % (size, m)
				break
			size = size / 1024.0
		
		return "%.2f %s" % (size, m)

