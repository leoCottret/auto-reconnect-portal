# web interactions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
import time # and visual feedbacks
import random
# os commands, env variables
import subprocess
import os
from dotenv import load_dotenv
# visual feedbacks (about the timer)
import tkinter as tk
from tkinter import messagebox
# logging
import logging


# execute an os command, stop if the command fails
def execute_command(os_command: str):
	p = subprocess.Popen(os_command, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate() # (stdout, stderr)
	# wait for command to finish
	p_status = p.wait()

	# 0 = command succeeded
	if p_status != 0:
		logging.error('AutoReconnectPortal, OS command error! command -> '+ str(os_command) + '\tstderr -> ' + str(err) +  "\tstdout -> " + str(output))
		display_pop_up('AutoReconnectPortal, OS command error!','command -> '+ str(os_command) + '\nstderr -> ' + str(err) +  "\nstdout -> " + str(output))
		exit()

	logging.debug('command executed successfully: ' + os_command)

# start clicking until success
def click_until_success(button_id: str, wait_time: int, driver):
	logging.debug('start try click of button with id: ' + str(button_id))

	# element_to_be_clickable > visibility_of_element_located > presence_of_element_located
	try:
		submit_button = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.ID, button_id)))
		try_click = True
		while try_click:
			time.sleep(random.uniform(CHECK_SPEED_MIN, CHECK_SPEED_MAX))
			try:
				logging.debug('try click!')
				submit_button.click()
				try_click = False
			except ElementClickInterceptedException:
				logging.debug('try click: ElementClickInterceptedException!')
			except:
				logging.debug('try click: unknown error')
	# TODO add specific check for button id not found instead of assuming every errors have this meaning
	except:
		logging.warning("couldn't find the button with id: " + str(button_id))
	time.sleep(1)

# display a pop up, stop the script until the pop up is closed
def display_pop_up(title, body):
	root = tk.Tk()
	root.attributes('-topmost',1) # set the pop up to be displayed at the foreground
	root.withdraw()
	logging.debug("pop up displayed at: " + time.strftime("%H:%M:%S", time.localtime()))
	messagebox.showinfo(title, body)
	root.update()


# reconnect to the portal
def reconnect():
	logging.info('start reconnection at: ' + time.strftime("%H:%M:%S", time.localtime()))
	# 1. execute os command 1
	execute_command(CMD_1)
	# 2. reconnect to the portal
	driver = webdriver.Chrome()
	driver.get(PORTAL_URL)
	driver.implicitly_wait(10)
	# if we're already connected, disconnect to reset connexion timer
	click_until_success("feedbackForm_disconnect_button", 5, driver)
	# connect!
	click_until_success("informativeWidget_connect_button", 10, driver)

	# check if we reconnected successfully
	check_feedback = True
	while check_feedback:
		time.sleep(random.uniform(CHECK_SPEED_MIN, CHECK_SPEED_MAX))
		message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "welcomeHeadline")))
		if str(message.text) == 'Bienvenue' or str(message.text) == 'Welcome':
			check_feedback = False
		else:
			logging.debug('check_feedback not ready yet')
	# add a random time sleep so it looks like we're taking time to close the page like a human otherwise it's instantaneous
	time.sleep(random.uniform(CHECK_SPEED_MIN, CHECK_SPEED_MAX))
	driver.quit()

	# 3. execute os command 2
	execute_command(CMD_2)

# --- MAIN ---
# load env variables
try:
	load_dotenv() 
	CMD_1 = os.getenv('CMD_1', 'you_didnt_set_an_env_variableCMD_1') # command executed before connection
	CMD_2 = os.getenv('CMD_2', 'you_didnt_set_an_env_variableCMD_2') # command executed after connection
	PORTAL_URL = os.getenv('PORTAL_URL', 'you_didnt_set_an_env_variablePORTAL_URL')
	LOGGING_FILE_PATH = os.getenv('LOGGING_FILE_PATH', 'you_didnt_set_an_env_variableLOGGING_FILE_PATH')

	# other global variables
	CHECK_SPEED_MIN = 0.2 # use min and max value to send click and such, to avoid detection if using a fixed value (just in case)
	CHECK_SPEED_MAX = 1.5
	TIME_BEFORE_CHECK = 60 # main loop timer, wait X seconds before checking if TIME_BEFORE_RECONNECT has been exceeded since "start"
	TIME_BEFORE_RECONNECT = 60 * 60 * 7 # wait X seconds before displaying a pop up, then reconnecting to the portal when the pop up is closed

	# connect a first time to the portal
	# TODO use the parameter instead of the hardcoded logging value
	logging.basicConfig(filename=LOGGING_FILE_PATH+'auto_reconnect_portal.log', encoding='utf-8', level=logging.INFO)

	logging.debug('starting AutoReconnectPortal at ' + time.strftime("%H:%M:%S", time.localtime()))
	reconnect()
	start = time.time()
	while True:
		time.sleep(TIME_BEFORE_CHECK)
		if time.time() - start > TIME_BEFORE_RECONNECT:
			display_pop_up('AutoReconnectPortal: time to reconnect!', "After clicking this pop up, the script will reconnect you.\n The pop up openned at: " + time.strftime("%H:%M:%S", time.localtime()))
			reconnect()
			start = time.time()

except KeyboardInterrupt:
	logging.info('script stopped by user')
except Exception as e:
	unknown_error = 'UNKNOWN ERROR: Type -> ' + str(type(e)) + ', Reason -> ' + str(e)
	logging.error(unknown_error)
	raise e # will print the detailled error in the console anyway, handy!