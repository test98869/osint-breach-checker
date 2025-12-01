# 🔍 OSINT Breach Checker

A modern, ethical security research tool that checks if an email has been compromised in data breaches and whether associated passwords have been exposed. Features both a CLI and a sleek dark-themed web interface.

![Dark Theme UI](https://img.shields.io/badge/UI-Dark%20Theme-8b5cf6)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Email Breach Check** - Search across multiple breach databases (IntelX, LeakCheck)
- **Password Exposure Check** - Uses HIBP Pwned Passwords API with k-anonymity
- **Risk Assessment** - Color-coded risk levels with actionable recommendations
- **Web Interface** - Beautiful dark-themed UI built with Flask
- **CLI Tool** - Command-line interface for quick checks
- **Privacy-Focused** - Passwords hashed locally, never sent in full
- **No Data Storage** - Nothing is logged or stored
- **Free to Use** - No API keys required

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/osint-breach-checker.git
cd osint-breach-checker

# Install dependencies
pip install -r requirements.txt
```

### Web Interface

```bash
# Easy way
./run.sh

# Or manually
python app.py
```

Then open http://localhost:5000 in your browser.

### CLI Tool

```bash
python breach_checker.py
```

The tool will prompt you for:
1. **Email address** to check
2. **Password** to verify (entered securely, not displayed)

## How It Works

### Email Breach Check
- Queries Have I Been Pwned API v3
- Returns list of breaches where email appears
- Shows breach dates and compromised data types

### Password Check (k-Anonymity)
- Hashes password locally using SHA-1
- Sends only first 5 characters of hash to API
- Receives ~500 hash suffixes back
- Matches locally without exposing full password
- Returns how many times password appears in breaches

### Risk Assessment
- **HIGH RISK**: Email breached AND password compromised → Change immediately
- **MEDIUM RISK**: Either email or password compromised → Change recommended
- **LOW RISK**: No exposure detected → Continue good practices

## API Rate Limits

- **Email breach check**: Uses HIBP web interface (free, reasonable limits)
- **Pwned Passwords**: No authentication required, generous rate limits
- Be respectful with usage - add delays between multiple checks

## Security & Privacy

- Passwords never leave your machine in plaintext
- Uses k-anonymity model (industry standard)
- No data is stored or logged
- Open source - audit the code yourself

## Legal & Ethical Use

This tool is for:
- Checking your own accounts
- Security research with permission
- Helping others assess their security posture

NOT for:
- Unauthorized access attempts
- Credential stuffing
- Any malicious activity

## Example Output

```
🔍 BREACH ANALYSIS REPORT
======================================================================

📧 Email: example@email.com

⚠️  This email appears in 3 breach(es):

  • LinkedIn
    Date: 2012-05-05
    Compromised data: Email addresses, Passwords

----------------------------------------------------------------------
✅ Password has NOT been found in known breaches

----------------------------------------------------------------------
📊 RISK ASSESSMENT:
  🟡 MEDIUM RISK - Email breached but password appears safe
  💡 RECOMMENDATION: Change password if you still use it for this account
======================================================================
```

## 📸 Screenshots

### Web Interface
- Dark-themed modern UI
- Real-time breach checking
- Color-coded risk assessment
- Mobile responsive design

### CLI Interface
- Simple command-line tool
- Formatted text output
- Quick security checks

## 🛠️ Tech Stack

- **Backend**: Python 3.7+, Flask
- **Frontend**: Vanilla JavaScript, CSS3
- **APIs**: HIBP Pwned Passwords, IntelX, LeakCheck
- **Security**: SHA-1 hashing, k-anonymity model

## 🔒 Privacy & Security

- **Local Hashing**: Passwords are hashed using SHA-1 on your machine
- **k-Anonymity**: Only first 5 characters of hash sent to API
- **No Storage**: Zero data logging or storage
- **Open Source**: Audit the code yourself

## ⚖️ Legal & Ethical Use

This tool is designed for:
- Checking your own accounts
- Security research with permission
- ✅ Helping others assess their security posture

NOT for:
- Unauthorized access attempts
- Credential stuffing
- Any malicious activity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Have I Been Pwned](https://haveibeenpwned.com/) - Troy Hunt's breach database
- [IntelX](https://intelx.io/) - Intelligence data platform
- [LeakCheck](https://leakcheck.io/) - Breach search engine

## ⚠️ Disclaimer

This tool is for educational and security research purposes only. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for misuse of this tool.

## 📞 Support

If you find this tool useful, please ⭐ star the repository!
