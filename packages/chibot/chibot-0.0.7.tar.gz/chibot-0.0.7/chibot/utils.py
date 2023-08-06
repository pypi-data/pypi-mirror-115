import re
import random
import datetime


class Utils:

    def __init__(self, funcList, name=''):
        self.name = name
        self.funcList = {
            "time": self.time,
            "date": self.date,
            "wish": self.wish,
            "week": self.weekName,
            "name": self.userName,
            "changeName": self.changeName
        }
        self.funcList.update(funcList)

    def normalize_utterances(self, utterances):
        normalized = ''
        for u in utterances:
            u = re.sub('\\W+', ' ', u)
            normalized += u.lower().strip() + '|'

        return normalized[:-1]

    def match_utterances(self, voice_input, utterances):
        # self.logger.info('Normalizing utterances')
        normalized = self.normalize_utterances(utterances)
        compiles = re.compile(normalized)
        value = compiles.search(voice_input)
        return value

    def choose_response(self, response):
        return random.choice(response)

    def wish(self, query=''):
        hours = datetime.datetime.now().hour
        if 0 <= hours <= 12:
            greeting = 'Good morning'
        elif 12 < hours <= 18:
            greeting = 'Good afternoon'
        else:
            greeting = 'Good evening'

        if query in greeting.lower():
            print(greeting)
        elif 'good night' in query or 'night' in query:
            print('Good night sir..')
        else:
            if query:
                print('It is ' + greeting.replace('Good ', '') + ' Sir..!')
            else:
                print(f'{greeting} boss,')

    def time(self, *args):
        hours = datetime.datetime.now().hour
        minu = datetime.datetime.now().minute

        am_pm = ' PM' if hours > 12 else ' AM'

        if hours > 12:
            hours -= 12
        houTe = 'hours' if hours > 1 else 'hour'
        minTe = 'minutes' if minu > 1 else 'minute'

        nowTime = 'It is ' + (str(hours) + ' ' + houTe if hours > 0 else '12') + \
                  ' and ' + str(minu) + ' ' + minTe + am_pm
        print(nowTime)
        return nowTime

    def date(self, week=False, *args):
        date = datetime.datetime.now().day
        month = datetime.datetime.now().strftime("%B")
        weekN = datetime.datetime.now().strftime("%A")

        speakWeek = f' and {weekN}' if week else ''

        today = str(date) + ' ' + month

        print('Today is ' + today + '. ' + speakWeek)

    def weekName(self, *args):
        week = datetime.datetime.now().strftime("%A")
        print(week)

    def userName(self, *args):
        if self.name:
            print('Hi ' + self.name)
        else:
            print('Please tell me your name.')
            output = input().lower()
            output.replace('my name is ', '').replace(
                ' is my name', '').replace("i'm ", '').replace('i am ', '')
            self.name = output.capitalize()
            print('Ok ' + self.name + ", I'll remember your name")

    def changeName(self, *args):
        print('Please tell me your name.')
        output = input().lower()
        output.replace('my name is ', '').replace(
            ' is my name', '').replace("i'm ", '').replace('i am ', '')
        self.name = output.capitalize()
        print('Ok ' + self.name + ", I'll remember your name")

    def funExecutor(self, key, query=''):
        run = False
        func = ''
        for execute in key['execution']:
            if execute['options'] == 'every':

                func = execute['execute']
                try:
                    self.funcList[func](query)
                except:
                    print("Unable to find function")
                if 'only' in execute:
                    run = True
            else:
                for option in execute['options']:
                    if option in query:
                        run = True
                        func = execute['execute']
                        if run and func:
                            try:
                                self.funcList[func](query)
                            except:
                                print("Unable to find function")
                        break

            if run:
                break
