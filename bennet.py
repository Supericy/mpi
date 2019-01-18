from lxml import html
from bs4 import BeautifulSoup
import smtplib


def sendemail(from_addr, to_addr_list, cc_addr_list, bcc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s ' % from_addr
    header += '\nTo: %s ' % ','.join(to_addr_list)
    header += '\nCc: %s ' % ','.join(cc_addr_list)
    header += '\nBcc: %s ' % ','.join(bcc_addr_list)
    header += '\nSubject: %s ' % subject
    message = header + '\n' + message

    print
    message
    server = smtplib.SMTP(smtpserver)
    # server.ehlo()
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    # print problems
    server.quit()


    sendemail(from_addr='cryptoradsbot@gmail.com',
              to_addr_list=['bennetgigliotti@gmail.com'],
              cc_addr_list=[],
              bcc_addr_list=[],
              subject='New Listing Detected for Camaro!',
              message=html,
              login='cryptoradsbot@gmail.com',
              password='XXXXXXXXX')

