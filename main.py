import sys
from os.path import basename
from PySide6.QtWidgets import (QApplication, QPushButton, QLabel, 
					QVBoxLayout, QFileDialog, QDialog, QSlider)
from PySide6.QtCore import Qt
from pygame import mixer


class Form(QDialog):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)
		mixer.init()
		mixer.music.set_volume(0.1)

		self.b_file = QPushButton('file')
		self.b_play = QPushButton('play')
		self.b_pause = QPushButton('pause')

		self.vol = QLabel('Volume')
		self.vol.setAlignment(Qt.AlignCenter)
		self.slider = QSlider(orientation=Qt.Horizontal)
		self.slider.setRange(1, 100)
		self.slider.setSliderPosition(10)

		self.cur_pl = 'Currently playing: \n'
		self.name_tr = QLabel(self.cur_pl)
		self.name_tr.setAlignment(Qt.AlignCenter)
		self.b_ext = QPushButton('quit')

		self.b_file.clicked.connect(self.open)
		self.b_pause.clicked.connect(mixer.music.pause)
		self.b_play.clicked.connect(mixer.music.unpause)
		self.slider.actionTriggered.connect(self.slide_vl)
		self.b_ext.clicked.connect(exit)

		layout = QVBoxLayout()
		layout.addWidget(self.b_file)
		layout.addWidget(self.b_play)
		layout.addWidget(self.b_pause)
		layout.addWidget(self.vol)
		layout.addWidget(self.slider)

		layout.addWidget(self.name_tr)
		layout.addWidget(self.b_ext)
		self.setLayout(layout)

	def open(self):
		path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'All Files (*.*)')
		if path != ('', ''):
			self.name_tr.setText(self.cur_pl + basename(path[0]))
			mixer.music.load(path[0])
			mixer.music.play()

	def vlme(self):
		a = mixer.music.get_volume()
		print(a)

	def slide_vl(self):
		a = self.slider.value()
		if a == 1: a = 0
		mixer.music.set_volume(a / 100)
		print(a, mixer.music.get_volume())

app = QApplication(sys.argv)

form = Form()
form.setWindowTitle('ThewrstAudioPlayer')
form.show()
app.exec()
