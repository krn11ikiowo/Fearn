#!/usr/bin/env python3
"""
Fearn Certificate and Provisioning Profile Generator
Generates self-signed certificates and provisioning profiles for iOS app signing.
"""

import argparse
import os
import subprocess
from datetime import datetime, timedelta
import uuid

def run_command(cmd, verbose=False):
    """Execute a shell command and return output."""
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout

def generate_private_key(key_path, verbose=False):
    """Generate a private key."""
    if verbose:
        print(f"Generating private key: {key_path}")
    cmd = ["openssl", "genrsa", "-out", key_path, "2048"]
    run_command(cmd, verbose)

def generate_certificate(key_path, cert_path, verbose=False):
    """Generate a self-signed certificate."""
    if verbose:
        print(f"Generating certificate: {cert_path}")
    cmd = [
        "openssl", "req",
        "-new", "-x509",
        "-key", key_path,
        "-out", cert_path,
        "-days", "365",
        "-subj", "/C=US/O=Fearn Development/OU=FEARNAPPLO/CN=Fearn App"
    ]
    run_command(cmd, verbose)

def generate_p12(key_path, cert_path, p12_path, password="fearn123", verbose=False):
    """Generate a PKCS12 (.p12) certificate."""
    if verbose:
        print(f"Generating P12 certificate: {p12_path}")
    cmd = [
        "openssl", "pkcs12",
        "-export",
        "-in", cert_path,
        "-inkey", key_path,
        "-out", p12_path,
        "-name", "Fearn Self-Signed",
        "-password", f"pass:{password}"
    ]
    run_command(cmd, verbose)

def apple_date(dt: datetime) -> str:
    """Return date in Apple plist format: 2026-07-17T19:24:38Z"""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def generate_mobileprovision(bundle_id, team_id, name, verbose=False):
    """Generate a valid provisioning profile."""
    if verbose:
        print(f"Generating provisioning profile for {bundle_id}")

    os.makedirs("certs", exist_ok=True)

    now = datetime.utcnow()
    expires = now + timedelta(days=365)

    creation_str = apple_date(now)
    expiration_str = apple_date(expires)
    uuid_str = str(uuid.uuid4())

    profile_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>AppIDName</key>
    <string>{name}</string>

    <key>AppIdentifierPrefix</key>
    <array>
        <string>{team_id}</string>
    </array>

    <key>ApplicationIdentifierPrefix</key>
    <array>
        <string>{team_id}</string>
    </array>

    <key>CreationDate</key>
    <date>{creation_str}</date>

    <key>Platform</key>
    <array>
        <string>iOS</string>
    </array>

    <key>Entitlements</key>
    <dict>
        <key>application-identifier</key>
        <string>{team_id}.{bundle_id}</string>

        <key>get-task-allow</key>
        <true/>

        <key>keychain-access-groups</key>
        <array>
            <string>{team_id}.*</string>
        </array>

        <key>aps-environment</key>
        <string>development</string>
    </dict>

    <key>ExpirationDate</key>
    <date>{expiration_str}</date>

    <key>Name</key>
    <string>{name} Provisioning Profile</string>

    <key>TeamIdentifier</key>
    <array>
        <string>{team_id}</string>
    </array>

    <key>TimeToLive</key>
    <integer>365</integer>

    <key>UUID</key>
    <string>{uuid_str}</string>

    <key>Version</key>
    <integer>1</integer>
</dict>
</plist>
"""

    profile_path = "certs/Fearn.mobileprovision"
    with open(profile_path, "w") as f:
        f.write(profile_content)

    if verbose:
        print(f"Provisioning profile created: {profile_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate certificates and provisioning profiles for Fearn")

    parser.add_argument("--bundle-id", default="com.krnlthemodder.fearn")
    parser.add_argument("--team-id", default="FEARNAPPLO")
    parser.add_argument("--name", default="Fearn")
    parser.add_argument("--password", default="fearn123")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    os.makedirs("certs", exist_ok=True)

    key_path = "certs/Fearn.key"
    cert_path = "certs/Fearn.crt"
    p12_path = "certs/Fearn.p12"

    try:
        generate_private_key(key_path, args.verbose)
        generate_certificate(key_path, cert_path, args.verbose)
        generate_p12(key_path, cert_path, p12_path, args.password, args.verbose)
        generate_mobileprovision(args.bundle_id, args.team_id, args.name, args.verbose)

        print("✓ Certificates and provisioning profile generated successfully")
        print(f"  - Private key: {key_path}")
        print(f"  - Certificate: {cert_path}")
        print(f"  - P12 Certificate: {p12_path}")
        print(f"  - Provisioning Profile: certs/Fearn.mobileprovision")

    except Exception as e:
        print(f"✗ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
