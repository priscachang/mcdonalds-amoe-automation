from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import re
import imaplib
import email as email_lib

class McDonaldsVerification:
    def __init__(self, email_address, email_password, 
                 first_name, last_name, suffix,
                 street_address, city, state, zip_code,
                 apartment="", imap_server="imap.gmail.com"):
        """
        McDonald's AMOE verification and data filling automation
        
        Args:
            email_address: Your email address
            email_password: Email password (use app password for Gmail)
            first_name: First name
            last_name: Last name
            suffix: Suffix (like Jr., Sr., III, etc.)
            street_address: Street address
            city: City
            state: State (like NY, CA)
            zip_code: Zip code
            apartment: Apartment number (optional)
            imap_server: IMAP server
        """
        self.email_address = email_address
        self.email_password = email_password
        self.imap_server = imap_server
        self.first_name = first_name
        self.last_name = last_name
        self.suffix = suffix
        self.street_address = street_address
        self.apartment = apartment
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        options = Options()
        # options.add_argument('--headless')  # Uncomment to run in background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)
        
    def connect_to_email(self):
        """Connect to email server"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_address, self.email_password)
            mail.select('inbox')
            return mail
        except Exception as e:
            print(f"✗ Failed to connect to email: {str(e)}")
            raise
        
    def get_verification_info(self, max_attempts=10, wait_time=15):
        """
        Get verification links and OTP codes from multiple verification emails
        Returns: list[(verification_link, otp_code)]
        """
        print("\n⏳ Waiting for verification emails...")
        
        for attempt in range(max_attempts):
            try:
                mail = self.connect_to_email()
                
                # Search for McDonald's emails (unread)
                status, messages = mail.search(None, '(FROM "playatmcd.com" UNSEEN)')
                if status != 'OK':
                    time.sleep(wait_time)
                    continue
                
                email_ids = messages[0].split()
                if not email_ids:
                    print(f"  Attempt {attempt + 1}/{max_attempts}... No new emails yet")
                    time.sleep(wait_time)
                    continue
                
                verification_items = []
                
                # Process all unread emails
                for email_id in email_ids:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    if status != 'OK':
                        continue
                    
                    raw_email = msg_data[0][1]
                    msg = email_lib.message_from_bytes(raw_email)
                    
                    # Parse email content
                    body_text = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() in ["text/plain", "text/html"]:
                                try:
                                    body_text += part.get_payload(decode=True).decode(errors="ignore")
                                except:
                                    pass
                    else:
                        body_text = msg.get_payload(decode=True).decode(errors="ignore")
                    
                    # 提取驗證連結
                    links = re.findall(r'https://amoe\.playatmcd\.com/verify_your_email\?token=[^\s<>"]+', body_text)
                    verification_link = links[0] if links else None
                    
                    # Extract OTP code (6 digits)
                    otp_patterns = (
                        re.findall(r'Your One Time Password Code:\s*(\d{6})', body_text)
                        or re.findall(r'<strong[^>]*>(\d{6})</strong>', body_text)
                        or re.findall(r'\b(\d{6})\b', body_text)
                    )
                    otp_code = otp_patterns[0] if otp_patterns else None
                    
                    if verification_link and otp_code:
                        verification_items.append((verification_link, otp_code))
                        print(f"✓ Found OTP: {otp_code}")
                
                mail.close()
                mail.logout()
                
                if verification_items:
                    print(f"\n✅ Found {len(verification_items)} verification emails in total")
                    return verification_items
            
            except Exception as e:
                print(f"  Error occurred while checking emails: {str(e)}")
            
            time.sleep(wait_time)
        
        print("✗ Could not find any verification emails")
        return []

    
    def step2_verify_email(self, verification_link, otp_code):
        """Step 2: Click verification link and enter OTP"""
        try:
            print("\n" + "=" * 60)
            print("Step 2: Email Verification")
            print("=" * 60)
            
            print(f"🌐 Opening verification link...")
            self.driver.get(verification_link)
            
            wait = WebDriverWait(self.driver, 15)
            time.sleep(1)
            
            # Enter OTP code
            try:
                otp_input = wait.until(
                    EC.presence_of_element_located((By.ID, "otp"))
                )
                otp_input.clear()
                otp_input.send_keys(otp_code)
                print(f"✓ Entered OTP code: {otp_code}")
            except Exception as e:
                print(f"✗ Failed to enter OTP: {str(e)}")
                return False
            
            time.sleep(1)
            
            # Click verification button
            try:
                verify_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                verify_button.click()
                print("✓ Clicked verification button")
                time.sleep(1)
                return True
            except Exception as e:
                print(f"⚠ Failed to click verification button: {str(e)}")
                return False
                
        except Exception as e:
            print(f"✗ Error occurred during verification: {str(e)}")
            return False
    
    def step3_fill_information(self):
        """Step 3: Fill in complete information"""
        try:
            print("\n" + "=" * 60)
            print("Step 3: Fill in Personal Information")
            print("=" * 60)
            
            wait = WebDriverWait(self.driver, 15)
            time.sleep(2)
            
            # First Name
            first_name_input = wait.until(
                EC.presence_of_element_located((By.ID, "first_name"))
            )
            first_name_input.clear()
            first_name_input.send_keys(self.first_name)
            print(f"✓ First Name: {self.first_name}")
            
            # Last Name
            last_name_input = self.driver.find_element(By.ID, "last_name")
            last_name_input.clear()
            last_name_input.send_keys(self.last_name)
            print(f"✓ Last Name: {self.last_name}")
            
            # Suffix
            try:
                suffix_select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[id='suffix']"))
                suffix_select.select_by_visible_text(self.suffix)
                print(f"✓ Suffix: {self.suffix}")
            except Exception as e:
                print(f"⚠ Suffix: {str(e)}")
            
            time.sleep(0.5)
            
            # Street Address
            street_input = self.driver.find_element(By.ID, "address")
            street_input.clear()
            street_input.send_keys(self.street_address)
            print(f"✓ Street Address: {self.street_address}")
            
            # Apartment (optional)
            if self.apartment:
                apartment_input = self.driver.find_element(By.ID, "address2")
                apartment_input.clear()
                apartment_input.send_keys(self.apartment)
                print(f"✓ Apartment: {self.apartment}")
            
            # City
            city_input = self.driver.find_element(By.ID, "city")
            city_input.clear()
            city_input.send_keys(self.city)
            print(f"✓ City: {self.city}")
            
            # State
            state_select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[id='state']"))
            state_select.select_by_value(self.state)
            print(f"✓ State: {self.state}")
            
            # Zip Code
            zip_input = self.driver.find_element(By.ID, "zip")
            zip_input.clear()
            zip_input.send_keys(self.zip_code)
            print(f"✓ Zip Code: {self.zip_code}")
            
            time.sleep(1)
            
            # Click Validate My Address
            try:
                validate_button = self.driver.find_element(By.ID, "validateaddress")
                self.driver.execute_script("arguments[0].click();", validate_button)
                print("✓ Clicked Validate My Address")
                time.sleep(2)
            except Exception as e:
                print(f"⚠ Validate Address: {str(e)}")
            
            # Click Validate My Address2
            try:
                validate_button2 = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm Address')]")
                self.driver.execute_script("arguments[0].click();", validate_button2)
                print("✓ Clicked Validate My Address2")
                time.sleep(2)
            except Exception as e:
                print(f"⚠ Validate Address2: {str(e)}")
            
            # Click Submit Game Code Request
            try:
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                submit_button.click()
                print("✓ Clicked Submit Game Code Request")
                time.sleep(2)
                return True
            except Exception as e:
                print(f"⚠ Submit button: {str(e)}")
                print("Please manually click the Submit button")
                return True
                
        except Exception as e:
            print(f"✗ Error occurred while filling in data: {str(e)}")
            return False
    
    def run(self):
        """Execute the complete automation process"""
        try:
            print("=" * 60)
            print("McDonald's AMOE Automatic Verification and Filling")
            print("=" * 60)
            
            # Setup browser
            self.setup_driver()
            
            # Step 2: Get verification information
            verification_list = self.get_verification_info()
            if not verification_list:
                print("\n✗ Unable to retrieve any verification emails")
                input("\nPress Enter to close...")
                return

            for i, (verification_link, otp_code) in enumerate(verification_list, start=1):
                print(f"\n=== Processing Email {i} ===")
                if not self.step2_verify_email(verification_link, otp_code):
                    print(f"✗ Email {i} verification failed, skipping")
                    continue
                if not self.step3_fill_information():
                    print(f"⚠ Email {i} filling incomplete, skipping")
                    continue
                print(f"✅ Email {i} completed!")

            
        except Exception as e:
            print(f"\n✗ Error occurred: {str(e)}")
            input("\nPress Enter to close...")
        
        finally:
            if self.driver:
                self.driver.quit()


# Usage example
if __name__ == "__main__":
    # Set your information
    automation = McDonaldsVerification(
        # Email settings
        email_address="prchangfighting@gmail.com",
        email_password="etbk mycn eqfx uozs",  # Gmail app password
        
        # Personal information
        first_name="Prisca",
        last_name="Chang",
        suffix="II",  # Leave empty or fill Jr., Sr., III, etc.
        
        # Address information
        street_address="50 West 97th Street",
        apartment="",  # Optional
        city="New York",
        state="NY",
        zip_code="10025-6053"
    )
    
    automation.run()