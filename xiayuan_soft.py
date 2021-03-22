import json
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import sys

import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QPushButton, QComboBox
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import random

from initdata import Data, PATH_LIST, __data_len__
from ui import Ui_MainWindow

matplotlib.use("Qt5Agg")


class Graph(QMainWindow, Ui_MainWindow):
    def __init__(self):

        #integrate pyqt
        super(Graph, self).__init__()

        # initialize pyqtui
        self.setupUi(self)
        self.setWindowTitle("Main Window")
        self.setMinimumSize(0, 0)

        # Initialize random data
        self.data = Data.init_data()

        # Set the number of questions to 0
        self.question_index = 0

    def closewin(self):
        self.close()


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'healthcare pathway visualization system'
        self.width = 1200
        self.height = 800
        self.initUI()

    def start_timing(self):
            self.m.start_time = datetime.now()

    def closewin(self):
        self.close()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(5, 5)
        self.m = PlotCanvas(self, width=8, height=7)
        self.m.move(0, 0)

        button = QPushButton('next', self)
        button.setToolTip('next')
        button.move(1000, 200)
        button.resize(140, 30)
        button.clicked.connect(self.nextClick)

        button = QPushButton('previous', self)
        button.setToolTip('previous')
        button.move(860, 200)
        button.resize(140, 30)
        button.clicked.connect(self.prveClick)

        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(160, 610, 59, 30))
        label.setObjectName("label")
        label.setText("Answer：")
        label.move(860, 120)

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(220, 600, 201, 26))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 81))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.clear()
        self.comboBox.addItems(PATH_LIST)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.setCurrentText('')
        self.comboBox.move(920, 120)
        self.show()

    def prveClick(self):
        if self.m.question_index > 0:
            self.m.question_index = self.m.question_index - 1
            print(self.m.question_index)
            self.m.show_image()

    def nextClick(self):
        if self.m.question_index < __data_len__:
            # Check if the answer is selected
            if self.comboBox.currentIndex() == -1 and len(self.comboBox.currentText()) == 0:
                messagebox.showinfo("Remind", "Please select an answer.")
                return
            self.m.show_image()
        else:
            # If the index of the problem is maximized. Then answer all the questions
            if self.m.question_index >= __data_len__:
                # Calculate Time
                cost = (datetime.now() - self.m.start_time).seconds
                # The path selected by the user
                select_path = self.comboBox.currentText()
                # Get the data from the last problem
                last_data = self.m.data[self.m.question_index - 1]
                # Iterate through the data of the previous problem
                # Find the option selected by the user, and assign the value
                for item in last_data:
                    if item['path_name'] == select_path:
                        item['select'] = True
                        item['cost'] = cost
                # Save the data selected by the user
                self.m.data[self.m.question_index - 1] = last_data
                messagebox.askyesno("Thanks", "The experiment is complete, thanks for participating.")
                json_str = json.dumps(self.m.data, indent=4)
                txt = "selectResult" + str(datetime.now().strftime('%Y%m%d%H%M%S')) + ".json"
                with open(txt, 'w') as f:
                    f.write(json_str)
                return

        # Calculate Time
        cost = (datetime.now() - self.m.start_time).seconds
        # Repeat start time
        self.m.start_time = datetime.now()
        # The path selected by the user
        select_path = self.comboBox.currentText()
        # Get the data from the last problem
        last_data = self.m.data[self.m.question_index - 1]
        # Iterate through the data of the previous problem
        # Find the option selected by the user, and assign the value
        for item in last_data:
            if item['path_name'] == select_path:
                item['select'] = True
                item['cost'] = cost
        # Save the data selected by the user
        self.m.data[self.m.question_index - 1] = last_data
        # Prepare the next number
        self.m.question_index = self.m.question_index + 1
        # Clear the content already selected in ComboBox
        self.comboBox.clear()
        self.comboBox.addItems(PATH_LIST)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.setCurrentText('')


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        # Initialize random data
        self.data = Data.init_data()

        # Set the number of questions to 0
        self.question_index = 0

        self.start_time = datetime.now()

        self.color_list = ['#88CCEE', '#CC6677', '#DDCC77', '#117733', '#332288', '#AA4499', '#44AA99', '#999933',
                           '#661100', '#6699CC', '#888888']

        self.color_list2 = ['#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF',
                            '#FFFFFF', '#FFFFFF', '#FFFFFF']

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.show_image()
        self.question_index = 1

    def test(self):
        self.fig.clf()
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def draw_bar1(self, x, y):
        """
        1. A bar chart with the same color and labeled without data.
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('1.The cost of patients choosing different pathways')
        self.axes.barh(x, y)
        font_size = 6
        self.axes.tick_params(labelsize=font_size)
        self.draw()

    def draw_bar2(self, x, y):
        """
        2. A bar chart with different colors and labeled with each data.
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('2.The cost of patients choosing different pathways')
        self.axes.barh(x, y, color=self.color_list)
        font_size = 6
        self.axes.tick_params(labelsize=font_size)
        b = self.axes.barh(x, y, color=self.color_list)
        for rect in b:
            w = rect.get_width()
            self.axes.text(w, rect.get_y() + rect.get_height() / 2, '%d' % int(w), ha='left', va='center')
        self.draw()

    def draw_bar3(self, x, y):
        """
        3.A bar charts with different colors without labeled data
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('3.The cost of patients choosing different pathways')
        self.axes.barh(x, y, color=self.color_list)
        font_size = 6
        self.axes.tick_params(labelsize=font_size)
        self.draw()

    def draw_pie4(self, x, y):
        """
        4.Pie chart with different colors without data (legend)
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('4.The cost of a single path as a percentage of the cost of 11 paths')
        self.axes.pie(y, labels=None, colors=self.color_list)
        self.axes.legend(x, loc="best", fontsize=7, bbox_to_anchor=(0.1, 1))
        self.draw()

    def draw_pie5(self, x, y):
        """
        5.Pie chart with different colors with data (legend)
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('5.The cost of a single path as a percentage of the cost of 11 paths')
        self.axes.pie(y, labels=y, colors=self.color_list)
        self.axes.legend(x, loc="best", fontsize=7, bbox_to_anchor=(0.1, 1))
        self.draw()

    def draw_pie6(self, x, y):
        """
        6.Pie chart without colors
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('6.The cost of a single path as a percentage of the cost of 11 paths')
        self.axes.pie(y, labels=x, colors=self.color_list2, wedgeprops={'linewidth': 3, "edgecolor": "black"})
        plt.legend(x, loc="best", fontsize=10, bbox_to_anchor=(0.1, 1))
        self.draw()

    def draw_column7(self, x, y):
        """
        7.Same color column chart with data
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('7.The cost of patients choosing different pathways')
        self.axes.bar(x, y)
        font_size = 8
        self.axes.tick_params(labelsize=font_size)
        for label in self.axes.get_xticklabels():
            label.set_rotation(15)
            label.set_horizontalalignment('right')
        for a, b in zip(x, y):
            self.axes.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
        self.draw()

    def draw_column8(self, x, y):
        """
        8.Different color column chart with data
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes.cla()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('8.The cost of patients choosing different pathways')
        self.axes.bar(x, y, color=self.color_list)
        font_size = 8
        self.axes.tick_params(labelsize=font_size)
        for label in self.axes.get_xticklabels():
            label.set_rotation(15)
            label.set_horizontalalignment('right')

        for a, b in zip(x, y):
            self.axes.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
        self.draw()

    def draw_column9(self, x, y):
        """
        9.Different color column chart without data
        :param x:
        :param y:
        :return:
        """
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('9.The cost of patients choosing different pathways')
        self.axes.bar(x, y, color=self.color_list)
        font_size = 8
        self.axes.tick_params(labelsize=font_size)
        for label in self.axes.get_xticklabels():
            label.set_rotation(15)
            label.set_horizontalalignment('right')
        self.draw()

    def show_image(self):
        x = []
        y = []
        # Take out the initialized data, and take out the X axis, Y axis data
        for item in self.data[self.question_index]:
            x.append(item['path_name'])
            y.append(item['path_cost'])

        # Determine the current number of the problem, and output the corresponding graph
        if self.question_index == 0:
            self.draw_bar1(x, y)
        if self.question_index == 1:
            self.draw_bar2(x, y)
        if self.question_index == 2:
            self.draw_bar3(x, y)
        if self.question_index == 3:
            self.draw_pie4(x, y)
        if self.question_index == 4:
            self.draw_pie5(x, y)
        if self.question_index == 5:
            self.draw_pie6(x, y)
        if self.question_index == 6:
            self.draw_column7(x, y)
        if self.question_index == 7:
            self.draw_column8(x, y)
        if self.question_index == 8:
            self.draw_column9(x, y)


if __name__ == "__main__":
    tk = Tk()
    tk.withdraw()
    app = QApplication(sys.argv)
    main = Graph()
    child = App()
    main.show()
    child.closewin()

    main.pushButton_2.clicked.connect(main.closewin)
    main.pushButton_2.clicked.connect(child.start_timing)
    main.pushButton_2.clicked.connect(child.show)

    sys.exit(app.exec_())
