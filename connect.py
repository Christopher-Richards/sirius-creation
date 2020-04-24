import mechanize
import re
import requests
import time
import random

def saveEmail(email):
  file = open('emailCreation.txt','w')
  file.write(email)
  file.close()

def openEmail():
  file = open('emailCreation.txt','r')
  email = file.read()
  file.close()
  return email

def getRandomName():
  global randomLastName
  global randomFirstName
  global postalCode
  global randomNumber
  file = open('firstnames.txt','r')
  randomFirstName = random_line(file)
  m = re.match(r"(^[^\t\s]+)",randomFirstName)
  randomFirstName = str.lower(m.group(1))
  print randomFirstName
  file.close()
  file = open('surnames.txt','r')
  randomLastName = random_line(file)
  randomLastName = randomLastName.rstrip()
  print randomLastName
  file.close()
  file = open('postalcodes.txt','r')
  postalCode = random_line(file)
  postalCode = postalCode.rstrip()
  file.close()
  print postalCode
  file = open('randomnumbers.txt','r')
  randomNumber = random_line(file)
  randomNumber = randomNumber.rstrip()
  print randomNumber
  file.close()

####
# Below function is not mine and was lifted from:
# https://stackoverflow.com/questions/3540288/how-do-i-read-a-random-line-from-one-file-in-python
####
def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

def select_form(form):
  return form.attrs.get('id', None) == 'gform_7'

def submitForm(br,email):
  br.select_form(predicate=select_form)
  br.form.set_all_readonly(False)
  br.form['frmHome_tbxFirstName'] = randomFirstName
  br.form['frmHome_tbxLastName'] = randomLastName
  br.form['frmHome_tbxEmail'] = email
  br.form['frmHome_tbxPhone'] = randomNumber
  br.form['frmHome_tbxZip'] = postalCode
  #br.find_control("input_18.1").items[0].selected=True
  br.submit(id='frmHome_btnNext')

def connectSirius():
  br = mechanize.Browser()
  br.open("https://www.siriusxm.ca/freetrial/")
  forms = list(br.forms())
  for f in forms:
    print f

  email = openEmail()
  submitForm(br,email)

def parseEmailContent():
  s = requests.session()
  email = openEmail()
  print email
  m = re.match(r"^([^\@]+)",email)
  user = m.group(1)
  payload = {'f':'set_email_user', 'email_user': user}
  req = s.post('http://api.guerrillamail.com/ajax.php', data=payload)
  print req.text

  payload = {'f':'check_email','seq':'0'}
  req = s.get('http://api.guerrillamail.com/ajax.php', params=payload)
  print req.text

  #187028583
  while True:
    if "siriusxm.ca" not in req.text:
      payload = {'f':'check_email','seq':'0'}
      req = s.get('http://api.guerrillamail.com/ajax.php', params=payload)
      time.sleep(20)
      continue
    else:
      break

  m = re.match(r"^.+\[\{\"mail_id\"\:\"([^\"]+).+\"mail_from\"\:\"([^\"]+)",req.text)
  mail_id = m.group(1)
  mail_from = m.group(2)

  payload = {'f':'fetch_email','email_id':mail_id}
  req = s.get('http://api.guerrillamail.com/ajax.php', params=payload)
  print req.text

  m = re.match(r".+Username\s+\\\/\s+Nom d'utilisateur\:\s+([^\r\n\s]+).+Password\s+\\\/\s+Mot de passe\:\s+([^\r\n\s]+)",req.text)
  email = m.group(1)
  password = m.group(2)

  file = open('siriusEmail.txt','w')
  file.write(email)
  file.write("\n")
  file.write(password)
  file.close()

def createSharklasersEmail():
  s = requests.session()
  payload = {'f':'get_email_address'}
  req = s.get('http://api.guerrillamail.com/ajax.php', params=payload)
  print req.text #prints out the current email address

  m = re.match(r"\{\"email_addr\"\:\"([^\@]+\@[^\"]+)",req.text)
  email = m.group(1)
  saveEmail(email)

  payload = {'f':'check_email','seq':'0'}
  req = s.get('http://api.guerrillamail.com/ajax.php', params=payload)
  print req.text

#parseEmailContent()
getRandomName()
#createSharklasersEmail()
#connectSirius()
#parseEmailContent()
