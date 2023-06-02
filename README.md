# minitel-wish-wizard
##Wish Wizard system build with old French minitels

1. Installation on Linux oder Raspberry
needs: If running on RASPI: SSH access & perhaps VNC
    - mariadb: `sudo apt install mariadb` (auf Raspberrysystem) or `sudo apt install mariadb-server` (auf anderem linux) 
    - libmariadb-dev: `sudo apt install libmariadb-dev` 
    - python (should be there, higer than  3.0)
        - perhaps python-is-python3: `sudo apt install python-is-python3`
     - with 'pip' 
        - and mysql.connector: `pip install mysql.connector`

2. Programm needs from mariadb the database 'minitel':
    - Acces with: sudo mariadb
        - `CREATE DATABASE minitel;`
        - `utilisateur1 : CREATE USER 'utilisateur1'@'%';`
        - `GRANT ALL ON *.* TO 'utilisateur1'@'%';`
    
    - Tables: whishes , prefs (are installed on first use of wishwizard.py)
        - To delete (drop) table : (for maintenance)
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
        - "crontab -e" and "@reboot sleep 60 && cd /home/pi/minitel && /usr/bin/python /home/pi/minitel/wish_server_locV0.py"
        - oder eventuel mit .desktop  (file in directory)
   
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
