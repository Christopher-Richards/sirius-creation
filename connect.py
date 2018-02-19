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

def select_form(form):
  return form.attrs.get('id', None) == 'gform_7'

def submitForm(br,email):
  br.select_form(predicate=select_form)
  br.form.set_all_readonly(False)
  br.form['input_1'] = 'Edward'
  br.form['input_3'] = 'Broxane'
  br.form['input_14'] = email
  br.form['input_15'] = email
  br.form['input_9'] = 'M1S 2H5'
  br.find_control("input_18.1").items[0].selected=True
  br.submit(id='gform_submit_button_7')

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
  m = re.match(r"^.+\[\{\"mail_id\"\:\"([^\"]+).+\"mail_from\"\:\"([^\"]+)",req.text)
  mail_id = m.group(1)
  mail_from = m.group(2)

  while True:
    if "siriusxm.ca" not in mail_from:
      time.sleep(20)
      continue
    else:
      break
  
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


parseEmailContent()
