# Library Media Website
A basic media player for a local website to be hosted on a raspi 4

Files within the ```videos/``` folder are automatically added to the system.

A website is hosted at ```$ip-addr:5000/``` to control the VLC instance.  

## To Run
### Install Dependencies
```
pip3 install -r requirements.txt
```

### Run the script
```
python3 main.py
```

### Control the player
```
Navigate to http://$ip-addr:5000/
where $ip-addr is the ip address of the device running the media player
```
