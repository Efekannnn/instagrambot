# Proxy and Multi-Bot Setup Guide

This guide covers how to use proxies and run multiple Instagram bots simultaneously.

## 📡 Proxy Configuration

### Why Use Proxies?

1. **Avoid IP Bans**: Instagram tracks IP addresses for suspicious activity
2. **Multiple Accounts**: Run multiple accounts from the same server
3. **Geographic Targeting**: Appear to be from specific locations
4. **Anonymity**: Hide your real IP address

### Types of Proxies

1. **Datacenter Proxies**
   - ✅ Cheap and fast
   - ❌ Easier to detect
   - Best for: Testing, low-risk activities

2. **Residential Proxies**
   - ✅ Hard to detect (real ISP IPs)
   - ❌ More expensive
   - Best for: Production use, valuable accounts

3. **Mobile Proxies**
   - ✅ Highest trust level
   - ❌ Most expensive
   - Best for: High-value accounts, aggressive actions

### Setting Up Proxies

#### Method 1: Environment Variables
```bash
# In .env file
PROXY_HOST=proxy.example.com
PROXY_PORT=8080
PROXY_PROTOCOL=http
PROXY_USERNAME=user
PROXY_PASSWORD=pass
```

#### Method 2: Configuration File
```yaml
# In config/bot_config.yaml
proxy:
  enabled: true
  host: "proxy.example.com"
  port: 8080
  protocol: "http"  # or "socks5"
  username: "user"
  password: "pass"
```

#### Method 3: Command Line (Docker)
```bash
docker run -e PROXY_HOST=proxy.example.com \
           -e PROXY_PORT=8080 \
           instagram-bot
```

### Testing Proxies

Test your proxy before using it:
```bash
./scripts/test-proxy.sh
```

Or manually:
```bash
curl -x http://user:pass@proxy.example.com:8080 http://httpbin.org/ip
```

## 🤖 Multi-Bot Setup

### Basic Multi-Bot Configuration

1. **Create Multi-Bot Environment File**:
```bash
cp .env.multi.example .env.multi
```

2. **Edit .env.multi**:
```env
# Bot 1
BOT1_USERNAME=account1
BOT1_PASSWORD=password1
BOT1_PROXY_HOST=proxy1.example.com
BOT1_PROXY_PORT=8080

# Bot 2
BOT2_USERNAME=account2
BOT2_PASSWORD=password2
BOT2_PROXY_HOST=proxy2.example.com
BOT2_PROXY_PORT=8080

# Bot 3
BOT3_USERNAME=account3
BOT3_PASSWORD=password3
BOT3_PROXY_HOST=proxy3.example.com
BOT3_PROXY_PORT=8080
```

3. **Run Multiple Bots**:
```bash
./scripts/run-multi.sh
```

### Advanced Multi-Bot Manager

Use the multi-bot manager for coordinated runs:

1. **Configure accounts** in `config/multi_bot_config.yaml`:
```yaml
accounts:
  - username: "account1"
    password: "password1"
    config_path: "config/conservative_config.yaml"
    proxy:
      host: "proxy1.example.com"
      port: 8080
  
  - username: "account2"
    password: "password2"
    config_path: "config/aggressive_config.yaml"
    proxy:
      host: "proxy2.example.com"
      port: 8080
```

2. **Run the manager**:
```bash
docker run -v ./config:/app/config instagram-bot python src/multi_bot_manager.py
```

### Scheduling Multiple Bots

Enable scheduled runs for each account:
```yaml
accounts:
  - username: "account1"
    password: "password1"
    schedule:
      enabled: true
      times: ["09:00", "15:00", "21:00"]
```

Run scheduler:
```bash
python src/multi_bot_manager.py --schedule
```

## 🔄 Proxy Rotation

### Automatic Rotation

Configure proxy rotation in `config/multi_bot_config.yaml`:
```yaml
proxies:
  enabled: true
  rotate: true  # Automatically rotate proxies
  list:
    - host: "proxy1.example.com"
      port: 8080
    - host: "proxy2.example.com"  
      port: 8080
    - host: "proxy3.example.com"
      port: 8080
```

### Manual Proxy Management

Use the proxy manager directly:
```python
from proxy_manager import AdvancedProxyManager

manager = AdvancedProxyManager()
manager.validate_all_proxies()  # Test all proxies
proxy = manager.get_next_proxy()  # Get next in rotation
```

## 📊 Monitoring Multiple Bots

### View All Logs
```bash
docker-compose -f docker-compose.multi.yml logs -f
```

### View Specific Bot
```bash
docker-compose -f docker-compose.multi.yml logs -f instagram-bot-1
```

### Check Status
```bash
docker-compose -f docker-compose.multi.yml ps
```

### Individual Log Files
Logs are stored separately for each bot:
- Bot 1: `logs/bot1/`
- Bot 2: `logs/bot2/`
- Bot 3: `logs/bot3/`

## ⚡ Performance Optimization

### Resource Allocation
```yaml
# In docker-compose.multi.yml
deploy:
  resources:
    limits:
      memory: 2G  # Limit per bot
      cpus: '0.5'
    reservations:
      memory: 1G  # Minimum guaranteed
```

### Concurrent Limits
```yaml
# In multi_bot_config.yaml
general:
  max_concurrent_bots: 3  # Don't overload system
  delay_between_starts: 60  # Stagger bot starts
```

## 🛡️ Safety Tips for Multiple Bots

1. **Use Different Proxies**: Never run multiple accounts on the same IP
2. **Vary Configurations**: Use different settings for each bot
3. **Stagger Activities**: Don't run all bots at the same time
4. **Monitor Carefully**: Watch for blocks across accounts
5. **Isolate Accounts**: Keep bot accounts separate from personal accounts

## 🚨 Common Issues

### Proxy Connection Failed
- Verify proxy credentials
- Check proxy is not blacklisted
- Test proxy connectivity manually
- Try different proxy protocol (HTTP vs SOCKS5)

### Multiple Bots Interfering
- Increase delay between starts
- Use different action schedules
- Ensure unique proxy per bot
- Check resource limits

### High Resource Usage
- Reduce concurrent bot limit
- Enable headless mode
- Disable image loading
- Increase memory limits

## 📋 Example Scenarios

### Scenario 1: Growth Agency
Run 10 client accounts with residential proxies:
```yaml
general:
  max_concurrent_bots: 5
  delay_between_starts: 120

proxies:
  enabled: true
  rotate: false  # Each account gets dedicated proxy
```

### Scenario 2: Personal Brand Network
Manage 3 related accounts with different strategies:
```yaml
accounts:
  - username: "main_brand"
    config_path: "config/aggressive_config.yaml"
  - username: "brand_community"
    config_path: "config/moderate_config.yaml"
  - username: "brand_support"
    config_path: "config/conservative_config.yaml"
```

### Scenario 3: Geographic Targeting
Target different regions with location-specific proxies:
```yaml
accounts:
  - username: "brand_usa"
    proxy:
      host: "us.proxy.com"
      country: "US"
  - username: "brand_uk"
    proxy:
      host: "uk.proxy.com"
      country: "UK"
```

## 🔧 Advanced Proxy Features

### Proxy Validation
```bash
# Validate all proxies in config
python -c "from proxy_manager import AdvancedProxyManager; m = AdvancedProxyManager(); m.validate_all_proxies()"
```

### Proxy Pool Management
```python
# Automatically assign proxies to accounts
from proxy_manager import ProxyPool

pool = ProxyPool(proxy_list)
proxy1 = pool.assign_proxy("account1")
proxy2 = pool.assign_proxy("account2")
```

## 📚 Recommended Proxy Providers

1. **Budget Options**:
   - Webshare.io (Datacenter)
   - Proxy-Cheap (Mixed)

2. **Premium Options**:
   - Bright Data (Residential)
   - SmartProxy (Residential/Mobile)
   - IPRoyal (Residential)

3. **Mobile Proxies**:
   - Proxy-Store
   - AirProxy

Always test proxies with Instagram before committing to a provider!

---

**Remember**: Using multiple accounts and proxies adds complexity. Start small, test thoroughly, and scale gradually. The goal is sustainable growth, not quick gains that risk your accounts.