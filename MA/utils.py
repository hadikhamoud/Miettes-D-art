import random
import string
# from django.contrib.gis.geoip2 import GeoIP2
from datetime import datetime
import threading
from django.core.mail import EmailMessage
from django.conf import settings
import os
from email.mime.image import MIMEImage
from datetime import datetime
import pytz
from pathlib import Path
from django.core.mail import EmailMultiAlternatives
from bs4 import BeautifulSoup as bs

# ___________________________For view.py_______________________________________________


def get_total_and_items(queryset):
    total = 0
    number = 0
    for item in queryset:
        number += item.Quantity
        total += item.Item.Price * item.Quantity
    return total, number


# def get_country(request):
#     g = GeoIP2()
#     US = True
#     ip = request.META.get('REMOTE_ADDR', None)
#     if ip:
#         Country = g.city(ip)['country_code']
#         if Country == 'LB':
#             US = False
#     else:
#         Country = 'US'

#     return Country, US


def generate_Ref_code():
    chars = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
    numbers = random.randint(100000,999999)
    return chars+str(numbers)


# ___________________________For models.py_______________________________________________

def get_default_size():
    return ['XS', 'S', 'M', 'L', 'XL']


def get_default_color():
    return ['Gold', 'Silver']


def generate_timestamp():
    dateNow = datetime.now()
    tzNow = pytz.timezone("Asia/Beirut")
    return tzNow.localize(dateNow)


print(generate_timestamp())

BASE_DIR = Path(__file__).resolve().parent.parent

# _________________________To send Emails seperate from main thread________________________

def handleImage(imgPath):

    with open(os.path.join(BASE_DIR, imgPath[1:]), 'rb') as f:

        img = MIMEImage(f.read())
        print(imgPath)
        img.add_header('Content-ID', '<{name}>'.format(name=imgPath[1:]))
        img.add_header('Content-Disposition', 'inline', filename=imgPath[1:])

    return img


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender,Images=[]):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        self.Images = Images
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        for image in self.Images:
            img = handleImage(image)
            msg.attach(img)
        msg.send(fail_silently=False)


def send_html_mail(subject, html_content, recipient_list, sender,Images=[]):
    EmailThread(subject, html_content, recipient_list, sender,Images=Images).start()





#_________________________For adding products_______________________________________________

# from selenium import webdriver










#_________________________extracting images_______________________________

# def save_image(url,imageName):
#     ext = url.split(".")[2]
#     urllib.request.urlretrieve(url,f'{os.path.join(IMAGE_DIR,imageName)}.{ext}')



# def extract_images(reader):
#     div = reader.find_all("div",{"class":"image-widget-data"})
#     links = []
#     for e in div:
#         tag = e.find_all("a")
#         links+= [t["href"] for t in tag]
#     return links


def extract_title(reader):
    inpt = reader.find("input",{"id":"edit-title"})
    return inpt["value"]

def extract_description(reader):
    div = reader.find("div",{"id":"edit-field-description"})
    textarea = div.find("textarea",text=True)
    textareaReader = bs(textarea.text,"lxml")
    return textareaReader.get_text()


def extract_category(reader):
    div = reader.find("div",{"id":"edit-field-category-und"})
    checkedInput = div.find("input",{"checked":"checked"})
    checkedDiv=checkedInput.parent
    return checkedDiv.find("label",text=True).text


def extract_price(reader):
    inpt = reader.find("input",{"id":"edit-commerce-price-und-0-amount"})
    return inpt["value"]

def extract_status(reader):
    inpt = reader.find("input",{"name":"status","checked":"checked"})
    if inpt["value"]==1:
        return "active"
    return "disabled"


def extract_SKU(reader):
    inpt = reader.find("input",{"id":"edit-sku"})
    return inpt["value"]

# def extract_SKU(reader):

# dir = "/Users/hadihamoud/Desktop/Personal work/Miettes_General_Scraper/Products_HTML_Pages/Product_ BE100B _ Miettesdart1.html"

