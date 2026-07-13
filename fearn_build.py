#!/usr/bin/env python3
"""
Fearn Build & Release Script - Automated version management and releases
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Tuple

class BuildManager:
    """Manage builds, versions, and releases"""
    
    def __init__(self, repo_path: str = '.'):
        self.repo_path = Path(repo_path)
        self.version_file = self.repo_path / 'VERSION'
        self.changelog_file = self.repo_path / 'CHANGELOG.md'
        self.releases_dir = self.repo_path / 'releases'
    
    def log(self, message: str):
        """Print log message"""
        print(f"[INFO] {message}")
    
    def error(self, message: str):
        """Print error message"""
        print(f"[ERROR] {message}")
    
    def get_version(self) -> Tuple[int, int, int]:
        """Get current version"""
        try:
            if self.version_file.exists():
                with open(self.version_file, 'r') as f:
                    parts = f.read().strip().split('.')
                    return tuple(map(int, parts[:3]))
        except Exception:
            pass
        return (1, 0, 0)
    
    def set_version(self, version: Tuple[int, int, int]):
        """Set version"""
        with open(self.version_file, 'w') as f:
            f.write(f"{version[0]}.{version[1]}.{version[2]}")
    
    def version_string(self, version: Tuple[int, int, int]) -> str:
        """Convert version tuple to string"""
        return f"{version[0]}.{version[1]}.{version[2]}"
    
    def git_commit(self, message: str) -> bool:
        """Create git commit"""
        try:
            subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', message], check=True, capture_output=True)
            self.log(f"Committed: {message}")
            return True
        except Exception as e:
            self.error(f"Commit failed: {e}")
            return False
    
    def git_tag(self, tag: str) -> bool:
        """Create git tag"""
        try:
            subprocess.run(['git', 'tag', '-a', tag, '-m', f"Release {tag}"], 
                         check=True, capture_output=True)
            self.log(f"Tagged: {tag}")
            return True
        except Exception as e:
            self.error(f"Tag failed: {e}")
            return False
    
    def git_push(self, push_tags: bool = False) -> bool:
        """Push to remote"""
        try:
            subprocess.run(['git', 'push'], check=True, capture_output=True)
            if push_tags:
                subprocess.run(['git', 'push', '--tags'], check=True, capture_output=True)
            self.log("Pushed to remote")
            return True
        except Exception as e:
            self.error(f"Push failed: {e}")
            return False
    
    def push_bugfix(self, description: str, is_major: bool = False) -> bool:
        """Push bugfix with version bump"""
        print("\n" + "="*60)
        print("  Fearn - Bugfix Release")
        print("="*60)
        
        current = self.get_version()
        self.log(f"Current version: {self.version_string(current)}")
        
        # Calculate new version
        if is_major:
            new_version = (current[0], current[1] + 70, 0)
            print(f"  Type: MAJOR BUGFIX (+0.70)")
        else:
            new_version = (current[0], current[1], current[2] + 1)
            print(f"  Type: MINOR BUGFIX (+0.0.1)")
        
        new_version_str = self.version_string(new_version)
        print(f"  New version: {new_version_str}")
        print(f"  Description: {description}")
        print()
        
        # Update version file
        self.set_version(new_version)
        
        # Create commit
        if is_major:
            commit_msg = f"[RELEASE] v{new_version_str} - Major bugfix: {description}"
        else:
            commit_msg = f"[PATCH] v{new_version_str} - {description}"
        
        if not self.git_commit(commit_msg):
            return False
        
        # For major releases, create tag and release notes
        if is_major:
            self.releases_dir.mkdir(exist_ok=True)
            release_file = self.releases_dir / f"v{new_version_str}.md"
            
            with open(release_file, 'w') as f:
                f.write(f"# Fearn v{new_version_str}\n\n")
                f.write(f"**Type:** MAJOR BUGFIX\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write(f"## Changes\n\n- {description}\n")
            
            self.log(f"Release notes created: {release_file}")
            
            # Commit release notes
            self.git_commit(f"Release notes for v{new_version_str}")
            
            # Tag release
            if not self.git_tag(f"v{new_version_str}"):
                return False
        
        # Push
        if not self.git_push(push_tags=is_major):
            return False
        
        print("\n" + "="*60)
        print("  Release Complete!")
        print("="*60)
        print(f"  Version: {new_version_str}")
        if is_major:
            print(f"  Release: Created with tag v{new_version_str}")
        print("="*60 + "\n")
        
        return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Fearn Build Script")
        print("\nUsage: python3 fearn_build.py [command] [options]")
        print("\nCommands:")
        print("  push-patch <description>  - Push minor bugfix (v+0.0.1)")
        print("  push-major <description>  - Push major bugfix (v+0.70) with release")
        print("\nExamples:")
        print("  python3 fearn_build.py push-patch 'Fixed crash on startup'")
        print("  python3 fearn_build.py push-major 'Fixed critical security issue'")
        sys.exit(1)
    
    manager = BuildManager()
    command = sys.argv[1]
    
    if command == 'push-patch' and len(sys.argv) > 2:
        description = ' '.join(sys.argv[2:])
        success = manager.push_bugfix(description, is_major=False)
        sys.exit(0 if success else 1)
    elif command == 'push-major' and len(sys.argv) > 2:
        description = ' '.join(sys.argv[2:])
        success = manager.push_bugfix(description, is_major=True)
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
