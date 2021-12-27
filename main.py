import sys
import psycopg2

from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()
        self.setWindowTitle("Schedule")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_timetable_tab()
        self._create_teacher_tab()
        self._create_subject_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="telebot",
                        user="postgres",
                        password="12345",
                        host="localhost",
                        port="5432")
        self.cursor = self.conn.cursor()
#Отображение вкладок
    def _create_timetable_tab(self):
        self.timetable_tab = QWidget()
        self.tabs.addTab(self.timetable_tab, "Timetable")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()
        self.shbox5 = QHBoxLayout()
        self.shbox6 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)
        self.svbox.addLayout(self.shbox5)
        self.svbox.addLayout(self.shbox6)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox2.addWidget(self.tuesday_gbox)
        self.shbox3.addWidget(self.wednesday_gbox)
        self.shbox4.addWidget(self.thursday_gbox)
        self.shbox5.addWidget(self.friday_gbox)

        self._create_monday_table()
        self._create_tuesday_table()
        self._create_wednesday_table()
        self._create_thursday_table()
        self._create_friday_table()

        self.update_schedule_button = QPushButton("Update")
        self.shbox6.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.timetable_tab.setLayout(self.svbox)
# Отображение таблиц по дням недели
    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(9)
        self._update_monday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)
    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tuesday_table.setColumnCount(9)
        self._update_tuesday_table()
        self.tvbox = QVBoxLayout()
        self.tvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.tvbox)
    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.wednesday_table.setColumnCount(9)
        self._update_wednesday_table()
        self.wdbox = QVBoxLayout()
        self.wdbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.wdbox)
    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.thursday_table.setColumnCount(9)
        self._update_thursday_table()
        self.thbox = QVBoxLayout()
        self.thbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.thbox)
    def _create_friday_table(self):
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.friday_table.setColumnCount(9)
        self._update_friday_table()
        self.frbox = QVBoxLayout()
        self.frbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.frbox)
#обновление таблицы с расписанием по дням недели
    def _update_monday_table(self):
        self.monday_table.clear()
        self.monday_table.setHorizontalHeaderLabels(
            ["Id", "Week", "Day", "Subject", "Teacher", "Room", "Time", " ", " "])
        self.cursor.execute("SELECT * FROM timetable where day='Понедельник'")
        records = list(self.cursor.fetchall())
        self.monday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.monday_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.monday_table.setItem(i, 6, QTableWidgetItem(str(r[6])))
            self.monday_table.setCellWidget(i, 7, joinButton)
            self.monday_table.setCellWidget(i, 8, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_from_monday_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_monday_table(num))
        i+=1
        joinButton = QPushButton("Join")
        self.monday_table.setCellWidget(i, 7, joinButton)
        joinButton.clicked.connect(lambda ch, num=i: self._add_to_monday_table(i))
        self.monday_table.resizeRowsToContents()
    def _update_tuesday_table(self):
        self.tuesday_table.clear()
        self.tuesday_table.setHorizontalHeaderLabels(
            ["Id", "Week", "Day", "Subject", "Teacher", "Room", "Time", " ", " "])
        self.cursor.execute("SELECT * FROM timetable where day='Вторник'")
        records = list(self.cursor.fetchall())
        self.tuesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.tuesday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.tuesday_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.tuesday_table.setItem(i, 6, QTableWidgetItem(str(r[6])))
            self.tuesday_table.setCellWidget(i, 7, joinButton)
            self.tuesday_table.setCellWidget(i, 8, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_from_tuesday_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_tuesday_table(num))
        i += 1
        joinButton = QPushButton("Join")
        self.tuesday_table.setCellWidget(i, 7, joinButton)
        joinButton.clicked.connect(lambda ch, num=i: self._add_to_tuesday_table(num))
        self.tuesday_table.resizeRowsToContents()
    def _update_wednesday_table(self):
        self.wednesday_table.clear()
        self.wednesday_table.setHorizontalHeaderLabels(
            ["Id", "Week", "Day", "Subject", "Teacher", "Room", "Time", " ", " "])
        self.cursor.execute("SELECT * FROM timetable where day='Среда'")
        records = list(self.cursor.fetchall())
        self.wednesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.wednesday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.wednesday_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.wednesday_table.setItem(i, 6, QTableWidgetItem(str(r[6])))
            self.wednesday_table.setCellWidget(i, 7, joinButton)
            self.wednesday_table.setCellWidget(i, 8, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_from_wednesday_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_wednesday_table(num))
        i += 1
        joinButton = QPushButton("Join")
        self.wednesday_table.setCellWidget(i, 7, joinButton)
        joinButton.clicked.connect(lambda ch, num=i: self._add_to_wednesday_table(num))
        self.wednesday_table.resizeRowsToContents()
    def _update_thursday_table(self):
        self.thursday_table.clear()
        self.thursday_table.setHorizontalHeaderLabels(
            ["Id", "Week", "Day", "Subject", "Teacher", "Room", "Time", " ", " "])
        self.cursor.execute("SELECT * FROM timetable where day='Четверг'")
        records = list(self.cursor.fetchall())
        self.thursday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.thursday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.thursday_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.thursday_table.setItem(i, 6, QTableWidgetItem(str(r[6])))
            self.thursday_table.setCellWidget(i, 7, joinButton)
            self.thursday_table.setCellWidget(i, 8, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_from_thursday_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_thursday_table(num))
        i += 1
        joinButton = QPushButton("Join")
        self.thursday_table.setCellWidget(i, 7, joinButton)
        joinButton.clicked.connect(lambda ch, num=i: self._add_to_thursday_table(num))
        self.thursday_table.resizeRowsToContents()
    def _update_friday_table(self):
        self.friday_table.clear()
        self.friday_table.setHorizontalHeaderLabels(
            ["Id", "Week", "Day", "Subject", "Teacher", "Room", "Time", " ", " "])
        self.cursor.execute("SELECT * FROM timetable where day='Пятница'")
        records = list(self.cursor.fetchall())
        self.friday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.friday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.friday_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.friday_table.setItem(i, 6, QTableWidgetItem(str(r[6])))
            self.friday_table.setCellWidget(i, 7, joinButton)
            self.friday_table.setCellWidget(i, 8, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_from_friday_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_friday_table(num))
        i += 1
        joinButton = QPushButton("Join")
        self.friday_table.setCellWidget(i, 7, joinButton)
        joinButton.clicked.connect(lambda ch, num=i: self._add_to_friday_table(num))
        self.friday_table.resizeRowsToContents()
#метод, изменяющий запись в базе данных по нажатию на кнопку "Join"
    def _change_from_monday_table(self, rowNum):
        row = list()
        for i in range(self.monday_table.columnCount()-2):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE timetable SET week=%s, day=%s, subject=%s, full_name=%s, room_numb=%s, "
                                "start_time=%s WHERE id=%s", (row[1], row[2], row[3], row[4], row[5], row[6], row[0]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _add_to_monday_table(self, rowNum):
        row = list()
        for i in range(self.monday_table.columnCount()-2):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO timetable (week, day, subject, full_name, room_numb, start_time) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (row[1], row[2], row[3], row[4], row[5], row[6]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _change_from_tuesday_table(self, rowNum):
        row = list()
        for i in range(self.tuesday_table.columnCount()-2):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE timetable SET week=%s, day=%s, subject=%s, full_name=%s, room_numb=%s, "
                                "start_time=%s WHERE id=%s", (row[1], row[2], row[3], row[4], row[5], row[6], row[0]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _add_to_tuesday_table(self, rowNum):
        row = list()
        for i in range(self.tuesday_table.columnCount()-2):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO timetable (week, day, subject, full_name, room_numb, start_time) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (row[1], row[2], row[3], row[4], row[5], row[6]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _change_from_wednesday_table(self, rowNum):
        row = list()
        for i in range(self.wednesday_table.columnCount() - 2):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE timetable SET week=%s, day=%s, subject=%s, full_name=%s, room_numb=%s, "
                                "start_time=%s WHERE id=%s", (row[1], row[2], row[3], row[4], row[5], row[6], row[0]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _add_to_wednesday_table(self, rowNum):
        row = list()
        for i in range(self.wednesday_table.columnCount() - 2):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO timetable (week, day, subject, full_name, room_numb, start_time) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (row[1], row[2], row[3], row[4], row[5], row[6]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _change_from_thursday_table(self, rowNum):
        row = list()
        for i in range(self.thursday_table.columnCount() - 2):
            try:
                row.append(self.thursday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE timetable SET week=%s, day=%s, subject=%s, full_name=%s, room_numb=%s, "
                                "start_time=%s WHERE id=%s", (row[1], row[2], row[3], row[4], row[5], row[6], row[0]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _add_to_thursday_table(self, rowNum):
        row = list()
        for i in range(self.thursday_table.columnCount() - 2):
            try:
                row.append(self.thursday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO timetable (week, day, subject, full_name, room_numb, start_time) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (row[1], row[2], row[3], row[4], row[5], row[6]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _change_from_friday_table(self, rowNum):
        row = list()
        for i in range(self.friday_table.columnCount()-2):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE timetable SET week=%s, day=%s, subject=%s, full_name=%s, room_numb=%s, "
                                "start_time=%s WHERE id=%s", (row[1], row[2], row[3], row[4], row[5], row[6], row[0]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _add_to_friday_table(self, rowNum):
        row = list()
        for i in range(self.friday_table.columnCount()-2):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO timetable (week, day, subject, full_name, room_numb, start_time) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (row[1], row[2], row[3], row[4], row[5], row[6]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
#метод, обновляющий все таблицы на выбранной вкладке
    def _update_schedule(self):
        self._update_monday_table()
        self._update_tuesday_table()
        self._update_wednesday_table()
        self._update_thursday_table()
        self._update_friday_table()
#Вкладка с таблицей учителей
    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")
        self.teacher_gbox = QGroupBox("Teachers")
        self.tvbox = QVBoxLayout()
        self.thbox1 = QHBoxLayout()
        self.thbox2 = QHBoxLayout()
        self.tvbox.addLayout(self.thbox1)
        self.tvbox.addLayout(self.thbox2)
        self.thbox1.addWidget(self.teacher_gbox)
        self._create_teacher_table()
        self.update_teacher_button = QPushButton("Update")
        self.thbox2.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._update_teacher)
        self.teacher_tab.setLayout(self.tvbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teacher_table.setColumnCount(5)
        self._update_teacher_table()
        self.teacherbox = QVBoxLayout()
        self.teacherbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.teacherbox)
#метод для обновления таблицы с учителями
    def _update_teacher_table(self):
        self.teacher_table.clear()
        self.teacher_table.setHorizontalHeaderLabels(["Id", "Full name", "Subject", " ", " "])
        self.cursor.execute("SELECT * FROM teacher ORDER BY id")
        records = list(self.cursor.fetchall())
        self.teacher_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.teacher_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, joinButton)
            self.teacher_table.setCellWidget(i, 4, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_from_teacher_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_teacher(num))
        i+=1
        joinButton = QPushButton("Join")
        self.teacher_table.setCellWidget(i, 3, joinButton)
        joinButton.clicked.connect(lambda ch, num=i: self._add_to_teacher_table(num))
        self.teacher_table.resizeRowsToContents()

    def _change_from_teacher_table(self, rowNum):
        row = list()
        for i in range(self.teacher_table.columnCount()-2):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE teacher SET full_name=%s, subject=%s WHERE id=%s", (row[1], row[2], row[0]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()

    def _add_to_teacher_table(self, rowNum):
        row = list()
        for i in range(self.teacher_table.columnCount()-2):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO teacher (full_name, subject) VALUES (%s, %s)", (row[1], row[2]))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()

    def _delete_from_teacher(self, rowNum):
        row = self.teacher_table.item(rowNum, 0).text()
        self.cursor.execute("DELETE FROM teacher WHERE id=%s", [row])
        self.conn.commit()

    def _update_teacher(self):
        self._update_teacher_table()

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")
        self.subject_gbox = QGroupBox("Subjects")
        self.sbvbox = QVBoxLayout()
        self.sbhbox1 = QHBoxLayout()
        self.sbhbox2 = QHBoxLayout()
        self.sbvbox.addLayout(self.sbhbox1)
        self.sbvbox.addLayout(self.sbhbox2)
        self.sbhbox1.addWidget(self.subject_gbox)
        self._create_subject_table()
        self.update_subject_button = QPushButton("Update")
        self.sbhbox2.addWidget(self.update_subject_button)
        self.update_subject_button.clicked.connect(self._update_subject)
        self.subject_tab.setLayout(self.sbvbox)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subject_table.setColumnCount(3)
        self._update_subject_table()
        self.subjectbox = QVBoxLayout()
        self.subjectbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.subjectbox)

    def _update_subject_table(self):
        self.subject_table.clear()
        self.subject_table.setHorizontalHeaderLabels(["Name", " ", " "])
        self.cursor.execute("SELECT * FROM subject")
        records = list(self.cursor.fetchall())
        self.subject_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.subject_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.subject_table.setCellWidget(i, 1, joinButton)
            self.subject_table.setCellWidget(i, 2, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, arg=str(r[0]): self._change_from_subject_table(num, arg))
            deleteButton.clicked.connect(lambda ch, arg=str(r[0]): self._delete_from_subject(arg))
        i+=1
        joinButton = QPushButton("Join")
        self.subject_table.setCellWidget(i, 1, joinButton)
        joinButton.clicked.connect(lambda ch, num=i: self._add_to_subject_table(num))
        self.subject_table.resizeRowsToContents()

    def _change_from_subject_table(self, rowNum, arg):
        row = list()
        for i in range(self.subject_table.columnCount()-2):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name=%s WHERE name=%s", (row[0], arg))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()

    def _add_to_subject_table(self, rowNum):
        row = list()
        for i in range(self.subject_table.columnCount()-2):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO subject (name) VALUES (%s)", (row[0],))
        except:
            QMessageBox.about(self, "Error", "Check the fields input")
        self.conn.commit()
    def _update_subject(self):
        self._update_subject_table()
    def _delete_from_subject(self, rowNum):
        self.cursor.execute("DELETE FROM subject WHERE name=%s", [rowNum])
        self.conn.commit()

    def _delete_from_monday_table(self, rowNum):
        row = self.monday_table.item(rowNum, 0).text()
        self.cursor.execute("DELETE FROM timetable WHERE id=%s", [row])
        self.conn.commit()
    def _delete_from_tuesday_table(self, rowNum):
        row = self.tuesday_table.item(rowNum, 0).text()
        self.cursor.execute("DELETE FROM timetable WHERE id=%s", [row])
        self.conn.commit()
    def _delete_from_wednesday_table(self, rowNum):
        row = self.wednesday_table.item(rowNum, 0).text()
        self.cursor.execute("DELETE FROM timetable WHERE id=%s", [row])
        self.conn.commit()
    def _delete_from_thursday_table(self, rowNum):
        row = self.thursday_table.item(rowNum, 0).text()
        self.cursor.execute("DELETE FROM timetable WHERE id=%s", [row])
        self.conn.commit()
    def _delete_from_friday_table(self, rowNum):
        row = self.friday_table.item(rowNum, 0).text()
        self.cursor.execute("DELETE FROM timetable WHERE id=%s", [row])
        self.conn.commit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

