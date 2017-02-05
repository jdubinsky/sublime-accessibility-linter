import sublime
import sublime_plugin

class AccessibilityLinter(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		view.run_command('accessibility_linter')

	def on_selection_modified_async(self, view):
		view.run_command('accessibility_linter')

class AccessibilityLinterCommand(sublime_plugin.TextCommand):
	supported_html_tags = {
		'button',
	}
	status_messages = {}
	status_message_key = "accessibility"

	def run(self, edit):
		current_region = self.view.sel()[0]
		current_region_tuple = (current_region.a, current_region.b)
		message = self.get_status_message_for_current_region(current_region_tuple)
		if message:
			sublime.status_message(message)
			return
		else:
			sublime.status_message('')

		view_size = self.view.size()
		regions_by_line = self.view.split_by_newlines(sublime.Region(0, view_size))
		regions = self.get_error_regions(regions_by_line)
		self.status_messages = {(region.a, region.b): 'test' for region in regions}
		self.view.add_regions('cross', regions, 'cross', 'cross')

	def get_error_regions(self, regions_by_line):
		lines = [
			self.view.substr(region) for region in regions_by_line
		]
		a = 0
		regions = []
		for line in lines:
			line_length = len(line)
			if self.should_show_region(line):
				regions.append(
					sublime.Region(a, a + line_length)
				)
			a += line_length + 1
		return regions

	def get_status_message_for_current_region(self, current_region):
		a, b = current_region
		for region in self.status_messages.keys():
			line_a, line_b = region
			if a >= line_a and b <= line_b:
				return self.status_messages[region]
		return None

	def should_show_region(self, line):
		stripped_line = line.strip().lower()
		if not self.looks_like_html(stripped_line):
			return False
		for word in stripped_line.strip('<').strip('>').split():
			if word in self.supported_html_tags:
				return True

	def looks_like_html(self, line):
		if not line:
			return False
		return line[0] == '<'