#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel,QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPixmap, QImage, QIcon, QColor

import killbots
import numpy



square_size = 40

class Killapp(QWidget, killbots.killbots):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("images/bot.png"))
        self.initUI()

    def initUI(self):      
        self.IMG_BOT = QPixmap("images/bot.png")
        self.IMG_FASTBOT = QPixmap("images/fastbot.png")
        self.IMG_HERO = QPixmap("images/hero.png")
        self.IMG_JUNK = QPixmap("images/junk.png")
        
        top_bar = QHBoxLayout()
 

        self.text_energy = "Energy : "+ str(self.energy)
        self.label_energy = QLabel(self.text_energy, self)
        top_bar.addWidget(self.label_energy, Qt.AlignTop)       


        b_bot = QPushButton(QtGui.QIcon("images/hero.png"),"")
        top_bar.addWidget(b_bot, Qt.AlignTop)

        
        self.text_score = "Score : 0"
        self.label_score = QLabel(self.text_score, self)
        top_bar.addWidget(self.label_score, Qt.AlignTop)          


        grid = QVBoxLayout(self)
        grid.addLayout(top_bar)
        
        self.text_main = "main surface, ready \n to be ufllfd"
        self.label_main = QLabel(self.text_main, self)
        self.label_main.setFixedSize(self.col*square_size, self.row*square_size)
        grid.addWidget(self.label_main, Qt.AlignBottom)  



        move_bar = QHBoxLayout()

        b_ul = QPushButton(QtGui.QIcon("images/up_left.png"),"")
        b_u = QPushButton(QtGui.QIcon("images/up.png"),"")
        b_ur = QPushButton(QtGui.QIcon("images/up_right.png"),"")
        b_l = QPushButton(QtGui.QIcon("images/left.png"),"")
        b_r = QPushButton(QtGui.QIcon("images/right.png"),"")
        b_dl = QPushButton(QtGui.QIcon("images/down_left.png"),"")
        b_d = QPushButton(QtGui.QIcon("images/down.png"),"")
        b_dr = QPushButton(QtGui.QIcon("images/down_right.png"),"")
        b_w = QPushButton(QtGui.QIcon("images/wait.png"),"")
        b_t = QPushButton(QtGui.QIcon("images/teleport.png"),"")
        b_ts = QPushButton(QtGui.QIcon("images/teleport_safely.png"),"")
        b_n = QPushButton(QtGui.QIcon("images/do_nothing.png"),"")
        

        move_bar.addWidget(b_ul)
        #b_ul.clicked.connect(self.c_ul)
        move_bar.addWidget(b_u)
        move_bar.addWidget(b_ur)
        move_bar.addWidget(b_l)
        move_bar.addWidget(b_r)
        move_bar.addWidget(b_dl)
        move_bar.addWidget(b_d)
        move_bar.addWidget(b_dr)
        move_bar.addWidget(b_w)
        move_bar.addWidget(b_t)
        move_bar.addWidget(b_ts)
        move_bar.addWidget(b_n)
        

        grid.addLayout(move_bar)
        """

        9 = wait
        10 = teleport
        11 = teleport safely
        12 = do nothing 
        """
        
        self.setLayout(grid)
        
        self.setGeometry(50, 50, 350, 200)
        self.setWindowTitle('kILL BOTS')
        self.show()




    def paintEvent(self, event):
        painter = QPainter(self)
        #p.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0x000000))

        
        rec = self.label_main.geometry ()

        painter.fillRect(rec.x(), rec.y(), rec.width(), 
                         rec.height(), QColor(0x707070))

        #Tracer des col
        painter.drawLine(rec.x(), rec.y(), rec.x(), rec.y()+rec.height())
        dx = rec.width() // self.col #il peut manquer un pixel avec les divisions
        for i in range(self.col):
            j=i+1
            painter.drawLine(rec.x() + j*dx, rec.y(),
                             rec.x() + j*dx, rec.y()+rec.height())

        #Tracer des row
        painter.drawLine(rec.x(), rec.y(), rec.x() + rec.width(), rec.y())
        dy = rec.height() // self.col #il peut manquer un pixel avec les divisions
        for i in range(self.row):
            j=i+1
            painter.drawLine(rec.x(), rec.y() + j*dy,
                             rec.x() + rec.width(), rec.y() + j*dy)
            
        source = QRect(0,0,48,48)


        for i in range(self.row) :
            for j in range(self.col):
                if self.land[i][j] !=0 :
                    target = QRect(rec.x()+i*dx, rec.y()+j*dy, dx, dy)
                    if self.land[i][j] == 1 :
                        painter.drawPixmap(target, self.IMG_HERO, source)
                    if self.land[i][j] == 2 :
                        painter.drawPixmap(target, self.IMG_BOT, source)
                    if self.land[i][j] == 3 :
                        painter.drawPixmap(target, self.IMG_FASTBOT, source)
                    if self.land[i][j] == 4 :
                        painter.drawPixmap(target, self.IMG_JUNK, source)
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Killapp()
    sys.exit(app.exec_())
