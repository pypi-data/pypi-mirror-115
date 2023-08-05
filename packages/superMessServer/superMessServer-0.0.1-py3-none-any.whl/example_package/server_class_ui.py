"""

Модуль сервера

Строго не судите) Этож учебный проект)



"""

import select
import socket
import pickle
import dis
import sys
import os
import hashlib
from log_config import *
from threading import Thread
from datetime import datetime
from PyQt5 import QtWidgets, uic
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def login_required(func):
    def wrapper(*args, **kwargs):
        for resource in args[1]:
            if resource is not args[2]:
                if resource not in args[0].INPUTS:
                    args[1].remove(resource)
                    print("Сообщение от незарегистрированного клента пропущено")
                else:
                    func(*args, **kwargs)
            else:
                func(*args, **kwargs)
    return wrapper


class messages_history(Base):
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


class user_acc(Base):
    __tablename__ = 'user_acc'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    login = Column(String)
    passhash = Column(String)
    time = Column(DateTime)

    def __init__(self, user, login, passhash, time):
        self.user = user
        self.login = login
        self.passhash = passhash
        self.time = time

    def __repr__(self):
        return "<user_acc('%s','%s','%s','%s')>" % \
            (self.user, self.login, self.passhash,  self.time)


class ServerVerifier(type):
    def __init__(self, cls_name, bases, cls_dict):
        for key, value in cls_dict.items():
            try:
                instructions = dis.get_instructions(value)
            except TypeError:
                continue
            if instructions:
                for el in instructions:
                    assert not el.argval == 'connect', 'Запрещено вызывать connect для сокетов'

                    if el.opname == 'LOAD_ATTR':
                        assert not el.argval == 'SOCK_DGRAM', 'Запрещено использовать сокеты для UDP'
        type.__init__(self, cls_name, bases, cls_dict)


class PortDescriptor:
    def __init__(self, default):
        self._validate_value(default)
        self._default = default
        self._name = None

    def __get__(self, instance, owner):
        return getattr(instance, self._name, self._default)

    def __set__(self, instance, value):
        self._validate_value(value)
        setattr(instance, self._name, value)

    def __set_name__(self, owner, name):
        self._name = f'__{name}'

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")

    @staticmethod
    def _validate_value(val):
        if not isinstance(val, int):
            raise TypeError(f'Порт не целочисленный, передан тип {type(val)}!')
        if not 0 < val <= 65365:
            raise ValueError('Порт должен быть от 0 до 65365')


class ServerTread(Thread):
    port = PortDescriptor(7777)._default

    def __init__(self, interval, host, port,  buffersize):
        super().__init__()
        self.daemon = True
        self.interval = interval
        self.INPUTS = []
        self.OUTPUTS = []
        self.MESSAGES = []
        self.GROUPS = {}
        self.USERS = []
        self.MAX_CONNECTIONS = buffersize
        self.host = host
        self.port = port
        self.countmes = 0

    def get_non_blocking_server_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.bind((self.host, self.port))
        server.listen(self.MAX_CONNECTIONS)
        return server

    def run(self):
        server_socket = self.get_non_blocking_server_socket()
        self.INPUTS.append(server_socket)
        print("сервер онлаин, ctrl + c для остановки и любой пост)")
        print(self.INPUTS)
        try:
            print("1")
            while self.INPUTS:
                readables, writables, exceptional = select.select(
                    self.INPUTS, self.OUTPUTS, self.INPUTS)
                self.handle_readables(readables, server_socket)
                if len(self.MESSAGES) > 0:
                    self.handle_send_messages(writables, self.MESSAGES)
                    self.MESSAGES = []

        except KeyboardInterrupt:
            print("2")
            self.clear_resource(server_socket)
            print("Сервер выключен. Удачи.")

    @login_required
    def handle_readables(self, readables, server):
        for resource in readables:
            if resource is server:
                connection, client_address = resource.accept()
                connection.setblocking(0)
                self.INPUTS.append(connection)
                print("new connection from {address}".format(
                    address=client_address))
                # connection.send(bytes('Hello, im server', encoding='UTF-8'))
            else:
                data = ""
                try:
                    data = resource.recv(1024)
                except ConnectionResetError:
                    pass

                if data:
                    print(pickle.loads(data))
                    self.MESSAGES.append([resource, pickle.loads(data)])
                    if resource not in self.OUTPUTS:
                        self.OUTPUTS.append(resource)
                else:
                    self.clear_resource(resource)

    def clear_resource(self, resource):
        """
        Очистка ресурсов использования сокета
        """
        if resource in self.OUTPUTS:
            self.OUTPUTS.remove(resource)
        if resource in self.INPUTS:
            self.INPUTS.remove(resource)
        resource.close()
        print('closing connection ' + str(resource))
        if resource in self.USERS:
            index_client = [self.USERS[i][0]
                            for i in range(len(self.USERS))].index(resource)
            if (index_client >= 0):
                self.USERS.pop(index_client)
        window.CllientList.clear()
        for el in self.USERS:
            # window.CllientList.append(el)
            window.CllientList.addItem(el[1])
        window.countClients.setText(str(len(self.USERS)))

    def handle_writables(self, writables):
        for resource in writables:
            try:
                # resource.send(bytes('Hello, im server\n', encoding='UTF-8'))
                pass
            except OSError:
                self.clear_resource(resource)

    def connect_bd(self):
        if os.path.exists("server.db"):
            self.engine = create_engine("sqlite:///server.db")
        else:
            self.engine = create_engine("sqlite:///server.db")
            self.metadata = Base.metadata
            self.metadata.create_all(self.engine)

    def handle_send_messages(self, writables, messages):
        log = logging.getLogger('app')
        for each_mess in messages:
            if each_mess[1].get('action') == 'msgall':
                for resource in self.INPUTS[1:]:
                    if resource != each_mess[0]:
                        try:
                            resource.send(pickle.dumps(each_mess[1]))
                        except OSError:
                            self.clear_resource(resource)
                self.countmes += 1
                window.countmess.setText(str(self.countmes))
            elif each_mess[1].get('action') == 'getlistclient':
                msg = {
                    "action": "getlistclient_resp",
                    "response": "202",
                    "alert": [self.USERS[i][1] for i in range(len(self.USERS))]
                }
                each_mess[0].send(pickle.dumps(msg))
            elif each_mess[1].get('action') == 'auth':
                if each_mess[1].get('user') not in self.USERS:
                    self.USERS.append([each_mess[0], each_mess[1].get('user')])
                window.CllientList.clear()
                for el in self.USERS:
                    # window.CllientList.append(el)
                    window.CllientList.addItem(el[1])
                window.countClients.setText(str(len(self.USERS)))

                # each_mess[1].get('pass')
                self.connect_bd()
                passhash = hashlib.pbkdf2_hmac(
                    'sha256', each_mess[1].get('pass').encode(), b'salt12s', 100000)
                result = self.engine.execute(
                    "select passhash from user_acc where login = '" + each_mess[1].get('login')+"'")
                data_from_history = result.first()
                # hmac.compare_digest(digest, response)
                if data_from_history is None:
                    # Сохраняем нового пользователя с хешом
                    Session = sessionmaker(bind=self.engine)
                    session = Session()
                    session.add(user_acc(each_mess[1].get('user'), each_mess[1].get(
                        'login'), passhash, datetime.now()))
                    session.commit()
                    msg = {
                        "action": "authok",
                        "response": "202",
                        "hash": passhash
                    }
                    each_mess[0].send(pickle.dumps(msg))
                elif data_from_history[0] == passhash:
                    msg = {
                        "action": "authok",
                        "response": "202",
                        "hash": passhash
                    }
                    each_mess[0].send(pickle.dumps(msg))
                else:
                    msg = {
                        "action": "authok",
                        "response": "500",
                        "hash": None,
                        "msg": "Auth error"
                    }
                    each_mess[0].send(pickle.dumps(msg))
                    # СДЕЛАТЬ ДИСКОННЕКТ

                # data_from_history = result.fetchall()
                # for el in data_from_history:
                #    window.MessageList.append(el[1]+':' + el[2])

            elif each_mess[1].get('action') == 'msg':
                try:
                    each_mess[0].send(pickle.dumps(each_mess[1]))
                    log.info(pickle.dumps(each_mess[1]))
                except OSError:
                    self.clear_resource(resource)
            elif each_mess[1].get('action') == 'msguser':
                # написать функцию отправки конкретному пользователю
                print(each_mess[1])
            elif each_mess[1].get('action') == 'msggrp':
                if self.GROUPS.get(each_mess[1].get('group')) is None:
                    msg = {
                        "action": "msg",
                        "msg": "Вы не состоите в указанной группе. Воспользуйтесь другой опцией"
                    }
                    self.MESSAGES.append([each_mess[0], msg])
                    log.info(msg)
                else:
                    msg = ''
                    state = False
                    for ech_el in self.GROUPS.get(each_mess[1].get('group')):
                        if ech_el == each_mess[0]:
                            state = True
                    if state:
                        for ech_el in self.GROUPS.get(each_mess[1].get('group')):
                            if ech_el != each_mess[0]:
                                msg = {
                                    "action": "msg",
                                    "user": each_mess[1].get('user'),
                                    "group": each_mess[1].get('group'),
                                    "msg": each_mess[1].get('msg')
                                }
                                self.MESSAGES.append([ech_el, msg])
                                self.countmes += 1
                                window.countmess.setText(str(self.countmes))
                    else:
                        msg = {
                            "action": "msg",
                            "msg": "Вы не состоите в указанной группе. Воспользуйтесь другой опцией"
                        }
                        self.MESSAGES.append([each_mess[0], msg])
                        log.info(msg)
            elif each_mess[1].get('action') == 'grpadd':
                if self.GROUPS.get(each_mess[1].get('group')) is None:
                    self.GROUPS.update(
                        {each_mess[1].get('group'): [each_mess[0]]})
                    msg = {
                        "action": "msg",
                        "msg": "Группа найдена не была. Группа создана"
                    }
                    self.MESSAGES.append([each_mess[0], msg])
                    log.info(msg)
                else:
                    msg = ''
                    for ech_el in self.GROUPS.get(each_mess[1].get('group')):
                        if ech_el == each_mess[0]:
                            msg = {
                                "action": "msg",
                                "msg": "Вы уже состоите в указанной группе"
                            }
                            self.MESSAGES.append([each_mess[0], msg])
                            log.info(msg)
                    if msg == '':
                        temlist = self.GROUPS.get(each_mess[1].get('group'))
                        temlist.append(each_mess[0])
                        self.GROUPS.update(
                            {each_mess[1].get('group'): temlist})
                        msg = {
                            "action": "msg",
                            "msg": "Вы добавлены в группу"
                        }
                        self.MESSAGES.append([each_mess[0], msg])
                        log.info(msg)


if __name__ == '__main__':

    # if os.path.exists("server.db"):
    # os.remove("server.db")

    app = QtWidgets.QApplication(sys.argv)
    window = uic.loadUi('server.ui')
    window.ExitButton.clicked.connect(app.quit)
    t = ServerTread(1, 'localhost', int(window.serverport.text()), 10)
    window.bdconnect.clicked.connect(t.connect_bd)
    t.start()
    window.show()
    sys.exit(app.exec_())
