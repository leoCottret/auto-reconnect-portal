# web interactions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options # to be able to specify the path of the chrome/chromedriver binaries
from selenium.common import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
import time # and visual feedbacks
import random
# os commands, env variables
import subprocess
import os
import sys
from dotenv import load_dotenv
# visual feedbacks (about the timer)
import tkinter as tk
from tkinter import messagebox
# logging
import logging

# get the path to this script, no matter the current directory of the user
# is used to get the location of the chrome/chromedriver binaries without having to specify their absolute path
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

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

# start clicking button until success
def click_until_success(button_id: str, wait_time: int, driver):
	logging.debug('start try click of button with id: ' + str(button_id))

	# with Selenium --> element_to_be_clickable > visibility_of_element_located > presence_of_element_located
	# ">" meaning here "is a stronger check than"
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
	time.sleep(0.2)


# start clicking checkbox until success
def click_until_success_checkbox(checkbox_id: str, wait_time: int, driver):
	logging.debug('start try click of button with id: ' + str(checkbox_id))

	# with Selenium --> element_to_be_clickable > visibility_of_element_located > presence_of_element_located
	# ">" meaning here "is a stronger check than"
	try:
		check = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='"+checkbox_id+"']")))
		action = webdriver.ActionChains(driver)
		try_click = True
		while try_click:
			time.sleep(random.uniform(CHECK_SPEED_MIN, CHECK_SPEED_MAX))
			try:
				logging.debug('try click!')
				action.move_to_element_with_offset(check,-20,-20).click().perform()
				try_click = False
			except ElementClickInterceptedException:
				logging.debug('try click: ElementClickInterceptedException!')
			except:
				logging.debug('try click: unknown error')
	# TODO add specific check for button id not found instead of assuming every errors have this meaning
	except:
		logging.warning("couldn't find the button with id: " + str(checkbox_id))
	time.sleep(0.2)

# send until success
def send_until_success(input_id: str, keys: str, wait_time: int, driver):
	logging.debug('start try send keys to input with id: ' + str(input_id))

	try:
		submit_button = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.ID, input_id)))
		try_click = True
		while try_click:
			time.sleep(random.uniform(CHECK_SPEED_MIN, CHECK_SPEED_MAX))
			try:
				submit_button.send_keys(keys)
				try_click = False
			except ElementClickInterceptedException:
				logging.debug('try click: ElementClickInterceptedException!')
			except:
				logging.debug('try click: unknown error')
	# TODO add specific check for button id not found instead of assuming every errors have this meaning
	except:
		logging.warning("couldn't find the button with id: " + str(input_id))
	time.sleep(0.2)

# display a pop up, pause the script until the pop up is closed
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
	options = Options()
	options.binary_location = get_script_path() + '/chrome/linux-121.0.6167.184/chrome-linux64/chrome'
	driver = webdriver.Chrome(chrome_options = options, executable_path= get_script_path() + '/chromedriver/linux-121.0.6167.184/chromedriver-linux64/chromedriver')
	driver.get(PORTAL_URL)
	driver.implicitly_wait(10)

	# log on, if needed
	send_until_success("uc-logonForm-login", ID, 5, driver) # main wait time for the page to load correctly
	send_until_success("uc-logonForm-passwd", PASS, 0, driver)
	click_until_success_checkbox("logonForm_logon_privatePolicy_accept", 0, driver)
	click_until_success("logonForm_connect_button", 0, driver)

	# if we're already connected, disconnect to reset connexion timer
	click_until_success("feedbackForm_disconnect_button", 0, driver)

	# check if we reconnected successfully
	check_feedback = True
	while check_feedback:
		# connect!
		click_until_success("informativeWidget_connect_button", 10, driver)
		time.sleep(random.uniform(CHECK_SPEED_MIN, CHECK_SPEED_MAX))
		message = ''
		try:
			message = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "welcomeHeadline")))
		except:
			logging.warning('no welcomeHeadline, the connection button probably doesn\'t work')
			driver.refresh() # since the portal is as stable as nitroglycerin, sometimes we need to refresh the page to get the connection button to work

		if hasattr(message, 'text') and (str(message.text) == 'Bienvenue' or str(message.text) == 'Welcome'):
			check_feedback = False
		else:
			logging.debug('check_feedback not ready yet')
	# add a random time sleep so it looks like we're taking time to close the page like a human otherwise it's instantaneous
	time.sleep(random.uniform(CHECK_SPEED_MIN, CHECK_SPEED_MAX))
	driver.quit()

	# 3. execute os command 2
	execute_command(CMD_2)

# --- MAIN ---
try:
	# load env variables
	load_dotenv() 
	CMD_1 = os.getenv('CMD_1', 'you_didnt_set_an_env_variableCMD_1') # command executed before connection
	CMD_2 = os.getenv('CMD_2', 'you_didnt_set_an_env_variableCMD_2') # command executed after connection
	ID = os.getenv('ID', 'you_didnt_set_an_env_variableID')
	PASS = os.getenv('PASS',  'you_didnt_set_an_env_variablePASS')
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