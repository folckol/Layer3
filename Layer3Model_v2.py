import base64
import json
import random
import string
import time
from threading import Thread
from urllib.parse import urlparse
import ua_generator
from logger import logger, MultiThreadLogger
from requests.cookies import RequestsCookieJar
import capmonster_python
import requests
import cloudscraper
from eth_account.messages import encode_defunct
from web3.auto import w3
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)


def generate_random_code():
    # Генерация случайной буквы
    letter = random.choice(string.ascii_uppercase)
    digit = str(random.randint(0, 9))
    symbols = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(19))
    code = letter + digit + symbols
    return code


def generate_random_code_2():
    symbols = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(6))
    code = symbols
    return code


def generate_user_agent():
    browsers = [
        ("Chrome", random.randint(100, 114)),
        ("Firefox", random.randint(100, 114)),
        ("Safari", random.randint(10, 14)),
        ("Opera", random.randint(70, 80)),
        ("Edge", random.randint(80, 90))
    ]

    platform = random.choice(["Windows NT 10.0", "Macintosh; Intel Mac OS X 10_14_6", "X11; Linux x86_64"])

    browser, version = random.choice(browsers)
    gecko = "Gecko/20100101" if browser == "Firefox" else ""
    chrome_version = random.randint(80, 100)
    user_agent = f"Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.{random.randint(0, 999)} {gecko} {browser}/{version}"
    return user_agent


class Layer3:

    def __init__(self, accs_data, cap_key, id, logger):

        self.cookies = None
        self.logger = logger
        self.id = id
        self.cap_key = cap_key
        self.address = accs_data['address']
        self.private_key = accs_data['private_key']
        self.accs_proxy = accs_data['proxy']
        # self.tw_auth_token = accs_data['tw_auth_token']
        # self.tw_csrf = accs_data['tw_csrf']
        # self.discord_token = accs_data['discord_token']
        # self.mail = accs_data['mail']
        # self.mail_pass = accs_data['mail_pass']

        self.proxy = {'http': accs_data['proxy'], 'https': accs_data['proxy']}
        # print(accs_data['proxy'])
        self.static_sitekey = '6LddBO8eAAAAAEH9BqJaGJ-vMnO4_Sp8-TQ36RLl'

        # self.session = self._make_scraper()
        self.session = cloudscraper.create_scraper(delay=10, browser="chrome")
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.proxies = self.proxy
        self.ua = ua_generator.generate(platform="windows",browser="chrome").text
        self.session.user_agent = self.ua

        self.session.headers.update({'Content-Type': 'application/json',
                                     'X-L3-Tsit': generate_random_code_2()})

        # self.scraper = cfscrape.create_scraper(sess=self.session)

        # with self.session.get('https://layer3.xyz/quests', timeout=10) as response:
        #     print(response.text)
        #     pass

    def execute_task(self):

        skip_list = []

        for i in spList:
            for ii in i:

                response = self.session.get(f'https://layer3.xyz/quests/{ii}', cookies=self.cookies)
                # print(f"execute_task {response.text}")
                data = response.text.split('type="application/json">')[-1].split('</script>')[0]
                # print(f"data {data}")
                data = json.loads(data)

                task_ = data['props']['pageProps']['trpcState']['json']['queries'][0]['state']['data']
                # input()

                BountySteps = task_['BountySteps']
                claim = task_['id']

                if task_['namespace'] in skip_list:
                    continue

                skip_list.append(task_['namespace'])

                next = True
                self.logger.info('')
                self.logger.info(
                    f'''{self.address} | Приступаем к выполнению задач в подразделе "{task_['namespace']}"''')
                try:
                    r = self.ClaimXP(claim)
                    if r[0]['error']['json']['message'] == "You've already completed this quest!":
                        self.logger.success(f'''{self.address} | Подраздел "{task_['namespace']}" уже был заклеймлен''')

                        continue

                except:
                    pass

                for BountyStep in BountySteps:

                    try:
                        while True:
                            res = self.BountyStep(bountyStepId=BountyStep['id'],
                                                  inputData=None,
                                                  userAddressId=self.account_id)
                            if res != True:
                                if res == 'You still need to wait half a minute':
                                    time.sleep(random.randint(30, 40))
                                elif res == 'You still need to wait less than 5 seconds':
                                    time.sleep(random.randint(5, 15))
                                elif res == 'You still need to wait less than 10 seconds':
                                    time.sleep(random.randint(10, 20))
                                elif res == 'You still need to wait less than 20 seconds':
                                    time.sleep(random.randint(20, 30))
                                elif res == 'You still need to wait less than 40 seconds':
                                    time.sleep(random.randint(40, 50))
                                elif res == 'You still need to wait less than 50 seconds':
                                    time.sleep(random.randint(50, 60))
                                elif res == 'You still need to wait less than a minute':
                                    time.sleep(random.randint(60, 75))

                                elif res == 'Invalid input data':
                                    res = self.BountyStep(bountyStepId=BountyStep['id'],
                                                          inputData={
                                                              "answers": [
                                                                  {"questionUuid": "q1", "selectedChoices": ["a5"]},
                                                                  {"questionUuid": "q2",
                                                                   "selectedChoices": ["a1"]}]},
                                                          userAddressId=self.account_id)
                                    if res != True:
                                        if res == 'You still need to wait half a minute':
                                            time.sleep(random.randint(30, 40))
                                        elif res == 'You still need to wait less than 5 seconds':
                                            time.sleep(random.randint(5, 15))
                                        elif res == 'You still need to wait less than 10 seconds':
                                            time.sleep(random.randint(10, 20))
                                        elif res == 'You still need to wait less than 20 seconds':
                                            time.sleep(random.randint(20, 30))
                                        elif res == 'You still need to wait less than 40 seconds':
                                            time.sleep(random.randint(40, 50))
                                        elif res == 'You still need to wait less than 50 seconds':
                                            time.sleep(random.randint(50, 60))
                                        elif res == 'You still need to wait less than a minute':
                                            time.sleep(random.randint(60, 75))
                                        else:
                                            print(res)
                                            self.logger.error(
                                                f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task_['namespace']}". Ошибка - {res}''')
                                            next = False
                                            break

                                    self.logger.success(
                                        '{} | Задание {} выполнено'.format(self.address, BountyStep['id']))
                                    break



                                else:

                                    self.logger.error(
                                        f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task_['namespace']}". Ошибка - {res}''')
                                    next = False
                                    break

                            self.logger.success('{} | Задание {} выполнено'.format(self.address, BountyStep['id']))
                            break

                        if next == False:
                            break

                    except:
                        self.logger.error(
                            f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task_['namespace']}"''')
                        next = False
                        break

                    time.sleep(random.randint(2, 15))

                if next:
                    fastSkip = None

                    r = self.ClaimXP(claim)
                    try:
                        if r[0]['error']['json']['message'] == "You've already completed this quest!":
                            self.logger.success(
                                f'''{self.address} | Подраздел "{task_['namespace']}" уже был заклеймлен''')
                        elif r[0]['error']['json']['message'] == "You do not have the required achievement!":
                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - Не достигнут лвл для полоучения награды''')
                            fastSkip = True
                        elif r[0]['error']['json']['message'] == "You have not completed all steps!":
                            self.logger.success(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" Вы не прошли все задания''')
                        elif r[0]['error']['json']['message'] == "You are not authenticated!":
                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - Слетела авторизация''')
                            self.Authorize()
                        else:
                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - {r[0]['error']['json']['message']}''')

                    except:

                        try:

                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - {r[0]['error']['json']['message']}''')

                        except:
                            self.logger.success(
                                f'''{self.address} | Успешно заклеймили подраздел "{task_['namespace']}"''')

                    if not fastSkip:
                        time.sleep(random.randint(5, 10))

        with self.session.get(
                'https://layer3.xyz/api/trpc/config.globalAnnouncement,journey.listJourneys,collection.getCollections,collection.getIntroCollection,task.getFeaturedTasks,task.newTasksForUser,task.getLevelGatedTasks,walletModal.getDefaultConnectOptionIds,user.me?batch=1&input=%7B%220%22%3A%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D%2C%221%22%3A%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D%2C%222%22%3A%7B%22json%22%3A%7B%22isFeatured%22%3Atrue%7D%7D%2C%223%22%3A%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D%2C%224%22%3A%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D%2C%225%22%3A%7B%22json%22%3A%7B%22cursor%22%3A0%7D%7D%2C%226%22%3A%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D%2C%227%22%3A%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D%2C%228%22%3A%7B%22json%22%3Anull%2C%22meta%22%3A%7B%22values%22%3A%5B%22undefined%22%5D%7D%7D%7D', cookies=self.cookies) as response:
            result = response.json()
            # pprint(result)
            # input()

        nextCursor = result[-4]['result']['data']['json']['nextCursor']

        for task in result[2]['result']['data']['json']:

            taskName = task['name']
            tasks_ = task['tasks']
            self.logger.warning('')
            self.logger.info(f'{self.address} | Приступаем к подразделам в разделе "{taskName}"')

            for task_ in tasks_:
                BountySteps = task_['BountySteps']
                claim = task_['id']

                if task_['namespace'] in skip_list:
                    continue

                skip_list.append(task_['namespace'])

                next = True
                self.logger.info('')
                self.logger.info(
                    f'''{self.address} | Приступаем к выполнению задач в подразделе "{task_['namespace']}"''')
                try:
                    r = self.ClaimXP(claim)
                    if r[0]['error']['json']['message'] == "You've already completed this quest!":
                        self.logger.success(f'''{self.address} | Подраздел "{task_['namespace']}" уже был заклеймлен''')

                        continue

                except:
                    pass

                for BountyStep in BountySteps:

                    try:
                        while True:
                            res = self.BountyStep(bountyStepId=BountyStep['id'],
                                                  inputData=None,
                                                  userAddressId=self.account_id)
                            if res != True:
                                if res == 'You still need to wait half a minute':
                                    time.sleep(random.randint(30, 40))
                                elif res == 'You still need to wait less than 5 seconds':
                                    time.sleep(random.randint(5, 15))
                                elif res == 'You still need to wait less than 10 seconds':
                                    time.sleep(random.randint(10, 20))
                                elif res == 'You still need to wait less than 20 seconds':
                                    time.sleep(random.randint(20, 30))
                                elif res == 'You still need to wait less than 40 seconds':
                                    time.sleep(random.randint(40, 50))
                                elif res == 'You still need to wait less than 50 seconds':
                                    time.sleep(random.randint(50, 60))
                                elif res == 'You still need to wait less than a minute':
                                    time.sleep(random.randint(60, 75))

                                elif res == 'Invalid input data':
                                    res = self.BountyStep(bountyStepId=BountyStep['id'],
                                                          inputData={"answers": [
                                                              {"questionUuid": "q1", "selectedChoices": ["a5"]},
                                                              {"questionUuid": "q2", "selectedChoices": ["a1"]}]},
                                                          userAddressId=self.account_id)
                                    if res != True:
                                        if res == 'You still need to wait half a minute':
                                            time.sleep(random.randint(30, 40))
                                        elif res == 'You still need to wait less than 5 seconds':
                                            time.sleep(random.randint(5, 15))
                                        elif res == 'You still need to wait less than 10 seconds':
                                            time.sleep(random.randint(10, 20))
                                        elif res == 'You still need to wait less than 20 seconds':
                                            time.sleep(random.randint(20, 30))
                                        elif res == 'You still need to wait less than 40 seconds':
                                            time.sleep(random.randint(40, 50))
                                        elif res == 'You still need to wait less than 50 seconds':
                                            time.sleep(random.randint(50, 60))
                                        elif res == 'You still need to wait less than a minute':
                                            time.sleep(random.randint(60, 75))
                                        else:
                                            print(res)
                                            self.logger.error(
                                                f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task_['namespace']}". Ошибка - {res}''')
                                            next = False
                                            break

                                    self.logger.success(
                                        '{} | Задание {} выполнено'.format(self.address, BountyStep['id']))
                                    break



                                else:

                                    self.logger.error(
                                        f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task_['namespace']}". Ошибка - {res}''')
                                    next = False
                                    break

                            self.logger.success('{} | Задание {} выполнено'.format(self.address, BountyStep['id']))
                            break

                        if next == False:
                            break

                    except:
                        self.logger.error(
                            f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task_['namespace']}"''')
                        next = False
                        break

                    time.sleep(random.randint(2, 15))

                if next:
                    fastSkip = None

                    r = self.ClaimXP(claim)
                    try:
                        if r[0]['error']['json']['message'] == "You've already completed this quest!":
                            self.logger.success(
                                f'''{self.address} | Подраздел "{task_['namespace']}" уже был заклеймлен''')
                        elif r[0]['error']['json']['message'] == "You do not have the required achievement!":
                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - Не достигнут лвл для полоучения награды''')
                            fastSkip = True
                        elif r[0]['error']['json']['message'] == "You have not completed all steps!":
                            self.logger.success(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" Вы не прошли все задания''')
                        elif r[0]['error']['json']['message'] == "You are not authenticated!":
                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - Слетела авторизация''')
                            self.Authorize()
                        else:
                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - {r[0]['error']['json']['message']}''')

                    except:

                        try:

                            self.logger.error(
                                f'''{self.address} | Ошибка в подразделе "{task_['namespace']}" - {r[0]['error']['json']['message']}''')

                        except:
                            self.logger.success(
                                f'''{self.address} | Успешно заклеймили подраздел "{task_['namespace']}"''')

                    if not fastSkip:
                        time.sleep(random.randint(5, 10))

        while nextCursor:

            with self.session.get(
                    f'https://layer3.xyz/api/trpc/task.newTasksForUser?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22cursor%22%3A{nextCursor}%7D%7D%7D', cookies=self.cookies) as response:
                try:
                    nextCursor = response.json()[0]['result']['data']['json']['nextCursor']
                except:
                    # print(response.text)
                    self.Authorize()

                    with self.session.get(
                            f'https://layer3.xyz/api/trpc/task.newTasksForUser?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22cursor%22%3A{nextCursor}%7D%7D%7D',
                            cookies=self.cookies) as response:
                        try:
                            nextCursor = response.json()[0]['result']['data']['json']['nextCursor']
                        except:
                            print(response.text)

                # print(nextCursor)

                for task in response.json()[0]['result']['data']['json']['items']:

                    BountySteps = task['BountySteps']
                    claim = task['id']

                    if task['namespace'] in skip_list:
                        continue

                    skip_list.append(task['namespace'])

                    next = True
                    self.logger.info('')
                    self.logger.info(
                        f'''{self.address} | Приступаем к выполнению задач в подразделе "{task['namespace']}"''')
                    try:
                        r = self.ClaimXP(claim)
                        if r[0]['error']['json']['message'] == "You've already completed this quest!":
                            self.logger.success(
                                f'''{self.address} | Подраздел "{task['namespace']}" уже был заклеймлен''')
                            continue
                    except:
                        pass

                    for BountyStep in BountySteps:

                        try:
                            while True:
                                res = self.BountyStep(bountyStepId=BountyStep['id'],
                                                      inputData=None,
                                                      userAddressId=self.account_id)
                                if res != True:
                                    if res == 'You still need to wait half a minute':
                                        time.sleep(random.randint(30, 40))
                                    elif res == 'You still need to wait less than 5 seconds':
                                        time.sleep(random.randint(5, 15))
                                    elif res == 'You still need to wait less than 10 seconds':
                                        time.sleep(random.randint(10, 20))
                                    elif res == 'You still need to wait less than 20 seconds':
                                        time.sleep(random.randint(20, 30))
                                    elif res == 'You still need to wait less than 40 seconds':
                                        time.sleep(random.randint(40, 50))
                                    elif res == 'You still need to wait less than 50 seconds':
                                        time.sleep(random.randint(50, 60))
                                    elif res == 'You still need to wait less than a minute':
                                        time.sleep(random.randint(60, 75))

                                    elif res == 'Invalid input data':
                                        res = self.BountyStep(bountyStepId=BountyStep['id'],
                                                              inputData={"answers": [
                                                                  {"questionUuid": "q1", "selectedChoices": ["a5"]},
                                                                  {"questionUuid": "q2",
                                                                   "selectedChoices": ["a1"]}]},
                                                              userAddressId=self.account_id)
                                        if res != True:
                                            if res == 'You still need to wait half a minute':
                                                time.sleep(random.randint(30, 40))
                                            elif res == 'You still need to wait less than 5 seconds':
                                                time.sleep(random.randint(5, 15))
                                            elif res == 'You still need to wait less than 10 seconds':
                                                time.sleep(random.randint(10, 20))
                                            elif res == 'You still need to wait less than 20 seconds':
                                                time.sleep(random.randint(20, 30))
                                            elif res == 'You still need to wait less than 40 seconds':
                                                time.sleep(random.randint(40, 50))
                                            elif res == 'You still need to wait less than 50 seconds':
                                                time.sleep(random.randint(50, 60))
                                            elif res == 'You still need to wait less than a minute':
                                                time.sleep(random.randint(60, 75))
                                            else:

                                                self.logger.error(
                                                    f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task['namespace']}". Ошибка - {res}''')
                                                next = False
                                                break

                                        self.logger.success(
                                            '{} | Задание {} выполнено'.format(self.address, BountyStep['id']))
                                        break



                                    else:

                                        self.logger.error(
                                            f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task['namespace']}". Ошибка - {res}''')
                                        next = False
                                        break

                                self.logger.success('{} | Задание {} выполнено'.format(self.address, BountyStep['id']))
                                break

                            if next == False:
                                break

                        except:
                            self.logger.error(
                                f'''{self.address} | Задание {BountyStep["id"]} не выполнено, пропускаем подраздел "{task['namespace']}"''')
                            next = False
                            break

                        time.sleep(random.randint(2, 15))

                    if next:
                        fastSkip = None

                        r = self.ClaimXP(claim)
                        try:
                            if r[0]['error']['json']['message'] == "You've already completed this quest!":
                                self.logger.success(
                                    f'''{self.address} | Подраздел "{task['namespace']}" уже был заклеймлен''')
                            elif r[0]['error']['json']['message'] == "You do not have the required achievement!":
                                self.logger.error(
                                    f'''{self.address} | Ошибка в подразделе "{task['namespace']}" - Не достигнут лвл для полоучения награды''')
                                fastSkip = True
                            elif r[0]['error']['json']['message'] == "You are not authenticated!":
                                self.logger.error(
                                    f'''{self.address} | Ошибка в подразделе "{task['namespace']}" - Слетела авторизация''')
                                self.Authorize()
                            else:
                                self.logger.error(
                                    f'''{self.address} | Ошибка в подразделе "{task['namespace']}" - {r[0]['error']['json']['message']}''')

                        except:

                            try:

                                self.logger.error(
                                    f'''{self.address} | Ошибка в подразделе "{task['namespace']}" - {r[0]['error']['json']['message']}''')

                            except:
                                self.logger.success(
                                    f'''{self.address} | Успешно заклеймили подраздел "{task['namespace']}"''')

                        if not fastSkip:
                            time.sleep(random.randint(5, 10))

        # with self.session.get('https://layer3.xyz/_next/data/xvG8qcZek3W990h8yzppA/quests/bridge-to-base-mainnet.json?namespace=bridge-to-base-mainnet') as response:
        #     ...

    def BountyStep(self, bountyStepId, inputData, userAddressId):

        # with self.session.post('https://layer3.xyz/api/trpc/track.questView?batch=1', json={"0":{"json":{"namespace":"beyond-ethereum-1"}}}, timeout=10 ) as response:
        #     print(response.text)

        if inputData:

            try:
                for i in inputData['answers']:
                    i['selectedChoices'] = [f"a{random.randint(1, 4)}"]
            except:
                pass

            payload = {
                "0": {"json": {"bountyStepId": bountyStepId, "inputData": inputData, "userAddressId": userAddressId}}}

            with self.session.post('https://layer3.xyz/api/trpc/bountyStep.completeBountyStep?batch=1', json=payload, cookies=self.cookies,
                                   timeout=30) as response:
                # print(response.text)
                if response.status_code == 400:
                    return response.json()[0]['error']['json']['message']
                else:
                    return True
        else:
            payload = {
                "0": {"json": {"bountyStepId": bountyStepId, "inputData": inputData, "userAddressId": userAddressId},
                      "meta": {"values": {"inputData": ["undefined"]}}}}

            with self.session.post('https://layer3.xyz/api/trpc/bountyStep.completeBountyStep?batch=1', json=payload, cookies=self.cookies,
                                   timeout=30) as response:
                if response.status_code == 400:
                    return response.json()[0]['error']['json']['message']
                else:
                    return True

    def ClaimXP(self, taskId):

        payload = {"0": {"json": {"taskId": taskId}}}

        try:
            with self.session.post('https://layer3.xyz/api/trpc/bountyClaim.claimTask?batch=1', json=payload, cookies=self.cookies,
                                   timeout=30) as response:

                return response.json()
        except:
            try:
                with self.session.post('https://layer3.xyz/api/trpc/bountyClaim.claimTask?batch=1', json=payload, cookies=self.cookies,
                                       timeout=30) as response:
                    return response.json()
            except:
                pass

    # def EmailVerif(self, email, emailPass):
    #
    #     payload = {"0":{"json":{"email":email}}}
    #
    #     with self.session.post('https://layer3.xyz/api/trpc/user.addEmail?batch=1', json=payload,
    #                            timeout=30) as response:
    #         # print(response.text)
    #         pass
    #
    #     time.sleep(5)
    #
    #     link = get_last_mail(email, emailPass)
    #
    #     self.session.get(link, timeout=10)
    #
    #     time.sleep(2)

    def GMStrick(self):

        payload = {"0": {"json": {"timezoneOffset": 0, "markXpActivityAsSeen": True}}}

        try:
            with self.session.post('https://layer3.xyz/api/trpc/gm.addGm?batch=1', json=payload, cookies=self.cookies,
                                   timeout=10) as response:
                # print(response.text)
                if response.text == '[{"result":{"data":{"json":1}}}]':
                    self.logger.success('Success GM')
                    return 1010101010

                elif response.text == '''[{"error":{"json":{"message":"You've already GM'd today","code":-32600,"data":{"code":"BAD_REQUEST","httpStatus":400,"path":"gm.addGm"}}}}]''':
                    self.logger.success("Already GM'd today")
                    return 1

                else:

                    try:
                        d = response.json()[0]['result']['data']['json']['newStreak']
                        self.logger.success('Success GM', d)
                        return d
                    except:

                        print(response.text)
                        return None
        except:
            print('Proxy Error')
            return None

    def Captcha_Solver(self):
        cap = capmonster_python.RecaptchaV2Task(self.cap_key)
        tt = cap.create_task("https://layer3.xyz/", self.static_sitekey)
        captcha = cap.join_task_result(tt)
        captcha = captcha["gRecaptchaResponse"]
        return captcha

    def GetNonce(self):

        self.code = generate_random_code()

        status = self.get_cf_clearance()
        # print(status, '11')
        if status:
            # self.logger.info(f"{self.address} | cf_clearance успешно получен")
            # print(self.cf_clearance)

            self.session.headers.update({
                'authority': 'layer3.xyz',
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/json',
                'origin': 'https://layer3.xyz',
                'referer': 'https://layer3.xyz/quests',
                'sec-ch-ua': '',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
            })

            params = {
                'batch': '1',
            }

            json_data = {"0":
                       {"json": None,
                        "meta":
                            {"values": ["undefined"]}
                        }, "1":
                       {"json":
                            {"connectIntentId": self.code,
                             "data":
                                 {"strategy": "injected",
                                  "buttonName": "MetaMask",
                                  "browser": "Chrome",
                                  "os": "Windows",
                                  "didConnect": True,
                                  "connectedWalletConnector": "INJECTED",
                                  "connectedWalletName": "MetaMask"}}}}

            response = self.session.post(
                'https://layer3.xyz/api/trpc/auth.getWalletSignatureNonce,track.walletModal',
                params=params,
                json=json_data,
                cookies=self.cookies
            )
            # print(f"text nonce {response.text}")
            # print(response.text)
            return response.json()[0]['result']['data']['json']
        else:
            # self.logger.error(f"{self.address} | Ошибка получения cf_clearance")
            return None

    def get_cf_clearance(self):
        site_key = "0x4AAAAAAADnPIDROrmt1Wwj"
        action = "managed"
        cData = "7f21b9d64af9994b"
        chlPageData = "3gAFo2l2MbhiYk52ZWJJdHkxOXpnVnI2eXdKYkJRPT2jaXYyuGVlcS9LNGVEZzZscEJ2VVhWemJrcFE9PaFk2gEAZk5FcFhzTkdzNmxSL2ZHS3hXeTBMWEUxSTFidlpaMy9uM2RuMnYrQk84clNqeXE2R01qU2p1OFBSVHV1SEFlTDZtdmxBZDRMbUs4Z253UUdyUmFYQnJVbGgzOGc1RkNCR0FTaDh1b09qa3pwSUdVc3BCQnlBWnFqMzVMVkc3NW5zUDVYRm15bDdBclhSRFRRVWNPTnptTTFPTXJFWVhyNmRiNGZ0NkV4R1d4K0N4Q2ZIdG9Td2cxSC8zQkorOFpOQ2VyOFVoNDRqRjlrUzNTTUQvUzJ1V1pweHVRdEFEMU1kakszOVc3VGZyTzFkb0R1bWlIYmZlMERSVVFJTk1hUKFt2SxVd0tjdGQrTG8vQjgvbmpROUdDZ01pbzNUQ0dMSzhVck9jTXBUU2JGNXVjPaF0tE1UWTVNVEkyTmpnek15NDRNRGs9"
        url = "https://layer3.xyz/quests"

        response = self.session.get("https://layer3.xyz/quests")
        if '<head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0' in response.text:
            return True

        html_base64_encoded = base64.b64encode(response.text.encode('utf-8')).decode('utf-8')

        # print(html_base64_encoded)
        proxy_url = self.accs_proxy
        parsed = urlparse(proxy_url)

        proxy_ip = parsed.hostname
        proxy_port = parsed.port
        proxy_log, proxy_pass = parsed.username, parsed.password

        json = {
            "clientKey": self.cap_key,
            "task": {
                "type": "TurnstileTask",
                "websiteURL": url,
                "websiteKey": site_key,
                "proxyType": "http",
                "proxyAddress": proxy_ip,
                "proxyPort": proxy_port,
                "proxyLogin": proxy_log,
                "proxyPassword": proxy_pass,
                "cloudflareTaskType": "cf_clearance",
                "htmlPageBase64": html_base64_encoded,
                "userAgent": self.ua,
                "pageAction": action,
                "data": cData,
                "pageData": chlPageData
            }
        }

        # pprint(json)

        while True:
            with self.session.post("https://api.capmonster.cloud/createTask", json=json, timeout=60) as response:
                # print(response.text)
                # print(response.json())
                taskId = response.json()['taskId']
                # print(taskId)

            time.sleep(5)

            json1 = {
                "clientKey": self.cap_key,
                "taskId": taskId
            }

            res = False

            while True:
                with self.session.post("https://api.capmonster.cloud/getTaskResult/", json=json1, timeout=60) as response:
                    result = response.json()
                    # print(response.text)
                    # print(result)

                    if result['errorId'] == 0 and result['status'] == "ready":
                        # self.logger.info(f"Result: {result}")
                        self.cf_clearance = result['solution']['cf_clearance']
                        res = True
                        break

                    elif result['errorId'] != 0:
                        # print(response.text)
                        break
                    # Wait for 3 seconds before sending the next request
                    time.sleep(5)

            if res == True:
                break
        # print('True, 111')

        self.cookies = {
            'cf_clearance': self.cf_clearance,
        }

        return True

    def Registration(self):

        self.nonce = self.GetNonce()

        # print(f'Layer3 One-Time Key: {self.nonce}')

        message = encode_defunct(text=self._get_message_to_sign(self.nonce))
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        self.signature = signed_message["signature"].hex()

        payload = {"0": {"json": {"address": self.address,
                                  "signedMessage": self.signature,
                                  "nonce": self.nonce,
                                  "captchaValue": self.Captcha_Solver(),
                                  "referralCode": None,
                                  "walletMetadata":
                                      {"walletName": "MetaMask", "connectorType": "INJECTED", "os": "Windows",
                                       "browser": "Chrome"},
                                  "chainId": 1,
                                  "baseNetwork": "EVM"}}}

        # print(payload)

        with self.session.post('https://layer3.xyz/api/trpc/auth.login?batch=1', json=payload, cookies=self.cookies,
                               timeout=30) as response:
            # print(f"text reg {response.text}")

            cookie = {'name': 'layer3_access_token',
                      'value': response.json()[0]['result']['data']['json']['accessToken'], 'domain': '.layer3.xyz'}
            # print(cookie)
            requests_cookie = RequestsCookieJar()
            requests_cookie.set(**cookie)
            self.session.cookies.update(requests_cookie)

            return "reg", response.json()[0]['result']['data']['json']['user']['UserAddresses'][0]['id']


    def Authorize(self):

        self.nonce = self.GetNonce()

        print(time.time() - start_time)
        input()

        # print(f'Layer3 One-Time Key: {self.nonce}')

        message = encode_defunct(text=self._get_message_to_sign(self.nonce))
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        self.signature = signed_message["signature"].hex()

        payload = {"0": {"json": {"connectIntentId": self.code,
                                  "data": {"strategy": "injected",
                                           "buttonName": "MetaMask",
                                           "browser": "Chrome",
                                           "os": "Windows",
                                           "didConnect": True,
                                           "connectedWalletConnector": "INJECTED",
                                           "connectedWalletName": "MetaMask",
                                           "didSign": True}}},
                   "1": {"json": {"address": self.address,
                                  "signedMessage": self.signature,
                                  "baseNetwork": "EVM",
                                  "chainId": 1,
                                  "nonce": self.nonce,
                                  "captchaValue": None,
                                  "referralCode": None,
                                  "walletMetadata": {"walletName": "MetaMask",
                                                     "connectorType": "INJECTED",
                                                     "os": "Windows",
                                                     "browser": "Chrome"}},
                         "meta": {"values": {"captchaValue": ["undefined"]}}}}

        # print(payload)

        with self.session.post('https://layer3.xyz/api/trpc/track.walletModal,auth.login?batch=1', json=payload, cookies=self.cookies,
                               timeout=30) as response:
            # print(f"{response.text}")



            try:
                cookie = {'name': 'layer3_access_token',
                          'value': response.json()[1]['result']['data']['json']['accessToken'], 'domain': '.layer3.xyz'}
                requests_cookie = RequestsCookieJar()
                requests_cookie.set(**cookie)
                self.session.cookies.update(requests_cookie)

                self.account_id = response.json()[1]['result']['data']['json']['user']['IdentityAddress']['id']
                xp = response.json()[1]['result']['data']['json']['user']['xp']
                # print(self.account_id)
                # logger.info(f"Account ID: {self.account_id} | XP: {xp}")
                return response.json()[1]['result']['data']['json']['user']['xp'], \
                    response.json()[1]['result']['data']['json']['user']['IdentityAddress']['id']
            except:
                return self.Registration()


    def _get_message_to_sign(self, nonce) -> str:
        return f"Layer3 One-Time Key: {nonce}"

    # def _make_scraper(self):
    #     ssl_context = ssl.create_default_context()
    #     ssl_context.set_ciphers(
    #         "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
    #         "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
    #         "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
    #         "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
    #         "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
    #         "AECDH-AES128-SHA:AECDH-AES256-SHA"
    #     )
    #     ssl_context.set_ecdh_curve("prime256v1")
    #     ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
    #     ssl_context.check_hostname = False
    #
    #     return cloudscraper.create_scraper(
    #         debug=False,
    #         ssl_context=ssl_context
    #     )


def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return (lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def Thread_(data, numb):
    logger = MultiThreadLogger(numb)

    count = 0
    while count < len(data):
        time.sleep(random.randint(50, 150) / 100)
        print(f'В работе {data[count][0]}')

        global start_time
        start_time = time.time()

        LA = Layer3({'address': data[count][0],
                     'private_key': data[count][1],
                     'proxy': f'http://{data[count][2].split(":")[2]}:{data[count][2].split(":")[3]}@{data[count][2].split(":")[0]}:{data[count][2].split(":")[1]}'},
                    capKey,
                    count + 1,
                    logger)


        xp, account_id = LA.Authorize()
        if xp == "reg":
            LA = Layer3({'address': data[count][0],
                         'private_key': data[count][1],
                         'proxy': f'http://{data[count][2].split(":")[2]}:{data[count][2].split(":")[3]}@{data[count][2].split(":")[0]}:{data[count][2].split(":")[1]}'},
                        capKey,
                        count + 1,
                        logger)

            xp, account_id = LA.Authorize()

        logger.success(f'{data[count][0]} | Авторизация прошла успешно')
        logger.success(f'{data[count][0]} | На аккаунте {xp} xp, ID - {account_id}')

        LA.execute_task()
        count += 1


if __name__ == '__main__':



    capKey = ''
    threadsCount = 1

    addresses = []
    privates = []
    proxy = []

    with open('InputData/proxy.txt') as file:
        for i in file:
            proxy.append(i.rstrip())

    with open('InputData/privates.txt') as file:
        for i in file:
            privates.append(i.rstrip())

    with open('InputData/addresses.txt') as file:
        for i in file:
            addresses.append(i.rstrip())

    try:
        with open('config') as file:
            for i in file:
                if 'capKey' in i.rstrip():
                    capKey = i.rstrip().replace('capKey=', '')
                elif 'threadsCount' in i.rstrip():
                    threadsCount = int(i.rstrip().replace('threadsCount=', ''))
    except:
        print('Вы неправильно настроили конфиг')
        input('')
        exit(1)

    spList = []
    with open('InputData/specialQuests.txt') as file:
        local = []
        for i in file:
            if i.rstrip() == '':
                spList.append(local)
                local = []
            else:
                local.append(i.rstrip())

    # print(spList)

    fullData = []
    count = 0
    while count < len(addresses):
        fullData.append([addresses[count], privates[count], proxy[count]])
        count += 1

    allThreads = split_list(fullData, threadsCount)

    c = 0
    threads = []
    for i in allThreads:
        thr = Thread(target=Thread_, args=(i, c))
        threads.append(thr)
        c += 1

    for i in threads:
        i.start()

    for i in threads:
        i.join()

    input('\n\nСкрипт успешно завершил работу')
