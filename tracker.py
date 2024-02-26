from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#Function used to track the aicraft
def is_flying():
    flight_to_track = {
        "A6-EUT": "https://www.flightradar24.com/UAE2AR/341c9691", #Add the aircrafts you want to track
        "F-ONEO Aircalin": "https://www.flightradar24.com/ACI800/341c1ba5",
        "D-ABOL": "https://www.flightradar24.com/CFG9AP/341ece84"
    }

    options = Options()
    options.headless = True  # NOT WORKING for now?
    driver = webdriver.Firefox(options=options)

    for serial, url in flight_to_track.items():
        driver.get(url)
        time.sleep(5)  # Wait for the page to load and JavaScript to execute

        # Check if the "Live flight not found" message is present
        not_flying_elements = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Live flight not found')]")
        
        if not_flying_elements:
            print(f"{serial}: The aircraft is not airborne")
        else:
            print(f"{serial}: The aircraft is airborne")
            send_email(serial)
            

    driver.quit()

#function used to send notification email
def send_email(serial):

    
    # Set up the email parameters
    smtp_server = 'xxx' #smtp server you are going to use
    smtp_port = 587
    sender_email = 'xxx' #add the email address you are going to use to send email
    sender_password = 'xxx'#add the password for this account
    recipient_email = 'xxx' #add the recipient(s)
    subject = 'Flight Tracker: {} is airborne'.format(serial)
    body = "Hello, \n\n{} is airborne\n\nHave a nice day".format(serial)

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))


    # Send the email
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email, recipient_email, msg.as_string())
    smtp.quit() 

    print('[+] Email sent, all done !')

def main():
   while True:
      is_flying()
      time.sleep(3600)  # Sleep for 60 minutes 


main()
