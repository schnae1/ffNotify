# Program logs into NFL Fantasy Football website
# and checks if anyone has dropped a player.
# If there is a drop, a text message is sent to
# notify the user. Checks every 30 minutes.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from twilio.rest import Client

#launch url
url = "https://fantasy.nfl.com/"

# create a new Chrome session
driver = webdriver.Chrome(executable_path='/home/eric/Python/fan_notify/chromedriver') # change path according to machine
driver.get(url)
assert "Fantasy" in driver.title

# get sign in link and click
menu_bar = driver.find_element_by_id('mobile-menu-button')
menu_bar.click()

sign_in_link = driver.find_element_by_class_name('sign-in-state')
sign_in_link.click()

# enter in credentials and log in
usr_email = driver.find_element_by_id('fanProfileEmailUsername')
usr_email.send_keys('email@address.com')

usr_psswd = driver.find_element_by_id('fanProfilePassword')
usr_psswd.send_keys('password')

submit_button = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div/div[3]/div[2]/main/div/div[2]/div[2]/form/div[3]/button')
submit_button.click()

driver.implicitly_wait(5) # wait 5 seconds

# navigate to desired page
league_link = driver.find_element_by_id('my_league')
league_link.click()

driver.implicitly_wait(5) # wait 5 seconds

Transactions_link = driver.find_element_by_link_text('Transactions')
Transactions_link.click()

drops_link = driver.find_element_by_link_text('Drops')
drops_link.click()

# Hand off to Beautiful Soup
soup = BeautifulSoup(driver.page_source, 'lxml')

# Get initial drop list
initial_drop = []
for item in soup.find_all("td", class_="playerNameAndInfo"):
	initial_drop.append(str(item.find_next("a").text))

while True:
	# Refresh page and hand off to Beautiful Soup
	driver.refresh()
	driver.implicitly_wait(5)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	
	# Get current drop list
	curr_drop = []
	for item in soup.find_all("td", class_="playerNameAndInfo"):
		curr_drop.append(str(item.find_next("a").text))

	if initial_drop != curr_drop:
		diff = list(set(curr_drop) - set(initial_drop))
		diff = ' '.join(diff)
		# Twilio Account SID and Auth Token
		client = Client("****Account SID****", "***Auth Token***")
		client.api.account.messages.create(to = "*yournumber*", from_ = "*twilio number*", body = diff)
		initial_drop = curr_drop[:]
	
	# Wait 30 minutes, 1800 seconds
	time.sleep(1800)

driver.close()
