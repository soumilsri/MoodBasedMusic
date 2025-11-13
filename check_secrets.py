#!/usr/bin/env python3
"""
Security Check Script
Checks for accidentally committed API keys or secrets before Git commit
"""

import os
import re
import sys

# Patterns that might indicate API keys
SUSPICIOUS_PATTERNS = [
    r'AIzaSy[A-Za-z0-9_-]{35}',  # Google API keys
    r'sk-[A-Za-z0-9]{32,}',      # OpenAI/other API keys
    r'[A-Za-z0-9]{32,}',          # Long alphanumeric strings (potential keys)
]

# Files to check
FILES_TO_CHECK = [
    'app.py',
    'mood_music_app.py',
    '*.py',
]

# Files to exclude
EXCLUDE_FILES = [
    '.env',
    '.git',
    '__pycache__',
    'venv',
    'env',
    '.env.example',
    'check_secrets.py',
]

def check_file(filepath):
    """Check a single file for suspicious patterns"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for i, line in enumerate(content.split('\n'), 1):
                for pattern in SUSPICIOUS_PATTERNS:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        # Check if it's in a comment or string (might be example)
                        if 'example' in line.lower() or 'your_' in line.lower():
                            continue
                        issues.append({
                            'file': filepath,
                            'line': i,
                            'pattern': pattern,
                            'match': match.group()[:20] + '...' if len(match.group()) > 20 else match.group()
                        })
    except Exception as e:
        pass
    return issues

def main():
    """Main function"""
    print("=" * 60)
    print("Security Check - Scanning for exposed API keys...")
    print("=" * 60)
    print()
    
    issues = []
    
    # Check .env file exists and is not empty (should be gitignored)
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'AIzaSy' in content or 'your_' not in content.lower():
                print("WARNING: .env file contains actual API keys!")
                print("   Make sure .env is in .gitignore")
                print()
    
    # Check Python files
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FILES]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if any(exclude in filepath for exclude in EXCLUDE_FILES):
                    continue
                file_issues = check_file(filepath)
                issues.extend(file_issues)
    
    # Report results
    if issues:
        print("POTENTIAL SECURITY ISSUES FOUND:")
        print()
        for issue in issues:
            print(f"  File: {issue['file']}")
            print(f"  Line: {issue['line']}")
            print(f"  Pattern: {issue['match']}")
            print()
        print("=" * 60)
        print("DO NOT COMMIT until these are resolved!")
        print("=" * 60)
        return 1
    else:
        print("No exposed API keys found in source files!")
        print()
        print("Safe to commit!")
        return 0

if __name__ == '__main__':
    sys.exit(main())

