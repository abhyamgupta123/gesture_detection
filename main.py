import sys, os
import serial
import serial.tools.list_ports                  # this is for detecting avaiable ports
import keyboard
# importing for GUI:-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import gestureui

from time import sleep

class gestureUIHandler(gestureui.Ui_MainWindow, QtWidgets.QMainWindow, QtWidgets.QDialog):
    def __init__(self):
        self.ports = {"avaiable_ports": 0,
                      "ports_list": []
                      }
        self.final_port = None
        self.gestures = {"up":{"enabled":False, "type":None, "value":None},
                         "down":{"enabled":False, "type":None, "value":None},
                         "left":{"enabled":False, "type":None, "value":None},
                         "right":{"enabled":False, "type":None, "value":None},
                         "far":{"enabled":False, "type":None, "value":None},
                         "near":{"enabled":False, "type":None, "value":None},
                         }

    def buttons(self):
        self.rd_up_k.toggled.connect(lambda: self.btnstate(self.rd_up_k, self.up_k))
        self.rd_up_a.toggled.connect(lambda: self.btnstate(self.rd_up_a, self.up_a))
        self.rd_down_k.toggled.connect(lambda: self.btnstate(self.rd_down_k, self.down_k))
        self.rd_down_a.toggled.connect(lambda: self.btnstate(self.rd_down_a, self.down_a))
        self.rd_left_k.toggled.connect(lambda: self.btnstate(self.rd_left_k, self.left_k))
        self.rd_left_a.toggled.connect(lambda: self.btnstate(self.rd_left_a, self.left_a))
        self.rd_right_k.toggled.connect(lambda: self.btnstate(self.rd_right_k, self.right_k))
        self.rd_right_a.toggled.connect(lambda: self.btnstate(self.rd_right_a, self.right_a))
        self.rd_far_k.toggled.connect(lambda: self.btnstate(self.rd_far_k, self.far_k))
        self.rd_far_a.toggled.connect(lambda: self.btnstate(self.rd_far_a, self.far_a))
        self.rd_near_k.toggled.connect(lambda: self.btnstate(self.rd_near_k, self.near_k))
        self.rd_near_a.toggled.connect(lambda: self.btnstate(self.rd_near_a, self.near_a))

        # setting triggeres for buttons:-
        self.runbtn.clicked.connect(lambda: self.buttonacions('run'))
        self.stopbtn.clicked.connect(lambda: self.buttonacions('stop'))


        # setting actions for actionbuttons:-
        self.actionClose.triggered.connect(lambda: self.quit())
        self.actionRefreshlist.triggered.connect(lambda: self.refresh_ports())
        self.actionPort1.triggered.connect(lambda: self.set_port())
        self.actionRun.triggered.connect(lambda: self.buttonacions('run'))
        self.actionStop.triggered.connect(lambda: self.buttonacions('stop'))


    def refresh_ports(self):
        avail_ports = list(serial.tools.list_ports.comports())
        self.ports["avaiable_ports"] = len(avail_ports)
        for port in avail_ports:
            self.ports["ports_list"].append(port)

        # now showing avaiable ports:-
        if(self.ports["avaiable_ports"] == 0):
            self.actionPort1.setText(self.translateui("MainWindow", "No available Devices"))
        elif(self.ports["avaiable_ports"] == 1):
            self.actionPort1.setText(self.translateui("MainWindow", str(self.ports["ports_list"][0])))
        else:
            self.actionPort1.setText(self.translateui("MainWindow", "More then 1 ports available"))

    def set_port(self):
        if(self.ports["avaiable_ports"] == 1):
            self.final_port = str(self.ports["ports_list"][0]).split("-")[0].lstrip().rstrip()                    # as the format of port is like - /dev/tty0-USBSerial1.0
            self.change_portactionName(self.final_port + "(Selected)")                                            # setting the final port

    def btnstate(self, btn, box):
        if (btn.isChecked()):
            box.setEnabled(True)
        else:
            box.setEnabled(False)

    def register_logs(self, log_value):
        self.textEdit.append(str(log_value))

    def proccess_commands(self, lineEditBox, input_type, name, gesture):
        if(lineEditBox.isEnabled()):
            if(lineEditBox.text().rstrip().lstrip() != ""):
                # Handle keyboard press
                self.gestures[gesture]["enabled"] = True
                self.gestures[gesture]["type"] = input_type
                self.gestures[gesture]["value"] = str(lineEditBox.text())
                # print("{} is enabled".format(name))
                self.register_logs("{} is enabled".format(name))                                                    # registering log
            else:
                if(not (self.gestures[gesture]["enabled"])):
                    self.gestures[gesture]["enabled"] = False
                    # print("{} is empty hence not running gesture".format(name))
                    self.register_logs("{} is empty hence not running gesture".format(name))                        # registering log
        else:
            if(not (self.gestures[gesture]["enabled"])):
                self.gestures[gesture]["enabled"] = False
            # print("{} is not enabled".format(name))
            self.register_logs("{} is not enabled".format(name))                                                    # registering log

    def buttonacions(self, param):
        if(param == 'run'):
            # assign tasks on run:-
            # here passing all lineEdit objects to take it's entries and register the shortcuts values to dictionary
            self.proccess_commands(self.up_k, "keyboard_shortcut", "upward keyboard action", "up")
            self.proccess_commands(self.up_a, "application_shortcut", "upward application action", "up")
            self.proccess_commands(self.down_k, "keyboard_shortcut", "upward keyboard action", "down")
            self.proccess_commands(self.down_a, "application_shortcut", "upward application action", "down")
            self.proccess_commands(self.left_k, "keyboard_shortcut", "upward keyboard action", "left")
            self.proccess_commands(self.left_a, "application_shortcut", "upward application action", "left")
            self.proccess_commands(self.right_k, "keyboard_shortcut", "upward keyboard action", "right")
            self.proccess_commands(self.right_a, "application_shortcut", "upward application action", "right")
            self.proccess_commands(self.far_k, "keyboard_shortcut", "upward keyboard action", "far")
            self.proccess_commands(self.far_a, "application_shortcut", "upward application action", "far")
            self.proccess_commands(self.near_k, "keyboard_shortcut", "upward keyboard action", "near")
            self.proccess_commands(self.near_a, "application_shortcut", "upward application action", "near")
            # print(self.gestures)

            try:
                if(len(self.ports) >= 1 and self.final_port.lstrip().rstrip() != ""):
                    self.run_backend_thread()
                else:
                    # print("No port is selected, hence aborting..!!")
                    self.register_logs("No port is selected, hence aborting..!!")                                 # registering log
            except Exception as e:
                # print("Please refresh the ports list and select the desired device/port")
                self.register_logs("Please refresh the ports list and select the desired device/port")            # registering log
        else:
            # handle when user stops prograame:-
            self.runbtn.setEnabled(True)                                                                          # enabling the run button again
            self.backend_thread.exit_signal.emit("stop")
            pass

    def run_backend_thread(self):
        self.backend_thread = handlbackend(self.final_port, self.gestures)
        self.backend_thread.start()
        self.backend_thread.logs_signal.connect(lambda value: self.register_logs(value))
        self.runbtn.setEnabled(False)

    def quit(self):
        print("programme stopped")
        self.register_logs("programme stopped")                                                                   # registering log
        # sys.exit()
        QtCore.QCoreApplication.instance().quit()



class handlbackend(QThread, QRunnable):
    exit_signal = pyqtSignal(object)
    logs_signal = pyqtSignal(object)

    def __init__(self, port, gestures):
        super(handlbackend, self).__init__()
        self.port = port
        self.gestures = gestures

    def send_register_log(self, log_value):
        # print(log_value)
        self.logs_signal.emit(log_value)

    def connect_to_port(self):
        try:
            self.software_serial = serial.Serial(self.port, 9600)
            # if successfully connected to port then start detecting gestures and work accordingly:-
            # print("Gesture detection started running")
            # print("Successfully connected to port")
            # registering logs
            self.send_register_log("Gesture detection started running")
            self.send_register_log("Successfully connected to port")
            self.main()
        except Exception as e:
            # print("the port is not available!")
            # print(e)                                                                                              # handle to register error in logs
            # registering logs
            self.send_register_log("the port is not available!")
            self.send_register_log(e)

    def raise_exit_flag(self, flag):
        if flag == "stop":
            self.exit_flag = True


    def main(self):
        while True:
            if self.exit_flag == True:
                # print("Gesture detection stopped")
                self.send_register_log("Gesture detection stopped")
                break
            else:
                output = self.software_serial.readline().decode().rstrip()
                # print("OUTPUT: " + str(output))
                self.send_register_log("OUTPUT: " + str(output))
                if output == "LEFT":
                    # print("Left gesture performed")
                    self.send_register_log("Left gesture performed")
                    if (self.gestures["left"]["enabled"]):
                        if(self.gestures["left"]["type"] == "keyboard_shortcut"):
                            keyboard.press_and_release(self.gestures["left"]["value"])
                        elif(self.gestures["left"]["type"] == "application_shortcut"):
                            status_code = os.system(self.gestures["left"]["value"] + " &")
                            if status_code == 0:
                                # print("Command/application_shortcut for left gesture executed successfully")
                                self.send_register_log("Command/application_shortcut for left gesture executed successfully")
                            else:
                                # print("Failed to execute command/application_shortcut ")
                                self.send_register_log("Failed to execute command/application_shortcut ")
                        else:
                            # print("Shortcut for left gesture is not initialised correctly")
                            self.send_register_log("Shortcut for left gesture is not initialised correctly")
                    else:
                        # print("Shortcut for left gesture is not initialised.")
                        self.send_register_log("Shortcut for left gesture is not initialised.")

                elif output == "RIGHT":
                    # print("Right gesture performed")
                    self.send_register_log("Right gesture performed")
                    if (self.gestures["right"]["enabled"]):
                        if(self.gestures["right"]["type"] == "keyboard_shortcut"):
                            keyboard.press_and_release(self.gestures["right"]["value"])
                        elif(self.gestures["right"]["type"] == "application_shortcut"):
                            status_code = os.system(self.gestures["right"]["value"] + " &")
                            if status_code == 0:
                                # print("Command/application_shortcut for right gesture executed successfully")
                                self.send_register_log("Command/application_shortcut for right gesture executed successfully")
                            else:
                                # print("Failed to execute command/application_shortcut ")
                                self.send_register_log("Failed to execute command/application_shortcut ")
                        else:
                            # print("Shortcut for right gesture is not initialised correctly")
                            self.send_register_log("Shortcut for right gesture is not initialised correctly")
                    else:
                        # print("Shortcut for right gesture is not initialised.")
                        self.send_register_log("Shortcut for right gesture is not initialised.")

                elif output == "UP":
                    # print("Upward gesture performed")
                    self.send_register_log("Upward gesture performed")
                    if (self.gestures["up"]["enabled"]):
                        if(self.gestures["up"]["type"] == "keyboard_shortcut"):
                            keyboard.press_and_release(self.gestures["up"]["value"])
                        elif(self.gestures["up"]["type"] == "application_shortcut"):
                            status_code = os.system(self.gestures["up"]["value"] + " &")
                            if status_code == 0:
                                # print("Command/application_shortcut for up gesture executed successfully")
                                self.send_register_log("Command/application_shortcut for up gesture executed successfully")
                            else:
                                # print("Failed to execute command/application_shortcut ")
                                self.send_register_log("Failed to execute command/application_shortcut ")
                        else:
                            # print("Shortcut for upward gesture is not initialised correctly")
                            self.send_register_log("Shortcut for upward gesture is not initialised correctly")
                    else:
                        # print("Shortcut for upward gesture is not initialised.")
                        self.send_register_log("Shortcut for upward gesture is not initialised.")

                elif output == "DOWN":
                    # print("Downward gesture performed")
                    self.send_register_log("Downward gesture performed")
                    if (self.gestures["down"]["enabled"]):
                        if(self.gestures["down"]["type"] == "keyboard_shortcut"):
                            keyboard.press_and_release(self.gestures["down"]["value"])
                        elif(self.gestures["down"]["type"] == "application_shortcut"):
                            status_code = os.system(self.gestures["down"]["value"] + " &")
                            if status_code == 0:
                                # print("Command/application_shortcut for down gesture executed successfully")
                                self.send_register_log("Command/application_shortcut for down gesture executed successfully")
                            else:
                                # print("Failed to execute command/application_shortcut ")
                                self.send_register_log("Failed to execute command/application_shortcut ")
                        else:
                            # print("Shortcut for downward gesture is not initialised correctly")
                            self.send_register_log("Shortcut for downward gesture is not initialised correctly")
                    else:
                        # print("Shortcut for downward gesture is not initialised.")
                        self.send_register_log("Shortcut for downward gesture is not initialised.")

                    # keyboard.press_and_release(125)                           # for pressing windows button

                elif output == "FAR":
                    # print("Far gesture performed")
                    self.send_register_log("Far gesture performed")
                    if (self.gestures["far"]["enabled"]):
                        if(self.gestures["far"]["type"] == "keyboard_shortcut"):
                            keyboard.press_and_release(self.gestures["far"]["value"])
                        elif(self.gestures["far"]["type"] == "application_shortcut"):
                            status_code = os.system(self.gestures["far"]["value"] + " &")
                            if status_code == 0:
                                # print("Command/application_shortcut for far gesture executed successfully")
                                self.send_register_log("Command/application_shortcut for far gesture executed successfully")
                            else:
                                # print("Failed to execute command/application_shortcut ")
                                self.send_register_log("Failed to execute command/application_shortcut ")
                        else:
                            # print("Shortcut for far gesture is not initialised correctly")
                            self.send_register_log("Shortcut for far gesture is not initialised correctly")
                    else:
                        # print("Shortcut for far gesture is not initialised.")
                        self.send_register_log("Shortcut for far gesture is not initialised.")
                    # print("far")
                    # keyboard.press_and_release("Home")
                elif output == "NEAR":
                    # print("Upward gesture performed")
                    self.send_register_log("Upward gesture performed")
                    if (self.gestures["up"]["enabled"]):
                        if(self.gestures["up"]["type"] == "keyboard_shortcut"):
                            keyboard.press_and_release(self.gestures["up"]["value"])
                        elif(self.gestures["up"]["type"] == "application_shortcut"):
                            status_code = os.system(self.gestures["up"]["value"] + " &")
                            if status_code == 0:
                                # print("Command/application_shortcut for near gesture executed successfully")
                                self.send_register_log("Command/application_shortcut for near gesture executed successfully")
                            else:
                                # print("Failed to execute command/application_shortcut ")
                                self.send_register_log("Failed to execute command/application_shortcut ")
                        else:
                            # print("Shortcut for near gesture is not initialised correctly")
                            self.send_register_log("Shortcut for near gesture is not initialised correctly")
                    else:
                        # print("Shortcut for near gesture is not initialised.")
                        self.send_register_log("Shortcut for near gesture is not initialised.")
                    # print("near")
                # print(output)

    @pyqtSlot()
    def run(self):
        self.exit_signal.connect(self.raise_exit_flag)
        self.exit_flag = False
        self.connect_to_port()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    service = gestureUIHandler()
    service.setupUi(MainWindow)
    # service.radiobuttons()
    service.buttons()
    MainWindow.show()
    sys.exit(app.exec_())
