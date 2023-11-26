import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class DatabaseHandler(QDialog):
    def __init__(self):
        super(DatabaseHandler, self).__init__()
        uic.loadUi("add_coffee.ui", self)

    def accept(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('INSERT INTO coffee(Name, Variety, Roasting, Description, Price, Size) VALUES (?,?,?,?,?,?)',
                    [self.NameLineEdit.text(), self.RoastingLineEdit.text(), self.TypeLineEdit.text(),
                     self.TasteLineEdit.text(), self.PriceLineEdit.text(), self.SizeLineEdit.text()])
        con.commit()
        con.close()
        self.done(1)

    def reject(self):
        self.done(0)


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        uic.loadUi("main.ui", self)
        self.table()
        self.addInfoButton.clicked.connect(self.run)

    def run(self):
        Database = DatabaseHandler()
        Database.show()
        Database.exec()
        self.table()

    def table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        db = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setColumnCount(len(db[0]) - 1)
        self.tableWidget.setRowCount(len(db))
        self.tableWidget.setHorizontalHeaderLabels(
            ["Название сорта", "Степень обжарки", "Молотый/В зернах", "Описание вкуса", "Цена", "Объем упаковки"])
        for x, element1 in enumerate(db):
            for j, element2 in enumerate(element1[1:]):
                self.tableWidget.setItem(x, j, QTableWidgetItem(element2))
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = Example()
    example.show()
    sys.exit(app.exec())
