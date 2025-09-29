#!/usr/bin/env python3
"""
Multi-Bot Manager for Instagram
Manage multiple Instagram bots with different accounts and proxies
"""

import os
import sys
import time
import logging
import threading
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from dotenv import load_dotenv
from bot_with_proxy import InstagramBotWithProxy, ProxyManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/multi_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MultiBotManager:
    """Manage multiple Instagram bots simultaneously"""
    
    def __init__(self, config_path='config/multi_bot_config.yaml'):
        self.config = self.load_config(config_path)
        self.bots = []
        self.proxy_manager = None
        self.setup_proxy_manager()
        
    def load_config(self, config_path):
        """Load multi-bot configuration"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Multi-bot configuration loaded from {config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"Config file not found at {config_path}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Default multi-bot configuration"""
        return {
            'general': {
                'max_concurrent_bots': 3,
                'delay_between_starts': 60,
                'use_threading': True
            },
            'proxies': {
                'enabled': False,
                'rotate': True,
                'list': []
            },
            'accounts': []
        }
    
    def setup_proxy_manager(self):
        """Initialize proxy manager if proxies are configured"""
        proxy_config = self.config.get('proxies', {})
        
        if proxy_config.get('enabled', False):
            proxy_list = proxy_config.get('list', [])
            if proxy_list:
                self.proxy_manager = ProxyManager(proxy_list)
                logger.info(f"Proxy manager initialized with {len(proxy_list)} proxies")
    
    def get_proxy_for_account(self, account_config):
        """Get proxy for a specific account"""
        # Check if account has specific proxy
        if 'proxy' in account_config:
            return account_config['proxy']
        
        # Use proxy manager if available
        if self.proxy_manager:
            proxy_config = self.config.get('proxies', {})
            if proxy_config.get('rotate', True):
                return self.proxy_manager.get_next_proxy()
            else:
                return self.proxy_manager.get_random_proxy()
        
        return None
    
    def run_bot(self, account_config, proxy=None):
        """Run a single bot instance"""
        username = account_config.get('username')
        password = account_config.get('password')
        
        if not username or not password:
            logger.error(f"Missing credentials for account: {account_config}")
            return False
        
        try:
            logger.info(f"Starting bot for account: {username}")
            
            # Use account-specific config if provided
            config_path = account_config.get('config_path', 'config/bot_config.yaml')
            
            # Create bot instance
            bot = InstagramBotWithProxy(
                username=username,
                password=password,
                config_path=config_path,
                proxy=proxy
            )
            
            # Run bot
            bot.run()
            
            logger.info(f"Bot completed successfully for account: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Error running bot for {username}: {str(e)}")
            return False
    
    def run_sequential(self):
        """Run bots sequentially"""
        accounts = self.config.get('accounts', [])
        delay = self.config['general'].get('delay_between_starts', 60)
        
        for i, account in enumerate(accounts):
            if i > 0:
                logger.info(f"Waiting {delay} seconds before starting next bot...")
                time.sleep(delay)
            
            proxy = self.get_proxy_for_account(account)
            self.run_bot(account, proxy)
    
    def run_concurrent(self):
        """Run bots concurrently with threading"""
        accounts = self.config.get('accounts', [])
        max_concurrent = self.config['general'].get('max_concurrent_bots', 3)
        delay = self.config['general'].get('delay_between_starts', 60)
        
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            
            for i, account in enumerate(accounts):
                if i > 0 and i % max_concurrent == 0:
                    # Wait for batch to complete before starting new batch
                    logger.info("Waiting for current batch to complete...")
                    for future in as_completed(futures):
                        result = future.result()
                    futures.clear()
                
                if i > 0:
                    time.sleep(delay)
                
                proxy = self.get_proxy_for_account(account)
                future = executor.submit(self.run_bot, account, proxy)
                futures.append(future)
            
            # Wait for remaining bots
            for future in as_completed(futures):
                result = future.result()
    
    def run(self):
        """Main execution method"""
        accounts = self.config.get('accounts', [])
        
        if not accounts:
            logger.error("No accounts configured!")
            return
        
        logger.info(f"Starting multi-bot manager with {len(accounts)} accounts")
        
        use_threading = self.config['general'].get('use_threading', True)
        
        if use_threading:
            logger.info("Running bots concurrently...")
            self.run_concurrent()
        else:
            logger.info("Running bots sequentially...")
            self.run_sequential()
        
        logger.info("All bots completed!")


class BotScheduler:
    """Schedule multiple bots with different timings"""
    
    def __init__(self, config_path='config/multi_bot_config.yaml'):
        self.manager = MultiBotManager(config_path)
        self.config = self.manager.config
    
    def schedule_account(self, account_config):
        """Schedule a single account"""
        import schedule
        
        username = account_config.get('username')
        schedule_config = account_config.get('schedule', {})
        
        if not schedule_config.get('enabled', False):
            return
        
        times = schedule_config.get('times', ['09:00', '15:00', '20:00'])
        
        for time_str in times:
            schedule.every().day.at(time_str).do(
                lambda acc=account_config: self.run_single_account(acc)
            )
        
        logger.info(f"Scheduled {username} at times: {times}")
    
    def run_single_account(self, account_config):
        """Run a single account"""
        proxy = self.manager.get_proxy_for_account(account_config)
        self.manager.run_bot(account_config, proxy)
    
    def start_scheduler(self):
        """Start the scheduler for all accounts"""
        accounts = self.config.get('accounts', [])
        
        for account in accounts:
            self.schedule_account(account)
        
        logger.info("Scheduler started. Waiting for scheduled times...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Bot Manager for Instagram')
    parser.add_argument(
        '--config',
        default='config/multi_bot_config.yaml',
        help='Path to multi-bot configuration file'
    )
    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Run in schedule mode'
    )
    
    args = parser.parse_args()
    
    if args.schedule:
        scheduler = BotScheduler(args.config)
        scheduler.start_scheduler()
    else:
        manager = MultiBotManager(args.config)
        manager.run()


if __name__ == "__main__":
    main()