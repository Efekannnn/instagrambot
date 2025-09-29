#!/usr/bin/env python3
"""
Advanced Instagram Bot Example
Shows additional features and custom behaviors
"""

import os
from dotenv import load_dotenv
from instapy import InstaPy
from instapy.util import smart_run

load_dotenv()


def advanced_bot_example():
    """Example of advanced bot features"""
    
    # Create session
    session = InstaPy(
        username=os.getenv('INSTAGRAM_USERNAME'),
        password=os.getenv('INSTAGRAM_PASSWORD'),
        headless_browser=True
    )
    
    with smart_run(session):
        # Advanced relationship bounds
        session.set_relationship_bounds(
            enabled=True,
            potency_ratio=0.8,  # 80% of interactions with accounts having good ratio
            delimit_by_numbers=True,
            max_followers=10000,
            max_following=5000,
            min_followers=100,
            min_following=50,
            min_posts=5
        )
        
        # Skip specific types of accounts
        session.set_skip_users(
            skip_private=True,
            private_percentage=100,
            skip_no_profile_pic=True,
            no_profile_pic_percentage=100,
            skip_business=False,
            skip_non_business=False,
            business_percentage=50
        )
        
        # Advanced commenting with spintax
        session.set_comments([
            'This is {amazing|incredible|fantastic}! {😍|💯|🔥}',
            '{Love|Really like} your {content|post|work}!',
            'Keep {it up|going|creating}! {👏|💪|✨}'
        ])
        
        # Like posts from followers of specific accounts
        session.like_by_users(
            usernames=['target_account1', 'target_account2'],
            amount=10,
            randomize=True,
            interact=True,
            media='Photo'
        )
        
        # Follow users who liked posts of competitors
        session.follow_likers(
            usernames=['competitor1', 'competitor2'],
            photos_grab_amount=3,
            follow_likers_per_photo=2,
            randomize=True,
            sleep_delay=600,
            interact=True
        )
        
        # Unfollow users who don't follow back
        session.unfollow_users(
            amount=10,
            nonFollowers=True,  # Only unfollow non-followers
            style="FIFO",  # First In First Out
            unfollow_after=72 * 60 * 60,  # 3 days in seconds
            onlyInstapyFollowed=True  # Only users followed by bot
        )
        
        # Story interaction
        session.story_by_tags(
            tags=['coding', 'programming'],
            amount=5
        )
        
        # Smart hashtag targeting
        smart_hashtags = [
            'python', 'javascript', 'webdev',
            'coding', 'programming', 'developer'
        ]
        
        session.like_by_tags(
            tags=smart_hashtags,
            amount=50,
            skip_top_posts=True,
            interact=True,
            randomize=True,
            media='Photo'
        )
        
        # Join engagement pods (follow users who engaged with your posts)
        session.join_pods(
            topic='technology',
            engagement_mode='no_comments',
            share_amount=3,
            share_media_type=['Photo'],
            like_engage_amount=5
        )


def scheduled_campaigns():
    """Example of different campaigns for different times"""
    
    from datetime import datetime
    
    current_hour = datetime.now().hour
    
    session = InstaPy(
        username=os.getenv('INSTAGRAM_USERNAME'),
        password=os.getenv('INSTAGRAM_PASSWORD'),
        headless_browser=True
    )
    
    with smart_run(session):
        # Morning campaign (6-12)
        if 6 <= current_hour < 12:
            # Target morning/productivity hashtags
            session.like_by_tags(
                tags=['morningmotivation', 'productivity', 'earlybird'],
                amount=20
            )
        
        # Afternoon campaign (12-18)
        elif 12 <= current_hour < 18:
            # Target professional hashtags
            session.like_by_tags(
                tags=['professional', 'business', 'entrepreneur'],
                amount=20
            )
        
        # Evening campaign (18-22)
        elif 18 <= current_hour < 22:
            # Target leisure/hobby hashtags
            session.like_by_tags(
                tags=['hobby', 'lifestyle', 'evening'],
                amount=20
            )


def location_based_targeting():
    """Target users by location"""
    
    session = InstaPy(
        username=os.getenv('INSTAGRAM_USERNAME'),
        password=os.getenv('INSTAGRAM_PASSWORD'),
        headless_browser=True
    )
    
    with smart_run(session):
        # Target by location IDs (need to find these manually)
        locations = [
            '213385402',  # San Francisco
            '212999109',  # New York
            '213326726'   # Los Angeles
        ]
        
        session.like_by_locations(
            locations=locations,
            amount=30,
            skip_top_posts=True
        )


def competitor_analysis():
    """Analyze and target competitor audiences"""
    
    session = InstaPy(
        username=os.getenv('INSTAGRAM_USERNAME'),
        password=os.getenv('INSTAGRAM_PASSWORD'),
        headless_browser=True
    )
    
    with smart_run(session):
        # Get followers of competitors
        competitors = ['competitor1', 'competitor2', 'competitor3']
        
        for competitor in competitors:
            # Follow users who recently liked competitor's posts
            session.follow_likers(
                usernames=[competitor],
                photos_grab_amount=5,
                follow_likers_per_photo=3,
                randomize=True,
                sleep_delay=600,
                interact=True
            )
            
            # Like posts of competitor's active followers
            session.follow_user_followers(
                usernames=[competitor],
                amount=10,
                randomize=True,
                interact=True,
                sleep_delay=60
            )


if __name__ == "__main__":
    # Run the example you want
    advanced_bot_example()