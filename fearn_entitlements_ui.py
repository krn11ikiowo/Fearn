#!/usr/bin/env python3
"""
Fearn Entitlements Manager - Clean UI for managing iOS app entitlements
"""

import os
import sys
import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

class EntitlementType(Enum):
    """iOS Entitlement types"""
    PUSH_NOTIFICATIONS = 'aps-environment'
    ICLOUD = 'com.apple.developer.icloud-services'
    HEALTHKIT = 'com.apple.developer.healthkit'
    HOMEKIT = 'com.apple.developer.homekit'
    WALLET = 'com.apple.developer.wallet'
    GAME_CENTER = 'com.apple.developer.game-center'
    NFC = 'com.apple.developer.nfc.readersession.formats'
    ASSOCIATED_DOMAINS = 'com.apple.developer.associated-domains'
    CONTACTS = 'com.apple.developer.contacts.notes'
    SENSORKIT = 'com.apple.developer.sensorkit'
    NETWORKING_VPN = 'com.apple.developer.networking.vpn'
    NEARBY_INTERACTION = 'com.apple.developer.nearby-interaction'
    MEDIA_PLAYER = 'com.apple.developer.media-player'
    WEATHER = 'com.apple.developer.weather'
    KEYCHAIN = 'keychain-access-groups'
    UBIQUITY = 'com.apple.developer.ubiquity-kvstore-identifier'
    DRIVE = 'com.apple.developer.drive'
    EXPOSURE_NOTIFICATION = 'com.apple.developer.exposure-notification'
    PAYMENT_PASS = 'com.apple.developer.payment-pass-provisioning'
    PRINT = 'com.apple.developer.print'
    BIOMETRIC = 'com.apple.developer.authentication.biometric'
    DEVICE_CHECK = 'com.apple.developer.devicecheck.appattest-environment'
    MAPS = 'com.apple.developer.maps'
    CLASS_KIT = 'com.apple.developer.ClassKit-environment'
    WEB_BROWSER = 'com.apple.developer.web-browser-engine'
    WEARABLE_CONFIG = 'com.apple.developer.wearable-configuration'
    INTER_APP_AUDIO = 'inter-app-audio'
    FAMILY_CONTROLS = 'com.apple.developer.family-controls'
    SENSORS = 'com.apple.developer.sensors.motion'
    COREMEDIA_HEVC = 'com.apple.developer.coremedia.extension.hevc'
    USER_MANAGEMENT = 'com.apple.developer.user-management'

class EntitlementsManager:
    """Manage iOS app entitlements with clean UI"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.entitlements = {}
        self.team_id = 'XXXXXXXXXX'
        self.bundle_id = 'com.example.app'
    
    def log(self, message: str, level: str = 'INFO'):
        """Log with formatting"""
        if self.verbose or level != 'DEBUG':
            print(f"[{level}] {message}")
    
    def print_header(self, title: str):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_section(self, title: str):
        """Print section header"""
        print(f"\n{title}")
        print(f"{'-'*60}")
    
    def print_menu(self, options: List[tuple]):
        """Print formatted menu"""
        for idx, (key, description) in enumerate(options, 1):
            print(f"  {idx}. {key:<20} - {description}")
        print(f"\n  0. Back")
    
    def save_to_file(self, filepath: str):
        """Save entitlements to file"""
        try:
            output = {
                'team_id': self.team_id,
                'bundle_id': self.bundle_id,
                'entitlements': self.entitlements
            }
            with open(filepath, 'w') as f:
                json.dump(output, f, indent=2)
            self.log(f"Entitlements saved to {filepath}")
            return True
        except Exception as e:
            self.log(f"Failed to save: {e}", 'ERROR')
            return False
    
    def load_from_file(self, filepath: str):
        """Load entitlements from file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.team_id = data.get('team_id', self.team_id)
            self.bundle_id = data.get('bundle_id', self.bundle_id)
            self.entitlements = data.get('entitlements', {})
            self.log(f"Entitlements loaded from {filepath}")
            return True
        except Exception as e:
            self.log(f"Failed to load: {e}", 'ERROR')
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Fearn Entitlements Manager - iOS App Entitlements UI'
    )
    
    parser.add_argument('-l', '--load', help='Load entitlements from file')
    parser.add_argument('-s', '--save', help='Save entitlements to file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    manager = EntitlementsManager(verbose=args.verbose)
    
    if args.load:
        manager.load_from_file(args.load)
    
    if args.save:
        manager.save_to_file(args.save)

if __name__ == '__main__':
    main()
