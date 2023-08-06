import os
import time
import queue
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from .scripts import(
    Hcaptcha,
    ReCaptchaV2
    )

class InvalidSolverType(Exception):
    """Invalid solver type"""
    pass

class SolveTimedOut(Exception):
    """Current solve timed out"""
    pass


class new:
    def __init__(self, solver_type: str, url: str, site_key: str):

        if "hcaptcha" in solver_type.lower():
            self.script = Hcaptcha(site_key)
        elif "recaptchav2" in solver_type.lower():
            self.script = ReCaptchaV2(site_key)
        else:
            raise InvalidSolverType()

        self.queue = queue.Queue(maxsize=1)
        self._sentinel = object()

        options = Options()
        option_args = ["--allow-insecure-localhost", "--ignore-ssl-errors", 
            "--ignore-certificate-errors-spki-list", "--window-size=500,645", 
            "--ignore-certificate-errors", "user-agent=Chrome",
            "--disable-blink-features","--disable-blink-features=AutomationControlled",
            "--disable-extensions", "disable-infobars", "--allow-profiles-outside-user-dir"]
        for x in option_args:
            options.add_argument(x)

        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(url)
        self.driver.execute_script(self.script.template)

        time.sleep(3)

    def solve(self, timeout: float = 100):
        while True:
            if not self.queue.full():
                self.queue.put('s')
                self.driver.execute_script(self.script.invoke)

                try:
                    resp = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, "captchaResp")))
                except:
                    self.driver.execute_script(self.script.template)
                    raise SolveTimedOut()

                time.sleep(1)

                captcha = resp.get_attribute("value")

                self.driver.execute_script(self.script.template)
                self.queue.get()
                return captcha
                        

    def close(self):
        self.queue.put(self._sentinel)
        self.driver.close()



