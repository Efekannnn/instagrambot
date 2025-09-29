#!/usr/bin/env python3
"""
Advanced Proxy Manager for Instagram Bot
Handles proxy rotation, validation, and management
"""

import os
import time
import random
import requests
import logging
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import yaml

logger = logging.getLogger(__name__)


class AdvancedProxyManager:
    """Advanced proxy management with validation and rotation"""
    
    def __init__(self, proxy_file='config/proxies.yaml'):
        self.proxy_file = proxy_file
        self.proxies = []
        self.valid_proxies = []
        self.failed_proxies = []
        self.current_index = 0
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file"""
        try:
            with open(self.proxy_file, 'r') as f:
                data = yaml.safe_load(f)
                self.proxies = data.get('proxies', [])
                logger.info(f"Loaded {len(self.proxies)} proxies")
        except FileNotFoundError:
            logger.warning(f"Proxy file not found: {self.proxy_file}")
            self.proxies = []
    
    def save_proxies(self):
        """Save proxy list with status"""
        data = {
            'proxies': self.proxies,
            'valid_proxies': self.valid_proxies,
            'failed_proxies': self.failed_proxies,
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(self.proxy_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def format_proxy_url(self, proxy: Dict) -> str:
        """Format proxy dictionary to URL string"""
        protocol = proxy.get('protocol', 'http')
        host = proxy.get('host')
        port = proxy.get('port', 8080)
        username = proxy.get('username', '')
        password = proxy.get('password', '')
        
        if username and password:
            return f"{protocol}://{username}:{password}@{host}:{port}"
        else:
            return f"{protocol}://{host}:{port}"
    
    def test_proxy(self, proxy: Dict, timeout: int = 10) -> bool:
        """Test if proxy is working"""
        proxy_url = self.format_proxy_url(proxy)
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        test_urls = [
            'http://httpbin.org/ip',
            'https://api.ipify.org?format=json'
        ]
        
        for url in test_urls:
            try:
                response = requests.get(
                    url,
                    proxies=proxies,
                    timeout=timeout
                )
                if response.status_code == 200:
                    logger.info(f"Proxy working: {proxy.get('host')}:{proxy.get('port')}")
                    return True
            except Exception as e:
                logger.debug(f"Proxy test failed for {proxy.get('host')}: {str(e)}")
        
        return False
    
    def validate_all_proxies(self, max_workers: int = 10):
        """Validate all proxies concurrently"""
        logger.info("Validating all proxies...")
        self.valid_proxies = []
        self.failed_proxies = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self.test_proxy, self.proxies)
            
            for proxy, is_valid in zip(self.proxies, results):
                if is_valid:
                    self.valid_proxies.append(proxy)
                else:
                    self.failed_proxies.append(proxy)
        
        logger.info(f"Validation complete: {len(self.valid_proxies)} valid, {len(self.failed_proxies)} failed")
        self.save_proxies()
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Get next proxy in rotation"""
        if not self.valid_proxies:
            logger.warning("No valid proxies available")
            return None
        
        proxy = self.valid_proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.valid_proxies)
        return proxy
    
    def get_random_proxy(self) -> Optional[Dict]:
        """Get random proxy from valid list"""
        if not self.valid_proxies:
            logger.warning("No valid proxies available")
            return None
        
        return random.choice(self.valid_proxies)
    
    def get_proxy_by_location(self, country: str) -> Optional[Dict]:
        """Get proxy from specific country"""
        country_proxies = [
            p for p in self.valid_proxies 
            if p.get('country', '').lower() == country.lower()
        ]
        
        if country_proxies:
            return random.choice(country_proxies)
        
        logger.warning(f"No proxies available for country: {country}")
        return None
    
    def mark_proxy_failed(self, proxy: Dict):
        """Mark a proxy as failed"""
        if proxy in self.valid_proxies:
            self.valid_proxies.remove(proxy)
            self.failed_proxies.append(proxy)
            self.save_proxies()
            logger.info(f"Marked proxy as failed: {proxy.get('host')}")
    
    def get_proxy_stats(self) -> Dict:
        """Get proxy statistics"""
        return {
            'total': len(self.proxies),
            'valid': len(self.valid_proxies),
            'failed': len(self.failed_proxies),
            'success_rate': len(self.valid_proxies) / len(self.proxies) * 100 if self.proxies else 0
        }


class ProxyPool:
    """Manage a pool of proxies for multiple bots"""
    
    def __init__(self, proxies: List[Dict]):
        self.all_proxies = proxies
        self.available_proxies = proxies.copy()
        self.assigned_proxies = {}  # username -> proxy mapping
    
    def assign_proxy(self, username: str) -> Optional[Dict]:
        """Assign a proxy to a specific account"""
        if username in self.assigned_proxies:
            return self.assigned_proxies[username]
        
        if not self.available_proxies:
            logger.warning("No available proxies in pool")
            return None
        
        # Assign least used proxy
        proxy = self.available_proxies.pop(0)
        self.assigned_proxies[username] = proxy
        
        # Add back to available list for reuse if needed
        if len(self.assigned_proxies) > len(self.all_proxies):
            self.available_proxies.append(proxy)
        
        return proxy
    
    def release_proxy(self, username: str):
        """Release proxy assignment"""
        if username in self.assigned_proxies:
            proxy = self.assigned_proxies.pop(username)
            if proxy not in self.available_proxies:
                self.available_proxies.append(proxy)


def main():
    """Test proxy manager"""
    manager = AdvancedProxyManager()
    
    # Validate all proxies
    manager.validate_all_proxies()
    
    # Show stats
    stats = manager.get_proxy_stats()
    print(f"Proxy Stats: {stats}")
    
    # Get some proxies
    for i in range(5):
        proxy = manager.get_next_proxy()
        if proxy:
            print(f"Proxy {i+1}: {proxy.get('host')}:{proxy.get('port')}")


if __name__ == "__main__":
    main()