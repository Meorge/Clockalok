# A window test.

import os
import struct
import sys
import traceback
from analogclock import AnalogClock

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
Qt = QtCore.Qt

import TPLLib


class Window(QtWidgets.QMainWindow):
    """Main Window"""
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        global stopwatchInProgress, timerInProgress
        stopwatchInProgress = False
        timerInProgress = False
        
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)

        self.stopwatchCount = QtWidgets.QLabel('00:00.0000')
        self.stopwatchCount.setAlignment(Qt.AlignHCenter)
        self.stopwatchButton = QtWidgets.QPushButton('Start')
        self.stopwatchButton_Stop = QtWidgets.QPushButton('Clear')
        
        self.stopwatchButton_Lap = QtWidgets.QPushButton('Add Lap')
        self.stopwatchButton_Lap.setEnabled(False)
        self.stopwatchButton_Lap.clicked.connect(self.addLap)
        self.lapCount = QtWidgets.QTreeWidget()
        self.lapCount.setHeaderLabels(['#', 'Time'])
        self.lapCount.header().setStretchLastSection(True)
        
        self.stopwatchButton_Stop.clicked.connect(self.clearStopwatch)
        
        self.stopwatchLayout = QtWidgets.QVBoxLayout()
        self.stopwatchLayout.addWidget(self.stopwatchCount)
        self.stopwatchLayout.addWidget(self.stopwatchButton)
        self.stopwatchLayout.addWidget(self.stopwatchButton_Stop)
            
        self.stopwatchLayout.addWidget(self.stopwatchButton_Lap)
        self.stopwatchLayout.addWidget(self.lapCount)
        
        self.stopwatchLW = QtWidgets.QWidget()
        self.stopwatchLW.setLayout(self.stopwatchLayout)
        self.tabWidget.addTab(self.stopwatchLW, 'Stopwatch')
        
        
        
        #### timer
        self.timerCount = QtWidgets.QLabel('00:00.0000')
        
        self.minuteSpin = QtWidgets.QSpinBox()
        self.minuteSpinLabel = QtWidgets.QLabel(' minutes')
        
        self.secondSpin = QtWidgets.QSpinBox()
        self.secondSpinLabel = QtWidgets.QLabel(' seconds')
        
        
        self.spinnerLayout = QtWidgets.QGridLayout()
        self.spinnerLayout.addWidget(self.minuteSpin, 0,0)
        self.spinnerLayout.addWidget(self.minuteSpinLabel, 0,1)
        self.spinnerLayout.addWidget(self.secondSpin, 1,0)
        self.spinnerLayout.addWidget(self.secondSpinLabel, 1,1)
        
        self.spinnerLW = QtWidgets.QWidget()
        self.spinnerLW.setLayout(self.spinnerLayout)
        
        self.timerBar = QtWidgets.QProgressBar()
        self.timerCount.setAlignment(Qt.AlignHCenter)
        self.timerButton = QtWidgets.QPushButton('Start')
        self.timerButton.clicked.connect(self.startTimer)
        
        self.timerLayout = QtWidgets.QVBoxLayout()
        self.timerLayout.addWidget(self.timerCount)
        self.timerLayout.addWidget(self.spinnerLW)
        self.timerLayout.addWidget(self.timerBar)
        self.timerLayout.addWidget(self.timerButton)
        
        self.timerW = QtWidgets.QWidget()
        self.timerW.setLayout(self.timerLayout)
        self.tabWidget.addTab(self.timerW, 'Timer')
        
        
        #### clock
        self.clockWidget = AnalogClock()
        self.timeLabel = QtWidgets.QLabel('Getting the time...')
        self.timeLabel.setAlignment(Qt.AlignHCenter)
        #self.clockWidget.setAlignment(Qt.AlignTop)
        
        
        self.clockLayout = QtWidgets.QVBoxLayout()
        self.clockLayout.addWidget(self.clockWidget)
        self.clockLayout.addWidget(self.timeLabel)
        #self.clockLayout.setAlignment(self.clockWidget, Qt.AlignHCenter)
        self.clockLW = QtWidgets.QWidget()
        self.clockLW.setLayout(self.clockLayout)
        
        self.tabWidget.addTab(self.clockLW, 'Clock')
        self.clockWidget.setMaximumWidth(200)
        
        
        self.stopwatchButton.clicked.connect(self.startStopwatch)
        
        
        self.stopwatchCount.setStyleSheet('QLabel {font-weight: 100; font-size: 40px;}')
        self.timerCount.setStyleSheet('QLabel {font-weight: 100; font-size: 40px;}')
        self.timeLabel.setStyleSheet('QLabel {font-weight: 100; font-size: 35px;}')

        self.millisecondTimer = QtCore.QTimer()
        self.millisecondTimer.setSingleShot(False)
        self.millisecondTimer.setTimerType(Qt.PreciseTimer)
        self.millisecondTimer.timeout.connect(self.updateMilliseconds)
    
    
        self.millisecondTimer_T = QtCore.QTimer()
        self.millisecondTimer_T.setSingleShot(False)
        self.millisecondTimer_T.setTimerType(Qt.PreciseTimer)
        self.millisecondTimer_T.timeout.connect(self.updateMilliseconds_T)
    
    
        self.clockTimer = QtCore.QTimer()
        self.clockTimer.setSingleShot(False)
        self.clockTimer.setTimerType(Qt.PreciseTimer)
        self.clockTimer.timeout.connect(self.updateClocks)
        self.clockTimer.start(1)

    def updateClocks(self):
        hour = QtCore.QTime.currentTime().hour()
        if hour > 12:
            hour = hour - 12
            tod = 'PM'
        else:
            tod = 'AM'
        minute = QtCore.QTime.currentTime().minute()
        self.timeLabel.setText(str(hour) + ':' + str(minute) + ' ' + tod)
        self.clockWidget.update()


    def startTimer(self):
        global timerInProgress, minutesLeft, secondsLeft, millisecondsLeft, millisecondCounter
        if not timerInProgress:
            minutesLeft = self.minuteSpin.value()
            minutesLeft_MS = self.minutesToMilliseconds(minutesLeft)
            
            secondsLeft = self.secondSpin.value()
            secondsLeft_MS = self.secondsToMilliseconds(secondsLeft)
            
            
            totalMS = minutesLeft_MS + secondsLeft_MS
            self.timerBar.setRange(0, totalMS)
            self.millisecondTimer_T.start(1)
            timerInProgress = True
            self.timerButton.setText('Stop')
        else:
            self.millisecondTimer_T.stop()
            self.timerBar.setValue(0)
            minutesLeft, secondsLeft, millisecondsLeft, millisecondCounter = 0,0,0,0
            timerInProgress = False
            self.timerCount.setText('00:00.0000')
            self.timerButton.setText('Start')
    
    
    def startStopwatch(self):
        global stopwatchInProgress
        if not stopwatchInProgress:
            self.millisecondTimer.start(1)
            stopwatchInProgress = True
            self.stopwatchButton.setText('Pause')
            self.stopwatchButton_Stop.setEnabled(False)
            self.stopwatchButton_Lap.setEnabled(True)
            self.stopwatchButton_Lap.setText('Add Lap')
        else:
            self.millisecondTimer.stop()
            stopwatchInProgress = False
            self.stopwatchButton.setText('Resume')
            self.stopwatchButton_Lap.setEnabled(True)
            self.stopwatchButton_Stop.setEnabled(True)
            self.stopwatchButton_Lap.setText('Clear Laps')

    def clearStopwatch(self):
        global minutes, seconds, milliseconds
        self.millisecondTimer.stop()
        self.stopwatchCount.setText('00:00.0000')
        minutes, seconds, milliseconds = 0,0,0
        stopwatchInProgress = False
        self.stopwatchButton.setText('Start')
    
    def addLap(self):
        global numberoflaps
        if stopwatchInProgress:
            numberoflaps += 1
            newLapItem = QtWidgets.QTreeWidgetItem()
            newLapItem.setText(0, str(numberoflaps))
            newLapItem.setText(1, self.stopwatchCount.text())
            self.lapCount.addTopLevelItem(newLapItem)
        elif not stopwatchInProgress:
            self.lapCount.clear()
            numberoflaps = 0
        
    def updateMilliseconds(self):
        global minutes, seconds, milliseconds
        milliseconds = int(milliseconds) + 1
        if int(milliseconds) > 1000:
            milliseconds = 00
            seconds = int(seconds) + 1
            if int(seconds) == 60:
                seconds = 0
                minutes = int(minutes) + 1

        if int(minutes) < 10: minutes = '0' + str(int(minutes))
        if int(seconds) < 10: seconds = '0' + str(int(seconds))
        if int(milliseconds) < 10: milliseconds = '000' + str(int(milliseconds))
        elif int(milliseconds) < 100 and int(milliseconds) > 10: milliseconds = '00' + str(int(milliseconds))
        elif int(milliseconds) < 1000 and int(milliseconds) > 100: milliseconds = '0' + str(int(milliseconds))

        self.stopwatchCount.setText(str(minutes) + ':' + str(seconds) + '.' + str(milliseconds))


    def updateMilliseconds_T(self):
        global minutesLeft, secondsLeft, millisecondsLeft, millisecondCounter
        millisecondCounter += 1

        self.timerBar.setValue(millisecondCounter)
        #print(str(minutesLeft) + ' minutes left\n' + str(secondsLeft) + ' seconds left\n' + str(millisecondsLeft) + ' milliseconds left\n\n')
        millisecondsLeft = int(millisecondsLeft) - 1
        if int(millisecondsLeft) < 0:
            millisecondsLeft = 999
            secondsLeft = int(secondsLeft) - 1
            if int(secondsLeft) < 0:
                secondsLeft = 59
                minutesLeft = int(minutesLeft) - 1
                if int(minutesLeft) < 0:
                    minutesLeft = 0

        if int(minutesLeft) < 10: minutesLeft = '0' + str(int(minutesLeft))
        if int(secondsLeft) < 10: secondsLeft = '0' + str(int(secondsLeft))
        if int(millisecondsLeft) < 10: millisecondsLeft = '000' + str(int(millisecondsLeft))
        elif int(millisecondsLeft) < 100 and int(millisecondsLeft) > 10: millisecondsLeft = '00' + str(int(millisecondsLeft))
        elif int(millisecondsLeft) < 1000 and int(millisecondsLeft) > 100: millisecondsLeft = '0' + str(int(millisecondsLeft))

        self.timerCount.setText(str(minutesLeft) + ':' + str(secondsLeft) + '.' + str(millisecondsLeft))

        if self.timerCount.text() == '00:00.0000': self.alarmForFinishedTimer()

    def alarmForFinishedTimer(self):
        global minutesLeft, secondsLeft, millisecondsLeft, millisecondCounter
        self.millisecondTimer_T.stop()
    
        self.timerMSG = QtWidgets.QMessageBox()
        self.timerMSG.setText('The timer has completed.')
        QtMultimedia.QSound.play('submarine.wav')
        minutesLeft, secondsLeft, millisecondsLeft, millisecondCounter = 0,0,0,0
        self.timerBar.setValue(0)
        self.timerMSG.exec_()


    def minutesToMilliseconds(self, minutes):
        return minutes * 60000

    def secondsToMilliseconds(self, seconds):
        return seconds * 1000

if __name__ == '__main__':
    global app, window
    global minutes, seconds, milliseconds
    global minutesLeft, secondsLeft, millisecondsLeft, millisecondCounter
    global numberoflaps
    minutes, seconds, milliseconds = 0,0,0
    minutesLeft, secondsLeft, millisecondsLeft, millisecondCounter = 0,0,0,0
    numberoflaps = 0
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec_())

    
