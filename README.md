# Fully Automated Instagram Bot

This repository contains a Python-based Instagram bot designed to automate various activities on Instagram such as logging in, posting content, sending direct messages, and interacting with posts based on hashtags.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview
The fully automated Instagram bot uses Selenium WebDriver to interact with the Instagram web interface. It can automate activities such as logging in, liking posts, following users, sending direct messages, and posting images with captions.

## Features
- **Login**: Logs into an Instagram account using credentials provided in a text file.
- **Post Content**: Posts images with captions specified in a text file.
- **Direct Messaging**: Sends direct messages to users listed in a text file.
- **Like and Follow**: Likes posts and follows users based on specified hashtags.

## Installation
To run this project locally, you need to have Python and Selenium WebDriver installed on your machine. Follow these steps to set up the project:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/fully-automated-insta-bot.git
   ```
2. Navigate to the project directory:
   ```bash
   cd fully-automated-insta-bot
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the ChromeDriver that matches your Chrome browser version from [here](https://sites.google.com/a/chromium.org/chromedriver/) and place it in the project directory.

## Usage
1. Update the `Login.txt` file with your Instagram username and password in the following format:
   ```
   your_username
   your_password
   ```

2. Populate the other text files (`hashtags.txt`, `post.txt`, `directmessage.txt`, `data.txt`) with the relevant data required for the bot to operate.

3. Run the main script:
   ```bash
   python main.py
   ```

## Files
- `Login.txt`: Contains Instagram login credentials.
- `data.txt`: Contains data used by the bot (e.g., target users for direct messages).
- `directmessage.txt`: Contains messages to be sent via direct messaging.
- `hashtags.txt`: Contains hashtags to be used for finding posts to like and users to follow.
- `post.txt`: Contains image paths and captions for posting.
- `main.py`: Main script to run the bot.
- `chromedriver.exe`: ChromeDriver executable used by Selenium WebDriver.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
