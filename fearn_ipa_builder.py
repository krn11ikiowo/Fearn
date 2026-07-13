#!/usr/bin/env python3
"""
Fearn IPA Builder - Build complete iOS application packages
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from typing import Optional

class IPABuilder:
    """Build complete IPA files"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.template_dir = Path('Payload')
    
    def log(self, message: str, level: str = 'INFO'):
        """Log message"""
        if self.verbose or level != 'DEBUG':
            print(f"[{level}] {message}")
    
    def print_header(self, title: str):
        """Print header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def build_ipa(self, app_name: str, bundle_id: str, version: str = "1.0",
                  team_id: str = "XXXXXXXXXX", output_dir: str = ".") -> bool:
        """Build an IPA file"""
        self.print_header(f"Building IPA: {app_name}")
        
        try:
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Create build directory
            build_dir = Path('.ipa_build')
            if build_dir.exists():
                shutil.rmtree(build_dir)
            build_dir.mkdir()
            
            # Create Payload directory
            payload_dir = build_dir / 'Payload'
            app_bundle_dir = payload_dir / f"{app_name}.app"
            app_bundle_dir.mkdir(parents=True, exist_ok=True)
            
            self.log(f"Creating app bundle: {app_name}.app")
            
            # Create Info.plist
            info_plist = app_bundle_dir / 'Info.plist'
            info_plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>{bundle_id}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{version}</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
</dict>
</plist>"""
            
            with open(info_plist, 'w') as f:
                f.write(info_plist_content)
            self.log("Created Info.plist")
            
            # Create PkgInfo
            pkg_info = app_bundle_dir / 'PkgInfo'
            with open(pkg_info, 'wb') as f:
                f.write(b'APPL????')
            self.log("Created PkgInfo")
            
            # Create Code Signature directory
            codesig_dir = app_bundle_dir / '_CodeSignature'
            codesig_dir.mkdir(exist_ok=True)
            
            # Create CodeResources
            code_resources = codesig_dir / 'CodeResources'
            code_resources_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>files</key>
    <dict>
        <key>Info.plist</key>
        <data>PLACEHOLDER</data>
    </dict>
    <key>rules</key>
    <dict>
        <key>^</key>
        <true/>
    </dict>
</dict>
</plist>"""
            
            with open(code_resources, 'w') as f:
                f.write(code_resources_content)
            self.log("Created CodeResources")
            
            # Create iTunesMetadata.plist
            itunes_metadata = build_dir / 'iTunesMetadata.plist'
            itunes_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>bundleShortVersionString</key>
    <string>{version}</string>
    <key>bundleVersion</key>
    <string>1</string>
    <key>softwareVersionBundleId</key>
    <string>{bundle_id}</string>
</dict>
</plist>"""
            
            with open(itunes_metadata, 'w') as f:
                f.write(itunes_content)
            self.log("Created iTunesMetadata.plist")
            
            # Create IPA (zip file)
            ipa_name = f"{app_name}-{version}.ipa"
            ipa_path = output_path / ipa_name
            
            self.log(f"Creating IPA archive: {ipa_name}")
            
            # Change to build directory and create zip
            cwd = os.getcwd()
            os.chdir(build_dir)
            subprocess.run(['zip', '-r', '-q', str(ipa_path.absolute()), '.'],
                         check=True, capture_output=True)
            os.chdir(cwd)
            
            self.log(f"IPA created: {ipa_path}")
            
            # Clean up
            shutil.rmtree(build_dir)
            self.log("Build directory cleaned")
            
            self.print_header(f"Build Complete!")
            print(f"  App Name: {app_name}")
            print(f"  Bundle ID: {bundle_id}")
            print(f"  Version: {version}")
            print(f"  Output: {ipa_path}")
            print()
            
            return True
        
        except Exception as e:
            self.log(f"Build failed: {e}", 'ERROR')
            if build_dir.exists():
                shutil.rmtree(build_dir)
            return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Fearn IPA Builder - Build iOS application packages'
    )
    
    parser.add_argument('-n', '--name', required=True, help='App name')
    parser.add_argument('-b', '--bundle-id', required=True, help='Bundle ID')
    parser.add_argument('-v', '--version', default='1.0', help='App version')
    parser.add_argument('-t', '--team-id', default='XXXXXXXXXX', help='Team ID')
    parser.add_argument('-o', '--output', default='.', help='Output directory')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    builder = IPABuilder(verbose=args.verbose)
    success = builder.build_ipa(
        app_name=args.name,
        bundle_id=args.bundle_id,
        version=args.version,
        team_id=args.team_id,
        output_dir=args.output
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
