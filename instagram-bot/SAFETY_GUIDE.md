# Instagram Bot Safety Guide

## 🚨 Critical Safety Information

Using automation on Instagram carries significant risks. This guide helps minimize those risks, but **cannot guarantee your account's safety**.

## 📊 Risk Levels

### ✅ Low Risk Activities
- Liking 50-100 posts/day
- Following 10-20 users/day
- Viewing stories
- Using aged accounts (6+ months)
- Running during normal hours (8am-10pm)

### ⚠️ Medium Risk Activities
- Liking 100-200 posts/day
- Following 20-50 users/day
- Commenting with templates
- Unfollowing users
- Using accounts 3-6 months old

### 🚫 High Risk Activities
- Liking 200+ posts/day
- Following 50+ users/day
- Mass unfollowing
- Spammy comments
- Running 24/7
- Using new accounts (<3 months)
- Using the same actions repeatedly

## 🛡️ Best Practices

### 1. **Account Preparation**
- Use aged accounts when possible
- Complete your profile fully
- Post organic content regularly
- Build some followers manually first
- Enable 2FA for security

### 2. **Natural Behavior Patterns**
```yaml
# Good schedule example
schedule:
  enabled: true
  start_hour: 9    # Start after breakfast
  end_hour: 22     # Stop before bed
  run_duration_minutes: 20-40  # Short bursts
```

### 3. **Action Delays**
- Add random delays between actions
- Never perform actions too quickly
- Take breaks between campaigns

### 4. **Content Quality**
```yaml
# Target quality over quantity
actions:
  like:
    by_tags:
      tags:
        - "yournichetag"    # Specific to your niche
        - "relatedtag"      # Related content
      amount: 5-10          # Small amounts per tag
```

### 5. **Gradual Increase**
Week 1: 50 likes/day, 10 follows/day
Week 2: 75 likes/day, 15 follows/day
Week 3: 100 likes/day, 20 follows/day
Week 4+: Maintain or slowly increase

## 🔍 Detection Indicators

### Instagram May Flag You If:
1. Actions are too fast/consistent
2. You like/follow random unrelated content
3. Your follow/unfollow ratio is suspicious
4. You use the same comment repeatedly
5. You're active 24/7 without breaks
6. Geographic impossibilities (actions from different locations)

### Warning Signs:
- "Action Blocked" messages
- Forced logouts
- Verification requests
- Reduced reach/engagement
- Followers can't find your account

## 🚑 Recovery Steps

### If You Get Action Blocked:
1. **Stop all automation immediately**
2. Wait 24-48 hours minimum
3. Use Instagram manually and lightly
4. Don't log in from multiple devices
5. Consider these limits were too high

### If Account Is Compromised:
1. Change password immediately
2. Revoke all third-party access
3. Enable 2FA if not already
4. Report to Instagram if needed
5. Wait 2-4 weeks before any automation

## 📈 Safe Growth Strategies

### 1. **Content First**
- Post quality content regularly
- Use relevant hashtags organically
- Engage genuinely with your niche

### 2. **Smart Targeting**
```python
# Target engaged users in your niche
session.set_relationship_bounds(
    enabled=True,
    max_followers=5000,      # Not targeting huge accounts
    min_followers=100,       # Not targeting bots
    min_following=50,        # Active users
    min_posts=10            # Real accounts
)
```

### 3. **Meaningful Interactions**
- Like full posts, not just thumbnails
- Watch story completely
- Vary your interaction patterns
- Comment genuinely when possible

## 🎯 Recommended Safe Limits

### Conservative (Safest):
```yaml
limits:
  like_per_day: 50
  follow_per_day: 10
  unfollow_per_day: 10
  comment_per_day: 5
```

### Moderate:
```yaml
limits:
  like_per_day: 100
  follow_per_day: 20
  unfollow_per_day: 20
  comment_per_day: 10
```

### Aggressive (Higher Risk):
```yaml
limits:
  like_per_day: 200
  follow_per_day: 40
  unfollow_per_day: 40
  comment_per_day: 20
```

## 🔒 Technical Safety

### 1. **IP Address**
- Use residential IPs when possible
- Avoid datacenter IPs
- Don't switch IPs frequently
- Consider using your home network

### 2. **Browser Fingerprinting**
- The bot uses headless Chrome
- Randomize viewport sizes
- Clear cookies periodically

### 3. **API Limits**
- Instagram has hidden rate limits
- They change without notice
- What worked yesterday might not work today

## 📝 Monitoring Checklist

Daily:
- [ ] Check for any warnings/blocks
- [ ] Monitor follower growth rate
- [ ] Review engagement quality
- [ ] Verify actions are completing

Weekly:
- [ ] Analyze account insights
- [ ] Adjust limits based on performance
- [ ] Review and update target hashtags
- [ ] Check competitor strategies

## 🎓 Final Recommendations

1. **Start Extremely Conservative**: You can always increase later
2. **Quality > Quantity**: Better to engage with 10 relevant users than 100 random ones
3. **Be Patient**: Organic growth takes time
4. **Have Backup Plans**: Don't rely on one account
5. **Stay Informed**: Instagram changes policies frequently

## ⚖️ Legal Considerations

- Automation violates Instagram's Terms of Service
- Your account can be terminated without warning
- Instagram owes you no explanation or recourse
- Business accounts may face additional scrutiny
- Consider the impact on your brand/reputation

## 🆘 Emergency Contacts

If your account is compromised:
1. Instagram Help Center
2. Change all passwords
3. Document everything
4. Consider professional social media management

---

**Remember**: No automation is 100% safe. The safest approach is manual, genuine engagement. Use this tool understanding and accepting all risks involved.

**Pro Tip**: The most successful Instagram accounts combine minimal automation with excellent content and genuine community building. Use automation to supplement, not replace, real engagement.