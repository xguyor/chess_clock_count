
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pygame
import webbrowser


def main():

    #
    # # Specify the path to your HTML file
    # html_file = "file:///Users/guyor/PycharmProjects/chess_clock_alert/login.html"
    # # Open the HTML file in the default web browser
    # webbrowser.open_new_tab(html_file)



    chrome_options = Options()
    # user_data_directory = os.getcwd()
    # chrome_options.add_argument(f"user-data-dir={user_data_directory}\\userdata")
    service = Service('/usr/local/bin')  # Replace with the actual path to the chromedriver executable
    driver = webdriver.Chrome(service=service)

    # Open chess.com and log in
    driver.get("https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/")
    # Perform login steps here (enter username and password, click login)

    # Check if the login credentials file exists
    credentials_file_path = "/Users/guyor/PycharmProjects/chess_clock_alert/credentials.txt"


    try:
        with open(credentials_file_path, "r") as file:
            # Read the credentials from the file
            username, password = file.read().strip().split(",")
            # Find the username/email input field and enter the value
            username_input = driver.find_element(By.ID, "username")
            username_input.send_keys(username)

            # Find the password input field and enter the value
            password_input = driver.find_element(By.ID, "password")
            password_input.send_keys(password)

            # Find the login button and click it
            login_button = driver.find_element(By.ID, "login")
            login_button.click()

    except FileNotFoundError:
        # If the file doesn't exist, prompt the user for the credentials
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        # Save the credentials to the file for future runs
        with open(credentials_file_path, "w") as file:
            file.write(f"{username},{password}")



    # Navigate to the game URL
    game_url = "https://www.chess.com/play/online/new"
    driver.get(game_url)

    # Find the button element
    button = driver.find_element(By.CSS_SELECTOR, "button[data-cy='new-game-time-selector-button']")

    # Click the button
    button.click()


    # time.sleep(5)

    time_option = input("Enter the option number (1min - 60,3min - 180, or 5min - 300): ")
    # Find the button element
    button = driver.find_element(By.CSS_SELECTOR, f"button[data-cy='time-selector-category-{time_option}']")

    # Click the button
    button.click()


    # Find the button element
    button = driver.find_element(By.CSS_SELECTOR, "button[data-cy='new-game-index-play']")

    # Click the button
    button.click()

    # Wait for the game to load
    # time.sleep(7)


    pygame.init()
    mp3_file1_path = '30secsleft.mp3'
    mp3_file2_path = '20seccount.mp3'
    mp3_file3_path = '15seccount.mp3'


    # Start monitoring the clock
    while True:

        # clock_element = driver.execute_script("return document.querySelector('span[data-cy=\"clock-time\"]').innerText;")
        element = driver.find_element(By.CSS_SELECTOR, '.clock-component.clock-bottom .clock-time-monospace')
        current_time = element.text

        #alert when 30 seconds lefet
        if current_time == '0:30':
            pygame.mixer.music.load(mp3_file1_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
            pygame.mixer.music.stop()


        pattern = r'^0:15\.\w+$'
        match = re.match(pattern, current_time)
        if match:
            pygame.mixer.music.load(mp3_file3_path)
            pygame.mixer.music.play()
            while True:
                while len(driver.find_elements(By.CSS_SELECTOR, '.clock-component.clock-bottom.clock-player-turn')) != 0:
                    if len(driver.find_elements(By.CSS_SELECTOR, '.board-modal-container-container')) != 0:
                        pygame.mixer.music.stop()
                        break
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.unpause()
                    else:
                        continue

                pygame.mixer.music.pause()
                while len(driver.find_elements(By.CSS_SELECTOR,'.clock-component.clock-bottom.clock-player-turn')) == 0:
                    if len(driver.find_elements(By.CSS_SELECTOR, '.board-modal-container-container')) != 0:
                        pygame.mixer.music.stop()
                        break
                    continue

        # Check if the clock has run out
        if current_time == "0:00":
            pygame.mixer.music.stop()
            break

        # Wait for a short interval before checking the clock again
        time.sleep(0.5)

    # Close the browser
    pygame.quit()
    # driver.quit()

if __name__ == '__main__':
    main()
