from fuzzywuzzy import fuzz
from random import choice, randint
import sys
import os

def clear():
    system = sys.platform
    operation = 'clear'
    if system == 'win32':
        operation = 'cls'
    os.system(operation)

class Dreamer():

    def __init__(self):
        self.vocabulary = []
        self.trained = []
        self.last = None
    
    def display(self):
        for train in self.trained:
            print(f'✅ Trained {train}')

    def train(self, file:str='vocabulary.dream'):
        with open(file, 'r', encoding='utf-8') as dataset:
            for line in dataset.read().splitlines():
                self.vocabulary.append(line)
        clear()
        self.trained.append(file)
        self.display()
    
    def listrain(self, source: list):
        for item in source:
            self.vocabulary.append(item)
        clear()
        self.trained.append('List')
        self.display()

    def dream(self, request: str):
        biggest_index = 0
        biggest_match = 0
        for data in self.vocabulary:
            matching = fuzz.ratio(data, request)
            if matching > biggest_match:
                biggest_index = self.vocabulary.index(data)
                biggest_match = matching
        ops = []
        counter = 0
        for data in self.vocabulary:
            if data == self.vocabulary[biggest_index]:
                try:
                    pos = self.vocabulary.index(data, counter, len(self.vocabulary)-1)
                    ops.append(self.vocabulary[pos + 1])
                    counter = pos + 1
                except:
                    pos = self.vocabulary.index(data)
                    ops.append(self.vocabulary[pos - 1])
        response = choice(ops)
        self.last = response
        return response

    def learn(self, request: str, response: str=None, file='general.dream'):
        if response == None:
            response = self.last
        for l in self.vocabulary:
            if request == l:
                return
        base = ''
        with open(file, 'r', encoding='utf-8') as dataset:
            base = dataset.read()
        with open(file, 'w', encoding='utf-8') as dataset:
            if self.last == None and response == None:
                self.last = choice(self.vocabulary)
                response = self.last
            if response == 'null':
                dataset.write(f'{base}\n{request}'.lstrip().rstrip())
            else:
                dataset.write(f'{base}\n{response}\n{request}'.lstrip().rstrip())

    def reload(self, file:str='general.dream'):
        self.vocabulary.clear()
        with open(file, 'r', encoding='utf-8') as dataset:
            for line in dataset.read().splitlines():
                self.vocabulary.append(line)

if __name__ == '__main__':
    d = Dreamer()
    d.listrain(['oi', 'olá', 'boa noite', 'tudo bem?'])
    d.train('policy22.dream')
    d.listrain(['att', 'wtf'])
    while True:
        req = input('Você: ')
        #d.learn(req, 'general.dream')
        rp = d.dream(req)
        print(rp)
        #d.reload('general.dream')