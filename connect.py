import mechanize
import re
import requests
import time

def saveEmail(email):
  file = open('emailCreation.txt','w')
  file.write(email)
  file.close()

def openEmail():
  file = open('emailCreation.txt','r')
  email = file.read()
  return email

def connect_sirius():
  br = mechanize.Browser()
  br.open("https://www.siriusxm.ca/freetrial/")
  forms = list(br.forms())
  for f in forms:
    print f

  email = openEmail()
  print email

def connect_sharklasers():
  s = requests.session()
  payload = {'f':'get_email_address'}
  req = s.get('http://api.guerrillamail.com/ajax.php', params=payload)
  print req.text #prints out the current email address

  m = re.match(r"\{\"email_addr\"\:\"([^\@]+\@[^\"]+)",req.text)
  email = m.group(1)
  saveEmail(email)
  print m.group(1)

  #time.sleep(20)
  payload = {'f':'check_email','seq':'0'}
  req = s.get('http://api.guerrillamail.com/ajax.php', params=payload)
  print req.text

  try:
      if req.text is None: # The variable
          print('It is None')
  except NameError:
      print ("This variable is not defined")
  else:
      print ("It is defined and has a value")

connect_sirius()
