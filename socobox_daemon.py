#!/usr/bin/env python3
import sys
import asyncio
import logging
import os.path
import json

from re import compile
from argparse import ArgumentParser
from evdev import InputDevice, list_devices, ecodes
from soco import SoCo, discover

def find_player(player_name: str) -> SoCo:
    sonos = None
    logging.debug('Found the following players')
    for player in list(discover()):
        logging.info(f"Found Sonos speaker {player.player_name}")
        if player.player_name == player_name:
            logging.info(f"(This is will be selected as sonosbox player)")
            sonos = player
    return sonos

def get_rfid_reader():
    devices = [InputDevice(dev) for dev in list_devices()]
    return devices

def find_rfid_reader(reader_name: str) -> InputDevice:
    device = None
    devices = get_rfid_reader()
    for dev in devices:
        logging.info(f'Found event device {dev} ({dev.name})')
        if dev.name == reader_name:
            logging.info(f'   (This will be used as reader)')
            device = dev
    return device

def load_config(filename:str) -> dict:
    config = {}
    logging.info(f'Using {args.file} as config file')
    if os.path.exists(args.file):
        logging.info(f'Found file, try to parse it')
        with open (args.file) as f:
            config = json.load(f)
            logging.info(f'Loaded: {config}')
    else:
        logging.warning(f'Could not read config, using defaults instead')
        config['player_name'] = 'Fernsehzimmer'
        config['rfid_reader_name'] = 'HXGCoLtd Keyboard'
    return config

async def scan_card(device:InputDevice) -> str:
    keycode_regex = compile('KEY_([0-9,A-Z]{1})')
    code = ''
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:
            keycode = ecodes.KEY[event.code]
            if keycode == 'KEY_ENTER':
                yield code
                code = ''
            else:
                code += keycode_regex.findall(keycode)[0]

async def main(device:InputDevice, player:SoCo):
    async for cardId in scan_card(device):
        logging.info(f'Received card ID {cardId}')
        sonos_actions(player,cardId)

def sonos_actions(player:SoCo, cardId:str):
        playlist = player.get_sonos_playlist_by_attr('name', cardId)
        if playlist != None:
            player.unjoin()
            player.stop()
            player.clear_queue()
            player.add_to_queue(playlist)
            player.play()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Print with log level DEBUG')
    parser.add_argument('-f', '--file', action='store', default='config.json', help='Load configuration from file')
    parser.add_argument('--list_devices', action='store_true', help='List all event input devices')
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    if args.list_devices:
        devices = get_rfid_reader()
        print('Attached devices')
        for dev in devices:
            print(f'  "{dev.name}" (Info: {dev})')
        sys.exit()
    
    config = load_config(args.file)
    device = find_rfid_reader(config['rfid_reader_name'])
    if device == None:
        sys.exit(f'No event device found with name {config["rfid_reader_name"]}')
    player = find_player(config['player_name'])
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(device, player))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

