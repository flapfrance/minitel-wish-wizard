# minitel-wish-wizard
## Wish Wizard system build with old French minitels
This is the Link to the FB page, for more Informations and for the WISH WIZARD User to share there experience!

<img src="https://github.com/flapfrance/minitel-wish-wizard/blob/main/WW_QR.png" width=10% height=10%>


Special thanks to cquest and his Python library: https://github.com/cquest/pynitel and all the informations found at the "Musée du minitel" : https://www.museeminitel.fr/

0. News: V1.35 Printerintegration (to finish) , after wishchoice to pervious list, some dbchanges (need dbupdate on on wishes and prefs) 
also changes the connection automaticly from 1200 to 4800 Bauds (works on Minitel1, on t Minitel2 the minitel needs to be switched on and probably changed to 4800 Bauds : Fnct and "P", then "4", not tested yet)
1. Installation on Linux oder Raspberry
needs: If running on RASPI: SSH access & perhaps VNC to install Raspi headless, I use old 10' Laptops (32 or 64 bits) with Raspberry desktop as Server or Mono installation (so no need fo vnc), and raspberrys as clients (even Raspi 2 works well) 
    - mariadb: ~~`sudo apt install mariadb` (auf Raspberrysystem) or~~ `sudo apt install mariadb-server` (auf anderem linux) 
    - libmariadb-dev: `sudo apt install libmariadb-dev` 
    - python (should be there, higer than  3.0)
        - perhaps python-is-python3: `sudo apt install python-is-python3`
     - with 'pip' 
        - and mysql.connector: `pip install mysql.connector`
    - To have access to /ttyUSB0 add USER (your user name) to dialout group `sudo usermod -a -G dialout $USER` and restart.
If  not working try also `sudo usermod -a -G tty $USER` & restart

2. Programm needs from mariadb the database 'minitel':
    - Acces with: `sudo mariadb`
        - `CREATE DATABASE minitel;`
        - utilisateur1 : `CREATE USER 'utilisateur1'@'%';`
        - `GRANT ALL ON *.* TO 'utilisateur1'@'%';`
    
    - Tables: whishes , prefs (are installed on first use of wishwizard.py)
        - To delete (drop) table : (for maintenance or reset)
        - `sudo mariadb`
        - `USE minitel;`
        - `DROP TABLE wishes;`

3. Start via:
    - By CLI:
        - Start out of the directory ./minitel: `python wishwizard.py` bzw. `python3 wishwizard.py`
    - Autostart for Server:
        - minitelstart.service datei copy to /etc/systemd/system (check path in file)
        - `sudo systemctl enable minitelstart.service`
        - `sudo systemctl daemon-reload`
    - or for clients oder standalone Raspi's
        - "crontab -e" and "@reboot sleep 60 && cd /home/pi/minitel && /usr/bin/python /home/pi/minitel/wishwizard.py" (`sleep 60` only needed if the dataserver should start first)
        - or perhaps with  .desktop  (file in directory), not tested
4. Printer (Thermal):
   
    - install the python bibliotheque: `pip install python-escpos[all]`
    - For USB printers:
        - Find out the hex values of your printer: `lsusb`
        - note the `ID xxxx:yyyy`    
        - Create  a udev rule for the printer: `sudo nano /etc/udev/rules.d/99-escpos.rules` . 
        - Insert `SUBSYSTEM=="usb", ATTRS{idVendor}=="xxxx", ATTRS{idProduct}=="yyyy", MODE="0666", GROUP="dialout"`
        - Then: `sudo service udev restart`
        - Add the Hexvalues to the programm via the preferences page (Code 98) (Actuall only the first two values are used)
        actual it need to be inserted in to the code around line 108 in the def printCheck()
   - for serial printers:
       - never tested, i don't have a serial printer but perhaps it works like this:
       - If there is no USB printer the programm looks for a serial one. In the pref page you should write "/dev/tty0" or similair inthe first field.
4. Network:
    - For multi-minitel installation  create a (wifi) network. Actually the  Programm uses  192.168.0.1-255
    Server is on 192.168.0.99. If there are Networkproblems change IP adresse in "wishwizard.py" (around line 1384).
    The clients can be attached via DHCP

5. Special codes: 
    - On pages Choices (1 or 2) :
        - 99 to open delete whishes page
        - 98 preferences (Timer for Screensaver, and Hexcodes for USBprinters works well , the rest is wip)
6. Possible changes in the code:
    - Language at start: (around Line 145 ) lang = "DE" (or FR, EN, or ES)
