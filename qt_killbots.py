#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel,QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPixmap, QImage, QIcon, QColor

import killbots
import numpy


class qt_killbots(killbots.killbots):
    
    def __init__(self, update):
        super().__init__()
        self.update= update()
        
    def update_display(self):
        self.update()


    
square_size = 40

class Killapp(QWidget):


    
    
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("images/bot.png"))
        self.killbots = qt_killbots(self.update)
        self.initUI()

    def initUI(self):      
        self.IMG_BOT = QPixmap("images/bot.png")
        self.IMG_FASTBOT = QPixmap("images/fastbot.png")
        self.IMG_HERO = QPixmap("images/hero.png")
        self.IMG_JUNK = QPixmap("images/junk.png")
        
        top_bar = QHBoxLayout()
 

        self.text_energy = "Energy : "+ str(self.killbots.energy)
        self.label_energy = QLabel(self.text_energy, self)
        top_bar.addWidget(self.label_energy, Qt.AlignTop)       


        b_bot = QPushButton(QtGui.QIcon("images/hero.png"),"")
        top_bar.addWidget(b_bot, Qt.AlignTop)
        b_bot.clicked.connect(self.c_reset)

        
        self.text_score = "Score : 0"
        self.label_score = QLabel(self.text_score, self)
        top_bar.addWidget(self.label_score, Qt.AlignTop)          


        grid = QVBoxLayout(self)
        grid.addLayout(top_bar)
        
        self.text_main = ""
        self.label_main = QLabel(self.text_main, self)
        self.label_main.setFixedSize(self.killbots.col*square_size, self.killbots.row*square_size)
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


        b_ul.clicked.connect(self.c_ul)
        b_u.clicked.connect(self.c_u)
        b_ur.clicked.connect(self.c_ur)
        b_l.clicked.connect(self.c_l)
        b_r.clicked.connect(self.c_r)
        b_dl.clicked.connect(self.c_dl)
        b_d.clicked.connect(self.c_d)
        b_dr.clicked.connect(self.c_dr)
        b_w.clicked.connect(self.c_w)
        b_t.clicked.connect(self.c_t)
        b_ts.clicked.connect(self.c_ts)
        b_n .clicked.connect(self.c_n)
        

        grid.addLayout(move_bar)

        
        self.setLayout(grid)
        
        self.setGeometry(50, 50, 350, 200)
        self.setWindowTitle('kILL BOTS')
        self.show()

    def make_action(self, action):
        #Test move ??
        res = self.killbots.action(action)
        if res == 2:
            self.killbots.populate()
        #Check dead
        self.update()
        

    def c_ul(self): self.make_action(0)
    def c_u(self): self.make_action(1)
    def c_ur(self): self.make_action(2)
    def c_l(self): self.make_action(3)
    def c_r(self): self.make_action(5)
    def c_dl(self): self.make_action(6)
    def c_d(self): self.make_action(7)
    def c_dr(self): self.make_action(8)
    def c_w(self): self.make_action(9)
    def c_t(self): self.make_action(10)
    def c_ts(self): self.make_action(11)
    def c_n(self): self.make_action(12)
        
    def c_reset(self):
        self.killbots.__init__(self.update)
        self.update()

    
    def paintEvent(self, event):
        painter = QPainter(self)
        #p.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0x000000))

        
        rec = self.label_main.geometry ()

        painter.fillRect(rec.x(), rec.y(), rec.width(), 
                         rec.height(), QColor(0x707070))

        #Tracer des col
        painter.drawLine(rec.x(), rec.y(), rec.x(), rec.y()+rec.height())
        dx = rec.width() // self.killbots.col #il peut manquer un pixel avec les divisions
        for i in range(self.killbots.col):
            j=i+1
            painter.drawLine(rec.x() + j*dx, rec.y(),
                             rec.x() + j*dx, rec.y()+rec.height())

        #Tracer des row
        painter.drawLine(rec.x(), rec.y(), rec.x() + rec.width(), rec.y())
        dy = rec.height() // self.killbots.row #il peut manquer un pixel avec les divisions
        for i in range(self.killbots.row):
            j=i+1
            painter.drawLine(rec.x(), rec.y() + j*dy,
                             rec.x() + rec.width(), rec.y() + j*dy)
            
        source = QRect(0,0,48,48)


        for i in range(self.killbots.row) :
            for j in range(self.killbots.col):
                if self.killbots.land[i][j] !=0 :
                    target = QRect(rec.x()+j*dx, rec.y()+i*dy, dx, dy)
                    if self.killbots.land[i][j] == 1 :
                        painter.drawPixmap(target, self.IMG_HERO, source)
                    if self.killbots.land[i][j] == 2 :
                        painter.drawPixmap(target, self.IMG_BOT, source)
                    if self.killbots.land[i][j] == 3 :
                        painter.drawPixmap(target, self.IMG_FASTBOT, source)
                    if self.killbots.land[i][j] == 4 :
                        painter.drawPixmap(target, self.IMG_JUNK, source)

        self.text_energy = "Energy : "+ str(self.killbots.energy)
        self.label_energy.setText(self.text_energy)
        self.text_score = "Score : "+ str(self.killbots.score)
        self.label_score.setText(self.text_score)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Killapp()
    sys.exit(app.exec_())
