import cairo
import gtk
import state

class Gui(gtk.Window):
	def __init__(self):
		super(Gui, self).__init__()

		self.statusicon = gtk.status_icon_new_from_stock(gtk.STOCK_GOTO_TOP)
		self.statusicon.connect("activate", self.on_status_clicked)

		self.connect("key-press-event", self.on_keypress)
		self.connect("delete-event", self.on_delete)
		self.connect("expose-event", self.on_expose)

		self.screen = self.get_screen()
		colormap = self.screen.get_rgba_colormap()
		if (colormap is not None and self.screen.is_composited()):
			self.set_colormap(colormap)
		else:
			print "Screen is not composited, transparency disabled!"

		self.set_app_paintable(True)
		self.maximize()
		self.show_all()

	def on_keypress(self, window, event):
		if event.keyval == gtk.keysyms.q:
			gtk.main_quit()
		if event.keyval == gtk.keysyms.t:
			state.toggle_opaque()
			self.queue_draw()
		if event.keyval == gtk.keysyms.space:
			self.toggle()

	def on_delete(self, window, event):
		self.toggle()
		return True

	def on_expose(self, widget, event):
		cr = widget.get_window().cairo_create()
		cr.set_source_rgba(0, 0, 0, 1.0 if state.opaque else 0.0)
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.paint()
		cr.set_operator(cairo.OPERATOR_OVER)
		return False

	def on_status_clicked(self, status):
		self.toggle()

	def toggle(self):
		if not state.minimized:
			self.statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
			self.iconify()
		else:
			self.statusicon.set_from_stock(gtk.STOCK_GOTO_TOP)
			self.deiconify()
		state.toggle_minimized()

def run():
	Gui()
	gtk.main()
