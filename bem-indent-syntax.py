import sublime
import sublime_plugin
import json
from os.path import dirname, realpath, join

try:
	# Python 2
	from node_bridge import node_bridge
except:
	from .node_bridge import node_bridge

# monkeypatch `Region` to be iterable
sublime.Region.totuple = lambda self: (self.a, self.b)
sublime.Region.__iter__ = lambda self: self.totuple().__iter__()

BIN_PATH = join(sublime.packages_path(), dirname(realpath(__file__)), 'bem-indent-syntax.js')

class bisCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if not self.has_selection():
			region = sublime.Region(0, self.view.sel()[0].begin())
			originalBuffer = self.view.substr(region)
			bised = self.bis(originalBuffer)
			if bised:
				self.view.replace(edit, region, bised)
			return
		for region in self.view.sel():
			if region.empty():
				continue
			originalBuffer = self.view.substr(region)
			bised = self.bis(originalBuffer)
			if bised:
				self.view.replace(edit, region, bised)

	def bis(self, data):
		try:
			return node_bridge(data, BIN_PATH)
		except Exception as e:
			sublime.error_message('bem-indent-syntax\n%s' % e)

	def has_selection(self):
		for sel in self.view.sel():
			start, end = sel
			if start != end:
				return True
		return False