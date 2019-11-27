from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import unittest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestJustEatTest(unittest.TestCase):  
    def setUp(self):
        #Inrializing the Chrome driver
        workingDir = os.path.dirname(os.path.abspath(__file__))
        self.driver= webdriver.Chrome(executable_path=workingDir+"\\chromedriver.exe")
        #base URL for the Paymi site
        base_url = "https://www.just-eat.co.uk/"
        self.driver.get(base_url)
        #maxmize the browser window 
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
   
    def test_InvaliadPostalCode_Should_Not_Allowed(self):
        #Xpath for the postcode input box and search button
        xpath_Postcode_inputBox = "//input[@name='postcode']"
        xpath_search_button ="//button[@data-test-id='find-restaurants-button']"
        errormessage_xpath = "//div[@id='errorMessage']"
        try:
            self.postcode_inputbox = self.driver.find_element_by_xpath(xpath_Postcode_inputBox)
            self.searchbutton = self.driver.find_element_by_xpath(xpath_search_button)

            self.postcode_inputbox.clear()
            self.postcode_inputbox.send_keys("Inavliad Post Code")
            self.searchbutton.click()
            errormessage = self.driver.find_element_by_xpath(errormessage_xpath)
            ActualText = errormessage.text
            self.assertEqual("Please enter a full, valid postcode",ActualText)
            print("Right error mesaage coming on entering invalid postcode")
        except NoSuchElementException:
            print(NoSuchElementException.msg)
    
    def test_click_search_without_postcode(self):
        xpath_search_button ="//button[@data-test-id='find-restaurants-button']"
        errormessage_xpath = "//div[@id='errorMessage']"
        try:
            self.searchbutton = self.driver.find_element_by_xpath(xpath_search_button)
            self.searchbutton.click()
            errormessage = self.driver.find_element_by_xpath(errormessage_xpath)
            ActualText = errormessage.text
            self.assertEqual("Please enter a postcode",ActualText)
            print("Right error Message comes clicking search without entering postal code")
        except NoSuchElementException:
            print(NoSuchElementException.msg)
    
    def test_ReturnListofResturants_for_valid_postalcod(self):
        xpath_Postcode_inputBox = "//input[@name='postcode']"
        xpath_search_button ="//button[@data-test-id='find-restaurants-button']"
        errormessage_xpath = "//div[@id='errorMessage']"
        restaurant_list ="//div[@data-test-id='openrestaurants']//section"
        try:
            self.postcode_inputbox = self.driver.find_element_by_xpath(xpath_Postcode_inputBox)
            self.searchbutton = self.driver.find_element_by_xpath(xpath_search_button)

            self.postcode_inputbox.clear()
            self.postcode_inputbox.send_keys("AR51 1AA")
            self.searchbutton.click()
            time.sleep(10)
            WebDriverWait(self.driver,20).until(
                EC.presence_of_element_located((By.XPATH,restaurant_list))
            )
            sections = self.driver.find_elements_by_xpath(restaurant_list)
            self.assertNotEqual(len(sections),0)
            print("Restaurant list is returning for valid PostalCode")
        except NoSuchElementException:
            print(NoSuchElementException.msg)
    
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()