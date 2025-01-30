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

tennisBall_driver = webdriver.Chrome(options=chrome_options) # Optional argument, if not specified will search path.
tennisBall_driver.get("https://www.amazon.com/Wilson-Open-Extra-Duty-Tennis/dp/B00IIP4BO0/ref=sr_1_5_pp?crid=24F3W4WRG751J&dib=eyJ2IjoiMSJ9.MY_QlAv6YIFpdbhOKmkupQ_T6Zd2G8nzjk9bLHPQHJrmQJrv4KmNu3QKQ0zPvhvesQJMRzyULPvexVH6ozPYuqwrxpOvYOWb7aMpx-Iu-N1d0PjZrj59erL-zE1hFjMRSVCFxPuaaM9EQEzU8QHe7g6Bf13Vp4_CEZLGz-aM1pniuAN7kNa7eJHfgWkRuDc5LYroG4wJFiiEJg0Jpx75saOv7T0Y7Vms9IRmUotKZShCKdsC0abuvTVNberLQ8fP_tr2bznyCM7IJAUxc_TjhsUdPcaSAZCfKDawEhR0WThIFh0z3y3w1GZCEa2jgaSfiUI26EF6l_vkZ5W260MAoFfSq12gBeXr_GoexAJLGI6AAn0iNJIfDkekVvSLAlSjHgtFh65XQ4jUQbxaNuymMpmGO0z6d_tM3ADgAo00o92NhDhkavkEa0YRYRsbD9xU.fDJs-txQqZ9Oflj2woLX5FOlrCK1B2EOzVu1frfzWYw&dib_tag=se&keywords=WILSON%2BUS%2BOpen%2BTennis%2BBalls%2B-%2B3%2BBalls&qid=1735670376&sprefix=wilson%2Bus%2Bopen%2Btennis%2Bballs%2B-%2B3%2Bballs%2Caps%2C163&sr=8-5&th=1") # Open the website

darkChocolate_driver = webdriver.Chrome(options=chrome_options) # Optional argument, if not specified will search path.
darkChocolate_driver.get("https://www.amazon.com/Lilys-Sweets-Dark-Chocolate-Salt/dp/B00Z9OYA6C/ref=sr_1_1?crid=1FOND1DMYSS0J&dib=eyJ2IjoiMSJ9.erY1K3JZ4z6gHVeqQLhnIyU3m68Dh9Fknn7S2KxPGayZ-giluTdvLAzqoSBvFuPMCfWN7i5C7bfEw9iPXK2eLhW7hSho1EcNUkY8LcOOio_jNxZXg5pXSa2lFTGKlPE3h3AXsrBEKJEhxRR1jfZT_Ue-X9wKfcwgyQgBXXdlhe3-JdB8uCtAeTP-0kp0PZ8fpjWuvAFvJLik_nw-Rjb9n5OjWydrPVwF_UzvdNHbs34Y191ZbIw7oBZ4xgi9WR10WgtqH-cCINCHWykAukcZ4ryWAS_wlw6E4OY58ysRbDMe5kZSTZODFc-w83gC3z9J1qBsqwj70H7uSqzB_LJS3LGgHo08aApJjqTm5dIDY8gVF44fjOO4iRm1XnJIgkp93niJtAlvcmFHDeVLSTSPMn7J_7EUu2VAF-jrKViG8JCTBfDozrKl_DF6nlqhc7ps.Ff90OCBImA9Fvj0XXv4InupmDijEGifsylsbIrzO4LU&dib_tag=se&keywords=LILY%27S+Sea+Salt+Extra+Dark+Chocolate+Style+No+Sugar+Added%2C+Sweets+Bars%2C+2.8+oz+%2812+Count%29&qid=1738185157&sprefix=lily%27s+sea+salt+extra+dark+chocolate+style+no+sugar+added%2C+sweets+bars%2C+2.8+oz+12+count+%2Caps%2C135&sr=8-1") # Open the website

def send_email(subject, body):
    load_dotenv()
    my_email = os.getenv("my_email")
    my_password = os.getenv("my_password")
    
    connection = smtplib.SMTP('smtp.gmail.com') # Create a connection to the SMTP server
    connection.starttls() # Secure the connection
    connection.login(user=my_email, password=my_password) # Login to the email server
    # subject = "US Open Tennis Ball Price Alert"
    # body = f"US Open tennis ball price is ${price}"

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

def check_tennis_ball_price(price, product_name):
    if price <= 6.17:
        print("Tennis Ball Price Equal or Below $6.17")
        print("Sending email...")
        subject = "Tennis Ball Price Alert"
        body = f"{product_name} price is ${price}"
        send_email(subject, body)
    else:
        print(f"{product_name} Price above $6.17")

def check_dark_chocolate_price(price, product_name):
    if price <= 40.44:
        print("Dark Chocolate Price Equal or Below $40.44")
        print("Sending email...")
        subject = "Lilys Dark Chocolate Price Alert"
        body = f"{product_name} price is ${price}"
        send_email(subject, body)
    else:
        print(f"{product_name} Price above $40.44")

def check_price(driver_instance):
    try:
        product_name = driver_instance.find_element(By.ID, "productTitle")
        whole_price = driver_instance.find_element(By.CLASS_NAME, "a-price-whole")
        decimal_price = driver_instance.find_element(By.CLASS_NAME, "a-price-fraction")
        price = float(whole_price.text + "." + decimal_price.text)
        print(f"{product_name.text} Price: ${price}")
        if "Wilson US Open" in product_name.text:
            check_tennis_ball_price(price, product_name.text)
        if "Dark Chocolate" in product_name.text:
            check_dark_chocolate_price(price, product_name.text)
        
    except NoSuchElementException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Stopped")
        driver_instance.quit()


check_price(tennisBall_driver)
check_price(darkChocolate_driver)

