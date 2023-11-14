import uuid

from GMStrickAuto import *

Session = sessionmaker(bind=engine)
session = Session()

accs = session.query(Record).all()
for acc in accs:
    print(acc.address, acc.XP)

# session.commit()
session.close()
