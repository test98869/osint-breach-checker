#!/usr/bin/env python3
"""
OSINT Breach Checker Tool
Checks email breaches and password exposure via free APIs
"""

import requests
import hashlib
import getpass
import sys
from typing import Dict, List, Optional, Tuple
import time
import re

class BreachChecker:
    def __init__(self):
        self.pwned_passwords_api = "https://api.pwnedpasswords.com"
        self.dehashed_search = "https://www.dehashed.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    def check_email_breaches_free(self, email: str) -> Tuple[bool, str]:
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
                    return True, f"Found in {count} breach record(s) via IntelX"
                else:
                    return False, "No breaches found"
            
        except Exception as e:
            pass  # Try next method
        
        # Method 2: Try LeakCheck (free search)
        try:
            url = f"https://leakcheck.io/api/public?check={email}"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('found') and data.get('found') > 0:
                    sources = data.get('sources', [])
                    details = []
                    for source in sources[:5]:
                        details.append(f"  • {source}")
                    
                    if len(sources) > 5:
                        details.append(f"  • ... and {len(sources) - 5} more")
                    
                    breach_info = f"Found in {data['found']} breach(es)"
                    if details:
                        breach_info += "\n" + "\n".join(details)
                    
                    return True, breach_info
                else:
                    return False, "No breaches found"
                    
        except Exception as e:
            pass  # Try next method
        
        # Method 3: Suggest manual check
        return None, (
            "Unable to check automatically (HIBP requires paid API key).\n"
            "  Please manually check at: https://haveibeenpwned.com/\n"
            "  Or try: https://leakcheck.io/"
        )
    
    def check_password_pwned(self, password: str) -> Optional[int]:
        """Check if password appears in Pwned Passwords using k-anonymity"""
        # Hash the password
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        url = f"{self.pwned_passwords_api}/range/{prefix}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Parse response to find our hash suffix
                hashes = response.text.splitlines()
                for line in hashes:
                    hash_suffix, count = line.split(':')
                    if hash_suffix == suffix:
                        return int(count)
                return 0  # Not found in breaches
            else:
                print(f"⚠️  Error checking password: HTTP {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
    
    def display_breach_report(self, email: str, breach_found: Optional[bool], 
                            breach_details: str, password_count: Optional[int]):
        """Display formatted breach report"""
        print("\n" + "="*70)
        print(f"🔍 BREACH ANALYSIS REPORT")
        print("="*70)
        print(f"\n📧 Email: {email}")
        
        # Email breach status
        if breach_found is None:
            print(f"\n❌ Could not check email breaches")
            print(f"   {breach_details}")
        elif breach_found:
            print(f"\n⚠️  {breach_details}")
        else:
            print("\n✅ Good news! This email has NOT been found in any known breaches.")
        
        # Password exposure status
        print("\n" + "-"*70)
        if password_count is None:
            print("❌ Could not check password exposure")
        elif password_count == 0:
            print("✅ Password has NOT been found in known breaches")
        else:
            print(f"⚠️  Password has been seen {password_count:,} times in breaches!")
        
        # Risk assessment
        print("\n" + "-"*70)
        print("📊 RISK ASSESSMENT:")
        
        if breach_found and password_count and password_count > 0:
            print("  🔴 HIGH RISK - Email breached AND password is compromised")
            print("  ⚡ ACTION REQUIRED: Change password immediately!")
        elif breach_found and (password_count == 0 or password_count is None):
            print("  🟡 MEDIUM RISK - Email breached but password appears safe")
            print("  💡 RECOMMENDATION: Change password if you still use it for this account")
        elif password_count and password_count > 0:
            print("  � MEDIUM RI SK - Password is compromised")
            print("  💡 RECOMMENDATION: Change this password everywhere you use it")
        else:
            print("  � LOW RMISK - No exposure detected")
            print("  💡 RECOMMENDATION: Continue using strong, unique passwords")
        
        print("="*70 + "\n")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         OSINT Breach Checker - Free Edition                   ║
║                    Ethical Security Research                  ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("📌 This tool uses free APIs (no API key required)")
    print("   - Email breach check via IntelX/LeakCheck")
    print("   - Password check via Pwned Passwords API")
    print("   Note: If automatic check fails, manual verification links provided\n")
    
    checker = BreachChecker()
    
    # Get email to check
    email = input("📧 Enter email address to check: ").strip()
    
    if not email or '@' not in email:
        print("❌ Invalid email address")
        sys.exit(1)
    
    # Get password to check
    print("\n🔐 Enter the password you want to check for this email:")
    print("   (Your password is hashed locally and never sent in full)")
    password = getpass.getpass("   Password: ")
    
    if not password:
        print("❌ Password cannot be empty")
        sys.exit(1)
    
    # Perform checks
    print("\n🔍 Checking email breaches...")
    breach_found, breach_details = checker.check_email_breaches_free(email)
    
    time.sleep(1.5)  # Rate limiting courtesy
    
    print("🔍 Checking password exposure...")
    password_count = checker.check_password_pwned(password)
    
    # Display report
    checker.display_breach_report(email, breach_found, breach_details, password_count)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
