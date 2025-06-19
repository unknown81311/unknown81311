# generate_svg.py
import os
import svgwrite
from github import Github

# Get GitHub username from environment variable
github_username = os.getenv("GITHUB_ACTOR", "Unknown User")

# Authenticate with GitHub API using token
github_token = os.getenv("GITHUB_TOKEN")
g = Github(github_token)
user = g.get_user()

# Calculate total stars, commits, PRs, issues
total_stars = 0
total_commits = 0
total_prs = 0
total_issues = 0

for repo in user.get_repos():
    total_stars += repo.stargazers_count
    if repo.owner.login == github_username:
        total_commits += repo.get_commits(author=github_username).totalCount
        total_prs += repo.get_pulls(state='all').totalCount
        total_issues += repo.get_issues(state='all').totalCount

# Create SVG
svg = svgwrite.Drawing(filename="github_username.svg", size=(600, 200))
svg.add(svg.text(f"GitHub User: {github_username}", insert=(10, 30), fill="black", font_size="20"))
svg.add(svg.text(f"Total Stars Earned: {total_stars}", insert=(10, 60), fill="black", font_size="16"))
svg.add(svg.text(f"Total Commits (as of 2025): {total_commits}", insert=(10, 90), fill="black", font_size="16"))
svg.add(svg.text(f"Total PRs: {total_prs}", insert=(10, 120), fill="black", font_size="16"))
svg.add(svg.text(f"Total Issues: {total_issues}", insert=(10, 150), fill="black", font_size="16"))
svg.save()

print("SVG created with GitHub stats.")
