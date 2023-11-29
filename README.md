# minitel-wish-wizard
## Wish Wizard system build with old French minitels
https://www.facebook.com/wishwizardproject This is the Link to the FB page, for more Informations and for the WISH WIZARD User to share there experience!

<img src="https://github.com/flapfrance/minitel-wish-wizard/blob/main/WW_QR.png" width=10% height=10%>


Special thanks to cquest and his Python library: https://github.com/cquest/pynitel and all the informations found at the "Musée du minitel" : https://www.museeminitel.fr/

0. News:  Installation on Raspi Bookworm / Debian12 has some difficulties, cause pip is less suported and refuse the istallation externalpachages (error: externally-managed-environment)  Install pip3, and use the flag --break-system-packages for pip installs, or the hard way, `sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED` should help
1.There is now an settings.ini file. If your minitel has a FNCT - Key, you can change speed to 4800. Also you can install a printer. Acces to the setting file via your computer or from the Mainpage on minitel by choosing '98' + ENVOI.
2. V1.4 Printerintegration (to finish for serial) , after wishchoice to pervious list, some dbchanges: db prefs now unneeded 
also changes the connection automaticly from 1200 to 4800 Bauds (works on Minitel1, on Minitel2  it need to be checked) There are some old Minitels1 without the FNCT key, they only can run with 1200 Bauds. You can set this in the settings.ini.
needs: If running on RASPI: SSH access & perhaps VNC to install Raspi headless, I use old 10' Laptops (32 or 64 bits) with Raspberry desktop as Server or Mono installation (so no need fo vnc), and raspberrys as clients (even Raspi 2 works well) 
    - mariadb: ~~`sudo apt install mariadb` (auf Raspberrysystem) or~~ `sudo apt install mariadb-server`
       -  To open acces over network change `bind-address = 127.0.0.1` to `0.0.0.0` in `sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf` 
    - libmariadb-dev: `sudo apt install libmariadb-dev
    - python (should be there, higer than  3.0)
        - perhaps python-is-python3: `sudo apt install python-is-python3`
     - with 'pip' 
        - and mysql.connector: `pip install mysql.connector`
    - To have access to /ttyUSB0 add USER (your user name) to dialout group `sudo usermod -a -G dialout $USER` and restart.
If  not working try also `sudo usermod -a -G tty $USER` & restart

3. Programm needs from mariadb the database 'minitel':
    - Acces with: `sudo mariadb`
        - `CREATE DATABASE minitel;`
        - utilisateur1 : `CREATE USER 'utilisateur1'@'%';`
        - `GRANT ALL ON *.* TO 'utilisateur1'@'%';`
    
    - Tables: whishes , prefs (are installed on first use of wishwizard.py)
        - To delete (drop) table : (for maintenance or reset)
        - `sudo mariadb`
        - `USE minitel;`
        - `DROP TABLE wishes;` or `DROP TABLE pref;`(Table pref will be replaced by settings.ini in next Version)

4. Start via:
    - By CLI:
        - Start out of the directory ./minitel: `python wishwizard.py` bzw. `python3 wishwizard.py`
    - Autostart for Server:
        - minitelstart.service datei copy to /etc/systemd/system (check path in file)
        - `sudo systemctl enable minitelstart.service`
        - `sudo systemctl daemon-reload`
    - or for clients oder standalone Raspi's
        - "crontab -e" and "@reboot sleep 60 && cd /home/pi/minitel && /usr/bin/python /home/pi/minitel/wishwizard.py" (`sleep 60` only needed if the dataserver should start first)
        - or perhaps with  .desktop  (file in directory), not tested
5. Printer (Thermal):
   
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
    - For multi-minitel installation  create a (wifi) network. Add the IP adresse of the serverwith the database to use in the preferences (98 on page choices) or directly in settings.ini.
    

5. Special codes: 
    - On pages Choices (1 or 2) :
        - 99 to open delete whishes page
        - 98 preferences ( IP adresse for the server database,Timer for Screensaver, and Hexcodes for USBprinters works well , the rest is wip)
            - use this page to change preferences, some changes may need a restart. To reset preferences, delete the settings.ini. 
