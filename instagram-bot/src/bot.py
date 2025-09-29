#!/usr/bin/env python3
"""
Instagram Bot using InstaPy
Main bot logic and execution
"""

import os
import sys
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from instapy import InstaPy
from instapy.util import smart_run
import yaml

# Try to import enhanced version with proxy support
try:
    from bot_with_proxy import InstagramBotWithProxy
    PROXY_SUPPORT = True
except ImportError:
    PROXY_SUPPORT = False

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class InstagramBot:
    """Instagram bot with configurable actions"""
    
    def __init__(self, username, password, config_path='config/bot_config.yaml'):
        self.username = username
        self.password = password
        self.config = self.load_config(config_path)
        self.session = None
        
    def load_config(self, config_path):
        """Load bot configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}, using defaults")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default bot configuration"""
        return {
            'general': {
                'headless_browser': True,
                'disable_image_load': True,
                'want_check_browser': True,
                'split_db': True
            },
            'actions': {
                'follow': {
                    'enabled': True,
                    'user_interact': {
                        'amount': 3,
                        'randomize': True,
                        'percentage': 80,
                        'media': 'Photo'
                    }
                },
                'like': {
                    'enabled': True,
                    'by_tags': {
                        'tags': ['programming', 'coding', 'developer'],
                        'amount': 10,
                        'skip_top_posts': True,
                        'interact': True
                    }
                },
                'comment': {
                    'enabled': False,
                    'percentage': 10,
                    'comments': [
                        'Nice post! 👍',
                        'Great content!',
                        'Love this!'
                    ]
                }
            },
            'limits': {
                'like_per_day': 100,
                'follow_per_day': 30,
                'unfollow_per_day': 30,
                'comment_per_day': 10
            },
            'schedule': {
                'enabled': True,
                'start_hour': 8,
                'end_hour': 20,
                'run_duration_minutes': 30
            }
        }
    
    def create_session(self):
        """Create and configure InstaPy session"""
        logger.info("Creating InstaPy session...")
        
        general_config = self.config.get('general', {})
        
        self.session = InstaPy(
            username=self.username,
            password=self.password,
            headless_browser=general_config.get('headless_browser', True),
            disable_image_load=general_config.get('disable_image_load', True),
            want_check_browser=general_config.get('want_check_browser', True),
            split_db=general_config.get('split_db', True),
            log_location='/app/logs/'
        )
        
        # Set up limits
        limits = self.config.get('limits', {})
        self.session.set_quota_supervisor(
            enabled=True,
            sleep_after=['likes', 'follows', 'unfollows', 'comments'],
            sleepyhead=True,
            stochastic_flow=True,
            notify_me=True,
            peak_likes_hourly=limits.get('like_per_day', 100) // 12,
            peak_likes_daily=limits.get('like_per_day', 100),
            peak_follows_hourly=limits.get('follow_per_day', 30) // 12,
            peak_follows_daily=limits.get('follow_per_day', 30),
            peak_unfollows_hourly=limits.get('unfollow_per_day', 30) // 12,
            peak_unfollows_daily=limits.get('unfollow_per_day', 30),
            peak_comments_hourly=limits.get('comment_per_day', 10) // 12,
            peak_comments_daily=limits.get('comment_per_day', 10),
        )
        
        # Set mandatory language
        self.session.set_mandatory_language(enabled=True, character_set=['LATIN'])
        
        # Set relationship bounds
        self.session.set_relationship_bounds(
            enabled=True,
            potency_ratio=None,
            delimit_by_numbers=True,
            max_followers=7500,
            max_following=4500,
            min_followers=50,
            min_following=50
        )
        
        logger.info("Session created successfully")
        return self.session
    
    def run_actions(self):
        """Execute bot actions based on configuration"""
        actions = self.config.get('actions', {})
        
        # Like by tags
        if actions.get('like', {}).get('enabled', False):
            like_config = actions['like'].get('by_tags', {})
            tags = like_config.get('tags', [])
            amount = like_config.get('amount', 10)
            
            if tags:
                logger.info(f"Liking posts by tags: {tags}")
                self.session.like_by_tags(
                    tags=tags,
                    amount=amount,
                    skip_top_posts=like_config.get('skip_top_posts', True),
                    interact=like_config.get('interact', True)
                )
        
        # Follow user followers
        if actions.get('follow', {}).get('enabled', False):
            follow_config = actions['follow'].get('user_interact', {})
            
            logger.info("Setting up user interaction")
            self.session.set_user_interact(
                amount=follow_config.get('amount', 3),
                randomize=follow_config.get('randomize', True),
                percentage=follow_config.get('percentage', 80),
                media=follow_config.get('media', 'Photo')
            )
        
        # Comments
        if actions.get('comment', {}).get('enabled', False):
            comment_config = actions['comment']
            comments = comment_config.get('comments', [])
            
            if comments:
                logger.info("Setting up comments")
                self.session.set_comments(
                    comments,
                    media='Photo'
                )
                self.session.set_do_comment(
                    enabled=True,
                    percentage=comment_config.get('percentage', 10)
                )
    
    def run(self):
        """Main bot execution"""
        try:
            self.create_session()
            
            with smart_run(self.session):
                logger.info("Bot started successfully")
                self.run_actions()
                logger.info("Bot actions completed")
                
        except Exception as e:
            logger.error(f"Error during bot execution: {str(e)}")
            raise
        finally:
            if self.session:
                self.session.end()
                logger.info("Session ended")


def main():
    """Main entry point"""
    # Get credentials from environment
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    if not username or not password:
        logger.error("Instagram credentials not found in environment variables")
        sys.exit(1)
    
    # Check schedule configuration
    config_path = 'config/bot_config.yaml'
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            schedule_config = config.get('schedule', {})
    except:
        schedule_config = {'enabled': False}
    
    if schedule_config.get('enabled', False):
        import schedule
        
        logger.info("Schedule mode enabled")
        
        def job():
            logger.info("Starting scheduled bot run")
            bot = InstagramBot(username, password)
            bot.run()
            logger.info("Scheduled bot run completed")
        
        # Schedule the job
        start_hour = schedule_config.get('start_hour', 8)
        end_hour = schedule_config.get('end_hour', 20)
        run_duration = schedule_config.get('run_duration_minutes', 30)
        
        # Run every hour between start and end times
        for hour in range(start_hour, end_hour):
            schedule.every().day.at(f"{hour:02d}:00").do(job)
        
        logger.info(f"Bot scheduled to run hourly between {start_hour}:00 and {end_hour}:00")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    else:
        # Run once
        logger.info("Running bot once")
        
        # Check if proxy is configured
        if PROXY_SUPPORT and (os.getenv('PROXY_HOST') or 'proxy' in config):
            logger.info("Using proxy-enabled bot")
            bot = InstagramBotWithProxy(username, password)
        else:
            bot = InstagramBot(username, password)
        
        bot.run()


if __name__ == "__main__":
    main()