import json
import uuid

from GMStrickAuto import *


tasks = []

with open('Files/Tasks.txt', 'r') as file:
    for i in file:
        tasks.append(i.rstrip())


Session = sessionmaker(bind=engine)
session = Session()

for i in tasks:

    name = i.split('|')[0]
    tasks_ = i.split('|')[1].split('---')[:-1]
    claimTask = i.split('|')[1].split('---')[-1]

    print(tasks_, claimTask)

    task = Task(name=name)

    BSs = []
    for k in tasks_:
        try:
            data = json.loads(k)
            BS = BountyStep(bounty_step_id = data['0']['json']['bountyStepId'],
                            input_data = None if data['0']['json']['inputData'] == None else json.dumps(data['0']['json']['inputData']),
                            user_address_id = data['0']['json']['userAddressId'])
            BSs.append(BS)
        except KeyError:
            print(data)

    task.bounty_steps = BSs

    BC = BountyClaim(TaskID=json.loads(claimTask)['0']['json']['taskId'])
    task.bounty_claims = [BC]

    session.add(task)
    session.commit()

session.close()

