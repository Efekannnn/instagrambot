import random
import string
from faker import Faker
import json
from datetime import datetime, timedelta

class UserGenerator:
    def __init__(self, locale='tr_TR'):
        self.fake = Faker(locale)
        self.used_usernames = set()
        self.used_emails = set()
        
        # Türkçe isimler ve kelimeler
        self.turkish_words = [
            'gunes', 'ay', 'yildiz', 'deniz', 'dag', 'cicek', 'bulut', 
            'ruzgar', 'mavi', 'yesil', 'mutlu', 'guzel', 'hayal', 'umut',
            'sevgi', 'dost', 'kardes', 'hayat', 'gonul', 'melek', 'sultan',
            'aslan', 'kaplan', 'kartal', 'sahin', 'yigit', 'cesur', 'altin'
        ]
        
        # Popüler Türk isimleri
        self.turkish_names = {
            'male': [
                'Ahmet', 'Mehmet', 'Ali', 'Hasan', 'Huseyin', 'Mustafa', 'Omer',
                'Emre', 'Can', 'Cem', 'Burak', 'Murat', 'Kemal', 'Fatih', 'Serkan',
                'Okan', 'Tolga', 'Onur', 'Ugur', 'Baris', 'Deniz', 'Kaan', 'Ege'
            ],
            'female': [
                'Ayse', 'Fatma', 'Zeynep', 'Elif', 'Merve', 'Busra', 'Esra',
                'Tugba', 'Seda', 'Asli', 'Gizem', 'Betul', 'Melis', 'Ceren',
                'Pinar', 'Burcu', 'Ezgi', 'Cansu', 'Dilara', 'Irem', 'Yasemin'
            ]
        }
        
    def generate_turkish_name(self, gender=None):
        """Türkçe isim üret"""
        if gender is None:
            gender = random.choice(['male', 'female'])
            
        first_name = random.choice(self.turkish_names[gender])
        last_name = self.fake.last_name()
        
        return first_name, last_name, gender
        
    def generate_username(self, first_name, last_name):
        """Benzersiz kullanıcı adı üret"""
        username_variations = []
        
        # İsimleri normalize et
        first_clean = self._normalize_turkish(first_name.lower())
        last_clean = self._normalize_turkish(last_name.lower())
        
        # Farklı username varyasyonları
        username_variations.extend([
            f"{first_clean}{last_clean}",
            f"{first_clean}.{last_clean}",
            f"{first_clean}_{last_clean}",
            f"{last_clean}{first_clean}",
            f"{first_clean}{random.randint(1, 999)}",
            f"{last_clean}{random.randint(1, 999)}",
            f"{first_clean}{last_clean}{random.randint(1, 99)}",
            f"{random.choice(self.turkish_words)}{first_clean}",
            f"{first_clean}{random.choice(self.turkish_words)}",
            f"{random.choice(self.turkish_words)}{random.randint(1, 999)}"
        ])
        
        # Benzersiz bir username bulana kadar dene
        for _ in range(100):
            username = random.choice(username_variations)
            username = username.replace(' ', '').replace('-', '')
            
            if len(username) > 30:
                username = username[:30]
                
            if username not in self.used_usernames and len(username) >= 3:
                self.used_usernames.add(username)
                return username
                
        # Fallback
        unique_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        username = f"{first_clean}{unique_suffix}"
        self.used_usernames.add(username)
        return username
        
    def _normalize_turkish(self, text):
        """Türkçe karakterleri normalize et"""
        turkish_chars = {
            'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
            'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
        }
        
        for turkish, english in turkish_chars.items():
            text = text.replace(turkish, english)
            
        return text
        
    def generate_email(self, username, domain='@gmail.com'):
        """Benzersiz email adresi üret"""
        email_variations = [
            f"{username}{domain}",
            f"{username}.{random.randint(1, 999)}{domain}",
            f"{username}.{datetime.now().year}{domain}",
            f"{username}.tr{domain}",
            f"{username}.istanbul{domain}"
        ]
        
        for _ in range(50):
            email = random.choice(email_variations)
            if email not in self.used_emails:
                self.used_emails.add(email)
                return email
                
        # Fallback
        unique_suffix = ''.join(random.choices(string.digits, k=6))
        email = f"{username}.{unique_suffix}{domain}"
        self.used_emails.add(email)
        return email
        
    def generate_password(self):
        """Güçlü şifre üret"""
        # En az 8 karakter, büyük/küçük harf, rakam ve özel karakter içermeli
        length = random.randint(12, 16)
        
        # Karakter setleri
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%&*"
        
        # Her tipten en az bir karakter garanti et
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Geri kalanını rastgele doldur
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
            
        # Karıştır
        random.shuffle(password)
        
        return ''.join(password)
        
    def generate_birthdate(self, min_age=18, max_age=35):
        """Doğum tarihi üret"""
        today = datetime.now()
        
        # Yaş aralığını belirle
        min_date = today - timedelta(days=max_age*365)
        max_date = today - timedelta(days=min_age*365)
        
        # Rastgele bir tarih seç
        time_between = max_date - min_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        
        birthdate = min_date + timedelta(days=random_days)
        
        return {
            'day': birthdate.day,
            'month': birthdate.month,
            'year': birthdate.year,
            'formatted': birthdate.strftime('%d/%m/%Y')
        }
        
    def generate_bio(self, name, age):
        """Instagram bio üret"""
        bios = [
            f"📍 İstanbul | {age} yaşında",
            f"✨ Hayat bir yolculuk | {name}",
            f"🌟 Mutluluk peşinde | {age}",
            f"📚 Kitap kurdu | ☕ Kahve bağımlısı",
            f"🎨 Sanat severim | 📷 Fotoğraf tutkunu",
            f"🌍 Gezgin ruh | ✈️ Dünya turu hayalim",
            f"🎵 Müzik ruhun gıdası | {name}",
            f"💪 Spor yaşam tarzım | 🏃‍♂️ Her gün yeni bir başlangıç",
            f"🍕 Yemek aşığı | 👨‍🍳 Amatör şef",
            f"🎮 Oyun sever | 🎯 Hedeflerime odaklı",
            f"📸 Anı koleksiyoncusu | {age} yaşında",
            f"🌈 Pozitif enerji | ✨ İyi vibes only",
            f"🎭 Tiyatro aşığı | 🎬 Film koleksiyoncusu",
            f"🏖️ Deniz, kum, güneş | Yaz aşığı",
            f"☕ Kahvesiz yapamam | 📖 Kitapsız asla"
        ]
        
        return random.choice(bios)
        
    def generate_user(self, email_domain='@gmail.com'):
        """Tam kullanıcı profili üret"""
        # İsim ve cinsiyet
        first_name, last_name, gender = self.generate_turkish_name()
        full_name = f"{first_name} {last_name}"
        
        # Kullanıcı adı
        username = self.generate_username(first_name, last_name)
        
        # Email
        email = self.generate_email(username, email_domain)
        
        # Şifre
        password = self.generate_password()
        
        # Doğum tarihi
        birthdate = self.generate_birthdate()
        age = datetime.now().year - birthdate['year']
        
        # Bio
        bio = self.generate_bio(first_name, age)
        
        # Telefon (opsiyonel - genelde email ile kayıt olunur)
        phone = self.fake.phone_number()
        
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'full_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'birthdate': birthdate,
            'bio': bio,
            'phone': phone,
            'created_at': datetime.now().isoformat()
        }
        
        return user_data
        
    def save_users_to_file(self, users, filename='generated_users.json'):
        """Üretilen kullanıcıları dosyaya kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
            
        print(f"✓ {len(users)} kullanıcı {filename} dosyasına kaydedildi.")
        
    def generate_multiple_users(self, count=10, email_domain='@gmail.com'):
        """Birden fazla kullanıcı üret"""
        users = []
        
        for i in range(count):
            user = self.generate_user(email_domain)
            users.append(user)
            print(f"✓ Kullanıcı {i+1}/{count} üretildi: {user['username']}")
            
        return users