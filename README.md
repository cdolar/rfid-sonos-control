# SoCo Box
The idea of this little script is to provide a way to control a Sonos box with RFID cards via a RaspberryPi and a generic USB RFID reader. 

The script uses the following Python libraries under the hood:
- [SoCo](http://docs.python-soco.com/en/latest/index.html) for controlling the Sonos speaker
- [evdev](https://python-evdev.readthedocs.io/en/latest/index.html) for RFID card reader input
- [GPIO zero](https://gpiozero.readthedocs.io/en/stable/index.html) for GPIO buttons

## Installation
Get the code from github and install it to `/home/pi/socobox`. 
```
cd /home/pi
git clone https://github.com/cdolar/socobox.git
cd socobox
```
If you have a chosen a different directory, make sure to edit the `socobox.service` and insert your path as working director.

Next, install the python requirements
```
pip3 install -r requirements.txt
```

Next, update the information in `config.json` by scanning your system with the helper scripts.
- Run `python3 list_devices.py` and copy-and-paste the name into the config under `rfid_reader_name`
- Run `python3 list_sonos_players.py` and copy-and-paste the name into the config under `player_name`

Last, install the `socobox.service` and check if it is running
```
sudo systemctl enable $(pwd)/socobox.service
sudo systemctl daemon-reload
sudo systemctl start socobox.service
sudo systemctl status socobox.service
```
The last command should indicate `active (running)` and the logs should indicate lines with `(This will be used as reader)` and `(This will be selected as sonosbox player)`.

## RFID Card Codes and Sonos Playlists
The code stored on the RFID cards is used to search the Sonos playlists. If there is a match, the playlist is queued and playback is started.

### Create a Sonos Playlist for a new RFID Card
Usually, the code stored to the RFID card is printed on the back of the card, e.g. `0011907736`. Use this code as the title of a new Sonos playlist. So do the following to create a new playlist:
- Create a new Sonos Playlist in your Sonos controller app
- Name the new playlist with the code on the back of your app
- Fill the playlist with titles

### Update a Sonos Playlist for an existing RFID Card
Update the Sonos Playlist that has the code of the respective RFID Card. It's as simple as that

## Buttons
In case you have attached buttons to the GPIO header of the RaspberryPi, they can be used to control the Sonos speaker. I have setup mine on BCM pins 16, 19 and 21. They control next title, previous title and restarting the playback queue. Edit the `socobox.daemon` file as needed.


