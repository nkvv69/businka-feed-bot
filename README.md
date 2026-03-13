# 🐾 Businka Feed Bot

**Businka Feed Bot** — Telegram-бот для напоминания о кормлении питомца 🐱.  
Бот помогает следить за временем кормлений, вести историю веса и управлять настройками питомца прямо из чата.

---

## 🇷🇺 О проекте

### ✨ Возможности
- 🍽️ Напоминания о кормлении  
- ⚖️ Учёт веса питомца  
- ⏰ Настройка времени кормления  
- 🐾 Изменение имени питомца  
- 📜 История веса  

---

### 🧠 Установка на Raspberry Pi

#### 1. Клонируй репозиторий:
```bash
cd /home/pi
git clone https://github.com/Cayman152/businka-feed-bot.git
cd businka-feed-bot
```

#### 2. Установи зависимости:
```bash
sudo apt update
sudo apt install python3-pip -y
pip install -r requirements.txt
```

#### 3. Добавь токен бота:
Открой файл `~/.bashrc` и добавь строку:
```bash
export BOT_TOKEN="ВАШ_ТОКЕН_ОТ_TELEGRAM_BOTFATHER"
```
Затем обнови окружение:
```bash
source ~/.bashrc
```

#### 4. Запусти бота вручную:
```bash
python3 businka_feed_bot_full.py
```

---

### ⚙️ Автозапуск через systemd
Создай сервис:
```bash
sudo nano /etc/systemd/system/businka-bot.service
```

Вставь:
```
[Unit]
Description=Businka Feed Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/businka-feed-bot/businka_feed_bot_full.py
WorkingDirectory=/home/pi/businka-feed-bot
Environment="BOT_TOKEN=ВАШ_ТОКЕН"
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Сохрани и запусти:
```bash
sudo systemctl daemon-reload
sudo systemctl enable businka-bot
sudo systemctl start businka-bot
```

Проверить работу:
```bash
sudo systemctl status businka-bot
```

---

## 🇬🇧 English version

### ✨ Features
- 🍽️ Feeding reminders  
- ⚖️ Pet weight tracking  
- ⏰ Feeding schedule customization  
- 🐾 Rename your pet  
- 📜 Weight history view  

### 🧠 Installation on Raspberry Pi

```bash
cd /home/pi
git clone https://github.com/Cayman152/businka-feed-bot.git
cd businka-feed-bot
sudo apt update
sudo apt install python3-pip -y
pip install -r requirements.txt
```

Set your bot token:
```bash
export BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
source ~/.bashrc
```

Run:
```bash
python3 businka_feed_bot_full.py
```

---

## 📜 License
MIT License © 2025 NKVV69  
See the [LICENSE](LICENSE) file for details.

---

🐾 *Created with ❤️ by NK*
