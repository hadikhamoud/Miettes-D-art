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

# _________________________To send Emails seperate from main thread________________________


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content,
                           self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        # img = handleImage("logo.png")
        # msg.attach(img)
        msg.send(fail_silently=False)


def send_html_mail(subject, html_content, recipient_list, sender):
    EmailThread(subject, html_content, recipient_list, sender).start()


def handleImage(imgName):
    img_dir = settings.IMG_DIR
    image = imgName
    file_path = os.path.join(img_dir, image)
    with open(file_path, 'rb') as f:

        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)

    return img



