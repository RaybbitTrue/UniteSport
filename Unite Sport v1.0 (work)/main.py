from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import os
import re

Window.clearcolor = (43/255.0, 43/255.0, 43/255.0, 1)					# настройка цвета заднего фона приложения
#Window.size = (540, 1080)												# настройка размера окна

global globnamenote														# оглавляемя глобальную переменную
globnamenote = ""														# задаём пустое значение для глобальной переменной

#главный_экран----------------------------------------------------------------------------------------------------------
class Container1(Screen):
	pass

#секундомер-------------------------------------------------------------------------------------------------------------
class Container2(Screen):

	# значение секунд:
	count = 0
	# значение десяток секунд:
	count2 = 0
	# значение минут:
	count3 = 0
	# значение десяток минут:
	count4 = 0
	# переменная для остановки и запуска секундомера,
	# в зависимости от значения (0 - включено, 1 - выключено):
	count0 = 0

	#настройки для кнопки старт:
	def Settings_Start(self):
		self.start_button.disabled = True  						# отключает кнопку
		self.start_button.background_color = (43, 43, 43, 0)  	# делает кнопку прозрачной

	#настройки для кнопки перезапуск:
	def Settings_Restart(self):
		self.restart_button.disabled = True 					# отключает кнопку
		self.restart_button.background_color = (43, 43, 43, 0)  # делает кнопку прозрачной

	# настройки для кнопки перезапуск:
	def Settings_Stop(self):
		self.stop_button.disabled = False  						# включает кнопку
		self.stop_button.opacity = 1  							# делает кнопку не прозрачной

	#кнопка старт:
	def Start_The_Clock(self):
		if self.count0 == 0:
			Clock.schedule_interval(self.Callback_Clock, 1)		# указывается колличество секунд, спустя которое будет работать функция
			self.Settings_Start()								# настройки для кнопки старт
			self.Settings_Restart()								# настройки для кнопки перезапуск
			self.Settings_Stop()  								# настройки для кнопки стоп
		elif self.count0 > 0:
			self.count0 = self.count0 - 1
			self.Settings_Start()
			self.Settings_Restart()
			self.Settings_Stop()
		else:
			pass

	# то, благодаря чему увеличивается время на таймере:
	def Callback_Clock(self, dt):

		# секунды и десятки секунд:
		if self.count < 9 and self.count0 == 0:
			self.count = self.count + 1
		elif self.count == 9 and self.count0 == 0:
			self.count = 0
			self.count2 = self.count2 + 1
		else:
			pass

		# минуты:
		if self.count2 == 6 and self.count == 0 and self.count0 == 0:
			self.count3 = self.count3 + 1
			self.count2 = 0
			self.count = 0
		else:
			pass

		# десятки минут:
		if self.count3 == 10 and self.count0 == 0:
			self.count3 = 0
			self.count4 = self.count4 + 1
		else:
			pass

		# вывод времени в таймер (label):
		self.timer_display.text = str(self.count4) + str(self.count3) + ":%s" % str(self.count2) + str(self.count)

	# кнопка стоп:
	def Stop_The_Clock(self):
		self.count0 = 1
		# для кнопки старт:
		self.start_button.disabled = False
		self.start_button.background_color = (43, 43, 43, 1)
		# для кнопки перезапуск:
		self.restart_button.disabled = False
		self.restart_button.background_color = (43, 43, 43, 1)
		# для кнопки стоп
		self.stop_button.disabled = True
		self.stop_button.opacity = 0

	# кнопка перезапуска:
	def Restart_The_Clock(self):
		self.count = 0
		self.count2 = 0
		self.count3 = 0
		self.count4 = 0

#калькулятор------------------------------------------------------------------------------------------------------------
class Container3(Screen):

	# подсчёт идёт благодаря функции "eval":
	def Calculate(self, calculation):
		if calculation:
			try:
				self.display.text = str(eval(calculation))
			except Exception:
				self.display.text = "ERROR"

#заметки----------------------------------------------------------------------------------------------------------------
class Container4(Screen):

	namefile = ""			# имя файла для названия новой заметки
	number = ""				# номер заметки
	new_number = ""			# новый номер для следующей заметки

	# функция проверки глобальной переменной на хранение имения файла и последующего чтения для записи в область заметки
	def on_enter(self):
		global globnamenote															# добавляем глобальную переменную

		if globnamenote == "":														# если глобальная переменная равна ничему
			pass																	# пропустить
		else:
			file = open(globnamenote + ".txt", "r")									# открываем файл на чтение
			self.display_notes.text = file.read()									# приравниваем поля ввода заметки к содержимому файла
			file.close()															# закрываем файл

	#функция удаления заметки из списка с именами заметок
	def Delete_Note(self):
		global globnamenote  														# добавляем глобальную переменную
		note_name = globnamenote + ".txt"											# создаём название файла из глобальной переменной и ".txt", и заносим в переменную
		os.remove(note_name)														# удаляем файл с нужным названием

		with open("namesfiles.txt", "r") as f:												# открываем файл на чтение в цикле
			lines = f.readlines()
		with open("namesfiles.txt", "w") as f:												# открываем файл на запись в цикле
			for line in lines:
				if line.strip("\n") != str(note_name):								# сравниваем каждую строку с нужной нам строкой
					f.write(line)													# если она не равна нужной строке, то записываем в файл
		self.Clear_Display_Notes()

	# функция очистки поля заметки
	def Clear_Display_Notes(self):
		global globnamenote															# добавляем глобальную переменную
		globnamenote = ""															# приравниваем глобальную переменную к пустоте
		self.display_notes.text = ""												# очищаем поле ввода заметки

	# функция обновления заметки
	def Update_Note(self):
		global globnamenote															# добавляем глобальную переменную

		file = open(globnamenote + ".txt", "w+")  									# открываем файл на запись
		file.write(self.display_notes.text)											# в файл записывается текст из поля ввода заметки
		file.close()  																# закрываем файл

	# функция проверки наличия текста в поле ввода заметки:
	def Check_Display_Notes(self):
		if self.display_notes.text != "":		# если поле ввода заметки не пусто, то:
			self.Add_notes()					# то запускаем функцию Add_notes
		else:
			pass

	# функция создания новой заметки (текстового файла):
	def Add_notes(self):
		self.Create_name_file()					# обращаемся к функции "Create_name_file"
		file = open(self.namefile, "w+")		# открываем файл на запись
		file.write(self.display_notes.text)		# в файл записывается текст из поля ввода заметки
		file.close()							# файл закрывается
		self.Write_number_in_number_file()		# обращаемся к функции "Write_number_in_number_file"
		self.display_notes.text = ""			# очищаем поле заметки
		self.Write_name_in_names_file()

	# функция на создание имени файла:
	def Create_name_file(self):
		self.namefile = self.display_notes.text.split("\n")[0]					# приравниваем переменную к первой строке текста файла
		import re																# импортируем "re"
		self.namefile = re.sub("[<>:/|?*]", "", self.namefile)					# убираем из названия файла все знаки с которыми не может быть создан ".txt" файл
		self.Get_Number_from_number_file()										# обращаемся к функции "Get_Number_from_number_file"
		self.namefile = str(self.number) + ")" + str(self.namefile) + ".txt"	# приравниваем имя файла к "номеру файла" + ")" + "имя файла" + ".txt"

	# функция для взятия номера заметки из файла с номером:
	def Get_Number_from_number_file(self):
		file = open("countfiles.txt", "r")		# открываем файл на чтение
		self.number = file.read()				# приравнивание переменной к содержимому файла
		file.close()							# закрываем файл

	# функция записи нового номера в файл с номером:
	def Write_number_in_number_file(self):
		file = open("countfiles.txt", "r")					# открываем файл на чтение
		self.new_number = file.read()						# приравнивание переменной к содержимому файла
		file.close()										# закрываем файл
		open('countfiles.txt', 'w').close()					# открываем файл на перезапись и закрываем для удаления всех данных в файле
		file = open("countfiles.txt", "a")					# открываем файл на дозапись
		self.new_number = eval(self.new_number + "+1")		# приравниваем переменную к сложению данных файла (1) и 1
		self.new_number = str(self.new_number)				# переводим в str
		file.write(self.new_number)							# записываем в файл получивщиеся данные (2)
		file.close()										# закрываем файл

	# функция записи имени файла в файл, с именами файлов:
	def Write_name_in_names_file(self):
		file = open("namesfiles.txt", "a")
		file.write(self.namefile + "\n")
		file.close()

#список-----------------------------------------------------------------------------------------------------------------
class Container5(Screen):

	# функция для добавления заметок в список заметок при каждом открытии экрана
	def on_enter(self):												# on_enter позволяет запускать функцию при каждом открытии экрана

		id_list = []												# массив для всех id
		a = 0

		# создаём label с надписью "заметки" в верху списка
		new_label = Label(
			size=(490, 50),
			text="Заметки:",
			font_size=(40),
			font_name='Ponter X.ttf',
			size_hint=(None, None)
		)
		self.grid_notes_list.add_widget(new_label)

		with open("namesfiles.txt") as f:  							# запускае цикл, который будет сам закрывать файл при каждом цикле
			for line in f:  										# за переменную, берём каждую строку
				str_line = line 									# приравниваем строку к переменной для удобства
				len_line = len(str_line)  							# создаём переменную и приравниваем к длинне строки
				line_without_last = str_line[:len_line - 1] 		# создаём переменную и приравниваем к строке, без последнего элемента (в виде \n, то есть переноса строки)
				line1 = line_without_last  							# приравниваем строку к этой же строке, но без последнего символа
				if os.path.isfile(line1) == True:					# запускаем цикл на проверку существоваения файла, если цикл работает, то создаём кнопку в списке заметок
					str_line = line1  								# приравниваем строку к переменной для удобства
					len_line = len(str_line)  						# создаём переменную и приравниваем к длинне строки
					line_without_last = str_line[:len_line - 4]  	# создаём переменную и приравниваем к строке, без ".txt"
					line2 = line_without_last  						# приравниваем строку к этой же линии, но без последних 4х символов
					# код создания кнопки в списке заметок:
					# --------------------------------------------------------------------------------------------------
					app = App.get_running_app()
					sm = app.root

					new_button = Button(
						#size=(490, 90),
						text=line2,
						font_size=(30),
						font_name='Ponter X.ttf',
						#size_hint=(None, None),
						size_hint=(0.9074, 0.083),
						background_normal='images/img_new_zam.png'
					)

					id1 = re.sub('\D', '', line2)					# для того, чтобы оставить из названий кнопок только цифры ("23)день ног" -> "23)
					id_list.append(id1)								# для добавления переменной в массив, объявленный в самом начале функции
					#print(id_list)
					self.ids[id1] = new_button						# добавляем для создаваемой кнопки свой id
					b = id_list[a]

					#new_button.bind(on_release=lambda *args: print(self.ids.__getattr__))
					#new_button.bind(on_release=lambda a=a: self.Read_Note(id_list[a]))
					new_button.bind(on_release=lambda a=a,b=b: self.Read_Note(b))
					#new_button.bind(on_release=lambda a=a: print(str((self.ids[id_list[a]].text))))
					#new_button.bind(on_release=lambda *args: print(str((self.ids.__getattr__))))
					new_button.bind(on_release=lambda *args: setattr(sm, 'current', "Container4"))	# программируем кнопку на переход на другой экран
					new_button.bind(on_release=lambda *args: self.Remove_Buttons())  				# программируем кнопку на удаления всех кнопок из списка заметок
					self.grid_notes_list.add_widget(new_button, -1)  								# добавляем кнопку в список заметок (-1 нужен для ориентации с низу вверх)
				# --------------------------------------------------------------------------------------------------
				else:
					pass
				a = a + 1
		# код создания пустых label в списке заметок:
		# --------------------------------------------------------------------------------------------------
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
		# --------------------------------------------------------------------------------------------------

	# функция для удаления всех виджетов в GridLayout (список заметок)
	def Remove_Buttons(self):
		self.grid_notes_list.clear_widgets()

	def Read_Note(self, i):
		global globnamenote														# обозначаем, что globnamenote это глобальная переменная
		#print(str((self.ids[i].text)))
		button_name = str((self.ids[i].text))									# приравниваем имя кнопки к переменной
		globnamenote = button_name												# записываем в глобальную переменную имя кнопки

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
			#new_button.bind(on_release=lambda x: self.Open_Note())							# кнопка запускает функцию
			new_button.bind(on_press=lambda *args: setattr(sm, 'current', "Container4"))	# кнопка переходит на экран
			self.grid_notes_list.add_widget(new_button)

			return new_button

class WindowManager(ScreenManager):
	pass

class MyApp(App):
	pass

if __name__ == '__main__':
	MyApp().run()