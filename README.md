# DirFuzzer by Shaheen

DirFuzzer is a high-speed directory brute-forcing tool designed for ethical hackers and penetration testers. It supports multithreading, status code filtering, extension guessing, and custom wordlists.

---

Features

- Multi-threaded directory and file fuzzing
- Live progress bar
- HTTP status code filtering
- Custom file extensions
- User-Agent spoofing
- Request timeout and delay support
- Clean, color-coded terminal output

---

##Usage

Example Cmd

python3 dirfuzzer.py -u http://example.com -w wordlist.txt -x .php,.html --status 200 403
