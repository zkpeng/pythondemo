import requests
from PIL import Image
import pytesseract
from io import BytesIO
from requests.cookies import RequestsCookieJar
from lxml import etree
import getpass

pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

headers = {
'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36','Upgrade-Insecure-Requests':'1'}
sessionid = None

def getsessionid():
 global sessionid
 if sessionid == None:
  headers1 = {'Referer':'http://gjj.jinan.gov.cn/'}
  headers2 = {'Referer':'http://123.233.117.50:801/jnwt/indexPerson.jsp'}
  sessionurl = 'http://123.233.117.50:801/jnwt/indexPerson.jsp'
  response = requests.get(sessionurl,headers=headers1)
  response = requests.get(sessionurl,headers=headers2)
  cookies = response.cookies.get_dict()
  sessionid = cookies['JSESSIONID']
 return sessionid
 
def getvericode():
 cookiejar = RequestsCookieJar()
 cookiejar.set('JSESSIONID', getsessionid())
 codepic = requests.get('http://123.233.117.50:801/jnwt/vericode.jsp',cookies=cookiejar)
 img = Image.open(BytesIO(codepic.content))
 imggry = img.convert('L')
 txt = pytesseract.image_to_string(imggry)
 return txt

def login():
 url = 'http://123.233.117.50:801/jnwt/per.login'
 vercode = getvericode()
 certinum = input('input your passport no:')
 perpwd = getpass.getpass('input your password:')
 params = {'certinum':certinum,'perpwd':perpwd,'vericode':vercode}
 cookiejar = RequestsCookieJar()
 cookiejar.set('JSESSIONID', getsessionid())
 result = requests.post(url,params=params,headers=headers,cookies=cookiejar)
 root=etree.HTML(result.text)
 result=root.xpath("//span[@class='icon person']/text()")
 if len(result) == 0:
  error=root.xpath("//div[@class='WTLoginError']/ul/li[@class='text']/text()")
  if error == None:
   print 'Login Failed...'
  else:
   print error[0].encode('gbk')
 else:
  print result[0].encode('gbk')

if __name__ == '__main__':
 login()
