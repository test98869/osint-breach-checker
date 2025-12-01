#!/usr/bin/env python3
"""
Web UI for OSINT Breach Checker
"""

from flask import Flask, render_template, request, jsonify
import hashlib
import requests
from typing import Tuple, Optional
import time

app = Flask(__name__)

class BreachChecker:
    def __init__(self):
        self.pwned_passwords_api = "https://api.pwnedpasswords.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    def check_email_breaches_free(self, email: str) -> Tuple[Optional[bool], str, list]:
        """Check if email appears in breaches using multiple free sources"""
        
        # Method 1: Try IntelX (free tier)
        try:
            url = "https://2.intelx.io/phonebook/search"
            payload = {"term": email, "maxresults": 100, "media": 0, "target": 1}
            headers = {**self.headers, "Content-Type": "application/json"}
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('selectors'):
                    count = len(data['selectors'])
                    return True, f"Found in {count} breach record(s)", []
                else:
                    return False, "No breaches found", []
            
        except Exception:
            pass
        
        # Method 2: Try LeakCheck (free search)
        try:
            url = f"https://leakcheck.io/api/public?check={email}"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('found') and data.get('found') > 0:
                    sources = data.get('sources', [])
                    breach_info = f"Found in {data['found']} breach(es)"
                    return True, breach_info, sources[:10]
                else:
                    return False, "No breaches found", []
                    
        except Exception:
            pass
        
        return None, "Unable to check automatically", []
    
    def check_password_pwned(self, password: str) -> Optional[int]:
        """Check if password appears in Pwned Passwords using k-anonymity"""
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        url = f"{self.pwned_passwords_api}/range/{prefix}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                hashes = response.text.splitlines()
                for line in hashes:
                    hash_suffix, count = line.split(':')
                    if hash_suffix == suffix:
                        return int(count)
                return 0
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None

checker = BreachChecker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or '@' not in email:
        return jsonify({'error': 'Invalid email address'}), 400
    
    if not password:
        return jsonify({'error': 'Password cannot be empty'}), 400
    
    # Check email breaches
    breach_found, breach_message, breach_sources = checker.check_email_breaches_free(email)
    
    time.sleep(0.5)  # Rate limiting
    
    # Check password
    password_count = checker.check_password_pwned(password)
    
    # Determine risk level
    if breach_found and password_count and password_count > 0:
        risk_level = "high"
        risk_message = "Email breached AND password is compromised"
        recommendation = "Change password immediately!"
    elif breach_found and (password_count == 0 or password_count is None):
        risk_level = "medium"
        risk_message = "Email breached but password appears safe"
        recommendation = "Change password if you still use it for this account"
    elif password_count and password_count > 0:
        risk_level = "medium"
        risk_message = "Password is compromised"
        recommendation = "Change this password everywhere you use it"
    else:
        risk_level = "low"
        risk_message = "No exposure detected"
        recommendation = "Continue using strong, unique passwords"
    
    return jsonify({
        'email': {
            'found': breach_found,
            'message': breach_message,
            'sources': breach_sources
        },
        'password': {
            'count': password_count,
            'found': password_count > 0 if password_count is not None else None
        },
        'risk': {
            'level': risk_level,
            'message': risk_message,
            'recommendation': recommendation
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
