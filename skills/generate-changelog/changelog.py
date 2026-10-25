#!/usr/bin/env python3
"""
Structured Git Changelog Generator
Parses git history since the latest tag and produces a structured CHANGELOG.md
categorized into Added, Fixed, Changed, Removed, and Maintenance adhering to Keep a Changelog.
"""

import subprocess
import sys
import re
import os
import argparse
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CATEGORIES = {
    'Added': ['feat', 'feature', 'add', 'create', 'new'],
    'Fixed': ['fix', 'bugfix', 'hotfix', 'patch', 'resolve'],
    'Changed': ['refactor', 'perf', 'change', 'update', 'modify', 'style'],
    'Removed': ['remove', 'delete', 'deprecate', 'drop', 'revert'],
    'Maintenance': ['chore', 'docs', 'test', 'ci', 'build', 'infra']
}

def run_git(args):
    try:
        res = subprocess.run(['git'] + args, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return ""

def get_latest_tag():
    out = run_git(['describe', '--tags', '--abbrev=0'])
    return out if out else None

def get_commits(since_tag=None):
    cmd = ['log', '--pretty=format:%H%x09%s%x09%an%x09%ad', '--date=short']
    if since_tag:
        cmd.append(f'{since_tag}..HEAD')
    
    raw = run_git(cmd)
    if not raw:
        return []

    commits = []
    for line in raw.split('\n'):
        parts = line.split('\t')
        if len(parts) >= 2:
            commit_hash = parts[0][:7]
            subject = parts[1]
            author = parts[2] if len(parts) > 2 else ""
            date = parts[3] if len(parts) > 3 else ""
            commits.append({
                'hash': commit_hash,
                'subject': subject,
                'author': author,
                'date': date
            })
    return commits

def categorize_commit(subject):
    m = re.match(r'^([a-zA-Z]+)(?:\([^\)]+\))?!?:?\s*(.*)$', subject)
    if m:
        prefix = m.group(1).lower()
        cleaned_msg = m.group(2).strip() or subject
        for cat, keywords in CATEGORIES.items():
            if prefix in keywords:
                return cat, cleaned_msg

    # Fallback to keyword matching in message
    sub_lower = subject.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if re.search(r'\b' + kw + r'\b', sub_lower):
                return cat, subject

    return 'Changed', subject

def generate_markdown(commits, version="Unreleased", previous_tag=None):
    today = datetime.now().strftime('%Y-%m-%d')
    sections = {cat: [] for cat in CATEGORIES.keys()}

    for c in commits:
        cat, msg = categorize_commit(c['subject'])
        sections[cat].append(f"- {msg} ([`{c['hash']}`]) by @{c['author']}")

    lines = []
    lines.append(f"## [{version}] - {today}")
    if previous_tag:
        lines.append(f"> Changes since `{previous_tag}`\n")
    else:
        lines.append("> Full project history\n")

    has_content = False
    for cat in ['Added', 'Fixed', 'Changed', 'Removed', 'Maintenance']:
        entries = sections[cat]
        if entries:
            has_content = True
            lines.append(f"### {cat}")
            lines.extend(entries)
            lines.append("")

    if not has_content:
        lines.append("- No documented changes in this range.\n")

    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate structured CHANGELOG from git history.")
    parser.add_argument('--output', '-o', default='CHANGELOG.md', help="Path to write output CHANGELOG.md")
    parser.add_argument('--version', '-v', default='Unreleased', help="Version title (e.g. v1.1.0)")
    parser.add_argument('--all', action='store_true', help="Include entire history instead of just since last tag")
    parser.add_argument('--stdout', action='store_true', help="Print directly to stdout without writing to file")

    args = parser.parse_args()

    latest_tag = None if args.all else get_latest_tag()
    commits = get_commits(since_tag=latest_tag)

    if not commits:
        print("ℹ️ No commits found for changelog range.", file=sys.stderr)
        return

    md = generate_markdown(commits, version=args.version, previous_tag=latest_tag)

    if args.stdout:
        print(md)
    else:
        # If CHANGELOG.md exists, prepend new release
        header = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).\n\n"
        existing = ""
        if os.path.exists(args.output):
            with open(args.output, 'r', encoding='utf-8') as f:
                existing = f.read()
            if existing.startswith("# Changelog"):
                # Strip initial header
                existing = re.sub(r'^# Changelog.*?\n\n', '', existing, flags=re.DOTALL)

        full_content = header + md + "\n\n" + existing.strip()
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(full_content.strip() + "\n")
        print(f"✅ Successfully wrote structured changelog to {args.output}")

if __name__ == '__main__':
    main()
