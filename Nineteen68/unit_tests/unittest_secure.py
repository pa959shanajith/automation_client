from appium import webdriver
from simple_aes_cipher import AESCipher, generate_secret_key
from appium.webdriver.common.touch_action import TouchAction
import platform
import unittest
import time

driver=None

def installApplication():
    try:
        if platform.system() == 'Darwin':
            desired_caps = {}
            desired_caps['platformName'] = 'iOS'
            desired_caps['appiumVersion'] = '1.6.5'
            desired_caps['platformVersion'] = '10.3'
            desired_caps['deviceName'] = 'iPhone 6s Plus'
            desired_caps['fullReset'] = False
            desired_caps['newCommandTimeout'] = 3600
            desired_caps['launchTimeout'] = 180000
            desired_caps['app'] = '/Users/nineteen68/Desktop/ios-R_2.0/apps/uicatalog/UICatalog.app'
            global driver
            driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
    except Exception as e:
        err_msg = "Not able to install or launch application"

def press(element):
    try:
        if element is not None:
            action = TouchAction(driver)
            action.tap(element).perform()
    except Exception as e:
        print "error"
        import traceback
        traceback.print_exc()
def swipe_up():
    try:
        size = driver.get_window_size()
        min_y = (size['height'] / 4)
        max_y = (size['height'] / 1.2)
        x_Value = (size['width'] * 0.50)
        #Swipe from down to up
        if platform.system() == 'Darwin':
            driver.execute_script('mobile: scroll', {'direction': 'down'})
        else:
            driver.swipe(x_Value, max_y, x_Value, min_y, 3000)
        time.sleep(3)
    except Exception as e:
        err_msg='Error thrown be android driver'
def setsecuretext(webelement,input):
    status= False
    if webelement is not None:
        try:
            if webelement.is_enabled():
                input=input
                if input is not None:
                    if platform.system() == 'Darwin':
                        webelement.clear()
                        secret_key = generate_secret_key('abcfhf')
                        encryption_obj = AESCipher(secret_key)
                        encrypt_text = encryption_obj.encrypt(input)
                        input_val = encryption_obj.decrypt(encrypt_text)
                        webelement.set_value(input_val)
                        status = True

            else:
                err_msg='element is disabled'

        except Exception as e:
            err_msg='exception occured'
            import traceback
            traceback.print_exc()
    return status
class Testclass(unittest.TestCase):
    def test_1(self):
        installApplication()
        swipe_up()
        with open("/Users/nineteen68/Downloads/secure.txt") as f:
            path = f.readlines()

        element=driver.find_element_by_xpath(path[0].strip('\n'))
        press(element)
        time.sleep(3)
        ele_secure=driver.find_element_by_xpath(path[1].strip('\n'))
        output=setsecuretext(ele_secure,"hi how r u")
        self.assertEqual(output,True)

if __name__ == '__main__':
    unittest.main()

