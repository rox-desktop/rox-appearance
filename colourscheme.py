import gtk

PADDING = 6

_rox_setting = None
_gtk_settings = gtk.settings_get_default()
_colours = {}

COLOUR_NAMES = [ 'bg_color', 'fg_color',
		'base_color', 'text_color',
		'selected_bg_color', 'selected_fg_color',
		'tooltip_bg_color', 'tooltip_fg_color' ]


def colour_scheme_parse(value):
	colours = {}
	lines = value.split('\n')
	for line in lines:
		if not ':' in line:
			continue
		k, v = line.split(':', 1)
		if not k in COLOUR_NAMES:
			continue
		colours[k.strip()] = v.strip()
	return colours


def compare_colour_schemes(scheme1, scheme2):
	if not isinstance(scheme1, dict):
		scheme1 = colour_scheme_parse(scheme1)
	if not isinstance(scheme2, dict):
		scheme2 = colour_scheme_parse(scheme2)
	if not scheme1 or not scheme2:
		return not(not scheme1 and not scheme2)
	for k, v in scheme1.items():
		if scheme2[k] != v:
			return 1
	return 0


def colour_scheme_string_from_gtk_settings(settings = None):
	if not settings:
		settings = _gtk_settings
	s = _gtk_settings.get_property('gtk-color-scheme')
	return s


def _colour_scheme_changed_cb(settings, spec):
	global _colours
	global _rox_setting
	new_scheme_str = colour_scheme_string_from_gtk_settings(settings)
	if compare_colour_schemes(new_scheme_str, _colours):
		_colours = colour_scheme_parse(new_scheme_str)
		_rox_setting._set(s)


def init(setting):
	global _rox_setting, _gtk_settings, _colours
	_rox_setting = setting
	_colours = colour_scheme_parse(colour_scheme_string_from_gtk_settings())
	_gtk_settings.connect('notify::gtk-color-scheme', _colour_scheme_changed_cb)


class ColoursDialog(gtk.Dialog):
	def __init__(self, parent_window):
		self.cwidgets = {}
		gtk.Dialog.__init__(self, 'Colour scheme', parent_window,
				gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
				(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
		self.table = gtk.Table(5, 3, False)
		self.table.attach(gtk.Label('Background'), 1, 2, 0, 1,
				gtk.FILL, gtk.FILL, PADDING, PADDING)
		self.table.attach(gtk.Label('Text'), 2, 3, 0, 1,
				gtk.FILL, gtk.FILL, PADDING, PADDING)
		self.__add_to_table(1, 'General:', 'bg_color', 'fg_color')
		self.__add_to_table(2, 'Input boxes:', 'base_color', 'text_color')
		self.__add_to_table(3, 'Selected items:',
				'selected_bg_color', 'selected_fg_color')
		self.__add_to_table(4, 'Tooltips:',
				'tooltip_bg_color', 'tooltip_fg_color')
		self.vbox.pack_start(self.table)
		button = gtk.Button('Defaults')
		button.connect('clicked', self.__defaults_clicked_cb)
		hbox = gtk.HBox()
		hbox.pack_end(button, False, False, PADDING)
		self.vbox.pack_start(hbox, padding = PADDING)
		self.vbox.show_all()
		self.colour_scheme_changed_id = \
				_gtk_settings.connect('notify::gtk-color-scheme',
						self.__colour_scheme_changed_cb)
		self.connect('destroy', self.__destroy_cb)
	
	def __destroy_cb(self, object):
		_gtk_settings.disconnect(self.colour_scheme_changed_id)
	
	def __colour_scheme_changed_cb(self, settings, spec):
		self.update_from_settings(settings)

	def __add_to_table(self, row, label, background, foreground):
		lw = gtk.Label(label)
		self.table.attach(lw, 0, 1, row, row + 1,
				xpadding = PADDING, ypadding = PADDING)
		bgw = self.__make_colour_button(background)
		self.table.attach(bgw, 1, 2, row, row + 1, 0, 0,
				xpadding = PADDING, ypadding = PADDING)
		fgw = self.__make_colour_button(foreground)
		self.table.attach(fgw, 2, 3, row, row + 1, 0, 0,
				xpadding = PADDING, ypadding = PADDING)
		self.cwidgets[foreground] = fgw
	
	def __make_colour_button(self, name):
		w = gtk.ColorButton()
		self.cwidgets[name] = w
		w.connect('color-set', self.__colour_set_cb, name)
		return w

	def __colour_set_cb(self, widget, name):
		global _colours
		colour_str = '#%04x%04x%04x\n' % (c.red, c.green, c.blue)
		_colours[name] = colour_str
		s = ""
		for k, v in self.cwidgets.items():
			c = v.get_color()
			s += '%s: %s\n' % (k, colour_str)
		global _rox_setting
		_rox_setting._set(s)

	def update_colour_widget_from_string(self, name, value):
		w = self.cwidgets[name]
		old_colour = w.get_color()
		new_colour = gtk.gdk.color_parse(value)
		if new_colour.red != old_colour.red or \
				new_colour.green != old_colour.green or \
				new_colour.blue != old_colour.blue:
			w.set_color(new_colour)
	
	def update_from_settings(self, settings = None):
		global _colours
		if not settings:
			settings = _gtk_settings
		_colours = colour_scheme_parse( \
				colour_scheme_string_from_gtk_settings(settings))
		for k, v in _colours.items():
			self.update_colour_widget_from_string(k, v)
	
	def __defaults_clicked_cb(self, widget):
		global _rox_setting
		_rox_setting._set('')


def open_colours_dialog(widget, parent_window):
	dialog = ColoursDialog(parent_window)
	dialog.update_from_settings()
	dialog.run()
	dialog.destroy()


def build_parent_button(box, node, label, option):
	button = gtk.Button(label)
	button.connect("clicked", open_colours_dialog, box)
	hbox = gtk.HBox()
	hbox.pack_start(button, False, False)
	return [hbox]
