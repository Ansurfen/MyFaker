import datetime
import json
from threading import Thread
from tkinter.filedialog import askopenfilename

import pandas
import requests
from faker import Faker
from faker.providers import BaseProvider
from ttkbootstrap.constants import *

from mvc.model import *

fake = Faker()
fake.add_provider(MyProvider)
fake.add_provider(InjectProvier)


def deal_requset(any):
    if "http://" not in any.url.get():
        log(any, 'url error')
        return
    if any.ctx_param.get() == "":
        log(any, 'param is nil')
        return
    headers = {'Content-Type': 'text/html'}
    if any.content_type.get() == "JSON":
        headers['Content-Type'] = 'application/json'
    else:
        headers['Content-Type'] = 'text/html'
    n = any.cnt.get()
    while n > 0:
        Thread(
            target=handler_request,
            args=(any,headers),
            daemon=True
        ).start()
        any.progressbar.start(10)
        n -= 1

def handler_request(any,headers):
    response = requests.request(any.method_var.get(
        ), any.url.get(), headers=headers, data=getData(any).encode())
    any.progressbar.stop()
    log(any, response.text)

def select_file(any):
    path = askopenfilename(title="Browse file")
    if path:
        any.file_path.set(path)


def exec_file(any):
    if any.file_param.get() == "":
        print("stream is nil")
        return
    n = any.cnt.get()
    while n > 0:
        if ".xlsx" in any.file_path.get():
            Thread(
                target=deal_excel,
                args=(any, any.file_path.get(), any.file_param.get()),
                daemon=True
            ).start()
            any.progressbar.start(10)
        elif ".txt" in any.file_path.get():
            Thread(
                target=deal_txt,
                args=(any, any.file_path.get(), any.file_param.get()),
                daemon=True
            ).start()
            any.progressbar.start(10)
        else:
            break
        n -= 1


def deal_excel(any, filename, stream):
    res = parseStream(stream)
    data_total = eval('[' + res[0] + ' for x in range(any.cnt2.get())]')
    df = eval('pandas.DataFrame(data=data_total,columns=' + res[1] + ')')
    df.to_excel(filename, index=False)
    any.progressbar.stop()
    log(any, filename + ' deal successfully.')


def deal_txt(any, filname, stream):
    with open(filname, 'w', errors='ignore', encoding='utf-8') as fp:
        res = parseStream(stream)
        data_total = eval('[' + res[0] + ' for x in range(any.cnt2.get())]')
        tmp = res[1].replace('["', "").replace('","', ',').replace('"]', "")
        fp.write(tmp+'\n')
        for n in range(0, len(data_total)):
            fp.write(",".join(data_total[n])+'\n')
        fp.close()
        any.progressbar.stop()
        log(any, filname + ' deal successfully.')


def log(any, msg):
    iid = any.loglist.insert(parent='', index=END, value=(
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg))
    any.loglist.selection_set(iid)
    any.loglist.see(iid)


def getData(any):
    return json.dumps(eval(any.ctx_param.get()))