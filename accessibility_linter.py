import string
import sublime
import sublime_plugin

status_messages = {}

class AccessibilityLinter(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		self.status_messages = view.run_command('accessibility_linter')
		print('did it work', self.status_messages)

	def on_selection_modified_async(self, view):
		print('mod')
		view.run_command('accessibility_linter_status_message')

class AccessibilityLinterStatusMessageCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		current_region = self.view.sel()[0]
		print('cur', current_region)
		print(status_messages)
		sublime.status_message('test')

class AccessibilityLinterCommand(sublime_plugin.TextCommand):
	supported_html_tags = {
		'button',
	}

	def run(self, edit):
		view_size = self.view.size()
		regions_by_line = self.view.split_by_newlines(sublime.Region(0, view_size))
		lines = [
			self.view.substr(region) for region in regions_by_line
		]
		print(lines)
		a = 0
		regions = []
		for line in lines:
			print('line', line)
			print('size', len(line))
			line_length = len(line)
			if self.should_show_region(line):
				print('a', a)
				print('b', a + line_length)
				regions.append(
					sublime.Region(a, a + line_length)
				)
			a += line_length + 1
		status_messages = {(region.a, region.b): 'test' for region in regions}
		print(status_messages)
		self.view.add_regions('cross', regions, 'cross', 'cross')
		return status_messages

	def should_show_region(self, line):
		stripped_line = line.strip().lower()
		if not self.looks_like_html(stripped_line):
			return False
		for word in stripped_line.strip('<').strip('>').split():
			print(word)
			if word in self.supported_html_tags:
				return True

	def looks_like_html(self, line):
		if line[0] == '<':
			return True
		return False