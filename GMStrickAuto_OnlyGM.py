import random
import time
import uuid
from threading import Thread

from requests.exceptions import ProxyError, ReadTimeout
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from Layer3Model import *

# Создаем соединение с базой данных
engine = create_engine('sqlite:///GmStrick.db', pool_size=1000, max_overflow=1000)
Base = declarative_base()


# Определяем модель данных


class Record(Base):
    __tablename__ = 'records'
    id = Column(String, primary_key=True)
    user = Column(String)

    address = Column(String)
    private = Column(String)
    proxy = Column(String)

    NeedTasks = Column(Boolean)
    readyTasks = Column(String)
    XP = Column(Integer)

    date = Column(DateTime, default=datetime.utcnow)
    GMstrick = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    user_ = relationship("User", back_populates="records")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(50))
    limit = Column(Integer, nullable=False, default=100)
    registration_date = Column(DateTime, nullable=False, default=datetime.utcnow())

    records = relationship("Record", back_populates="user_")


class BountyStep(Base):
    __tablename__ = 'bounty_steps'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    bounty_step_id = Column(Integer)
    input_data = Column(String)
    user_address_id = Column(Integer)

    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", back_populates="bounty_steps")

    def __init__(self, bounty_step_id, input_data, user_address_id):
        self.id = str(uuid.uuid4())
        self.bounty_step_id = bounty_step_id
        self.input_data = input_data
        self.user_address_id = user_address_id


# Определяем модель данных bountyClaim
class BountyClaim(Base):
    __tablename__ = 'bounty_claims'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    TaskID = Column(Integer)

    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", back_populates="bounty_claims")

    def __init__(self, TaskID):
        self.id = str(uuid.uuid4())
        self.TaskID = TaskID


# Определяем модель данных additionalInfo
class AdditionalInfo(Base):
    __tablename__ = 'additional_info'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    info = Column(String)

    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", back_populates="additional_info")

    def __init__(self, info):
        self.id = str(uuid.uuid4())
        self.info = info


# Определяем модель данных Task
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)

    bounty_steps = relationship("BountyStep", back_populates="task")
    bounty_claims = relationship("BountyClaim", back_populates="task")
    additional_info = relationship("AdditionalInfo", back_populates="task")

    def __init__(self, name):
        self.id = str(uuid.uuid4())  # Генерируем новый UUID при создании экземпляра Task
        self.name = name


def split_list(lst, n):
    # Вычисляем длину каждого подсписка
    sublist_length = len(lst) // n
    # Вычисляем количество элементов, которые будут распределены дополнительно
    remaining_elements = len(lst) % n

    result = []
    start = 0
    for i in range(n):
        # Вычисляем длину текущего подсписка
        length = sublist_length + (1 if i < remaining_elements else 0)
        # Определяем конечный индекс текущего подсписка
        end = start + length
        # Добавляем текущий подсписок к результату
        result.append(lst[start:end])
        # Переходим к следующему подсписку
        start = end

    return result


def Function(accs):

    print(len(accs))

    for acc in accs:

        Session = sessionmaker(bind=engine)
        session = Session()

        # print(acc.id, acc.date, acc.GMstrick)
        # input()

        L3Account = Layer3({'address': acc.address,
                            'private_key': acc.private,
                            'proxy': f'http://{acc.proxy.split(":")[2]}:{acc.proxy.split(":")[3]}@{acc.proxy.split(":")[0]}:{acc.proxy.split(":")[1]}'},
                           '8e4fc64e0919bbe0f0cfd62cd745ecbd',
                           1)

        try:

            try:
                XP, AccID = L3Account.Authorize()
            except:
                try:
                    L3Account.Registration()
                except:
                    print(acc.address, '- Error with Registration 1')
                    time.sleep(random.randint(15, 25))
                    continue

                time.sleep(5)
                try:
                    XP, AccID = L3Account.Authorize()
                except:
                    print(acc.address, '- Error with Login (registration completed) 1')
                    time.sleep(random.randint(15, 25))
                    continue
            # except ReadTimeout:
            #     print(acc.address, '- Error with Login 1')
            #     time.sleep(random.randint(15, 25))
            #     continue

            record = session.query(Record).filter(Record.id == acc.id).first()
            record.XP = XP

            session.commit()

        except ProxyError:
            print('Proxy Error 1')
            time.sleep(random.randint(15, 25))
            continue

        GMS = L3Account.GMStrick()

        if GMS == None:
            pass
        elif GMS == 1010101010:
            acc.GMstrick += 1
        else:
            acc.GMstrick = GMS

        acc.date = datetime.utcnow()

        session.commit()

        # input()

        time.sleep(random.randint(10, 25))

        session.close()


def Checker():
    while True:
        Session = sessionmaker(bind=engine)
        session = Session()

        all_accs = session.query(Record).all()
        session.close()

        op = split_list(all_accs, 2)

        threads = []

        for i in op:
            thread = Thread(target=Function, args=(i,))
            thread.start()
            threads.append(thread)

        for i in threads:
            i.join()

        # input()


if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)
    Checker()



