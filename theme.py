import os
import rox
from rox import OptionsBox, g
import string

from rox.basedir import xdg_data_dirs


def add_gtk_themes(themes, dir):
	if not os.path.isdir(dir):
		return
	for theme in os.listdir(dir):
		if theme.startswith('.'): continue
		if os.path.exists(os.path.join(dir, theme, 'gtk-2.0')):
			themes[theme] = True

def build_gtk_theme(box, node, label, option):
	hbox = g.HBox(False, 4)

	hbox.pack_start(box.make_sized_label(label), False, True, 0)

	button = g.combo_box_new_text()
	hbox.pack_start(button, True, True, 0)

	themes = {}
	user_dir = os.path.expanduser('~/.themes')
	add_gtk_themes(themes, user_dir)
	add_gtk_themes(themes, g.rc_get_theme_dir())

	names = themes.keys()
	names.sort()

	for name in names:
		button.append_text(name)

	def update_theme():
		i = -1
		for name in names:
			i += 1
			if name == option.value:
				button.set_active(i)
				break
	
	def read_theme(): return button.get_active_text()

	box.handlers[option] = (read_theme, update_theme)

	button.connect('changed', lambda w: box.check_widget(option))

	return [hbox]
    

def add_icon_themes(themes, dir):
	if not os.path.isdir(dir):
		return
	for theme in os.listdir(dir):
		if theme.startswith('.'): continue
		if os.path.exists(os.path.join(dir, theme, 'index.theme')):
			themes[theme] = True

def build_icon_theme(box, node, label, option):
	hbox = g.HBox(False, 4)

	hbox.pack_start(box.make_sized_label(label), False, True, 0)

	button = g.combo_box_new_text()
	hbox.pack_start(button, True, True, 0)

	themes = {}
	add_icon_themes(themes, os.path.expanduser('~/.icons'))
	for dir in xdg_data_dirs:
	    add_icon_themes(themes, dir+'/icons')
	add_icon_themes(themes, '/usr/local/share/pixmaps') 
	add_icon_themes(themes, '/usr/share/pixmaps')
	

	names = themes.keys()
	names.sort()

	for name in names:
		button.append_text(name)

	def update_theme():
		i = -1
		for name in names:
			i += 1
			if name == option.value:
				button.set_active(i)
	
	def read_theme(): return button.get_active_text()

	box.handlers[option] = (read_theme, update_theme)

	button.connect('changed', lambda w: box.check_widget(option))

	return [hbox]

OptionsBox.widget_registry['gtk-theme'] = build_gtk_theme
OptionsBox.widget_registry['icon-theme'] = build_icon_theme
