from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLineEdit, QButtonGroup, QLineEdit, 
							QPushButton, QMessageBox, QLabel, QVBoxLayout, 
							QHBoxLayout, QRadioButton, QApplication, QWidget, QListWidget, QTextEdit, QInputDialog)
import json


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Умные заметки")
main_win.resize(1080, 720)
main_win.show()


notes = {
   
}

def update():
	with open("notes_data.json", "w") as file:
		json.dump(notes, file)

with open("notes_data.json", "r") as file:
	notes = json.load(file)


#---------------------------------------------#
note_text = QTextEdit()

notes_list = QListWidget()
notes_list_title = QLabel("Список заметок")

notes_list_add_button = QPushButton("Создать заметку")
notes_list_remove_button = QPushButton("Удалить заметку")
notes_list_save_button = QPushButton("Сохранить заметку")
notes_list_edit_button = QPushButton("Изменить название")


tags_list = QListWidget()
tags_list_title = QLabel("Список тегов")

new_tag = QLineEdit()
new_tag.setPlaceholderText("Введите тег...")

tags_list_add_button = QPushButton("Добавить к заметке")
tags_list_remove_button = QPushButton("Открепить от заметки")
tags_list_search_button = QPushButton("Искать заметки по тегу")
#---------------------------------------------#


#---------------------------------------------#
main_h_layout = QHBoxLayout()
main_right_v_layout = QVBoxLayout()
main_left_v_layout = QVBoxLayout()

main_h_layout.addLayout(main_left_v_layout, stretch=3)
main_h_layout.addLayout(main_right_v_layout, stretch=2)

notes_buttons_h_layout1 = QHBoxLayout()
notes_buttons_h_layout2 = QHBoxLayout()
tags_buttons_h_layout = QHBoxLayout()

notes_buttons_h_layout1.addWidget(notes_list_add_button)
notes_buttons_h_layout1.addWidget(notes_list_remove_button)

notes_buttons_h_layout2.addWidget(notes_list_save_button)
notes_buttons_h_layout2.addWidget(notes_list_edit_button)

tags_buttons_h_layout.addWidget(tags_list_add_button)
tags_buttons_h_layout.addWidget(tags_list_remove_button)

main_left_v_layout.addWidget(note_text)

main_right_v_layout.addWidget(notes_list_title)
main_right_v_layout.addWidget(notes_list)
main_right_v_layout.addLayout(notes_buttons_h_layout1)
main_right_v_layout.addLayout(notes_buttons_h_layout2)

main_right_v_layout.addWidget(tags_list_title)
main_right_v_layout.addWidget(tags_list)
main_right_v_layout.addWidget(new_tag)
main_right_v_layout.addLayout(tags_buttons_h_layout)
main_right_v_layout.addWidget(tags_list_search_button)

main_win.setLayout(main_h_layout)
#---------------------------------------------#


#---------------------------------------------#
def add_note():
	note_name, ok = QInputDialog.getText(main_win, "Добавить заметку", "Название заметки: ")
	if ok and note_name != "":
		notes[note_name] = {"text": "", "tags": []}
		notes_list.addItem(note_name)
		tags_list.addItems(notes[note_name]["tags"])
	update()
	get_note_info()

def del_note():
	if notes_list.selectedItems():
		key = notes_list.selectedItems()[0].text()
	
		del notes[key]
		notes_list.clear()
		notes_list.addItems(notes)
		update()
		get_note_info()
	

def save_note():
	if notes_list.selectedItems():
		key = notes_list.selectedItems()[0].text()
	
		notes[key]["text"] = note_text.toPlainText()
		update()
		get_note_info()


	

notes_list_remove_button.clicked.connect(del_note)
notes_list_save_button.clicked.connect(save_note)
notes_list_add_button.clicked.connect(add_note)
notes_list_edit_button.clicked.connect(edit_note)
#---------------------------------------------#


#---------------------------------------------#
def search_note():
	if tags_list_search_button.text() == "Искать заметки по тегу" and new_tag.text() != "":
		tags_list_search_button.setText("Сбросить поиск")
		tag = new_tag.text()
		filtered = {}

		for note in notes:
			if tag in notes[note]["tags"]:
				filtered[note] = notes[note]
		
		notes_list.clear()
		tags_list.clear()
		notes_list.addItems(filtered)
	else:
		tags_list_search_button.setText("Искать заметки по тегу")
		new_tag.clear()
		notes_list.clear()
		tags_list.clear()
		notes_list.addItems(notes)

def add_tag():
	if notes_list.selectedItems():
		key = notes_list.selectedItems()[0].text()
	
		notes[key]["tags"].append(new_tag.text())
		new_tag.setText("")
		update()
		get_note_info()

def del_tag():
	if notes_list.selectedItems():
		note_key = notes_list.selectedItems()[0].text()

		if tags_list.selectedItems():
			tag_key = tags_list.selectedItems()[0].text()
	
			del notes[note_key]["tags"][notes[note_key]["tags"].index(tag_key)]
			update()
			get_note_info()
		elif new_tag.text() != "" and new_tag.text() in notes[note_key]["tags"]:
			del notes[note_key]["tags"][new_tag.text()]
		update()
		get_note_info()


tags_list_search_button.clicked.connect(search_note)
tags_list_add_button.clicked.connect(add_tag)
tags_list_remove_button.clicked.connect(del_tag)
#---------------------------------------------#


#---------------------------------------------#
def get_note_info():
	if notes_list.selectedItems():
		key = notes_list.selectedItems()[0].text()
	
		note_text.setText(notes[key]["text"])
		tags_list.clear()
		tags_list.addItems(notes[key]["tags"])
	else:
		note_text.setText("")
		tags_list.clear()

notes_list.itemClicked.connect(get_note_info)


notes_list.addItems(notes)

#---------------------------------------------#

app.exec()