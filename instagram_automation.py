import time
import random
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from colorama import init, Fore, Style

# Colorama'yı başlat
init()

class InstagramAutomation:
    def __init__(self, driver, user_data, save_screenshots=True):
        self.driver = driver
        self.user_data = user_data
        self.save_screenshots = save_screenshots
        self.screenshot_dir = "screenshots"
        
        if self.save_screenshots and not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            
    def _wait_random(self, min_seconds=1, max_seconds=3):
        """İnsan benzeri rastgele bekleme"""
        time.sleep(random.uniform(min_seconds, max_seconds))
        
    def _type_like_human(self, element, text):
        """İnsan gibi yavaş yazma"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
            
    def _save_screenshot(self, name):
        """Ekran görüntüsü al"""
        if self.save_screenshots:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.screenshot_dir}/{self.user_data['username']}_{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            print(f"  📸 Ekran görüntüsü kaydedildi: {filename}")
            
    def _handle_cookies(self):
        """Cookie popup'ını kapat"""
        try:
            # "Tümünü Kabul Et" veya "Accept All" butonunu ara
            cookie_buttons = [
                "//button[contains(text(), 'Tümünü Kabul Et')]",
                "//button[contains(text(), 'Accept All')]",
                "//button[contains(text(), 'Allow All')]",
                "//button[contains(text(), 'İzin Ver')]"
            ]
            
            for xpath in cookie_buttons:
                try:
                    cookie_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    cookie_btn.click()
                    print("  ✓ Cookie popup'ı kapatıldı")
                    self._wait_random(1, 2)
                    break
                except:
                    continue
                    
        except:
            pass
            
    def _check_if_logged_in(self):
        """Giriş yapılıp yapılmadığını kontrol et"""
        try:
            # Instagram ana sayfasındaki elementleri kontrol et
            home_elements = [
                "//a[@href='/']",  # Ana sayfa ikonu
                "//span[contains(@aria-label, 'Home')]",
                "//svg[@aria-label='Home']"
            ]
            
            for xpath in home_elements:
                try:
                    self.driver.find_element(By.XPATH, xpath)
                    return True
                except:
                    continue
                    
            return False
            
        except:
            return False
            
    def create_account(self):
        """Instagram hesabı oluştur"""
        try:
            print(f"\n{Fore.CYAN}🚀 Hesap oluşturma başlıyor: {self.user_data['username']}{Style.RESET_ALL}")
            
            # Instagram kayıt sayfasına git
            self.driver.get("https://www.instagram.com/accounts/emailsignup/")
            self._wait_random(3, 5)
            
            # Cookie popup'ını kapat
            self._handle_cookies()
            
            # Kayıt formunu doldur
            self._fill_signup_form()
            
            # Doğum tarihini gir
            self._enter_birthdate()
            
            # Hesabı oluştur
            self._complete_signup()
            
            # Profili tamamla (opsiyonel)
            self._complete_profile()
            
            print(f"\n{Fore.GREEN}✅ Hesap başarıyla oluşturuldu: {self.user_data['username']}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Hesap oluşturma hatası: {str(e)}{Style.RESET_ALL}")
            self._save_screenshot("error")
            return False
            
    def _fill_signup_form(self):
        """Kayıt formunu doldur"""
        print("  📝 Kayıt formu dolduruluyor...")
        
        try:
            # Email alanı
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "emailOrPhone"))
            )
            self._type_like_human(email_input, self.user_data['email'])
            self._wait_random(1, 2)
            
            # Tam ad alanı
            fullname_input = self.driver.find_element(By.NAME, "fullName")
            self._type_like_human(fullname_input, self.user_data['full_name'])
            self._wait_random(1, 2)
            
            # Kullanıcı adı alanı
            username_input = self.driver.find_element(By.NAME, "username")
            self._type_like_human(username_input, self.user_data['username'])
            self._wait_random(1, 2)
            
            # Şifre alanı
            password_input = self.driver.find_element(By.NAME, "password")
            self._type_like_human(password_input, self.user_data['password'])
            self._wait_random(1, 2)
            
            self._save_screenshot("form_filled")
            
            # Kayıt ol butonuna tıkla
            signup_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            signup_button.click()
            self._wait_random(3, 5)
            
            print("  ✓ Form başarıyla dolduruldu")
            
        except TimeoutException:
            raise Exception("Kayıt formu yüklenemedi")
            
    def _enter_birthdate(self):
        """Doğum tarihini gir"""
        print("  📅 Doğum tarihi giriliyor...")
        
        try:
            # Doğum tarihi sayfasının yüklenmesini bekle
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select[@title='Month:']"))
            )
            
            # Ay seçimi
            month_select = self.driver.find_element(By.XPATH, "//select[@title='Month:']")
            month_select.click()
            self._wait_random(0.5, 1)
            month_option = month_select.find_element(By.XPATH, f"//option[@value='{self.user_data['birthdate']['month']}']")
            month_option.click()
            
            # Gün seçimi
            day_select = self.driver.find_element(By.XPATH, "//select[@title='Day:']")
            day_select.click()
            self._wait_random(0.5, 1)
            day_option = day_select.find_element(By.XPATH, f"//option[@value='{self.user_data['birthdate']['day']}']")
            day_option.click()
            
            # Yıl seçimi
            year_select = self.driver.find_element(By.XPATH, "//select[@title='Year:']")
            year_select.click()
            self._wait_random(0.5, 1)
            year_option = year_select.find_element(By.XPATH, f"//option[@value='{self.user_data['birthdate']['year']}']")
            year_option.click()
            
            self._save_screenshot("birthdate_entered")
            
            # İleri butonuna tıkla
            next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'İleri')]")
            next_button.click()
            self._wait_random(2, 4)
            
            print("  ✓ Doğum tarihi girildi")
            
        except Exception as e:
            print(f"  ⚠️ Doğum tarihi girilemedi: {str(e)}")
            
    def _complete_signup(self):
        """Kayıt işlemini tamamla"""
        print("  🔐 Hesap oluşturuluyor...")
        
        try:
            # Onay kodu sayfasını kontrol et (email doğrulama gerekebilir)
            try:
                code_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "email_confirmation_code"))
                )
                print(f"  ⚠️ Email doğrulama gerekiyor: {self.user_data['email']}")
                print("  ⏳ Onay kodu bekleniyor (30 saniye)...")
                
                # Kullanıcının manuel olarak kodu girmesini bekle
                time.sleep(30)
                
            except TimeoutException:
                # Onay kodu gerekmiyorsa devam et
                pass
                
            # Hesap oluşturulduysa ana sayfaya yönlendirilir
            self._wait_random(3, 5)
            
            if self._check_if_logged_in():
                print("  ✓ Hesap başarıyla oluşturuldu ve giriş yapıldı")
                self._save_screenshot("account_created")
                return True
            else:
                # Bazı durumlarda ekstra adımlar olabilir
                self._handle_additional_steps()
                
        except Exception as e:
            print(f"  ❌ Hesap oluşturma hatası: {str(e)}")
            raise
            
    def _handle_additional_steps(self):
        """Ek adımları işle (güvenlik kontrolleri, vb.)"""
        try:
            # "Not Now" veya "Şimdi Değil" butonlarını ara
            skip_buttons = [
                "//button[contains(text(), 'Not Now')]",
                "//button[contains(text(), 'Şimdi Değil')]",
                "//a[contains(text(), 'Not Now')]",
                "//a[contains(text(), 'Şimdi Değil')]"
            ]
            
            for xpath in skip_buttons:
                try:
                    skip_btn = self.driver.find_element(By.XPATH, xpath)
                    skip_btn.click()
                    self._wait_random(1, 2)
                except:
                    continue
                    
        except:
            pass
            
    def _complete_profile(self):
        """Profili tamamla (bio ekle, vb.)"""
        try:
            print("  👤 Profil tamamlanıyor...")
            
            # Profil sayfasına git
            self.driver.get(f"https://www.instagram.com/{self.user_data['username']}/")
            self._wait_random(2, 3)
            
            # Profili düzenle butonuna tıkla
            try:
                edit_profile_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit Profile') or contains(text(), 'Profili Düzenle')]"))
                )
                edit_profile_btn.click()
                self._wait_random(2, 3)
                
                # Bio ekle
                bio_textarea = self.driver.find_element(By.XPATH, "//textarea[@id='pepBio']")
                self._type_like_human(bio_textarea, self.user_data['bio'])
                
                # Kaydet
                save_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                save_btn.click()
                self._wait_random(1, 2)
                
                print("  ✓ Profil tamamlandı")
                
            except:
                print("  ℹ️ Profil düzenleme atlandı")
                
        except Exception as e:
            print(f"  ⚠️ Profil tamamlama hatası: {str(e)}")
            
    def logout(self):
        """Instagram'dan çıkış yap"""
        try:
            # Profil menüsünü aç
            profile_menu = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@role='link' and contains(@tabindex, '-1')]"))
            )
            profile_menu.click()
            self._wait_random(1, 2)
            
            # Çıkış yap
            logout_btn = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Log Out') or contains(text(), 'Çıkış Yap')]")
            logout_btn.click()
            self._wait_random(1, 2)
            
            print("  ✓ Çıkış yapıldı")
            
        except:
            print("  ⚠️ Çıkış yapılamadı")
            
    def save_account_info(self, filename="accounts.xlsx"):
        """Hesap bilgilerini Excel'e kaydet"""
        account_info = {
            'Username': self.user_data['username'],
            'Email': self.user_data['email'],
            'Password': self.user_data['password'],
            'Full Name': self.user_data['full_name'],
            'Created At': self.user_data['created_at'],
            'Status': 'Active'
        }
        
        # Mevcut dosyayı kontrol et
        if os.path.exists(filename):
            df = pd.read_excel(filename)
            df = pd.concat([df, pd.DataFrame([account_info])], ignore_index=True)
        else:
            df = pd.DataFrame([account_info])
            
        # Excel'e kaydet
        df.to_excel(filename, index=False)
        print(f"  💾 Hesap bilgileri kaydedildi: {filename}")