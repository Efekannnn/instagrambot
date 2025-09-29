#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style
import pandas as pd

from proxy_manager import ProxyManager
from user_generator import UserGenerator
from instagram_automation import InstagramAutomation

# Colorama'yı başlat
init()

def print_banner():
    """Başlangıç banner'ı"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════╗
║     Instagram Çoklu Hesap Oluşturucu      ║
║              v1.0.0                       ║
╚═══════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def load_config():
    """Konfigürasyon dosyasını yükle"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"{Fore.GREEN}✓ Konfigürasyon yüklendi{Style.RESET_ALL}")
        return config
    except FileNotFoundError:
        print(f"{Fore.RED}✗ config.json dosyası bulunamadı!{Style.RESET_ALL}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}✗ config.json dosyası geçersiz!{Style.RESET_ALL}")
        sys.exit(1)

def test_proxies(proxy_manager, proxies):
    """Proxy'leri test et"""
    print(f"\n{Fore.YELLOW}🔍 Proxy'ler test ediliyor...{Style.RESET_ALL}")
    working_proxies = []
    
    for i, proxy in enumerate(proxies):
        print(f"\nProxy {i+1}/{len(proxies)}: {proxy}")
        if proxy_manager.test_proxy(proxy):
            working_proxies.append(proxy)
            
    print(f"\n{Fore.GREEN}✓ Çalışan proxy sayısı: {len(working_proxies)}/{len(proxies)}{Style.RESET_ALL}")
    return working_proxies

def create_accounts(config):
    """Ana hesap oluşturma fonksiyonu"""
    # Proxy yöneticisini oluştur
    proxy_manager = ProxyManager(config['proxies'])
    
    # Kullanıcı üreticisini oluştur
    user_generator = UserGenerator()
    
    # Sonuçları takip et
    results = {
        'successful': [],
        'failed': [],
        'total': config['settings']['account_count']
    }
    
    # Hesapları oluştur
    for i in range(config['settings']['account_count']):
        print(f"\n{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Hesap {i+1}/{config['settings']['account_count']} oluşturuluyor...{Style.RESET_ALL}")
        
        try:
            # Kullanıcı bilgilerini üret
            user_data = user_generator.generate_user(
                email_domain=config['settings']['email_domain']
            )
            
            # Proxy seç
            proxy = proxy_manager.get_random_proxy()
            print(f"Kullanılacak proxy: {proxy}")
            
            # Driver'ı başlat
            driver = proxy_manager.setup_driver_with_proxy(
                proxy, 
                headless=config['settings']['headless']
            )
            
            try:
                # Instagram automation'ı başlat
                instagram = InstagramAutomation(
                    driver, 
                    user_data,
                    save_screenshots=config['settings']['save_screenshots']
                )
                
                # Hesabı oluştur
                if instagram.create_account():
                    # Başarılı - bilgileri kaydet
                    instagram.save_account_info()
                    results['successful'].append(user_data)
                    print(f"{Fore.GREEN}✅ Hesap başarıyla oluşturuldu!{Style.RESET_ALL}")
                else:
                    results['failed'].append(user_data)
                    print(f"{Fore.RED}❌ Hesap oluşturulamadı!{Style.RESET_ALL}")
                    
            finally:
                # Driver'ı kapat
                driver.quit()
                
            # Hesaplar arası bekleme
            if i < config['settings']['account_count'] - 1:
                wait_time = random.randint(
                    config['settings']['min_wait'],
                    config['settings']['max_wait']
                )
                print(f"\n⏳ Sonraki hesap için {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
                
        except Exception as e:
            print(f"{Fore.RED}❌ Hata: {str(e)}{Style.RESET_ALL}")
            results['failed'].append({'error': str(e)})
            
    return results

def print_summary(results):
    """Özet rapor göster"""
    print(f"\n{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 ÖZET RAPOR{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
    
    success_rate = (len(results['successful']) / results['total']) * 100
    
    print(f"Toplam deneme: {results['total']}")
    print(f"{Fore.GREEN}✅ Başarılı: {len(results['successful'])}{Style.RESET_ALL}")
    print(f"{Fore.RED}❌ Başarısız: {len(results['failed'])}{Style.RESET_ALL}")
    print(f"Başarı oranı: {success_rate:.1f}%")
    
    if results['successful']:
        print(f"\n{Fore.GREEN}Başarılı hesaplar:{Style.RESET_ALL}")
        for user in results['successful']:
            print(f"  • {user['username']} - {user['email']}")
            
    if results['failed']:
        print(f"\n{Fore.RED}Başarısız denemeler:{Style.RESET_ALL}")
        for i, fail in enumerate(results['failed']):
            print(f"  • Deneme {i+1}: {fail.get('error', 'Bilinmeyen hata')}")

def main():
    """Ana fonksiyon"""
    print_banner()
    
    # Konfigürasyonu yükle
    config = load_config()
    
    # Proxy'leri test et (opsiyonel)
    print(f"\n{Fore.YELLOW}Proxy'leri test etmek ister misiniz? (e/h):{Style.RESET_ALL} ", end='')
    test_choice = input().lower()
    
    if test_choice == 'e':
        working_proxies = test_proxies(
            ProxyManager(config['proxies']), 
            config['proxies']
        )
        
        if not working_proxies:
            print(f"{Fore.RED}✗ Çalışan proxy bulunamadı!{Style.RESET_ALL}")
            sys.exit(1)
            
        # Sadece çalışan proxy'leri kullan
        config['proxies'] = working_proxies
        
    # Hesapları oluştur
    print(f"\n{Fore.CYAN}🚀 Hesap oluşturma işlemi başlıyor...{Style.RESET_ALL}")
    results = create_accounts(config)
    
    # Özet raporu göster
    print_summary(results)
    
    print(f"\n{Fore.GREEN}✅ İşlem tamamlandı!{Style.RESET_ALL}")
    print(f"Hesap bilgileri 'accounts.xlsx' dosyasına kaydedildi.")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ İşlem kullanıcı tarafından durduruldu.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Beklenmeyen hata: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)