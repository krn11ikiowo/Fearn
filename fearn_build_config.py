#!/usr/bin/env python3
"""
Fearn Build Configuration Manager
Handles certificate, provisioning profile, and build environment configuration
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum


class EnvironmentError(Exception):
    """Custom exception for environment/configuration errors"""
    pass


class BuildEnvironment(Enum):
    """Build environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    RELEASE = "release"


class BuildConfig:
    """Centralized configuration for IPA builds"""
    
    # Default certificate and profile paths
    DEFAULT_CERT_DIR = "certs"
    DEFAULT_CERT_P12 = "Fearn.p12"
    DEFAULT_PROVISION_PROFILE = "Fearn.mobileprovision"
    DEFAULT_ENTITLEMENTS = "Fearn.entitlements"
    
    # Default values
    DEFAULT_BUNDLE_ID = "com.krnlthemodder.fearn"
    DEFAULT_APP_NAME = "Fearn"
    DEFAULT_TEAM_ID = "XXXXXXXXXX"
    DEFAULT_VERSION = "1.7.0"
    
    def __init__(self, verbose: bool = False, env: BuildEnvironment = BuildEnvironment.DEVELOPMENT):
        self.verbose = verbose
        self.env = env
        self.logger = BuildLogger(verbose)
        
        # Certificate and profile configuration
        self.cert_dir = Path(os.getenv("FEARN_CERT_DIR", self.DEFAULT_CERT_DIR))
        self.cert_p12_path = self.cert_dir / os.getenv("FEARN_CERT_P12", self.DEFAULT_CERT_P12)
        self.cert_password = os.getenv("FEARN_CERT_PASSWORD", "fearn123")
        self.provisioning_profile_path = self.cert_dir / os.getenv("FEARN_PROVISION_PROFILE", self.DEFAULT_PROVISION_PROFILE)
        self.entitlements_path = self.cert_dir / os.getenv("FEARN_ENTITLEMENTS", self.DEFAULT_ENTITLEMENTS)
        
        # App configuration
        self.bundle_id = os.getenv("FEARN_BUNDLE_ID", self.DEFAULT_BUNDLE_ID)
        self.app_name = os.getenv("FEARN_APP_NAME", self.DEFAULT_APP_NAME)
        self.team_id = os.getenv("FEARN_TEAM_ID", self.DEFAULT_TEAM_ID)
        self.version = os.getenv("FEARN_VERSION", self.DEFAULT_VERSION)
        
        # Build paths
        self.build_dir = Path(os.getenv("FEARN_BUILD_DIR", "."))
        self.output_dir = Path(os.getenv("FEARN_OUTPUT_DIR", "."))
        self.payload_dir = Path(os.getenv("FEARN_PAYLOAD_DIR", "Payload"))
        
        # Feature flags
        self.sign_ipa = os.getenv("FEARN_SIGN_IPA", "true").lower() == "true"
        self.validate_ipa = os.getenv("FEARN_VALIDATE_IPA", "true").lower() == "true"
        self.create_release = os.getenv("FEARN_CREATE_RELEASE", "false").lower() == "true"
        
    def validate(self) -> bool:
        """Validate configuration completeness"""
        errors = []
        
        # Check certificate files
        if self.sign_ipa:
            if not self.cert_p12_path.exists():
                errors.append(f"Certificate not found: {self.cert_p12_path}")
            if not self.provisioning_profile_path.exists():
                errors.append(f"Provisioning profile not found: {self.provisioning_profile_path}")
        
        # Check required environment variables
        if not self.bundle_id or self.bundle_id == self.DEFAULT_BUNDLE_ID:
            self.logger.warn("Bundle ID is using default value, consider setting FEARN_BUNDLE_ID")
        
        if not self.cert_password:
            errors.append("Certificate password not set (FEARN_CERT_PASSWORD)")
        
        if errors:
            for error in errors:
                self.logger.error(error)
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "bundle_id": self.bundle_id,
            "app_name": self.app_name,
            "team_id": self.team_id,
            "version": self.version,
            "environment": self.env.value,
            "cert_dir": str(self.cert_dir),
            "cert_p12": str(self.cert_p12_path),
            "provisioning_profile": str(self.provisioning_profile_path),
            "entitlements": str(self.entitlements_path),
            "build_dir": str(self.build_dir),
            "output_dir": str(self.output_dir),
            "payload_dir": str(self.payload_dir),
            "sign_ipa": self.sign_ipa,
            "validate_ipa": self.validate_ipa,
            "create_release": self.create_release,
        }
    
    def save(self, path: str = "fearn_build_config.json"):
        """Save configuration to JSON file"""
        try:
            output_path = Path(path)
            output_path.write_text(json.dumps(self.to_dict(), indent=2))
            self.logger.success(f"Configuration saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            raise
    
    def load(self, path: str = "fearn_build_config.json"):
        """Load configuration from JSON file"""
        try:
            config_path = Path(path)
            if not config_path.exists():
                self.logger.warn(f"Configuration file not found: {config_path}")
                return False
            
            config_data = json.loads(config_path.read_text())
            
            # Update attributes from loaded config
            for key, value in config_data.items():
                if hasattr(self, key) and not isinstance(getattr(self, key), property):
                    setattr(self, key, value)
            
            self.logger.success(f"Configuration loaded from {config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False


class BuildLogger:
    """Unified logging for build process"""
    
    COLORS = {
        "INFO": "\033[94m",      # Blue
        "SUCCESS": "\033[92m",    # Green
        "WARN": "\033[93m",       # Yellow
        "ERROR": "\033[91m",      # Red
        "RESET": "\033[0m",       # Reset
        "BOLD": "\033[1m",        # Bold
    }
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.log_file = Path("fearn_build.log")
        self._init_log_file()
    
    def _init_log_file(self):
        """Initialize log file"""
        try:
            self.log_file.touch(exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create log file: {e}")
    
    def _format_message(self, message: str, level: str) -> str:
        """Format log message with color and timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = self.COLORS.get(level, "")
        reset = self.COLORS["RESET"]
        return f"{color}[{timestamp}] [{level}]{reset} {message}"
    
    def _write_log(self, message: str, level: str):
        """Write message to log file and stdout"""
        formatted = self._format_message(message, level)
        print(formatted)
        
        try:
            with open(self.log_file, "a") as f:
                f.write(f"[{level}] {message}\n")
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def info(self, message: str):
        """Log info message"""
        self._write_log(message, "INFO")
    
    def success(self, message: str):
        """Log success message"""
        self._write_log(message, "SUCCESS")
    
    def warn(self, message: str):
        """Log warning message"""
        self._write_log(message, "WARN")
    
    def error(self, message: str):
        """Log error message"""
        self._write_log(message, "ERROR")
    
    def debug(self, message: str):
        """Log debug message (only if verbose)"""
        if self.verbose:
            self._write_log(message, "DEBUG")


def main():
    """CLI for managing build configuration"""
    parser = argparse.ArgumentParser(
        description="Fearn Build Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fearn_build_config.py show
  python3 fearn_build_config.py validate
  python3 fearn_build_config.py save
  python3 fearn_build_config.py setup-secrets
        """
    )
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-e", "--env", choices=["development", "testing", "release"],
                       default="development", help="Build environment")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Show configuration
    subparsers.add_parser("show", help="Display current configuration")
    
    # Validate configuration
    subparsers.add_parser("validate", help="Validate configuration completeness")
    
    # Save configuration
    subparsers.add_parser("save", help="Save configuration to JSON file")
    
    # Setup secrets
    setup_secrets = subparsers.add_parser("setup-secrets", help="Interactive setup for secrets")
    setup_secrets.add_argument("--cert-path", help="Path to certificate .p12 file")
    setup_secrets.add_argument("--profile-path", help="Path to provisioning profile")
    setup_secrets.add_argument("--cert-password", help="Certificate password")
    
    args = parser.parse_args()
    
    # Create configuration
    env = BuildEnvironment(args.env)
    config = BuildConfig(verbose=args.verbose, env=env)
    logger = config.logger
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "show":
            logger.info("Current Build Configuration:")
            print(json.dumps(config.to_dict(), indent=2))
            return 0
        
        elif args.command == "validate":
            logger.info("Validating configuration...")
            if config.validate():
                logger.success("Configuration is valid!")
                return 0
            else:
                logger.error("Configuration validation failed")
                return 1
        
        elif args.command == "save":
            config.save()
            return 0
        
        elif args.command == "setup-secrets":
            logger.info("Setting up build secrets...")
            
            # Get certificate path
            cert_path = args.cert_path or input("Path to certificate (.p12) file: ")
            if not Path(cert_path).exists():
                logger.error(f"Certificate file not found: {cert_path}")
                return 1
            
            # Get profile path
            profile_path = args.profile_path or input("Path to provisioning profile: ")
            if not Path(profile_path).exists():
                logger.error(f"Provisioning profile not found: {profile_path}")
                return 1
            
            # Get certificate password
            cert_password = args.cert_password or input("Certificate password: ")
            
            # Copy files to certs directory
            config.cert_dir.mkdir(exist_ok=True)
            import shutil
            shutil.copy2(cert_path, config.cert_p12_path)
            shutil.copy2(profile_path, config.provisioning_profile_path)
            
            logger.success(f"Certificate copied to {config.cert_p12_path}")
            logger.success(f"Profile copied to {config.provisioning_profile_path}")
            
            # Save environment variables hint
            logger.info("\nSet these environment variables:")
            logger.info(f"export FEARN_CERT_PASSWORD='{cert_password}'")
            logger.info(f"export FEARN_BUNDLE_ID='{config.bundle_id}'")
            logger.info(f"export FEARN_TEAM_ID='{config.team_id}'")
            
            return 0
    
    except KeyboardInterrupt:
        logger.warn("Operation cancelled")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
