import gtk

class Gui(gtk.Window):
	def __init__(self):
		super(Gui, self).__init__()

		self.statusicon = gtk.status_icon_new_from_stock(gtk.STOCK_GOTO_TOP)
		self.statusicon.connect("activate", self.on_status_clicked)

		self.connect("key-press-event", self.on_keypress)
		self.connect("delete-event", self.on_delete)

		self.maximize()
		self.show_all()
		self.visible = True

	def on_keypress(self, window, event):
		if event.keyval == gtk.keysyms.q:
			gtk.main_quit()
		if event.keyval == gtk.keysyms.space:
			self.toggle()

	def on_delete(self, window, event):
		self.toggle()
		return True

	def on_status_clicked(self, status):
		self.toggle()

	def toggle(self):
		if self.visible:
			self.statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
			self.iconify()
		else:
			self.statusicon.set_from_stock(gtk.STOCK_GOTO_TOP)
			self.deiconify()
		self.visible = not self.visible

def run():
	Gui()
	gtk.main()
