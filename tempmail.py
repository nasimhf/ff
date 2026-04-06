import requests
import json
import os
import time
import sys
import random

# ==================== Save / Load Email ====================
SAVE_FILE = "email_saved.json"

def save_email(email, password):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({
                "email": email,
                "password": password
            }, f)
    except:
        pass

def load_email():
    if not os.path.exists(SAVE_FILE):
        return None, None
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("email"), data.get("password")
    except:
        return None, None

# ==================== Colors ====================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

c = Colors()

# ==================== Auto Update System ====================
def check_for_updates():
    repo_path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(repo_path, ".git")):
        print(f"{c.YELLOW}🔄 Checking for updates...{c.RESET}")
        os.system("git stash")
        result = os.system("git pull")
        if result == 0:
            print(f"{c.GREEN}✅ Tool updated successfully! Please restart.{c.RESET}")
            sys.exit(0)
        else:
            print(f"{c.RED}❌ Update failed{c.RESET}")

# ==================== Temporary Email Functions ====================
def create_temp_email(password=None):
    if not password:
        password = input(f"{c.YELLOW}🔑 Enter password (or press Enter for random): {c.RESET}").strip()
        if not password:
            password = str(random.randint(10000000, 99999999))
    
    url = f"https://api-mail-two.vercel.app/create?password={password}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'email' in data:
                print(f"\n{c.GREEN}✅ Email created successfully!{c.RESET}")
                print(f"{c.CYAN}📧 Email     : {c.WHITE}{data['email']}{c.RESET}")
                print(f"{c.CYAN}🔑 Password  : {c.WHITE}{data['password']}{c.RESET}")
                save_email(data['email'], data['password'])
                return data['email'], data['password']
            else:
                print(f"{c.RED}❌ Response error: {data}{c.RESET}")
        else:
            print(f"{c.RED}❌ Connection failed (Code {response.status_code}){c.RESET}")
    except Exception as e:
        print(f"{c.RED}❌ Error: {e}{c.RESET}")
    return None, None

def get_mails(email, password):
    url = f"https://api-mail-msg.vercel.app/mails?email={email}&password={password}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data
            else:
                print(f"{c.YELLOW}⚠️ No messages yet.{c.RESET}")
                return []
        else:
            print(f"{c.RED}❌ Failed to fetch messages (Code {response.status_code}){c.RESET}")
    except Exception as e:
        print(f"{c.RED}❌ Error: {e}{c.RESET}")
    return []

def display_mails(mails):
    if not mails:
        print(f"{c.YELLOW}📭 No messages.{c.RESET}")
        return
    
    print(f"\n{c.CYAN}{'═' * 60}{c.RESET}")
    print(f"{c.GREEN}📬 Message List ({len(mails)} messages){c.RESET}")
    print(f"{c.CYAN}{'═' * 60}{c.RESET}")
    
    for idx, mail in enumerate(mails, 1):
        subject = mail.get('subject', 'No Subject')
        sender = mail.get('from', 'Unknown Sender')
        date = mail.get('date', '')
        print(f"{c.WHITE}[{idx}] {subject[:50]}{c.RESET}")
        print(f"    {c.BLUE}📨 From: {sender}{c.RESET}")
        if date:
            print(f"    {c.MAGENTA}🕒 {date}{c.RESET}")
        print()

def read_mail_content(mail):
    html = mail.get('html', '')
    text = mail.get('text', '')
    
    if text:
        return text
    elif html:
        import re
        clean = re.sub(r'<[^>]+>', ' ', html)
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    else:
        return "No text content."

def wait_for_email(email, password, timeout=60, interval=5):
    print(f"\n{c.YELLOW}⏳ Waiting for message to {email}... (Max {timeout} seconds){c.RESET}")
    start = time.time()
    last_count = 0
    
    while time.time() - start < timeout:
        mails = get_mails(email, password)
        if len(mails) > last_count:
            new_mails = mails[last_count:]
            print(f"\n{c.GREEN}✅ Received {len(new_mails)} new message(s)!{c.RESET}")
            for mail in new_mails:
                subject = mail.get('subject', 'No Subject')
                print(f"{c.CYAN}📧 {subject}{c.RESET}")
                print(f"{c.WHITE}{read_mail_content(mail)[:300]}{c.RESET}")
                print(f"{c.CYAN}{'─' * 40}{c.RESET}")
            return True
        time.sleep(interval)
        print(f".", end='', flush=True)
    
    print(f"\n{c.RED}❌ No message received within {timeout} seconds.{c.RESET}")
    return False

# ==================== Main Menu ====================
def main():
    check_for_updates()
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{c.CYAN}{c.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     📧  Temporary Email Tool - Protect Your Accounts    ║")
    print("║     🔐  Create a secret email that cannot be stolen     ║")
    print("║     👨‍💻  Developer: @AA                                 ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(c.RESET)
    
    email, password = load_email()

    if email:
        print(f"{c.GREEN}📂 Loaded saved email:{c.RESET}")
        print(f"{c.WHITE}{email}{c.RESET}")

    while True:
        print(f"\n{c.YELLOW}═══════════════════════════════════════════════════════════{c.RESET}")
        print(f"{c.GREEN}[1] {c.WHITE}Create New Temporary Email{c.RESET}")
        print(f"{c.GREEN}[2] {c.WHITE}View Inbox Messages{c.RESET}")
        print(f"{c.GREEN}[3] {c.WHITE}Wait for New Message (Verification Code){c.RESET}")
        print(f"{c.GREEN}[4] {c.WHITE}Show Email & Password (Copy Manually){c.RESET}")
        print(f"{c.GREEN}[5] {c.WHITE}Exit{c.RESET}")
        print(f"{c.YELLOW}═══════════════════════════════════════════════════════════{c.RESET}")
        
        choice = input(f"{c.CYAN}[Choice] {c.RESET}").strip()
        
        if choice == '1':
            email, password = create_temp_email()
            if email:
                print(f"\n{c.GREEN}💡 You can use this email to register new accounts.{c.RESET}")
                print(f"{c.YELLOW}   Remember: Password is required to read messages later!{c.RESET}")
            input(f"\n{c.YELLOW}Press Enter to continue...{c.RESET}")
            
        elif choice == '2':
            if not email:
                print(f"{c.RED}❌ No active email. Create one first (Option 1).{c.RESET}")
                input(f"{c.YELLOW}Press Enter...{c.RESET}")
                continue
            mails = get_mails(email, password)
            display_mails(mails)
            if mails:
                try:
                    idx = int(input(f"{c.CYAN}Enter message number to view content (0 to go back): {c.RESET}"))
                    if 1 <= idx <= len(mails):
                        content = read_mail_content(mails[idx-1])
                        print(f"\n{c.WHITE}{'═' * 60}{c.RESET}")
                        print(f"{c.GREEN}📄 Message Content:{c.RESET}")
                        print(f"{c.WHITE}{content}{c.RESET}")
                        print(f"{c.WHITE}{'═' * 60}{c.RESET}")
                except:
                    pass
            input(f"\n{c.YELLOW}Press Enter to continue...{c.RESET}")
            
        elif choice == '3':
            if not email:
                print(f"{c.RED}❌ No active email. Create one first (Option 1).{c.RESET}")
                input(f"{c.YELLOW}Press Enter...{c.RESET}")
                continue
            wait_for_email(email, password)
            input(f"\n{c.YELLOW}Press Enter to continue...{c.RESET}")
            
        elif choice == '4':
            if email:
                print(f"\n{c.GREEN}📧 Email: {c.WHITE}{email}{c.RESET}")
                print(f"{c.GREEN}🔑 Password: {c.WHITE}{password}{c.RESET}")
                print(f"{c.YELLOW}💡 You can copy manually by long pressing.{c.RESET}")
            else:
                print(f"{c.RED}❌ No active email.{c.RESET}")
            input(f"\n{c.YELLOW}Press Enter to continue...{c.RESET}")
            
        elif choice == '5':
            print(f"{c.GREEN}👋 Thank you for using the tool. Goodbye!{c.RESET}")
            break
        else:
            print(f"{c.RED}❌ Invalid choice, try again.{c.RESET}")
            time.sleep(1)
        
        os.system('clear' if os.name == 'posix' else 'cls')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{c.YELLOW}⚠️ Cancelled by user{c.RESET}")
    except Exception as e:
        print(f"\n{c.RED}❌ Unexpected error: {e}{c.RESET}")
