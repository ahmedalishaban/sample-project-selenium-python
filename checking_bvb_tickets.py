import time
import tkinter as tk
from tkinter import messagebox
import pygame
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set the path to the web driver
driver_path = "msedgedriver.exe"

# Create a new instance of the Edge browser
driver = webdriver.Edge(driver_path)
driver.delete_all_cookies()
driver.maximize_window()

# Navigate to the desired website
driver.get("https://www.ticket-onlineshop.com/ols/bvb/de/bundesliga/channel/shop/index")
# Check if there are any captcha elements on the page
captcha_elements = driver.find_elements_by_xpath('//div[@class="g-recaptcha"]')
if captcha_elements:
    print("Captcha found, waiting 20 seconds...")
    time.sleep(20)

# Wait for the login button to become visible and clickable
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="header__button"]')))
login_button.click()

# Find the username and password fields and fill them in
username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="E-Mail"]')))
username_field.clear()
password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Kennwort"]')))
password_field.clear()
username_field.send_keys("mariegeleijnse@hotmail.com")
password_field.send_keys("paulalmere")

# Click the login button
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
login_button.click()

# Close the cookies popup
try:
    cookies_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button"]')))
    cookies_button.click()
except:
    pass

# wait appearing of elements
time.sleep(1)

# Display a message box with the message "Tickets are available!"
root = tk.Tk()
root.withdraw()
root.focus_set()

# Wait for the element you are interested in to appear
tickets_available = False
while not tickets_available:
    try:
        # Scrolling down to the card container elements
        card_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '(//header[@class="event-card__header"])[1]')))
        driver.execute_script("arguments[0].scrollIntoView();", card_element)
        time.sleep(0.5)

        #  click the tickets of match number 1
        tickets_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[@class="card event-card"])[1]//a')))
        tickets_button.click()
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//p[contains(text(), "Für diese Veranstaltung stehen aktuell keine Tickets zur Verfügung.")]')))

        # print no tickets if nothing changed
        print("No tickets found")

    except:
        result = messagebox.showinfo("Tickets Available", "Tickets are available!")
        time.sleep(0.5)
        # Make sound when Tickets are available!
        pygame.init()
        pygame.mixer.music.load("alert.mp3")
        pygame.mixer.music.play()

        if result == 'ok':
            # print tickets available if nothing changed
            print("Tickets are available!")
            tickets_available = True
            driver.quit()
            exit()
