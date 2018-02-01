
import mechanize
import re

def connect_sirius():
  br = mechanize.Browser()
  br.open("https://www.siriusxm.ca/freetrial/")
  forms = list(br.forms())
  for f in forms:
    print f

#  for f in br.forms():
#    print f

def connect_sharklasers():
  br = mechanize.Browser()
  resp = br.open("https://www.sharklasers.com/")
  content = resp.get_data()
  p = re.compile('Thank you for using SharkLasers - your temporary email address friend and spam fighter.+Email\:\s+([^\@]+\@.+)\\\\r\\\\n\\\\r\\\\nTips & Notes')
  if p.search(content):
    print 'found'
    match = p.search(content)
    email = str(match.groups())
    email = email.replace("('","")
    email = email.replace("',)","")
    saveEmail(email)
  else:
    print 'no match'

def saveEmail(email):
  file = open('emailCreation.txt','w')
  file.write(email)
  file.close()

connect_sharklasers()
#connect_sirius()

