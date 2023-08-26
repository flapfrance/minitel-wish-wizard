# minitel-wish-wizard
## Wish Wizard system build with old French minitels
More infos about this project here:

<img src="https://github.com/flapfrance/minitel-wish-wizard/blob/main/WW_QR.png" width=10% height=10%>

Special thanks to cquest and his Python library: https://github.com/cquest/pynitel and all the informations found at the "Musée du minitel" : https://www.museeminitel.fr/

1. Installation on Linux oder Raspberry
needs: If running on RASPI: SSH access & perhaps VNC to install Raspi headless, I use old 10' Laptops (32 or 64 bits) with Raspberry desktop as Server or Mono installation (so no need fo vnc), and raspberrys as clients (even Raspi 2 works well) 
    - mariadb: `sudo apt install mariadb` (auf Raspberrysystem) or `sudo apt install mariadb-server` (auf anderem linux) 
    - libmariadb-dev: `sudo apt install libmariadb-dev` 
    - python (should be there, higer than  3.0)
        - perhaps python-is-python3: `sudo apt install python-is-python3`
     - with 'pip' 
        - and mysql.connector: `pip install mysql.connector`

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
   
4. Network:
    - For multi-minitel installation  create a (wifi) network. Actually the  Programm uses  192.168.0.1-255
    Server is on 192.168.0.99. If there are Networkproblems change IP adresse in "wishwizard.py" (around line 1384).
    The clients can be attached via DHCP

5. Special codes: 
    - On pages Choices (1 or 2) :
        - 99 to open delete whishes page
        - 98 preferences (NOT READY YET)
6. Possible changes in the code:
    - Language at start: (around Line 145 ) lang = "DE" (or FR, EN, or ES)
