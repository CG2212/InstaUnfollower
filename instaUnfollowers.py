from selenium import webdriver
from secret import username
from secret import pwd
from time import sleep
import pandas as pd
class InstaBot:
	def __init__(self, username, pwd):
		self.driver = webdriver.Firefox()
		self.driver.get("https://www.instagram.com/accounts/login/?hl=en")
		sleep(5)
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input")\
			.send_keys(username)
		
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input")\
			.send_keys(pwd)
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button")\
			.click()
		sleep(10)
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")\
			.click()
		sleep(5)
		self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")\
			.click()
		sleep(5)
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div/div[2]/div[1]/div/div/a")\
			.click()
		sleep(5)
	def profile(self):
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")\
			.click()
		following = self._get_names()
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[4]/a")\
			.click()
		followers = self._get_names()
		not_following_back = [user for user in following if user not in followers]
		#print(not_following_back)
		
		df = pd.DataFrame({'People who dont follow back':not_following_back})
		df.to_csv('unfollowers.csv', index=False,encoding='utf-8')

	def _get_names(self):
		sleep(5)
		scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
		
		last_height,height = 0,1
		while last_height != height:
			last_height = height
			sleep(2)
			height = self.driver.execute_script("""
				arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;""", scroll_box)

		links = scroll_box.find_elements_by_tag_name("a")
		names = [name.text for name in links if name.text != ""]
		self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
			.click()
		return names
a = InstaBot(username, pwd)
a.profile()
