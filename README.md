# workerterminal
Worker terminal

# Install 

1. Create python virtual enviroment in project directory:
python3 -m venv workterminal-venv

and install all requirements packages from requirements.txt file
pip3 install -r requirements.txt

Use pip3 to make sure to use python3 version.

2. Add permision to read from usb port of RFID reader
sudo usermod -a -G dialout $USER

3. Copy file: chrome-kiosk.service to
/lib/systemd/system/kiosk-browser.service
and run 
sudo systemctl enable kiosk-browser.service




# Emulate RFID Reader
How to emulate RFID Reader read virtualCOM.sh

# References
[1] https://stackoverflow.com/questions/52187/virtual-serial-port-for-linux