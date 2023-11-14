import uuid

from GMStrickAuto import *


addresses = []
privates = []
proxy = []

with open('Files/Addresses.txt', 'r') as file:
    for i in file:
        addresses.append(i.rstrip())

with open('Files/Privates.txt', 'r') as file:
    for i in file:
        privates.append(i.rstrip())

with open('Files/Proxys.txt', 'r') as file:
    for i in file:
        proxy.append(i.rstrip())




Session = sessionmaker(bind=engine)
session = Session()

for i in range(len(privates)):
    rec = Record(id = str(uuid.uuid4()),
                 user = '',
                 address = addresses[i],
                 private = privates[i],
                 proxy = proxy[i],
                 GMstrick = 2,
                 NeedTasks = True
                 )
    session.add(rec)

session.commit()
session.close()

