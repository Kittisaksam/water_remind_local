# Water Drinking Reminder Bot 🚰

A Python-based water drinking reminder system that sends notifications to your Telegram bot 5 times per day. Perfect for maintaining healthy hydration habits!

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)

## ✨ Features

- 🕐 **5 Daily Reminders**: 9 AM, 12 PM, 3 PM, 6 PM, 9 PM
- 💬 **Telegram Notifications**: Get reminders directly on Telegram
- ⚙️ **Easy Configuration**: Simple `.env` file setup
- 🔄 **Auto-retry**: Handles network issues with intelligent retry logic
- 📝 **Comprehensive Logging**: Detailed logs for debugging and monitoring
- 🚀 **Auto-Start**: Runs automatically on macOS startup with launchd
- 🔁 **Self-Healing**: Automatically restarts if it crashes

## 📋 Prerequisites

- Python 3.7 or higher
- macOS (for launchd auto-start feature)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Your Telegram Chat ID

## 🚀 Quick Start

### 1. Clone or Download

```bash
git clone https://github.com/Kittisaksam/water_remind_local.git
cd water_remind_local
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file and add your credentials:

```bash
cp .env.example .env
nano .env  # or your favorite editor
```

Add your Telegram credentials:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 5. Test Run

```bash
python main.py
```

You should receive a test message on Telegram. Press `Ctrl+C` to stop.

### 6. Set Up Auto-Start (macOS)

```bash
# Load the service
launchctl load ~/Library/LaunchAgents/com.waterreminder.daemon.plist

# Start the service
launchctl start com.waterreminder.daemon
```

That's it! The bot will now start automatically when you log in.

## ⏰ Reminder Schedule

| Time   | Message                                    |
|--------|--------------------------------------------|
| 9:00   | Good morning! Time to drink water! 💧      |
| 12:00  | Lunch time reminder! Stay hydrated! 🌊     |
| 15:00  | Afternoon hydration break! 💦              |
| 18:00  | Evening water reminder! 🚰                |
| 21:00  | Last call for water today! Good night! 🌙  |

## 📖 Usage

### Manual Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run the bot
python main.py
```

The bot will:
1. Load configuration from `.env`
2. Test Telegram connection
3. Schedule 5 daily reminders
4. Run until you stop it with `Ctrl+C`

### Auto-Start Mode (macOS)

The service is managed by launchd:

```bash
# Check if service is running
launchctl list | grep waterreminder

# View logs in real-time
tail -f logs/daemon.log

# Stop service temporarily
launchctl stop com.waterreminder.daemon

# Start service
launchctl start com.waterreminder.daemon

# Disable auto-start permanently
launchctl unload ~/Library/LaunchAgents/com.waterreminder.daemon.plist
```

## 📁 Project Structure

```
water_remind_local/
├── .env                      # Telegram credentials (NOT in git) ⚠️
├── .env.example              # Template for credentials
├── .gitignore                # Exclude sensitive files
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── USAGE_GUIDE.md            # Detailed usage guide (Thai language)
├── config.py                 # Configuration management
├── telegram_notifier.py      # Telegram API integration
├── scheduler.py              # Scheduling logic
├── main.py                   # Application entry point
├── logs/                     # Log files directory
│   ├── app.log              # Application logs (manual mode)
│   ├── daemon.log           # Service logs (auto-start mode)
│   └── daemon.error.log     # Error logs
└── venv/                     # Virtual environment (NOT in git)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather | `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | `123456789` |

### Getting Your Telegram Credentials

**1. Create a Bot:**
- Open Telegram and search for [@BotFather](https://t.me/BotFather)
- Send `/newbot`
- Follow the instructions to name your bot
- Copy the bot token

**2. Get Your Chat ID:**
- Start a conversation with your bot
- Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
- Find your `chat.id` in the response

## 📊 Monitoring & Logs

### View Logs

```bash
# Manual mode logs
tail -f logs/app.log

# Auto-start mode logs
tail -f logs/daemon.log

# Error logs
cat logs/daemon.error.log
```

### Log Formats

**Successful Start:**
```
2026-01-18 10:00:06 - INFO - Loading configuration...
2026-01-18 10:00:11 - INFO - ✅ Telegram connection test successful!
2026-01-18 10:00:11 - INFO - 📅 Next reminder at 12:00
2026-01-18 10:00:11 - INFO - 🚀 Water Reminder Bot is now running!
```

**Reminder Sent:**
```
2026-01-18 12:00:01 - INFO - Sending reminder scheduled for 12:00
2026-01-18 12:00:02 - INFO - Message sent successfully: Lunch time reminder! 🌊
```

## 🛠️ Customization

### Change Reminder Times

Edit `scheduler.py`:

```python
REMINDER_MESSAGES = {
    "08:00": "Early morning hydration! 💧",
    "10:00": "Mid-morning water break! 💦",
    "14:00": "Afternoon drink! 🌊",
    "16:00": "Pre-evening hydration! 💧",
    "20:00": "Evening water time! 🚰",
}
```

### Change Reminder Messages

Edit the messages in `REMINDER_MESSAGES` dictionary in `scheduler.py`.

**Thai Example:**
```python
REMINDER_MESSAGES = {
    "09:00": "อรุณสวัสดิ์! ถึงเวลาดื่มน้ำแล้ว 💧",
    "12:00": "เที่ยงแล้ว อย่าลืมดื่มน้ำนะ 🌊",
    # ... etc
}
```

After changes, restart the service:
```bash
launchctl restart com.waterreminder.daemon
```

## 🔍 Troubleshooting

### Bot Not Sending Messages

1. **Check if service is running:**
   ```bash
   launchctl list | grep waterreminder
   ```

2. **Check logs for errors:**
   ```bash
   tail -n 50 logs/daemon.log
   ```

3. **Verify internet connection**

4. **Test credentials:**
   ```bash
   python main.py  # Run manually to see errors
   ```

### Invalid Bot Token

**Error:** `Invalid bot token. Please check TELEGRAM_BOT_TOKEN.`

**Solution:**
1. Verify token with @BotFather
2. Check `.env` file for typos or extra spaces
3. Restart service: `launchctl restart com.waterreminder.daemon`

### Invalid Chat ID

**Error:** `Invalid chat ID or message format. Please check TELEGRAM_CHAT_ID.`

**Solution:**
1. Send a message to your bot first
2. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find your correct chat ID
4. Update `.env` and restart service

### Service Not Starting After Reboot

**Solution:**
```bash
# Reload the service
launchctl unload ~/Library/LaunchAgents/com.waterreminder.daemon.plist
launchctl load ~/Library/LaunchAgents/com.waterreminder.daemon.plist
launchctl start com.waterreminder.daemon
```

## 📚 Documentation

- **README.md** - This file (overview and quick start)
- **USAGE_GUIDE.md** - Comprehensive usage guide in Thai (การใช้งานอย่างละเอียด)

## 🔒 Security

- ⚠️ **NEVER commit** `.env` to version control
- ⚠️ **Keep your bot token private** - it gives full control of your bot
- ✅ Use `.env.example` as a template
- ✅ The `.gitignore` file already excludes `.env` and other sensitive files

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created with ❤️ by [Kittisaksam](https://github.com/Kittisaksam)

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Inspiration
- [schedule](https://github.com/dbader/schedule) - Excellent scheduling library
- [@BotFather](https://t.me/BotFather) - Making Telegram bots easy

---

**Made with 💧 to keep you hydrated!**

Remember: Staying hydrated is one of the best things you can do for your health! 💧🌊💦
