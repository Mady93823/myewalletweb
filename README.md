# MyEWallet Bot

A Python Telegram bot for myewallet.global with user management, broadcasting, and website integration.

## Features

- **Welcome System**: Beautiful welcome message with image and "Open Wallet" button.
- **User Management**: MongoDB storage for user data (ID, name, activity).
- **Admin Tools**: Broadcast scheduling (/broadcast) and stats.
- **Docker Ready**: Easy deployment.

## Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- Telegram Bot Token

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mady93823/myewalletweb.git
   cd myewalletweb
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Copy `.env` (or create one) and fill in the values:
     ```env
     TELEGRAM_BOT_TOKEN=your_token
     MONGODB_URI=mongodb://localhost:27017/myewallet
     ADMIN_IDS=12345678,87654321
     ```

4. **Run the Bot**
   ```bash
   python run.py
   ```

## Docker Deployment

1. **Build the image**
   ```bash
   docker build -t myewallet-bot .
   ```

2. **Run the container**
   ```bash
   docker run -d --env-file .env --name myewallet-bot myewallet-bot
   ```

## Admin Commands

- `/broadcast [time] [message]`
  - `time`: `now`, `10s`, `15m`, `2h`
  - Example: `/broadcast 1h Maintenance in 1 hour!`
- `/help`: Show admin commands and stats.

## Testing

Run unit tests:
```bash
python -m unittest discover tests
```
