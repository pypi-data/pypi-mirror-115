from utils.utils import Utils
import json


class ChiBot():

    def __init__(self, funcList={}):
        try:
            with open('./chi-config.json') as config:
                self.config = json.load(config)
        except:
            self.config = {"name": "Chi Chi",
                           "conversations": []}
        self.utils = Utils(funcList)

    def run(self):

        while True:
            msg = input()
            for i in ['bye', 'good bye', 'exit']:
                if i in msg.lower():
                    print('Bye, have a nice day..')
                    exit()

            for key in self.config['conversations']:
                match = self.utils.match_utterances(msg, key['utterances'])
                if match:
                    break

            if 'responses' in key:
                response = self.utils.choose_response(key['responses'])
                print(response)

            if 'execution' in key:
                self.utils.funExecutor(key, msg)


ChiBot({}).run()
