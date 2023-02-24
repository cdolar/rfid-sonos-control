#! /usr/bin/env python3

from soco import SoCo, discover

if __name__ == '__main__':
    print('Found the following Sonos players')
    for player in list(discover()):
        print(f"{player.player_name}")
