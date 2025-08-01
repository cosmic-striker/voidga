#!/usr/bin/env python3
import sys
import os
import time
import readline
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Simulated filesystem
FS = {
    '/': ['bin', 'etc', 'home', 'tmp', 'usr', 'var', 'README.txt'],
    '/bin': ['ls', 'cat', 'echo'],
    '/etc': ['passwd', 'shadow', 'hostname', 'boot.conf'],
    '/home': ['ctf'],
    '/home/ctf': ['README.txt', 'flag.enc'],
    '/tmp': [],
    '/usr': ['share'],
    '/usr/share': ['doc'],
    '/usr/share/doc': ['welcome.txt'],
    '/var': ['log'],
    '/var/log': ['syslog.txt', 'auth.log', 'dmesg']
}
FILES = {
    # Root level
    '/README.txt': (
        '844e97b6039ae68e9033440b9595bdacd2c7f55be608bce3769c1a7e896bf17b7fc2786ef43c2a8609df5afac1a86948\n'
    ),
    '/etc/hostname': 'voidos\n',
    '/etc/boot.conf': (
        'secure_mode=true\n'
        'crypto_mask=BOOTLOADER123456\n'
        'enable_logging=true\n'
        'boot_delay=5\n'
    ),
    '/etc/passwd': (
        'root:x:0:0:root:/root:/bin/bash\n'
        'ctf:x:1000:1000:CTF User:/home/ctf:/bin/bash\n'
        'guest:x:1001:1001:Guest User:/home/guest:/bin/bash\n'
    ),
    '/etc/shadow': (
        'root:*:18922:0:99999:7:::\n'
        'ctf:*:18922:0:99999:7:::\n'
        'guest:*:18922:0:99999:7:::\n'
    ),
    '/etc/motd': 'Welcome to VoidOS! Authorized access only.\n',
    '/etc/issue': 'VoidOS \\n \\l\n',

    # Bin folder (empty files, commands not implemented)
    '/bin/ls': '',
    '/bin/cat': '',
    '/bin/echo': '',
    '/bin/grep': '',
    '/bin/sed': '',
    '/bin/awk': '',
    '/bin/curl': '',

    # Home directories
    '/home/ctf/README.txt': '844e97b6039ae68e9033440b9595bdacd2c7f55be608bce3769c1a7e896bf17b7fc2786ef43c2a8609df5afac1a86948\n',
    '/home/ctf/flag.enc': 'db19e59117ee631ab1aa8b4e8b18a93a85a31fc1377be9c8d561f53e6c83453462fa008cee126bae064dcc1098d5fffa\n',
    '/home/ctf/.bashrc': '# .bashrc file for ctf\nalias ll="ls -la"\n',
    '/home/guest/README.txt': 'Guest user home folder. Nothing important here.\n',
    '/home/guest/.bash_history': 'ls\ncat /etc/hostname\n',

    # User docs
    '/usr/share/doc/welcome.txt': 'Thank you for using VoidOS.\n',
    '/usr/share/doc/security.txt': 'Remember to check /var/log for system messages.\n',

    # Var logs
    '/var/log/syslog.txt': ('none'),  # Loaded dynamically from disk file
    '/var/log/auth.log': (
    '[INFO] authd: login failed from 192.168.1.42\n'
    '[INFO] authd: login succeeded for user ctf\n'
    '[WARN] authd: suspicious login attempt from 10.0.0.5\n'
    '[INFO] sshd: Accepted password for user admin from 172.16.2.3 port 2222 ssh2\n'
    '[INFO] sshd: Connection closed by 172.16.2.3 port 2222\n'
    '[DEBUG] kernel_param: cryptokey_init = 3ae2c995610c2e969702d797bb6aab0b\n'
    '[DEBUG] kernel_param: cryptokey_init = 34cedb42ade2efcdb3f0d6c7e0d75b0b\n'
    '[INFO] systemd-logind: New session 45 of user root\n'
    '[INFO] authd: login failed from 192.168.1.75\n'
    '[DEBUG] kernel_param: cryptokey_init = 24aff9b99b0ce2a29ee28759c7d2fe64\n'
    '[DEBUG] kernel_param: cryptokey_init = 6c2fd1d75e63ba48e3a9735b2f4a18cd\n'
    '[DEBUG] kernel_param: cryptokey_init = 4981cfeb8ccf19b9f13a679abcbb3452\n'
    '[DEBUG] kernel_param: cryptokey_init = 83bb98c768b3a0f8eecde5e4ed2ba2d5\n'  # 👈 Hidden value
    '[INFO] sshd: Failed password for invalid user test from 203.0.113.8 port 4096 ssh2\n'
    '[INFO] authd: login succeeded for user guest\n'
    '[INFO] sudo: user admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/ls\n'
    '[WARN] sshd: reverse mapping checking getaddrinfo for 203-0-113-8.example.com failed\n'
    '[INFO] sshd: Disconnected from 203.0.113.8 port 4096 [preauth]\n'
    ),

   '/var/log/dmesg': (
    '[    0.000000] Linux version 5.10.0-void (gcc@voidos) (gcc version 10.2.1) #1 SMP Thu Jul 18 10:00:00 UTC 2025\n'
    '[    0.000000] Command line: BOOT_IMAGE=/vmlinuz root=/dev/sda1 ro quiet splash\n'
    '[    0.001234] x86/fpu: Supporting XSAVE feature 0x001: \'x87 floating point registers\'\n'
    '[    0.002123] x86/fpu: Enabled xstate features 0x1, context size is 576 bytes, using \'standard\' format.\n'
    '[    0.003456] BIOS-e820: [mem 0x0000000000000000-0x000000000009ffff] usable\n'
    '[    0.007891] ACPI: Early table checksum verification disabled\n'
    '[    0.009384] ACPI: RSDP 0x00000000000F0420 000024 (v02 VOIDOS)\n'
    '[    0.010927] ACPI: XSDT 0x00000000BF7FA210 00006C (v01 VOIDOS VOIDTABLE 00000001 VOID)\n'
    '[    0.012600] ACPI: FACP 0x00000000BF7FB000 00010C (v05 VOIDOS VOIDFACP 00000001 VOID)\n'
    '[    0.013000] kernel: decrypt_iv=d65e8e7a8f2c65a1ec8ab219a5f3c920\n'#--->VI
    '[    0.013100] kernel: entropy pool initialized\n'
    '[    0.014200] Secure boot: Secure boot enabled\n'
),


    # Tmp folder - empty or temporary files
    '/tmp/.tempfile': 'Temporary data - not important\n',

    # Hidden config files (dotfiles)
    '/root/.hidden_config': 'This file contains no useful information.\n',
    '/root/.bash_history': 'ls\ncd /var/log\ncat syslog.txt\n',

    # Miscellaneous files to add noise
    '/var/run/lockfile': '',
    '/var/cache/voidos.cache': 'cached_data=123456\n',
    '/proc/cpuinfo': 'processor\t: 0\nmodel name\t: VoidOS CPU\n',
    '/proc/meminfo': 'MemTotal:       2048000 kB\nMemFree:        1024000 kB\n',
}

CUR_DIR = '/'
ENCRYPTED_IMG = 'os_encrypted.img'

ASCII_BOOT = r"""
          _______ _________ ______     _______     __   
|\     /|(  ___  )\__   __/(  __  \   (  __   )   /  \  
| )   ( || (   ) |   ) (   | (  \  )  | (  )  |   \/) ) 
| |   | || |   | |   | |   | |   ) |  | | /   |     | | 
( (   ) )| |   | |   | |   | |   | |  | (/ /) |     | | 
 \ \_/ / | |   | |   | |   | |   ) |  |   / | |     | | 
  \   /  | (___) |___) (___| (__/  )  |  (__) | _ __) (_
   \_/   (_______)\_______/(______/   (_______)(_)\____/
                                                        

"""

HELP_TEXT = """
Available commands:
  help           Show this help message
  ls             List files in current directory
  cd <dir>       Change directory
  cat <file>     Show file contents
  (enter key)    Attempt to unlock system
"""

PROMPT = 'voidos> '

# For netcat compatibility, use sys.stdin.readline()
def slow_print(text, delay=0.02):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()

def boot_animation():
    slow_print(ASCII_BOOT, 0.001)
    time.sleep(0.3)
    slow_print('VoidOS v1.0 — Bootloader Secure Terminal', 0.02)
    time.sleep(0.2)
    slow_print('System is encrypted. Type \'help\' to view available commands.\n', 0.02)

def resolve_path(cur, arg):
    if arg.startswith('/'):
        path = arg
    else:
        if cur == '/':
            path = '/' + arg
        else:
            path = cur + '/' + arg
    # Normalize
    parts = []
    for p in path.split('/'):
        if p == '' or p == '.':
            continue
        elif p == '..':
            if parts:
                parts.pop()
        else:
            parts.append(p)
    return '/' + '/'.join(parts) if parts else '/'

def list_dir(cur):
    return FS.get(cur, [])

def is_dir(path):
    return path in FS

def is_file(path):
    return path in FILES

def cat_file(path):
    # Try to read from disk if file exists
    disk_path = None
    if path == '/var/log/syslog.txt':
        disk_path = 'syslog.txt'
    if disk_path and os.path.exists(disk_path):
        with open(disk_path, 'r') as f:
            return f.read()
    return FILES.get(path, 'cat: {}: No such file'.format(path))

def main():
    global CUR_DIR
    boot_animation()
    while True:
        sys.stdout.write(PROMPT)
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:
            break
        cmd = line.strip()
        if not cmd:
            continue
        if cmd == 'help':
            print(HELP_TEXT)
        elif cmd == 'ls':
            files = list_dir(CUR_DIR)
            print('  '.join(files))
        elif cmd.startswith('cd '):
            arg = cmd[3:].strip()
            new_dir = resolve_path(CUR_DIR, arg)
            if is_dir(new_dir):
                CUR_DIR = new_dir
            else:
                print('cd: no such directory:', arg)
        elif cmd.startswith('cat '):
            arg = cmd[4:].strip()
            # Try both absolute and relative path
            file_path = resolve_path(CUR_DIR, arg)
            if is_file(file_path):
                print(cat_file(file_path))
            elif is_dir(file_path):
                print('cat: {}: Is a directory'.format(arg))
            else:
                # Try if the user is in a subdir and gave just the filename
                for p in FILES:
                    if p.endswith('/' + arg) and CUR_DIR in p:
                        print(cat_file(p))
                        break
                else:
                    print('cat: {}: No such file'.format(arg))
        elif cmd in ['rm', 'touch', 'echo', 'mv', 'cp', 'nano', 'vi', 'vim'] or any(cmd.startswith(x+' ') for x in ['rm', 'touch', 'echo', 'mv', 'cp', 'nano', 'vi', 'vim']):
            print('Read-only filesystem.')
        else:
            # Treat as password attempt
            key = cmd.replace('.', '')
            if len(key) == 16:
                try:
                    with open(ENCRYPTED_IMG, 'rb') as f:
                        iv = f.read(16)
                        ct = f.read()
                    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
                    pt = unpad(cipher.decrypt(ct), 16)
                    print(pt.decode())
                    print('\n[System unlocked. Exiting terminal.]')
                    break
                except Exception as e:
                    print('Incorrect key or system error.')
            else:
                print('Unknown command or incorrect key.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nSession closed.') 