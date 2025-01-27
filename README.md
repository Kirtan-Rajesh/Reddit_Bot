# README.md

# Reddit Bot Appium

This project is an automated bot for Reddit that utilizes Appium to post, comment, and send direct messages. The bot is designed to interact with the Reddit website through a mobile interface.

## Features

- Post new content to Reddit
- Comment on existing posts
- Send direct messages to users
- Automated user authentication

## Requirements

- Python 3.x
- Appium-Python-Client
- pytest or unittest
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/reddit-bot-appium.git
   cd reddit-bot-appium
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Set up Appium server and ensure it is running.

## Usage

1. Configure your Reddit account credentials in the `bot.py` file.
2. Run the bot:
   ```
   python src/bot.py
   ```

## Testing

To run the unit tests, use:
```
pytest src/tests/test_bot.py
```

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.