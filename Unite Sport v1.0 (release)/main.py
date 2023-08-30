from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import os
import re

Window.clearcolor = (43/255.0, 43/255.0, 43/255.0, 1)
#Window.size = (540, 1080)

global globnamenote
globnamenote = ""

class Container1(Screen):
	pass

class Container2(Screen):

	count = 0
	count2 = 0
	count3 = 0
	count4 = 0
	count0 = 0

	def Settings_Start(self):
		self.start_button.disabled = True
		self.start_button.background_color = (43, 43, 43, 0)

	def Settings_Restart(self):
		self.restart_button.disabled = True
		self.restart_button.background_color = (43, 43, 43, 0)

	def Settings_Stop(self):
		self.stop_button.disabled = False
		self.stop_button.opacity = 1

	def Start_The_Clock(self):
		if self.count0 == 0:
			Clock.schedule_interval(self.Callback_Clock, 1)
			self.Settings_Start()
			self.Settings_Restart()
			self.Settings_Stop()
		elif self.count0 > 0:
			self.count0 = self.count0 - 1
			self.Settings_Start()
			self.Settings_Restart()
			self.Settings_Stop()
		else:
			pass

	def Callback_Clock(self, dt):

		if self.count < 9 and self.count0 == 0:
			self.count = self.count + 1
		elif self.count == 9 and self.count0 == 0:
			self.count = 0
			self.count2 = self.count2 + 1
		else:
			pass

		if self.count2 == 6 and self.count == 0 and self.count0 == 0:
			self.count3 = self.count3 + 1
			self.count2 = 0
			self.count = 0
		else:
			pass

		if self.count3 == 10 and self.count0 == 0:
			self.count3 = 0
			self.count4 = self.count4 + 1
		else:
			pass

		self.timer_display.text = str(self.count4) + str(self.count3) + ":%s" % str(self.count2) + str(self.count)

	def Stop_The_Clock(self):
		self.count0 = 1
		self.start_button.disabled = False
		self.start_button.background_color = (43, 43, 43, 1)
		self.restart_button.disabled = False
		self.restart_button.background_color = (43, 43, 43, 1)
		self.stop_button.disabled = True
		self.stop_button.opacity = 0

	def Restart_The_Clock(self):
		self.count = 0
		self.count2 = 0
		self.count3 = 0
		self.count4 = 0

class Container3(Screen):

	def Calculate(self, calculation):
		if calculation:
			try:
				self.display.text = str(eval(calculation))
			except Exception:
				self.display.text = "ERROR"

class Container4(Screen):

	namefile = ""
	number = ""
	new_number = ""

	def on_enter(self):
		global globnamenote

		if globnamenote == "":
			pass
		else:
			file = open(globnamenote + ".txt", "r")
			self.display_notes.text = file.read()
			file.close()

	def Delete_Note(self):
		global globnamenote
		note_name = globnamenote + ".txt"
		os.remove(note_name)

		with open("namesfiles.txt", "r") as f:
			lines = f.readlines()
		with open("namesfiles.txt", "w") as f:
			for line in lines:
				if line.strip("\n") != str(note_name):
					f.write(line)
		self.Clear_Display_Notes()

	def Clear_Display_Notes(self):
		global globnamenote
		globnamenote = ""
		self.display_notes.text = ""

	def Update_Note(self):
		global globnamenote

		file = open(globnamenote + ".txt", "w+")
		file.write(self.display_notes.text)
		file.close()

	def Check_Display_Notes(self):
		if self.display_notes.text != "":
			self.Add_notes()
		else:
			pass

	def Add_notes(self):
		self.Create_name_file()
		file = open(self.namefile, "w+")
		file.write(self.display_notes.text)
		file.close()
		self.Write_number_in_number_file()
		self.display_notes.text = ""
		self.Write_name_in_names_file()

	def Create_name_file(self):
		self.namefile = self.display_notes.text.split("\n")[0]
		import re
		self.namefile = re.sub("[<>:/|?*]", "", self.namefile)
		self.Get_Number_from_number_file()
		self.namefile = str(self.number) + ")" + str(self.namefile) + ".txt"

	def Get_Number_from_number_file(self):
		file = open("countfiles.txt", "r")
		self.number = file.read()
		file.close()

	def Write_number_in_number_file(self):
		file = open("countfiles.txt", "r")
		self.new_number = file.read()
		file.close()
		open('countfiles.txt', 'w').close()
		file = open("countfiles.txt", "a")
		self.new_number = eval(self.new_number + "+1")
		self.new_number = str(self.new_number)
		file.write(self.new_number)
		file.close()

	def Write_name_in_names_file(self):
		file = open("namesfiles.txt", "a")
		file.write(self.namefile + "\n")
		file.close()

class Container5(Screen):

	def on_enter(self):

		id_list = []
		a = 0

		new_label = Label(
			size=(490, 50),
			text="Заметки:",
			font_size=(40),
			font_name='Ponter X.ttf',
			size_hint=(None, None)
		)
		self.grid_notes_list.add_widget(new_label)

		with open("namesfiles.txt") as f:
			for line in f:
				str_line = line
				len_line = len(str_line)
				line_without_last = str_line[:len_line - 1]
				line1 = line_without_last
				if os.path.isfile(line1) == True:
					str_line = line1
					len_line = len(str_line)
					line_without_last = str_line[:len_line - 4]
					line2 = line_without_last

					app = App.get_running_app()
					sm = app.root

					new_button = Button(
						size=(490, 90),
						text=line2,
						font_size=(30),
						font_name='Ponter X.ttf',
						size_hint=(None, None),
						background_normal='images/img_new_zam.png'
					)

					id1 = re.sub('\D', '', line2)
					id_list.append(id1)
					self.ids[id1] = new_button
					b = id_list[a]

					new_button.bind(on_release=lambda a=a,b=b: self.Read_Note(b))
					new_button.bind(on_release=lambda *args: setattr(sm, 'current', "Container4"))
					new_button.bind(on_release=lambda *args: self.Remove_Buttons())
					self.grid_notes_list.add_widget(new_button, -1)
				else:
					pass
				a = a + 1

		new_label2 = Label(
			size=(490, 90),
			text="",
			size_hint=(None, None)
		)
		new_label3 = Label(
			size=(490, 90),
			text="",
			size_hint=(None, None)
		)
		self.grid_notes_list.add_widget(new_label2)
		self.grid_notes_list.add_widget(new_label3)

	def Remove_Buttons(self):
		self.grid_notes_list.clear_widgets()

	def Read_Note(self, i):
		global globnamenote
		button_name = str((self.ids[i].text))
		globnamenote = button_name

	def Add_New_Button(self, *args):
			app = App.get_running_app()
			sm = app.root

			new_button = Button(
			size=(490, 90),
			text='День жима',
			font_size=(30),
			font_name='Ponter X.ttf',
			size_hint=(None, None),
			background_normal='img_new_zam.png'
			)

			new_button.bind(on_press=lambda *args: setattr(sm, 'current', "Container4"))
			self.grid_notes_list.add_widget(new_button)

			return new_button

class WindowManager(ScreenManager):
	pass

class MyApp(App):
	pass

if __name__ == '__main__':
	MyApp().run()