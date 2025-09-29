import random
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

class ProxyManager:
    def __init__(self, proxies):
        self.proxies = proxies
        self.used_proxies = set()
        
    def get_random_proxy(self):
        """Rastgele bir proxy seç"""
        available_proxies = [p for p in self.proxies if p not in self.used_proxies]
        
        if not available_proxies:
            # Tüm proxy'ler kullanıldıysa, listeyi sıfırla
            self.used_proxies.clear()
            available_proxies = self.proxies
            
        proxy = random.choice(available_proxies)
        self.used_proxies.add(proxy)
        return proxy
    
    def parse_proxy(self, proxy_url):
        """Proxy URL'sini parse et"""
        parsed = urlparse(proxy_url)
        
        proxy_config = {
            'scheme': parsed.scheme,
            'host': parsed.hostname,
            'port': parsed.port,
            'username': parsed.username,
            'password': parsed.password
        }
        
        return proxy_config
    
    def setup_driver_with_proxy(self, proxy_url, headless=False):
        """Proxy ile Chrome driver kurulumu"""
        proxy_config = self.parse_proxy(proxy_url)
        
        # Chrome seçenekleri
        options = uc.ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
            
        # Temel güvenlik ayarları
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        
        # Dil ve lokasyon ayarları
        options.add_argument('--lang=tr-TR')
        options.add_preference('intl.accept_languages', 'tr-TR,tr,en-US,en')
        
        # Proxy ayarları
        if proxy_config['scheme'] in ['http', 'https']:
            if proxy_config['username'] and proxy_config['password']:
                # Kimlik doğrulamalı proxy için extension oluştur
                proxy_extension = self._create_proxy_auth_extension(
                    proxy_config['host'],
                    proxy_config['port'],
                    proxy_config['username'],
                    proxy_config['password']
                )
                options.add_extension(proxy_extension)
            else:
                # Kimlik doğrulamasız proxy
                options.add_argument(f'--proxy-server={proxy_config["scheme"]}://{proxy_config["host"]}:{proxy_config["port"]}')
                
        elif proxy_config['scheme'] == 'socks5':
            options.add_argument(f'--proxy-server=socks5://{proxy_config["host"]}:{proxy_config["port"]}')
            
        # Driver oluştur
        driver = uc.Chrome(options=options)
        
        # User agent'ı güncelle
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": driver.execute_script("return navigator.userAgent").replace("Headless", "")
        })
        
        return driver
    
    def _create_proxy_auth_extension(self, host, port, username, password):
        """Kimlik doğrulamalı proxy için Chrome extension oluştur"""
        import zipfile
        import os
        
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Proxy Auth Extension",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
        
        background_js = f"""
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{host}",
                    port: parseInt({port})
                }},
                bypassList: ["localhost"]
            }}
        }};
        
        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
        
        function callbackFn(details) {{
            return {{
                authCredentials: {{
                    username: "{username}",
                    password: "{password}"
                }}
            }};
        }}
        
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """
        
        # Extension dosyalarını oluştur
        plugin_file = 'proxy_auth_plugin.zip'
        
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
            
        return plugin_file
    
    def test_proxy(self, proxy_url):
        """Proxy'nin çalışıp çalışmadığını test et"""
        try:
            driver = self.setup_driver_with_proxy(proxy_url, headless=True)
            driver.get("http://httpbin.org/ip")
            
            # IP adresini kontrol et
            import json
            pre = driver.find_element("tag name", "pre")
            data = json.loads(pre.text)
            
            print(f"✓ Proxy çalışıyor: {proxy_url}")
            print(f"  IP Adresi: {data.get('origin', 'Bilinmiyor')}")
            
            driver.quit()
            return True
            
        except Exception as e:
            print(f"✗ Proxy çalışmıyor: {proxy_url}")
            print(f"  Hata: {str(e)}")
            return False