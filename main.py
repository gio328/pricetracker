from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options) # Optional argument, if not specified will search path.
driver.get("https://www.amazon.com/Wilson-Open-Extra-Duty-Tennis/dp/B00IIP4BO0/ref=sr_1_5_pp?crid=24F3W4WRG751J&dib=eyJ2IjoiMSJ9.MY_QlAv6YIFpdbhOKmkupQ_T6Zd2G8nzjk9bLHPQHJrmQJrv4KmNu3QKQ0zPvhvesQJMRzyULPvexVH6ozPYuqwrxpOvYOWb7aMpx-Iu-N1d0PjZrj59erL-zE1hFjMRSVCFxPuaaM9EQEzU8QHe7g6Bf13Vp4_CEZLGz-aM1pniuAN7kNa7eJHfgWkRuDc5LYroG4wJFiiEJg0Jpx75saOv7T0Y7Vms9IRmUotKZShCKdsC0abuvTVNberLQ8fP_tr2bznyCM7IJAUxc_TjhsUdPcaSAZCfKDawEhR0WThIFh0z3y3w1GZCEa2jgaSfiUI26EF6l_vkZ5W260MAoFfSq12gBeXr_GoexAJLGI6AAn0iNJIfDkekVvSLAlSjHgtFh65XQ4jUQbxaNuymMpmGO0z6d_tM3ADgAo00o92NhDhkavkEa0YRYRsbD9xU.fDJs-txQqZ9Oflj2woLX5FOlrCK1B2EOzVu1frfzWYw&dib_tag=se&keywords=WILSON%2BUS%2BOpen%2BTennis%2BBalls%2B-%2B3%2BBalls&qid=1735670376&sprefix=wilson%2Bus%2Bopen%2Btennis%2Bballs%2B-%2B3%2Bballs%2Caps%2C163&sr=8-5&th=1") # Open the website

def send_email(price):
    load_dotenv()
    my_email = 'giovmendez@gmail.com'
    my_password = os.getenv("my_password")
    
    connection = smtplib.SMTP('smtp.gmail.com') # Create a connection to the SMTP server
    connection.starttls() # Secure the connection
    connection.login(user=my_email, password=my_password) # Login to the email server
    subject = "US Open Tennis Ball Price Alert"
    body = f"US Open tennis ball price is ${price}"

    try:
        connection.sendmail(
            from_addr=my_email, 
            to_addrs='giovmendez@gmail.com',
            msg=f'Subject:{subject}\n\n{body}')
        print('Email sent successfully')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.quit()
try:
    # find by class name
    whole_price = driver.find_element(By.CLASS_NAME, "a-price-whole")
    decimal_price = driver.find_element(By.CLASS_NAME, "a-price-fraction")
    price = whole_price.text + "." + decimal_price.text
    print(f"Price: ${price}")
    if price <= "6.17":
        print("Price equal or below $6.17")
        print("Sending email...")
        send_email(price)
    else:
        print("Price above $6.17")

except NoSuchElementException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Stopped")
    driver.quit()


