"""

Клиентский модуль
Запускается на клиентской стороне.
Содержит сотни багов и дырок, которые требуют исправления.

Строго не судите) Этож учебный проект)

"""

import time
import pickle
import os
import sys
import socket

from threading import Thread
from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import false, true
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QHelpEvent
from PyQt5.QtWidgets import QMessageBox


Base = declarative_base()
connect = True
connecthash = None
try_connect = false


class messages_history(Base):
    """ Таблица с историей переписки """
    __tablename__ = 'messages_history'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    messages = Column(String)
    time = Column(DateTime)

    def __init__(self, user, messages, time):
        self.user = user
        self.messages = messages
        self.time = time

    def __repr__(self):
        return "<messages_history('%s','%s','%s')>" % \
            (self.user, self.messages,  self.time)


class personal(Base):
    """

    Список контактов

    """
    __tablename__ = 'personal'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    additional_info = Column(String)

    def __init__(self, login, additional_info):
        self.login = login
        self.additional_info = additional_info

    def __repr__(self):
        return "<Person('%s','%s')>" % \
            (self.login, self.additional_info)


class clienthistory(Base):
    __tablename__ = 'clienthistory'
    id = Column(Integer, primary_key=True)
    login_time = Column(DateTime)
    ip_adr = Column(String)

    def __init__(self, login_time, ip_adr):
        self.login_time = login_time
        self.ip_adr = ip_adr

    def __repr__(self):
        return "<User('%s','%s')>" % \
            (self.login_time, self.ip_adr)


class contactlist(Base):
    __tablename__ = 'contactlist'
    id = Column(Integer, primary_key=True)
    id_owner = Column(Integer)
    id_client = Column(Integer)

    def __init__(self, id_owner, id_client):
        self.id_owner = id_owner
        self.id_client = id_client

    def __repr__(self):
        return "<User('%s','%s')>" % \
            (self.id_owner, self.id_client)


def save_messages(user, msg):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(messages_history(user, msg, datetime.now()))
    session.commit()


def editmsgbox():
    # app2 = QtWidgets.QApplication([])
    return_name_client = ''

    def press_ok(self):
        nonlocal return_name_client
        print("ok")
        return_name_client = line_edit.text()
        if (line_edit.text() != ''):
            window.ContactListView.addItems([line_edit.text()])
        w.close()

    def press_cancel(self):
        w.close()

    def show_tooltip(parent, widget):
        app.notify(widget, QHelpEvent(QHelpEvent.ToolTip,
                   widget.pos(), parent.mapToGlobal(widget.pos())))

    line_edit = QtWidgets.QLineEdit()
    line_edit.setToolTip('This <b>my</b> LINE EDIT!')

    button = QtWidgets.QPushButton('Add')
    button.setToolTip('Simple button...')
    button.clicked.connect(press_ok)

    button2 = QtWidgets.QPushButton('Cancel')
    button2.setToolTip('Simple button...')
    button2.clicked.connect(press_cancel)

    layout = QtWidgets.QFormLayout()
    layout.addRow('Line edit:', line_edit)
    layout.addRow('Button:', button)

    w = QtWidgets.QWidget()
    w.setWindowTitle('Tooltip example')
    w.setLayout(layout)
    w.show()

    QTimer.singleShot(1000, lambda: show_tooltip(w, line_edit))
    QTimer.singleShot(2000, lambda: show_tooltip(w, button))

    # app2.exec()
    return return_name_client


class ClockThread(Thread):
    """

    Основной класс ожидаюший входящих сообщений.
    Получает с сервера сообщения, и обрабатывает их.

    """

    def __init__(self, interval, client):
        super().__init__()
        self.daemon = True
        self.interval = interval
        self.client = client

    def run(self):
        """

        Запуск треда, который каждые Х секунд опрашивает входящую очередь на наличие новых сообщений

        """
        global connect
        global connecthash
        while connect:
            data = self.client.recv(1024)
            dictdata = pickle.loads(data)
            if dictdata.get('action') == 'msgall':
                window.MessageList.append(dictdata.get(
                    'user')+':' + dictdata.get('msg'))
                save_messages(dictdata.get('user'), dictdata.get('msg'))
            elif dictdata.get('action') == 'getlistclient_resp':
                window.ContactListView.clear()
                if 'All' not in dictdata.get('alert'):
                    window.ContactListView.addItems(['All'])
                window.ContactListView.addItems(dictdata.get('alert'))
            elif dictdata.get('action') == 'authok':
                if (dictdata.get('response') == '202'):
                    connecthash = dictdata.get('hash')
                else:
                    connecthash = "0"
            time.sleep(self.interval)


class UIClien():
    def __init__(self, host='localhost', port=7777):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.contact_list = []

    def GetListCliets_signal(self):
        if (len(window.LoginUser.text()) > 0):
            msg = {
                "action": "getlistclient",
                "user": window.LoginUser.text()
            }
            self.client.send(pickle.dumps(msg))

    def SendMesButton_signal(self):
        # window.ContactListView.selectedItems()[0].text()
        if (len(window.LoginUser.text()) > 0 and len(window.MessageData.text()) > 0):
            if len(window.ContactListView.selectedItems()) == 0 or (window.ContactListView.selectedItems()[0].text() == 'All'):
                msg = {
                    "action": "msgall",
                    "user": window.LoginUser.text(),
                    "msg": window.MessageData.text()
                }
                self.client.send(pickle.dumps(msg))
                window.MessageList.append('Me:' + window.MessageData.text())
                save_messages('Me', window.MessageData.text())
                window.MessageData.clear()
            else:
                msg = {
                    "action": "msguser",
                    "user": window.LoginUser.text(),
                    "touser": window.ContactListView.selectedItems()[0].text(),
                    "msg": window.MessageData.text()
                }
                self.client.send(pickle.dumps(msg))
                window.MessageList.append(
                    'To ' + window.ContactListView.selectedItems()[0].text() + ':' + window.MessageData.text())
                save_messages('To ' + window.ContactListView.selectedItems()
                              [0].text(), window.MessageData.text())
                window.MessageData.clear()

    def run_client(self):
        address_to_server = ((self.host, self.port))
        self.client.connect(address_to_server)

    def auth_client(self):
        msg = {
            "action": "auth",
            "user": logwindow.nickname.text(),
            "login": logwindow.login.text(),
            "pass": logwindow.password.text()
        }
        self.client.send(pickle.dumps(msg))

    def SaveContacts(self):
        entries = [str(window.ContactListView.item(i).text())
                   for i in range(window.ContactListView.count())]
        Session = sessionmaker(bind=engine)
        session = Session()
        engine.execute("DELETE from contactlist")
        session.commit()
        for el in entries:
            session.add(contactlist(el, el))
        session.commit()

    def SelectContact(self, item):
        # window.QMessageBox.information(self, "Info", item.text())
        window.Client_name.setText(item.text())

    def DelContact(self):
        message = 'Вы уверены, что хотите удалить контакт?'
        reply = QtWidgets.QMessageBox.question(
            None, 'Уведомление', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            listItems = window.ContactListView.selectedItems()
            if not listItems:
                return
            for item in listItems:
                window.ContactListView.takeItem(
                    window.ContactListView.row(item))
        else:
            print('Del cancel')
        # Доделать!!!!

    def AddContact(self):
        editmsgbox()

    def DisconnectButton(self):
        global connect
        connect = False


def start_client():
    global connecthash
    global obj
    global window  # = uic.loadUi('client.ui')
    global logwindow
    global try_connect
    try_connect = true
    obj.auth_client()
    while connecthash is None:
        time.sleep(1)
    # while (connecthash == None) or (connecthash == "0"):
    if connecthash == "0":
        QMessageBox.warning(
            logwindow, "Внимание", "Ошибка учетных данных\n Поправьте логин и пароль и попробуйте снова")
        connecthash = None
        try_connect = false
        return
    elif connecthash != "0" and connecthash is not None:
        try_connect = false
        logwindow.hide()
        window.show()


if __name__ == '__main__':

    # if os.path.exists("client.db"):
    #   os.remove("client.db")

    if os.path.exists("client.db"):
        engine = create_engine("sqlite:///client.db")
    else:
        engine = create_engine("sqlite:///client.db")
        personal_table = personal.__table__
        metadata = Base.metadata
        metadata.create_all(engine)

    result = engine.execute("select * from contactlist")
    data_from_pers = result.fetchall()
    print(data_from_pers)

    app = QtWidgets.QApplication(sys.argv)
    obj = UIClien()

    logwindow = uic.loadUi('auth.ui')
    window = uic.loadUi('client.ui')
    logwindow.Okbtn.clicked.connect(start_client)
    logwindow.ExitButton.clicked.connect(app.quit)
    window.ExitButton.clicked.connect(app.quit)
    window.GetListCliets.clicked.connect(obj.GetListCliets_signal)
    window.SendMesButton.clicked.connect(obj.SendMesButton_signal)
    window.SaveContact.clicked.connect(obj.SaveContacts)
    window.ContactListView.itemDoubleClicked.connect(obj.SelectContact)
    window.DelContact.clicked.connect(obj.DelContact)
    window.AddContact.clicked.connect(obj.AddContact)
    window.DisconnectButton.clicked.connect(obj.DisconnectButton)
    obj.run_client()
    obj.contact_list = data_from_pers
    if 'All' not in [data_from_pers[i][1] for i in range(len(data_from_pers))]:
        window.ContactListView.addItems(['All'])
    window.ContactListView.addItems(
        [data_from_pers[i][1] for i in range(len(data_from_pers))])
    result = engine.execute("select * from messages_history")
    data_from_history = result.fetchall()
    for el in data_from_history:
        window.MessageList.append(el[1]+':' + el[2])
    t = ClockThread(1, obj.client)
    t.start()
    logwindow.show()
    sys.exit(app.exec_())
