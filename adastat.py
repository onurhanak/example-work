from selenium import webdriver # we are not using requests because adastat needs javascript to load data
from selenium.webdriver.chrome.options import Options # we'll use options to run chrome headless
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

sleep_time=10

def adastat_scraper(wallet_address):

    # base url for adastat
    base_url='https://adastat.net/accounts/'

    # add wallet address to base url
    wallet_url=base_url+wallet_address

    inform_client=f'Getting data for {wallet_address} from {wallet_url}' 
    warn_client=f'Had an error getting data for {wallet_address} from {wallet_url}'    
    
    # add options and initialize driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    options.add_argument("--log-level=3") # to make it shut up
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path='chromedriver',options=options)
    
    try:
        driver.get(wallet_url)

        print(inform_client)

        # wait for page to load, 10 seconds seems to be enough
        sleep(sleep_time)
        WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.CLASS_NAME, 'uk-text-meta')))
        # get what we are interested in
        balance = driver.find_element(By.CSS_SELECTOR, "#main > div.uk-child-width-1-3\@m.uk-grid-match.uk-grid.margin-15-top.margin-15-bottom > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2)")
        total_amount = f'ADA {balance.text[:-2]}'

        balances=[]
        balances.append(total_amount)
        return balances
    
    except NoSuchElementException:
        print(warn_client)
        print('I will try again.')
        adastat_scraper(wallet_address)