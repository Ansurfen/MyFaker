import os
import random
import json
import yaml
from faker.providers import BaseProvider

diyfile = './random.yml'
df = 'def none(self):\n\treturn\n'


if os.path.exists(diyfile):
    result = yaml.load(open('random.yml'), Loader=yaml.FullLoader)
    for class_name in result:
        func = 'def ' + class_name + '(self):\n\t'
        arr = "obj = ["
        for r in result[class_name]:
            r = str(r)
            arr += '"' + r + '",'
        arr = arr[:len(
            arr)-1] + ']\n\trandom.shuffle(obj)\n\ti = random.randint(0, len(obj)-1)\n\treturn obj[i]'
        df += ''.join(func + arr+'\n')
    print("load config")
else:
    print("fail to load config")


class MyProvider(BaseProvider):
    def number(self, num):
        try:
            num = int(num)
            string = []
            for i in range(num):
                x = str(random.randint(0, 9))
                string.append(x)
            string = ''.join(string)
            return string
        except:
            print("The param is not number.")
            return


class InjectProvier(BaseProvider):
    exec(df)


def parseStream(stream):
    col = '['
    target = '['
    for excel_obj in stream.split(','):
        tmp = excel_obj.split(':')
        for i in range(0, len(tmp)):
            if i == 0:
                col += '"' + tmp[0] + '",'
            elif i == 1:
                target += tmp[1] + ','
    col = col[:len(col)-1] + ']'
    target = target[:len(target)-1] + ']'
    return target, col