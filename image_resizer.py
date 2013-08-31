#!/usr/bin/python
import Image
import os
import wx

sss

APP_SIZE = (500, 150)
EXTENSIONS = ('.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG')
DEFAULT_WIDTH = 300
DEBUG = False

class ImageResizer:
	def __init__(self):
		pass

	def resize(self, dir, resizeWidth):
		resize_dir = dir + '\\resize\\'
		if DEBUG: print 'resize, resize_dir=', resize_dir

		try: os.mkdir(resize_dir)
		except: pass
	
		for file in os.listdir(dir):
			basename = os.path.basename(file)
			name, ext = os.path.splitext(basename)
			if ext not in EXTENSIONS:
				continue
			if DEBUG: print 'resize, file=', file
			image = Image.open(dir+'\\'+file)
			w, h = image.size
			if DEBUG: print 'resize, old_size=', image.size
			if w > resizeWidth:
				new_h = h * resizeWidth / w
				image = image.resize((resizeWidth, new_h), Image.ANTIALIAS)
			if DEBUG: print 'resize, new_size=', image.size
			destname = resize_dir + name + '.jpeg'
			image.save(destname, format='jpeg', quality=100)

class IRApp(wx.Frame):
	mPathLabel = None
	mWidthLabel = None
	mStatusLabel = None

	def __init__(self, parent, title):
		super(IRApp, self).__init__(parent, title=title, size=APP_SIZE)
		self.ir = ImageResizer()
		self.InitUI()
	
	def InitUI(self):
		panel = wx.Panel(self)
		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(9)

		# 1st line
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(panel, label='Directory path:', size=(110,-1))
		st.SetFont(font)
		self.mPathLabel = wx.TextCtrl(panel)
		openButton = wx.Button(panel, 200, 'Open folder')
		openButton.Bind(wx.EVT_BUTTON, self.onOpenDir)
		hbox1.Add(st)
		hbox1.Add(self.mPathLabel, proportion=1)
		hbox1.Add(openButton)

		# 2nd line
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(panel, label='Default width:', size=(110,-1))
		st.SetFont(font)
		self.mWidthLabel = wx.TextCtrl(panel)
		self.mWidthLabel.SetValue('%d'%DEFAULT_WIDTH)
		hbox2.Add(st)
		hbox2.Add(self.mWidthLabel, proportion=1)

		# 3rd line
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(panel, label='Status:', size=(110,-1))
		st.SetFont(font)
		self.mStatusLabel = wx.StaticText(panel, label='Not started')
		hbox3.Add(st)
		hbox3.Add(self.mStatusLabel, proportion=1)

		# 4th line
		runButton = wx.Button(panel, 100, 'Run resizing!')
		runButton.Bind(wx.EVT_BUTTON, self.onRun)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox1, flag=wx.EXPAND|wx.ALL)
		vbox.Add(hbox2, flag=wx.EXPAND|wx.ALL)
		vbox.Add(hbox3, flag=wx.EXPAND|wx.ALL)
		vbox.Add(runButton, flag=wx.EXPAND)
		panel.SetSizer(vbox)

		self.Centre()
		self.Show()
	
	def onOpenDir(self, event):
		dialog = wx.DirDialog(self, 'Choose a directory:',
				style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_OK:
			self.mPathLabel.SetValue(dialog.GetPath())
		dialog.Destroy()
	
	def showPopup(self, msg):
		if DEBUG: print 'showPopup'
		wx.MessageBox(msg, 'Warning', wx.OK | wx.ICON_WARNING)
	
	def setStatus(self, status):
		self.mStatusLabel.SetLabel(status)

	def onRun(self, event):
		path = self.mPathLabel.GetValue()
		width = 0
		if self.mWidthLabel.GetValue():
			width = int(self.mWidthLabel.GetValue())
		if DEBUG: print 'onRun, path=', path, ', default width=', width

		if not width:
			self.showPopup('Width error')
			return

		if not path or not os.path.exists(path):
			self.showPopup('Directory path is wrong')
			return

		self.setStatus('Image resizing...')
		self.ir.resize(path, width)
		self.setStatus('Done')

if __name__ == '__main__':
	app = wx.App(redirect=False)
	IRApp(None, title="Image Resizer for Heesun")
	app.MainLoop()
