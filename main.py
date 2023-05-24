from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

import pygame
def main():

    # Set up Chrome driver
    chrome_options = Options()
    user_data_directory = ""
    chrome_options.add_argument(f"user-data-dir={user_data_directory}\\userdata")
    #chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service('/usr/local/bin')  # Replace with the actual path to the chromedriver executable
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open chess.com and log in
    driver.get("https://www.chess.com")
    # Perform login steps here (enter username and password, click login)



    # Navigate to the game URL
    game_url = "https://www.chess.com/play/online/new"
    driver.get(game_url)


    # Find the button element
    button = driver.find_element(By.CSS_SELECTOR, "button[data-cy='new-game-time-selector-button']")

    # Click the button
    button.click()
    time.sleep(5)

    time_option = input("Enter the option number (1min - 60,3min - 180, or 5min - 300): ")
    # Find the button element
    button = driver.find_element(By.CSS_SELECTOR, f"button[data-cy='time-selector-category-{time_option}']")

    # Click the button
    button.click()


    # Find the button element
    button = driver.find_element(By.CSS_SELECTOR, "button[data-cy='new-game-index-play']")

    # Click the button
    button.click()

    # # Wait for the game to load
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
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.unpause()
                    else:
                        continue

                pygame.mixer.music.pause()
                while len(driver.find_elements(By.CSS_SELECTOR,'.clock-component.clock-bottom.clock-player-turn')) == 0:
                    continue
        # Check if the clock has run out
        if current_time == "0:00":
            break

        # Wait for a short interval before checking the clock again
        time.sleep(0.5)

    # Close the browser
    pygame.quit()
    driver.quit()

if __name__ == '__main__':
    main()
