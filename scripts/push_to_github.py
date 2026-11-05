import sys
import os
from dulwich.repo import Repo
from dulwich.porcelain import push

repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
r = Repo(repo_path)

token = os.getenv("GITHUB_TOKEN")
if len(sys.argv) > 1:
    token = sys.argv[1]

if not token:
    print("Usage: python scripts/push_to_github.py <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>")
    print("Or set GITHUB_TOKEN environment variable.")
    sys.exit(1)

remote_url = f"https://ProgrammerNishit67:{token}@github.com/ProgrammerNishit67/quickcommerce-intelligence.git"

print("Pushing repository to GitHub...")
try:
    push(r, remote_url, refspecs=[b"refs/heads/master:refs/heads/main"])
    print("Push succeeded! Your project is now on GitHub.")
except Exception as e:
    # Try pushing directly to master if main fails
    try:
        push(r, remote_url, refspecs=[b"refs/heads/master:refs/heads/master"])
        print("Push succeeded to master! Your project is now on GitHub.")
    except Exception as e2:
        print("Push error:", e2)
