import os 
import re
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from django.conf import settings

class SeleniumProcessor:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")
        driver_path = settings.SELENIUM_WEBDRIVER_PATH
        self.service = ChromeService(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

    def _extract_social_links(self, page_source: str, updated_data: Dict[str, Any]) -> None:
        social_patterns = {
            'linkedin_url': r'https://(www\.)?linkedin\.com/(company|in)/[^\'"]+',
            'facebook_url': r'https://(www\.)?facebook\.com/[^\'"]+',
            'instagram_url': r'https://(www\.)?instagram\.com/[^\'"]+',
        }
        for key, pattern in social_patterns.items():
            match = re.search(pattern, page_source, re.IGNORECASE)
            if match:
                found_url = match.group(0)
                if key == 'facebook_url':
                    found_url = found_url.split('?')[0]
                if key == 'instagram_url':
                    found_url = found_url.split('?')[0]
                updated_data[key] = found_url

    def run_validation(self, url: str, old_data: Dict[str, Any]) -> Dict[str, Any]:
        updated_data = old_data.copy()

        if not url or url.lower() == 'n/a' or not url.startswith(('http', 'https')):
            updated_data['selenium_status'] = 'NO_VALID_URL'
            return updated_data
        
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            page_source = self.driver.page_source

            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', page_source)
            if email_match:
                updated_data['extracted_email'] = email_match.group(0)

            self._extract_social_links(page_source, updated_data)

            phone_match = re.search(r'\(?\+?\d{1,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4,10}', page_source)
            if phone_match:
                updated_data['extracted_phone'] = phone_match.group(0).strip()

            updated_data['selenium_status'] = 'SUCCESS_ENRICHED'

        except TimeoutException:
            updated_data['selenium_status'] = 'ERROR_TIMEOUT'
        except WebDriverException as e:
            updated_data['selenium_status'] = f'ERROR_WEBDRIVER: {str(e)[:100]}'
        except Exception as e:
            updated_data['selenium_status'] = f'ERROR_UNKWN: {str(e)[:100]}'
            print(f"Error en Selenium para {url}: {e}")
        return updated_data