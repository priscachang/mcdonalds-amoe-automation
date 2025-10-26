# McDonald's AMOE Email Verification Automation

An automated Python script that handles McDonald's AMOE (Alternate Method of Entry) email verification and form filling. This tool automatically retrieves verification emails, extracts OTP codes, and fills out the required information forms.

## 🚀 Features

- **Automated Email Processing**: Automatically retrieves and processes McDonald's verification emails
- **OTP Code Extraction**: Intelligently extracts 6-digit OTP codes from email content
- **Form Auto-Filling**: Automatically fills out personal information forms
- **Multi-Email Support**: Processes multiple verification emails in sequence
- **Error Handling**: Robust error handling with detailed status messages
- **Browser Automation**: Uses Selenium WebDriver for reliable web interactions

## 📋 Prerequisites

Before using this script, ensure you have:

1. **Python 3.7+** installed on your system
2. **Google Chrome** browser installed
3. **ChromeDriver** (will be handled automatically by Selenium)
4. **Gmail account** with 2-factor authentication enabled
5. **Gmail App Password** (see setup instructions below)

## 🛠️ Installation

1. **Clone or download** this repository to your local machine

2. **Install required Python packages**:

   ```bash
   pip install selenium imaplib email
   ```

   Or if you prefer using a requirements file:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver** (if not already installed):

   ```bash
   # On macOS with Homebrew
   brew install chromedriver

   # On Windows with Chocolatey
   choco install chromedriver

   # Or download manually from: https://chromedriver.chromium.org/
   ```

## 📧 Gmail Setup (Required)

### Step 1: Enable Two-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Find **"2-Step Verification"**
3. Enable it (if not already enabled)

### Step 2: Generate App Password

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Select **"Mail"** and your device
3. Click **"Generate"**
4. You'll receive a 16-character password (e.g., `abcd efgh ijkl mnop`)
5. **Save this password** - you'll need it for the script

> ⚠️ **Important**: Use the app password (not your regular Gmail password) in the script configuration.

## ⚙️ Configuration

Edit the script configuration in the `if __name__ == "__main__":` section:

```python
automation = McDonaldsVerification(
    # Email settings
    email_address="your-email@gmail.com",
    email_password="your-app-password",  # Use the 16-character app password

    # Personal information
    first_name="YourFirstName",
    last_name="YourLastName",
    suffix="",  # Leave empty or fill Jr., Sr., III, etc.

    # Address information
    street_address="Your Street Address",
    apartment="",  # Optional apartment number
    city="Your City",
    state="XX",  # Two-letter state code (e.g., NY, CA, TX)
    zip_code="12345"
)
```

### Configuration Parameters

| Parameter        | Description                   | Example                   |
| ---------------- | ----------------------------- | ------------------------- |
| `email_address`  | Your Gmail address            | `"user@gmail.com"`        |
| `email_password` | Gmail app password (16 chars) | `"abcd efgh ijkl mnop"`   |
| `first_name`     | Your first name               | `"John"`                  |
| `last_name`      | Your last name                | `"Doe"`                   |
| `suffix`         | Name suffix (optional)        | `"Jr."`, `"Sr."`, `"III"` |
| `street_address` | Street address                | `"123 Main St"`           |
| `apartment`      | Apartment number (optional)   | `"Apt 4B"`                |
| `city`           | City name                     | `"New York"`              |
| `state`          | Two-letter state code         | `"NY"`, `"CA"`, `"TX"`    |
| `zip_code`       | ZIP/postal code               | `"10001"`                 |

## 🚀 Usage

1. **Configure your information** in the script (see Configuration section above)

2. **Run the script**:

   ```bash
   python script.py
   ```

3. **The script will**:
   - Open a Chrome browser window
   - Monitor your Gmail for McDonald's verification emails
   - Automatically extract OTP codes and verification links
   - Fill out the verification forms
   - Process multiple emails if available

## 📊 How It Works

### Workflow Overview

1. **Email Monitoring**: Connects to Gmail and searches for unread McDonald's verification emails
2. **Data Extraction**: Extracts verification links and 6-digit OTP codes from email content
3. **Browser Automation**: Opens verification links in Chrome browser
4. **Form Filling**: Automatically fills out personal information forms
5. **Submission**: Submits the completed forms

### Process Steps

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Email Check   │───▶│  Extract OTP &   │───▶│  Browser Auto   │
│                 │    │  Verification    │    │  Form Filling   │
│                 │    │  Links           │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## ⚠️ Important Notes

- **Use responsibly**: This tool is for legitimate McDonald's promotions only
- **Rate limiting**: The script includes appropriate delays to avoid overwhelming servers
- **Email security**: Never share your Gmail app password
- **Terms of service**: Ensure your use complies with McDonald's terms of service

## 📄 License

This project is for educational purposes. Use at your own risk and ensure compliance with all applicable terms of service.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

---

**Happy automating! 🍟**
