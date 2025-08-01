# VoidOS Bootloader CTF Challenge

This is a Dockerized crypto-based CTF challenge simulating a malware-infected, locked bootloader environment. Connect via netcat to explore a fake terminal, analyze logs, and use cryptanalysis to unlock the system and reveal the flag.

## Files
- `malboot_nc.py`: Main challenge script (fake bootloader shell)
- `create_encrypted_os.py`: Helper to generate the encrypted payload
- `syslog.txt`: Log file containing obfuscated key(s) and decoys
- `os_encrypted.img`: Encrypted system image (auto-generated)
- `Dockerfile`: Container setup

## Build & Run

1. **Build the Docker image:**
   ```sh
   docker build -t voidos-ctf .
   ```
2. **Run the challenge:**
   ```sh
   docker run --rm -p 1337:1337 voidos-ctf
   ```
3. **Connect to the challenge:**
   ```sh
   nc localhost 1337
   ```

## Working

1. **Bootloader Simulation:**
   - When you connect, you see an ASCII boot animation and a message: `VoidOS v1.0 — Bootloader Secure Terminal`.
   - The system says it is encrypted and prompts you to type `help` for available commands.

2. **Exploring the Fake Shell:**
   - Use `ls` to list files and directories in the current location.
   - Use `cd <dir>` to change directories (e.g., `cd var`, `cd log`).
   - Use `cat <file>` to view the contents of files (e.g., `cat syslog.txt`).
   - The filesystem is read-only. Any attempt to modify files (e.g., `rm`, `touch`) will return a "Read-only filesystem." message.

3. **Finding the Key (Crypto Analysis Required!):**
   - In `/var/log/syslog.txt`, you will find several suspicious hex strings in log lines like:
     ```
     [DEBUG] kernel_param: cryptokey_init = <hex>
     ```
   - You will also find a log line with a mask:
     ```
     [INFO] Bootloader XOR mask: BOOTLOADER123456
     ```
   - Only one hex string is the real key XORed with the mask. The others are decoys.
   - To recover the AES key, XOR the correct hex string (as bytes) with the ASCII bytes of the mask.

4. **Unlocking the System:**
   - Enter the recovered key as a command at the prompt.
   - If correct, the system will decrypt the locked OS image and display a fake OS boot message along with the flag.
   - If incorrect, you will see an error message.

---

**Hint:** Careful log analysis and some XOR magic will unlock the system!

**Flag format:** `flag{you_have_unlocked_the_fake_os}` 