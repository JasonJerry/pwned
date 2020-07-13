# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 20:26:22 2020

@author: Jason
"""


import sys, hashlib, requests

def pwndb(pwd):
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('Error fetching "{}": {}'.format(
            url, res.status_code))
    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return sha1pwd, count
            
def main(args):
  pwd = args.strip()
  if pwd == "":
    print("Password field is empty.")
  else:
    try:
      sha1pwd, count = pwndb(pwd)
      if count:
        foundmsg = "{0} was found with {1} occurrences (hash: {2})"
        print(foundmsg.format(pwd, count, sha1pwd))
      else:
        print("{} was not found".format(pwd))
    except UnicodeError:
      errormsg = sys.exc_info()[1]
      print("{0} could not be checked: {1}".format(pwd, errormsg))

Password = input("Enter the password:(this will not be exposed !) ->")
main(Password)