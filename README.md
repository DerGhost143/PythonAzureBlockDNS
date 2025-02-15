# Block ADs DNS

A DNS server for blocking ads and unwanted websites.

## Setup

1. **Adjust the blacklist:**
   - Edit the `settings/blacklist.json` file to modify or expand the blocked domains.

2. **Configure ports (optional):**
   - By default, the following ports are used:
     - **TCP 54**
     - **UDP 54**
   - If needed, you can change the ports in the settings.

## Installation & Start

1. Ensure Python is installed.
2. Install required dependencies (if necessary):
   ```sh
   pip install -r requirements.txt

3. Start the DNS server:
   ```sh
   python main.py
