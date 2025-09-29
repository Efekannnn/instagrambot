# Instagram Bot with InstaPy and Docker

A fully containerized Instagram automation bot built with InstaPy and Docker. This bot can automatically like posts, follow users, and interact with content based on configurable rules.

## ⚠️ Important Disclaimer

**USE AT YOUR OWN RISK!** Instagram actively combats bot usage and may:
- Temporarily or permanently ban your account
- Shadowban your account (limiting reach)
- Request verification challenges

This tool is for educational purposes. Always comply with Instagram's Terms of Service.

## 🚀 Features

- **Dockerized**: Runs in an isolated container with all dependencies
- **Configurable**: YAML-based configuration for all bot behaviors
- **Safe Defaults**: Conservative limits to reduce detection risk
- **Scheduled Runs**: Optional scheduling for human-like behavior
- **Multiple Actions**:
  - Like posts by hashtags
  - Follow users intelligently
  - Comment on posts (disabled by default)
  - Unfollow after X days
- **Smart Limits**: Daily quotas and hourly distribution
- **Logging**: Comprehensive logs for monitoring

## 📋 Prerequisites

- Docker and Docker Compose installed
- Instagram account credentials
- Basic understanding of Instagram automation risks

## 🛠️ Installation

1. Clone or download this project:
```bash
cd /workspace/instagram-bot
```

2. Copy the environment file and add your credentials:
```bash
cp .env.example .env
```

3. Edit `.env` and add your Instagram credentials:
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

4. Build the Docker image:
```bash
./scripts/build.sh
```

## 🎯 Configuration

Edit `config/bot_config.yaml` to customize bot behavior:

### Key Settings:

- **actions**: Enable/disable specific bot actions
- **limits**: Daily limits for likes, follows, comments
- **schedule**: Run bot on a schedule vs one-time
- **safety**: Follower ratio limits and blacklisted words

### Example Configuration:

```yaml
actions:
  like:
    enabled: true
    by_tags:
      tags:
        - "programming"
        - "coding"
      amount: 10  # Posts per tag

limits:
  like_per_day: 100
  follow_per_day: 30
```

## 🚀 Usage

### One-Time Run:
```bash
./scripts/run.sh
```

### View Logs:
```bash
./scripts/logs.sh
```

### Stop Bot:
```bash
./scripts/stop.sh
```

### Scheduled Runs:

To enable scheduled runs, edit `config/bot_config.yaml`:

```yaml
schedule:
  enabled: true
  start_hour: 8   # 8 AM
  end_hour: 20    # 8 PM
  run_duration_minutes: 30
```

## 📁 Project Structure

```
instagram-bot/
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Container orchestration
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
├── src/
│   └── bot.py          # Main bot logic
├── config/
│   └── bot_config.yaml # Bot configuration
├── scripts/
│   ├── build.sh        # Build Docker image
│   ├── run.sh          # Start bot
│   ├── stop.sh         # Stop bot
│   └── logs.sh         # View logs
└── logs/               # Bot logs (created automatically)
```

## 🔒 Safety Recommendations

1. **Start Small**: Use low limits initially
2. **Be Human-Like**: Enable scheduling for natural behavior
3. **Quality Over Quantity**: Target relevant hashtags
4. **Monitor Regularly**: Check logs for issues
5. **Take Breaks**: Don't run 24/7
6. **Use Aged Accounts**: New accounts are more likely to be flagged

## 🐛 Troubleshooting

### Bot won't start:
- Check Docker is running: `docker --version`
- Verify credentials in `.env`
- Check logs: `./scripts/logs.sh`

### Chrome/ChromeDriver issues:
- The Dockerfile automatically installs matching versions
- If issues persist, rebuild: `docker-compose build --no-cache`

### Login failures:
- Verify credentials are correct
- Check if Instagram requires verification
- Try logging in manually first

## 📊 Monitoring

Logs are stored in the `logs/` directory:
- `bot.log`: General bot activity
- InstaPy creates additional detailed logs

Monitor for:
- Login failures
- Rate limit warnings
- Unusual errors

## 🔄 Updates

To update InstaPy or other dependencies:
1. Modify `requirements.txt`
2. Rebuild: `./scripts/build.sh`
3. Restart: `./scripts/run.sh`

## ⚡ Advanced Usage

### Custom Actions

Add custom actions in `src/bot.py`:

```python
# Example: Like posts from specific users
self.session.like_by_users(
    usernames=['user1', 'user2'],
    amount=5,
    randomize=True
)
```

### Multiple Accounts

Create separate directories with different `.env` files for each account.

## 🤝 Contributing

Feel free to improve this bot, but remember to use it responsibly!

## 📜 License

This project is for educational purposes only. Use at your own risk.

---

**Remember**: The best growth on Instagram comes from genuine engagement and quality content. Use automation sparingly and focus on creating value for your audience! 🌟