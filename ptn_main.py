
from ptn_v7 import Ui_MainWindow

from PyQt5 import QtWidgets, QtCore, QtGui

import telnetlib
import time
import csv
import os

BASEDIR = os.path.dirname(__file__)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)             # Setup UI from Ui_MainWindow class setupUi method by passing Mainwindow instance.
        # self.ui.comboBox1_node_ip.addItems(["" for _ in range(4)])   # Shifted to retranslateUi method

        self.ui.lineEdit1_ports_list.setHidden(True)
        self.ui.lineEdit2_command.setHidden(True)

        self.ui.comboBox2_port_type.addItems(["" for _ in range(5)])
        self.ui.comboBox3_port.addItems(["" for _ in range(6)])
        self.ui.comboBox4_display.addItems(["" for _ in range(3)])

        self.ui.textBrowser.setFontFamily("Consolas")
        # self.ui.textBrowser.setFontPointSize(self.ui.browser_font_size)

        self.retranslateUi()  # This updated method overrides the super class method (thus no need to edit the 'ui' auto generated code by Qt designer)

        # Connecting signals and its slots (Pyqt slots or Python functions), which are already not defined in Qt designer code
        self.ui.radioButton1_port.toggled['bool'].connect(self.update_C3_C4)
        self.ui.radioButton2_system.toggled['bool'].connect(self.update_C4)
        self.ui.radioButton3_ports_list.toggled['bool'].connect(self.ui.lineEdit1_ports_list.setVisible)
        self.ui.radioButton3_ports_list.toggled['bool'].connect(self.update_C4)
        self.ui.radioButton4_command.toggled['bool'].connect(self.ui.lineEdit2_command.setVisible)
        self.ui.radioButton4_command.toggled['bool'].connect(self.ui.label4_display.setHidden)
        self.ui.radioButton4_command.toggled['bool'].connect(self.ui.comboBox4_display.setHidden)
        self.ui.comboBox2_port_type.currentTextChanged.connect(self.update_C3_C4)
        self.ui.comboBox1_node_ip.setEditable(True)

        self.ui.actionOpen.triggered.connect(self.update_C1_with_csv_data) 
        self.ui.actionExit.triggered.connect(self.close) 

        # Added login credentials function
        try:
            self.username, self.password = MainWindow.get_login_credentials()
        except:
            self.username = ''
            self.password = ''
            self.show_popup("Login credentials file 'login.txt' missing or \nEntry not in 'username,password' format in txt file")
        self.ui.pushButton.clicked.connect(self.run)
        # self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "CPAN NMS"))
        self.ui.label2_port_type.setText(_translate("MainWindow", "Port Type"))
        self.ui.comboBox4_display.setItemText(0, _translate("MainWindow", "Bandwidth and Power"))
        self.ui.comboBox4_display.setItemText(1, _translate("MainWindow", "Performance"))
        self.ui.comboBox4_display.setItemText(2, _translate("MainWindow", "Config"))
        self.ui.label4_display.setText(_translate("MainWindow", "Display"))
        self.ui.lineEdit1_ports_list.setPlaceholderText(_translate("MainWindow", "List of ports eg: 1.1 2.1 3.1.2000"))
        self.ui.pushButton.setText(_translate("MainWindow", "OK"))
        self.ui.groupBox_monitor.setTitle(_translate("MainWindow", "Monitor"))
        self.ui.radioButton2_system.setText(_translate("MainWindow", "system"))
        self.ui.radioButton4_command.setText(_translate("MainWindow", "command"))
        self.ui.radioButton1_port.setText(_translate("MainWindow", "port"))
        self.ui.radioButton3_ports_list.setText(_translate("MainWindow", "ports list"))
        self.ui.comboBox2_port_type.setItemText(0, _translate("MainWindow", "10GE"))
        self.ui.comboBox2_port_type.setItemText(1, _translate("MainWindow", "GE-Optical"))
        self.ui.comboBox2_port_type.setItemText(2, _translate("MainWindow", "GE-Electrical"))
        self.ui.comboBox2_port_type.setItemText(3, _translate("MainWindow", "STM-1"))
        self.ui.comboBox2_port_type.setItemText(4, _translate("MainWindow", "Lag"))
        self.ui.label5_delay.setText(_translate("MainWindow", "Read delay"))
        self.ui.comboBox5_delay.setCurrentText(_translate("MainWindow", "min"))
        self.ui.comboBox5_delay.setItemText(0, _translate("MainWindow", "min"))
        self.ui.comboBox5_delay.setItemText(1, _translate("MainWindow", "max"))
        self.ui.comboBox3_port.setItemText(0, _translate("MainWindow", "0/1/0/1"))
        self.ui.comboBox3_port.setItemText(1, _translate("MainWindow", "0/1/0/2"))
        self.ui.comboBox3_port.setItemText(2, _translate("MainWindow", "0/4/0/1"))
        self.ui.comboBox3_port.setItemText(3, _translate("MainWindow", "0/4/0/2"))
        self.ui.comboBox3_port.setItemText(4, _translate("MainWindow", "0/6/0/1"))
        self.ui.comboBox3_port.setItemText(5, _translate("MainWindow", "0/6/0/2"))
        self.ui.label3_port.setText(_translate("MainWindow", "Port"))

        # Added the add items here for comboBox1 (shifted from __init__)

        filename = MainWindow.get_csv_filename()
        # print(filename)

        if filename:
            filepath = os.path.join(BASEDIR, filename)
        
        try:
            if filepath:
                self.update_C1_with_csv_data(filepath)
        except:
            self.ui.comboBox1_node_ip.addItems(["" for _ in range(1)])
            self.ui.comboBox1_node_ip.setItemText(0, _translate("MainWindow", "10.1.1.1  |  111-1  |  Thiruvalla"))
            
        
        self.ui.label1_node_ip.setText(_translate("MainWindow", "Node IP"))
        self.ui.menuFile.setTitle(_translate("MainWindow", "File"))
        self.ui.actionAlt_4.setText(_translate("MainWindow", "Alt+4"))
        self.ui.actionOpen.setText(_translate("MainWindow", "Import Nodes.csv"))
        self.ui.actionExit.setText(_translate("MainWindow", "Close"))

    def update_C3_C4(self):
        _translate = QtCore.QCoreApplication.translate
        if self.ui.comboBox2_port_type.currentText() == "GE-Optical":
            self.ui.comboBox3_port.clear()
            self.ui.comboBox3_port.addItems(["" for x in range(24)])
            self.ui.comboBox3_port.setItemText(0, _translate("MainWindow", "0/2/0/1"))
            self.ui.comboBox3_port.setItemText(1, _translate("MainWindow", "0/2/0/2"))
            self.ui.comboBox3_port.setItemText(2, _translate("MainWindow", "0/2/0/3"))
            self.ui.comboBox3_port.setItemText(3, _translate("MainWindow", "0/2/0/4"))
            self.ui.comboBox3_port.setItemText(4, _translate("MainWindow", "0/2/0/5"))
            self.ui.comboBox3_port.setItemText(5, _translate("MainWindow", "0/2/0/6"))
            self.ui.comboBox3_port.setItemText(6, _translate("MainWindow", "0/2/0/7"))
            self.ui.comboBox3_port.setItemText(7, _translate("MainWindow", "0/2/0/8"))
            self.ui.comboBox3_port.setItemText(8, _translate("MainWindow", "0/3/0/1"))
            self.ui.comboBox3_port.setItemText(9, _translate("MainWindow", "0/3/0/2"))
            self.ui.comboBox3_port.setItemText(10, _translate("MainWindow", "0/3/0/3"))
            self.ui.comboBox3_port.setItemText(11, _translate("MainWindow", "0/3/0/4"))
            self.ui.comboBox3_port.setItemText(12, _translate("MainWindow", "0/3/0/5"))
            self.ui.comboBox3_port.setItemText(13, _translate("MainWindow", "0/3/0/6"))
            self.ui.comboBox3_port.setItemText(14, _translate("MainWindow", "0/3/0/7"))
            self.ui.comboBox3_port.setItemText(15, _translate("MainWindow", "0/3/0/8"))
            self.ui.comboBox3_port.setItemText(16, _translate("MainWindow", "0/9/0/1"))
            self.ui.comboBox3_port.setItemText(17, _translate("MainWindow", "0/9/0/2"))
            self.ui.comboBox3_port.setItemText(18, _translate("MainWindow", "0/9/0/3"))
            self.ui.comboBox3_port.setItemText(19, _translate("MainWindow", "0/9/0/4"))
            self.ui.comboBox3_port.setItemText(20, _translate("MainWindow", "0/9/0/5"))
            self.ui.comboBox3_port.setItemText(21, _translate("MainWindow", "0/9/0/6"))
            self.ui.comboBox3_port.setItemText(22, _translate("MainWindow", "0/9/0/7"))
            self.ui.comboBox3_port.setItemText(23, _translate("MainWindow", "0/9/0/8"))

            self.ui.comboBox4_display.clear()
            self.ui.comboBox4_display.addItems(["" for x in range(3)])
            self.ui.comboBox4_display.setItemText(
                0, _translate("MainWindow", "Bandwidth and Power"))
            self.ui.comboBox4_display.setItemText(
                1, _translate("MainWindow", "Performance"))
            self.ui.comboBox4_display.setItemText(2, _translate("MainWindow", "Config"))

        elif self.ui.comboBox2_port_type.currentText() == "GE-Electrical":
            self.ui.comboBox3_port.clear()
            self.ui.comboBox3_port.addItems(["" for x in range(16)])
            self.ui.comboBox3_port.setItemText(0, _translate("MainWindow", "0/7/0/1"))
            self.ui.comboBox3_port.setItemText(1, _translate("MainWindow", "0/7/0/2"))
            self.ui.comboBox3_port.setItemText(2, _translate("MainWindow", "0/7/0/3"))
            self.ui.comboBox3_port.setItemText(3, _translate("MainWindow", "0/7/0/4"))
            self.ui.comboBox3_port.setItemText(4, _translate("MainWindow", "0/7/0/5"))
            self.ui.comboBox3_port.setItemText(5, _translate("MainWindow", "0/7/0/6"))
            self.ui.comboBox3_port.setItemText(6, _translate("MainWindow", "0/7/0/7"))
            self.ui.comboBox3_port.setItemText(7, _translate("MainWindow", "0/7/0/8"))
            self.ui.comboBox3_port.setItemText(8, _translate("MainWindow", "0/8/0/1"))
            self.ui.comboBox3_port.setItemText(9, _translate("MainWindow", "0/8/0/2"))
            self.ui.comboBox3_port.setItemText(10, _translate("MainWindow", "0/8/0/3"))
            self.ui.comboBox3_port.setItemText(11, _translate("MainWindow", "0/8/0/4"))
            self.ui.comboBox3_port.setItemText(12, _translate("MainWindow", "0/8/0/5"))
            self.ui.comboBox3_port.setItemText(13, _translate("MainWindow", "0/8/0/6"))
            self.ui.comboBox3_port.setItemText(14, _translate("MainWindow", "0/8/0/7"))
            self.ui.comboBox3_port.setItemText(15, _translate("MainWindow", "0/8/0/8"))

            self.ui.comboBox4_display.clear()
            self.ui.comboBox4_display.addItems(["" for x in range(3)])
            self.ui.comboBox4_display.setItemText(
                0, _translate("MainWindow", "Bandwidth"))
            self.ui.comboBox4_display.setItemText(
                1, _translate("MainWindow", "Performance"))
            self.ui.comboBox4_display.setItemText(2, _translate("MainWindow", "Config"))

        elif self.ui.comboBox2_port_type.currentText() == "10GE":
            self.ui.comboBox3_port.clear()
            self.ui.comboBox3_port.addItems(["" for x in range(6)])
            self.ui.comboBox3_port.setItemText(0, _translate("MainWindow", "0/1/0/1"))
            self.ui.comboBox3_port.setItemText(1, _translate("MainWindow", "0/1/0/2"))
            self.ui.comboBox3_port.setItemText(2, _translate("MainWindow", "0/4/0/1"))
            self.ui.comboBox3_port.setItemText(3, _translate("MainWindow", "0/4/0/2"))
            self.ui.comboBox3_port.setItemText(4, _translate("MainWindow", "0/6/0/1"))
            self.ui.comboBox3_port.setItemText(5, _translate("MainWindow", "0/6/0/2"))

            self.ui.comboBox4_display.clear()
            self.ui.comboBox4_display.addItems(["" for x in range(3)])
            self.ui.comboBox4_display.setItemText(
                0, _translate("MainWindow", "Bandwidth and Power"))
            self.ui.comboBox4_display.setItemText(
                1, _translate("MainWindow", "Performance"))
            self.ui.comboBox4_display.setItemText(2, _translate("MainWindow", "Config"))

        elif self.ui.comboBox2_port_type.currentText() == "STM-1":
            self.ui.comboBox3_port.clear()
            self.ui.comboBox3_port.addItems(["" for x in range(8)])
            self.ui.comboBox3_port.setItemText(0, _translate("MainWindow", "0/5/0/1"))
            self.ui.comboBox3_port.setItemText(1, _translate("MainWindow", "0/5/0/2"))
            self.ui.comboBox3_port.setItemText(2, _translate("MainWindow", "0/5/0/3"))
            self.ui.comboBox3_port.setItemText(3, _translate("MainWindow", "0/5/0/4"))
            self.ui.comboBox3_port.setItemText(4, _translate("MainWindow", "0/5/0/5"))
            self.ui.comboBox3_port.setItemText(5, _translate("MainWindow", "0/5/0/6"))
            self.ui.comboBox3_port.setItemText(6, _translate("MainWindow", "0/5/0/7"))
            self.ui.comboBox3_port.setItemText(7, _translate("MainWindow", "0/5/0/8"))

            self.ui.comboBox4_display.clear()
            self.ui.comboBox4_display.addItems(["" for x in range(3)])
            self.ui.comboBox4_display.setItemText(0, _translate("MainWindow", "Power"))
            self.ui.comboBox4_display.setItemText(
                1, _translate("MainWindow", "Performance"))
            self.ui.comboBox4_display.setItemText(2, _translate("MainWindow", "Config"))

        else:
            self.ui.comboBox3_port.clear()
            self.ui.comboBox3_port.addItems(["" for x in range(8)])
            self.ui.comboBox3_port.setItemText(0, _translate("MainWindow", "lag 1"))
            self.ui.comboBox3_port.setItemText(1, _translate("MainWindow", "lag 2"))
            self.ui.comboBox3_port.setItemText(2, _translate("MainWindow", "lag 3"))
            self.ui.comboBox3_port.setItemText(3, _translate("MainWindow", "lag 4"))
            self.ui.comboBox3_port.setItemText(4, _translate("MainWindow", "lag 5"))
            self.ui.comboBox3_port.setItemText(5, _translate("MainWindow", "lag 6"))
            self.ui.comboBox3_port.setItemText(6, _translate("MainWindow", "lag 7"))
            self.ui.comboBox3_port.setItemText(7, _translate("MainWindow", "lag 8"))

            self.ui.comboBox4_display.clear()
            self.ui.comboBox4_display.addItems(["" for x in range(2)])
            self.ui.comboBox4_display.setItemText(0, _translate(
                "MainWindow", "Lacp members and status"))
            self.ui.comboBox4_display.setItemText(1, _translate("MainWindow", "Config"))

    def update_C4(self):
        _translate = QtCore.QCoreApplication.translate
        self.ui.comboBox4_display.clear()
        if self.ui.radioButton2_system.isChecked():
            self.ui.comboBox4_display.addItems(["" for x in range(3)])
            self.ui.comboBox4_display.setItemText(
                0, _translate("MainWindow", "Current Alarm"))
            self.ui.comboBox4_display.setItemText(
                1, _translate("MainWindow", "System Usage"))
            self.ui.comboBox4_display.setItemText(2, _translate("MainWindow", "Version"))
        elif self.ui.radioButton3_ports_list.isChecked():
            self.ui.comboBox4_display.addItems(["" for x in range(4)])
            self.ui.comboBox4_display.setItemText(
                0, _translate("MainWindow", "Bandwidth and Power"))
            self.ui.comboBox4_display.setItemText(
                1, _translate("MainWindow", "Config"))
            self.ui.comboBox4_display.setItemText(
                2, _translate("MainWindow", "QoS Profiles"))
            self.ui.comboBox4_display.setItemText(
                3, _translate("MainWindow", "MAC Table"))

    @staticmethod
    def get_login_credentials():
        with open(os.path.join(BASEDIR, 'login.txt'), 'r') as f:
            username = ''
            password = ''
            for line in f:
                # print(line)
                try:
                    u, p = line.split(',')
                    username = u.strip()
                    password = p.strip()
                    print(f'Username: {username}\nPassword: {password}')
                    return username, password
                except ValueError:
                    print("ValueError: empty spaces present")


    @staticmethod
    def get_bandwidth(port_type, line):
        if port_type == "10GE" or port_type[2] in "146":
            util = float(line.split(":")[-1])
            bw = util * 100
        else:
            util = float(line.split()[3])
            bw = util * 10
        return bw

    @staticmethod
    def get_output(tel_out):
        temp_out = []
        output = tel_out.decode('ascii').split("\n")
        for line in output:
            if line != "\r":
                if "650" not in line:
                    if ">" not in line:
                        if "...." not in line:
                            if "show" not in line:
                                if "ems-show" not in line:
                                    temp_out.append(line)
        return temp_out

    @staticmethod
    def formatter(y):
        x = y.strip(",:;/+-.()[]}{<>''")
        if not x:
            return x
        if x[0] == "l":
            return x[0] + "ag " + x[-1]
        if x[0] != "0":
            x = "0/" + x[0] + "/0/" + x[2:]
        return x

    @staticmethod
    def teng_check(x):
        return x[2] in "146"

    @staticmethod
    def get_vsi_name(out):
        for line in out:
            if "vsi" in line:
                return line.split()[1]

    @staticmethod
    def get_csv_filename(): 
        files = os.listdir()
        for file_csv in files:
            if file_csv.endswith('.csv'):
                # print(file)
                return file_csv       

    def get_csv_filepath(self):
        fpath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Nodes.csv containing list of CPAN Nodes', '', 'CSV Files (*.csv)')
        return fpath

    def update_C1_with_csv_data(self, fpath):
        _translate = QtCore.QCoreApplication.translate
        if not fpath:     # If didn't get filename from os.path.join function (Nodes.csv file missing in default directory)
            fpath = self.get_csv_filepath()      # Select csv file from QFileDialog
        if fpath:
            # print(fpath)
            self.ui.comboBox1_node_ip.clear()
            with open(fpath, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                i=0
                max_length = 0
                next(csv_reader)         # To skip the header(first) line in csv file
                for line in csv_reader:
                    # print(line)
                    self.ui.comboBox1_node_ip.addItem("")
                    new_line = ("  |  ").join(line)
                    self.ui.comboBox1_node_ip.setItemText(i, _translate("MainWindow", new_line))
                    i+=1
                    if max_length < len(new_line):
                        max_length = len(new_line)

                self.ui.comboBox1_node_ip.setMinimumContentsLength(max_length-10)
        # print(fpath)

    def show_popup(self, error):
        msg = QtWidgets.QMessageBox()
        ip = self.ui.comboBox1_node_ip.currentText().split()[0]
        if self.username == '' or self.password == '':
            msg.setWindowTitle("Critical")
            msg.setText(
                "Error: {} ".format(error))
        else:       
            msg.setWindowTitle("Info")
            msg.setText(
                "Connection to node {} failed \nError: {} ".format(ip, error))
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # msg.buttonClicked.connect()
        msg.exec_()

    def show_progress(self, sleep):
        read_delay = self.ui.comboBox5_delay.currentText()
        if read_delay == 'max':
            read_delay_value = 1
        else:
            read_delay_value = 0

        count = 0
        count_step = int((progress_bar_limit * .2)/sleep)
        # print(f'count_step {count_step}')
        while count < progress_bar_limit:
            count += count_step
            # print(count)
            time.sleep(.2 + read_delay_value)
            self.ui.progressBar.setTextVisible(True)
            self.ui.progressBar.setValue(count)

    def login(self):
        try:
            ip = self.ui.comboBox1_node_ip.currentText().split()[0]
            if self.username == '' or self.password == '':
                self.show_popup("Enter valid login credentials in 'login.txt' file")
            else:
                self.telnet = telnetlib.Telnet(ip, port, connection_timeout)
                self.telnet.read_until(b"Username: ", reading_timeout)
                self.telnet.write(self.username.encode('ascii') + b"\n")
                self.telnet.read_until(b"Password:", reading_timeout)
                self.telnet.write(self.password.encode('ascii') + b"\n")
                time.sleep(.2)
                print("Logged In Node: {}".format(ip))
                return True
        except OSError as e:
            # self.ui.textBrowser.setText("Connection to node {} failed. Error: {}".format(self.ui.comboBox1_node_ip.currentText(), e))  # ADDED MESSAGEBOX
            self.show_popup(e)
            return False

        except Exception as e:
            # self.ui.textBrowser.setText("Not able to connect due to this error: {}".format(e)) # ADDED MESSAGEBOX
            self.show_popup(e)
            return False

    def run(self):
        ip = self.ui.comboBox1_node_ip.currentText().split()[0]

        if self.login():
            display = self.ui.comboBox4_display.currentText()

            if self.ui.radioButton1_port.isChecked():
                port_type = self.ui.comboBox2_port_type.currentText()
                port = self.ui.comboBox3_port.currentText()
                # key_words = self.ui.lineEdit1_ports_list.text().split()

                if port_type == "GE-Optical":

                    if display == "Bandwidth and Power":
                        self.telnet.write(b"show performance slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        new_output = "\nPORT GE {}\n\n".format(port)
                        new_line = ""
                        output = self.telnet.read_very_eager().decode('ascii').split("\n")
                        for line in output:
                            if "BW" in line:
                                bw = MainWindow.get_bandwidth(
                                    port_type, line)
                                if "RX" in line:
                                    new_line = "Input bandwidth: {:6.1f} Mbps".format(
                                        bw)
                                else:
                                    new_line = "Output bandwidth: {:5.1f} Mbps".format(
                                        bw)
                            elif "OP" in line:
                                if "ROP" not in line:
                                    power = line.split()[3]
                                    if "IOP" in line:
                                        new_line = "Rx power: {} dBm".format(
                                            power)
                                    else:
                                        new_line = "Tx power: {} dBm".format(
                                            power)
                            else:
                                continue
                            new_output += new_line + "\n"
                        self.ui.textBrowser.setText(new_output)
                        self.telnet.close()

                    elif display == "Performance":
                        self.telnet.write(b"show performance slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        time.sleep(sleep)
                        new_output = [
                            "\nCURRENT PERFORMANCE of PORT {}\n".format(port)]
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        time.sleep(delay)
                        self.telnet.write(b"show performance-cumu slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        new_output.append(
                            "\n\nCUMULATIVE PERFORMANCE of PORT {}\n".format(port))
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(new_output))
                        self.telnet.close()

                    else:
                        self.telnet.write(
                            b"show run inter gi " + port.encode('ascii') + b"\n")
                        self.show_progress(config_sleep)
                        output = ["\nCONFIG GE {}\n".format(port)]
                        output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(output))
                        self.telnet.close()

                elif port_type == "GE-Electrical":

                    if display == "Bandwidth":
                        self.telnet.write(b"show performance slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        new_output = "\nPORT GE-Electrical {}\n\n".format(port)
                        new_line = ""
                        output = self.telnet.read_very_eager().decode('ascii').split("\n")
                        for line in output:
                            if "BW" in line:
                                bw = MainWindow.get_bandwidth(
                                    port_type, line)
                                if "RX" in line:
                                    new_line = "Input bandwidth: {:6.1f} Mbps".format(
                                        bw)
                                else:
                                    new_line = "Output bandwidth: {:5.1f} Mbps".format(
                                        bw)
                            else:
                                continue
                            new_output += new_line + "\n"
                        self.ui.textBrowser.setText(new_output)
                        self.telnet.close()

                    elif display == "Performance":
                        self.telnet.write(b"show performance slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        time.sleep(sleep)
                        new_output = [
                            "\nCURRENT PERFORMANCE of PORT {}\n".format(port)]
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        time.sleep(delay)
                        self.telnet.write(b"show performance-cumu slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        new_output.append(
                            "\n\nCUMULATIVE PERFORMANCE of PORT {}\n".format(port))
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(new_output))
                        self.telnet.close()

                    else:
                        self.telnet.write(
                            b"show run inter gi " + port.encode('ascii') + b"\n")
                        self.show_progress(config_sleep)
                        output = ["\nCONFIG GE-Electrical {}\n".format(port)]
                        output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(output))
                        self.telnet.close()

                elif port_type == "10GE":

                    if display == "Bandwidth and Power":
                        self.telnet.write(
                            b"show inter ten " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                          
                        new_output = "\nPORT TENG {}\n\n".format(port)
                        new_line = ""
                        output = self.telnet.read_very_eager().decode('ascii').split("\n")
                        for line in output:
                            if "Power" in line:
                                new_line = line.strip()
                            elif "util" in line:
                                bw = MainWindow.get_bandwidth(
                                    port_type, line)
                                if "Input" in line:
                                    new_line = "Input bandwidth: {:5.0f} Mbps".format(
                                        bw)
                                else:
                                    new_line = "Output bandwidth: {:4.0f} Mbps".format(
                                        bw)
                            elif "error" in line:
                                new_line = line
                            elif "warn" in line:
                                new_line = line
                            else:
                                continue
                            new_output += new_line + "\n"
                        self.ui.textBrowser.setText(new_output)
                        self.telnet.close()

                    elif display == "Performance":
                        self.telnet.write(b"show performance slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        time.sleep(sleep)
                        new_output = [
                            "\nCURRENT PERFORMANCE of PORT {}\n".format(port)]
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        time.sleep(delay)
                        self.telnet.write(b"show performance-cumu slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        new_output.append(
                            "\n\nCUMULATIVE PERFORMANCE of PORT {}\n".format(port))
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(new_output))
                        self.telnet.close()

                    else:
                        self.telnet.write(
                            b"show run inter ten " + port.encode('ascii') + b"\n")
                        self.show_progress(config_sleep)
                        output = ["\nCONFIG TENG {}\n".format(port)]
                        output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(output))
                        self.telnet.close()

                elif port_type == "STM-1":

                    if display == "Power":
                        self.telnet.write(b"show performance slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        new_output = "\nPORT STM-1 {}\n\n".format(port)
                        new_line = ""
                        output = self.telnet.read_very_eager().decode('ascii').split("\n")
                        for line in output:
                            if "OP" in line:
                                if "ROP" in line:
                                    continue
                                power = line.split()[3]
                                if "IOP" in line:
                                    new_line = "Rx power: {} dBm".format(power)
                                else:
                                    new_line = "Tx power: {} dBm".format(power)
                            else:
                                continue
                            new_output += new_line + "\n"
                        self.ui.textBrowser.setText(new_output)
                        self.telnet.close()

                    elif display == "Performance":
                        self.telnet.write(b"show performance slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        time.sleep(sleep)
                        new_output = [
                            "\nCURRENT PERFORMANCE of PORT {}\n".format(port)]
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        time.sleep(delay)
                        self.telnet.write(b"show performance-cumu slot " + port[2].encode(
                            'ascii') + b" filter " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        new_output.append(
                            "\n\nCUMULATIVE PERFORMANCE of PORT {}\n".format(port))
                        new_output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(new_output))
                        self.telnet.close()

                    else:
                        self.telnet.write(
                            b"show run inter cep " + port.encode('ascii') + b"/1/0\n")
                        self.show_progress(config_sleep)
                        output = ["\nCONFIG STM-1 {}\n".format(port)]
                        output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(output))
                        self.telnet.close()

                elif port_type == "LAG":

                    if display == "Lacp members and status":
                        self.telnet.write(
                            b"show " + port.encode('ascii') + b"\n")
                        time.sleep(sleep)
                        output = [
                            "\n{} MEMBER PORTS and LACP STATUS\n".format(port.upper())]
                        output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        time.sleep(delay)
                        self.telnet.write(
                            b"show lacp count " + port.encode('ascii') + b"\n")
                        self.show_progress(sleep)
                        output.append("\n")
                        output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(output))
                        self.telnet.close()

                    else:
                        self.telnet.write(
                            b"show run inter  " + port.encode('ascii') + b"\n")
                        self.show_progress(config_sleep)
                        output = ["\nCONFIG {}\n".format(port.upper())]
                        output.extend(MainWindow.get_output(
                            self.telnet.read_very_eager()))
                        self.ui.textBrowser.setText("\n".join(output))
                        self.telnet.close()

            elif self.ui.radioButton2_system.isChecked():

                if display == "Current Alarm":
                    self.telnet.write(b"show current-alarm all\n")
                    self.show_progress(sleep)
                    output = ["\nCURRENT ALARM for NODE: {}\n".format(ip)]
                    output.extend(MainWindow.get_output(
                        self.telnet.read_very_eager()))
                    self.ui.textBrowser.setText("\n".join(output))
                    self.telnet.close()

                elif display == "System Usage":
                    self.telnet.write(b"ems-show system-usage\n")
                    self.show_progress(sleep)
                    output = ["\nSYSTEM USAGE for NODE: {}\n".format(ip)]
                    output.extend(MainWindow.get_output(
                        self.telnet.read_very_eager()))
                    self.ui.textBrowser.setText("\n".join(output))
                    self.telnet.close()

                elif display == "Version":
                    self.telnet.write(b"ems-show version compile\n")
                    self.show_progress(sleep)
                    output = ["\nSYSTEM VERSION for NODE: {}\n".format(ip)]
                    output.extend(MainWindow.get_output(
                        self.telnet.read_very_eager()))
                    self.ui.textBrowser.setText("\n".join(output))
                    self.telnet.close()

            elif self.ui.radioButton3_ports_list.isChecked():
                self.ui.textBrowser.clear()
                ports_list = self.ui.lineEdit1_ports_list.text().split()
                # print(ports_list)
                for port in ports_list:
                    formatted_port = MainWindow.formatter(port.lower())
                    # print(formatted_port)
                    if not formatted_port:
                        continue

                    if MainWindow.teng_check(formatted_port):

                        if display == "Bandwidth and Power":
                            self.telnet.write(
                                b"show inter ten " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(sleep)
                            new_output = "\nPORT TENG {}\n\n".format(port)
                            new_line = ""
                            output = self.telnet.read_very_eager().decode('ascii').split("\n")
                            for line in output:
                                if "Power" in line:
                                    new_line = line.strip()
                                elif "util" in line:
                                    bw = MainWindow.get_bandwidth(
                                        formatted_port, line)
                                    if "Input" in line:
                                        new_line = "Input bandwidth: {:5.0f} Mbps".format(
                                            bw)
                                    else:
                                        new_line = "Output bandwidth: {:4.0f} Mbps".format(
                                            bw)
                                elif "error" in line:
                                    new_line = line
                                elif "warn" in line:
                                    new_line = line
                                else:
                                    continue
                                new_output += new_line + "\n"
                            self.ui.textBrowser.append(new_output)
                            time.sleep(delay)

                        elif display == "Config":
                            self.telnet.write(
                                b"show run inter ten " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(config_sleep)
                            output = ["\nCONFIG TENG {}\n".format(port)]
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)

                        elif display == "QoS Profiles":
                            pass

                        elif display == "MAC Table":
                            pass

                    elif formatted_port[0] == "l":

                        if display == "Bandwidth and Power":
                            self.telnet.write(
                                b"show " + formatted_port.encode('ascii') + b"\n")
                            time.sleep(sleep)
                            output = [
                                "\n{} MEMBER PORTS and LACP STATUS\n".format(port.upper())]
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            time.sleep(delay)
                            self.telnet.write(
                                b"show lacp count " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(sleep)
                            output.append("\n")
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)

                        elif display == "Config":
                            self.telnet.write(
                                b"show run inter " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(config_sleep)
                            output = ["\nCONFIG {}\n".format(port.upper())]
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)

                        elif display == "QoS Profiles":
                            pass

                        elif display == "MAC Table":
                            self.telnet.write(
                                b"show run inter " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(config_sleep)
                            outputs = self.telnet.read_very_eager().decode('ascii').split("\n")
                            vsi_name = MainWindow.get_vsi_name(outputs)
                            if vsi_name:
                                output = [
                                    "\nMAC Table related to {} member ports\n".format(port)]
                                time.sleep(delay)
                                self.telnet.write(
                                    b"show vpls mac vsi " + vsi_name.encode('ascii') + b"\n")
                                self.show_progress(2)
                                output.extend(MainWindow.get_output(
                                    self.telnet.read_very_eager()))
                                self.ui.textBrowser.append("\n".join(output))
                                time.sleep(delay)

                    elif formatted_port[2] == "5":

                        if display == "Bandwidth and Power":
                            self.telnet.write(b"show performance slot " + formatted_port[2].encode(
                                'ascii') + b" filter " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(sleep)
                            new_output = "\nPORT STM-1 {}\n\n".format(port)
                            new_line = ""
                            output = self.telnet.read_very_eager().decode('ascii').split("\n")
                            for line in output:
                                if "OP" in line:
                                    if "ROP" in line:
                                        continue
                                    power = line.split()[3]
                                    if "IOP" in line:
                                        new_line = "Rx power: {} dBm".format(
                                            power)
                                    else:
                                        new_line = "Tx power: {} dBm".format(
                                            power)
                                else:
                                    continue
                                new_output += new_line + "\n"
                            self.ui.textBrowser.append(new_output)
                            time.sleep(delay)

                        elif display == "Config":
                            self.telnet.write(
                                b"show run inter cep " + formatted_port.encode('ascii') + b"/1/0\n")
                            self.show_progress(config_sleep)
                            output = ["\nCONFIG STM-1 {}\n".format(port)]
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)

                        elif display == "QoS Profiles":
                            pass

                        elif display == "MAC Table":
                            pass

                    else:

                        if display == "Bandwidth and Power":
                            self.telnet.write(b"show performance slot " + formatted_port[2].encode(
                                'ascii') + b" filter " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(sleep)
                            new_output = "\nPORT GE {}\n\n".format(port)
                            new_line = ""
                            output = self.telnet.read_very_eager().decode('ascii').split("\n")
                            for line in output:
                                if "BW" in line:
                                    bw = MainWindow.get_bandwidth(
                                        formatted_port, line)
                                    if "RX" in line:
                                        new_line = "Input bandwidth: {:6.1f} Mbps".format(
                                            bw)
                                    else:
                                        new_line = "Output bandwidth: {:5.1f} Mbps".format(
                                            bw)
                                elif "OP" in line:
                                    if "ROP" not in line:
                                        power = line.split()[3]
                                        if "IOP" in line:
                                            new_line = "Rx power: {} dBm".format(
                                                power)
                                        else:
                                            new_line = "Tx power: {} dBm".format(
                                                power)
                                else:
                                    continue
                                new_output += new_line + "\n"
                            self.ui.textBrowser.append(new_output)
                            time.sleep(delay)

                        elif display == "Config":
                            self.telnet.write(
                                b"show run inter gi " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(config_sleep)
                            output = ["\nCONFIG GE {}\n".format(port)]
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)

                        elif display == "QoS Profiles":
                            self.telnet.write(
                                b"show qos-profile application inter gi " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(sleep)
                            output = [
                                "\nLogical QoS (car-profile-outbound) for GE {}\n".format(port)]
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)
                            self.telnet.write(
                                b"show port shaping inter gi " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(sleep)
                            output = [
                                "\nPhysical QoS (port-shaping-inbound) for GE {}\n".format(port)]
                            output.extend(MainWindow.get_output(
                                self.telnet.read_very_eager()))
                            self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)

                        elif display == "MAC Table":
                            self.telnet.write(
                                b"show run inter gi " + formatted_port.encode('ascii') + b"\n")
                            self.show_progress(config_sleep)
                            outputs = self.telnet.read_very_eager().decode('ascii').split("\n")
                            vsi_name = MainWindow.get_vsi_name(outputs)
                            if vsi_name:
                                time.sleep(delay)
                                output = [
                                    "\nMAC Table related to GE {}\n".format(port)]
                                self.telnet.write(
                                    b"show vpls mac vsi " + vsi_name.encode('ascii') + b"\n")
                                self.show_progress(2)
                                output.extend(MainWindow.get_output(
                                    self.telnet.read_very_eager()))
                                self.ui.textBrowser.append("\n".join(output))
                            time.sleep(delay)

                self.telnet.close()

            elif self.ui.radioButton4_command.isChecked():
                self.ui.textBrowser.clear()
                command = self.ui.lineEdit2_command.text()
                if command:
                    self.telnet.write(
                        command.encode('ascii') + b"\n")
                    self.show_progress(config_sleep)
                    output = ["\n{}".format(command)]
                    output.extend(MainWindow.get_output(
                        self.telnet.read_very_eager()))
                    self.ui.textBrowser.setText("\n".join(output))

        else:
            print("Connection to host failed {}".format(ip))
            # self.telnet.close() # No need since if telnet already fails, this will raise an ERROR



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QtGui.QIcon('ptn.ico'))
    progress_bar_limit = 100
    # ui_font_size = 7
    # ui_font_size = 9
    # browser_font_size = 7.5
    # browser_font_size = 10
    port = 23
    connection_timeout = 5
    reading_timeout = 5
    delay = .3
    sleep = 1
    config_sleep = 5
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())