#!/usr/bin/env python3
"""
Unit tests for Git Changelog Generator
"""

import unittest
from changelog import categorize_commit, generate_markdown

class TestChangelogGenerator(unittest.TestCase):

    def test_categorize_conventional_commits(self):
        # Added
        cat, msg = categorize_commit("feat: implement dark mode toggle")
        self.assertEqual(cat, "Added")
        self.assertEqual(msg, "implement dark mode toggle")

        cat, msg = categorize_commit("feat(auth)!: add OAuth2 login flow")
        self.assertEqual(cat, "Added")
        self.assertEqual(msg, "add OAuth2 login flow")

        # Fixed
        cat, msg = categorize_commit("fix: resolve null pointer in user session")
        self.assertEqual(cat, "Fixed")
        self.assertEqual(msg, "resolve null pointer in user session")

        cat, msg = categorize_commit("hotfix(cache): invalidate stale keys on delete")
        self.assertEqual(cat, "Fixed")
        self.assertEqual(msg, "invalidate stale keys on delete")

        # Changed
        cat, msg = categorize_commit("refactor(db): rewrite connection pooling")
        self.assertEqual(cat, "Changed")
        self.assertEqual(msg, "rewrite connection pooling")

        cat, msg = categorize_commit("perf: reduce JSON serialization overhead by 40%")
        self.assertEqual(cat, "Changed")
        self.assertEqual(msg, "reduce JSON serialization overhead by 40%")

        # Removed
        cat, msg = categorize_commit("remove: drop deprecated v1 API routes")
        self.assertEqual(cat, "Removed")
        self.assertEqual(msg, "drop deprecated v1 API routes")

        cat, msg = categorize_commit("deprecate: mark legacy auth token helper")
        self.assertEqual(cat, "Removed")

        # Maintenance
        cat, msg = categorize_commit("chore: bump dependency versions")
        self.assertEqual(cat, "Maintenance")

        cat, msg = categorize_commit("docs: update README installation steps")
        self.assertEqual(cat, "Maintenance")

    def test_generate_markdown_structure(self):
        mock_commits = [
            {'hash': 'a1b2c3d', 'subject': 'feat: add stripe checkout', 'author': 'alex', 'date': '2026-10-25'},
            {'hash': 'e5f6g7h', 'subject': 'fix: handle card decline gracefully', 'author': 'sam', 'date': '2026-10-25'},
            {'hash': 'i9j0k1l', 'subject': 'remove: delete unused legacy billing hook', 'author': 'dev', 'date': '2026-10-25'}
        ]

        md = generate_markdown(mock_commits, version="v1.2.0", previous_tag="v1.1.0")
        self.assertIn("## [v1.2.0]", md)
        self.assertIn("Changes since `v1.1.0`", md)
        self.assertIn("### Added", md)
        self.assertIn("add stripe checkout", md)
        self.assertIn("### Fixed", md)
        self.assertIn("handle card decline gracefully", md)
        self.assertIn("### Removed", md)
        self.assertIn("delete unused legacy billing hook", md)

if __name__ == '__main__':
    unittest.main()
