import sys
import os
import json
import urllib.request
import urllib.error
from dulwich.repo import Repo
from dulwich.porcelain import push

def auto_publish(token: str):
    username = "ProgrammerNishit67"
    repo_name = "quickcommerce-intelligence"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "QuickCommerce-Intelligence-Publisher",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    print("Step 1: Checking / creating repository on GitHub...")
    # Check if repo exists
    repo_exists = False
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{username}/{repo_name}", headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                repo_exists = True
                print(f"Repository {username}/{repo_name} already exists.")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Repository {username}/{repo_name} does not exist yet. Creating...")
        else:
            print(f"GitHub API Error: {e.code} - {e.reason}")

    # Create if not exists
    if not repo_exists:
        create_payload = json.dumps({
            "name": repo_name,
            "description": "QuickCommerce Intelligence - End-to-End Quick Commerce Operations Analytics Platform (Blinkit / Zepto / Swiggy Instamart)",
            "private": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": False
        }).encode("utf-8")

        req = urllib.request.Request("https://api.github.com/user/repos", data=create_payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as res:
                print("Successfully created repository on GitHub!")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            print(f"Failed to create repository: {e.code} {err_body}")
            return False

    print("\nStep 2: Pushing all project code and commits to GitHub...")
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    r = Repo(repo_path)
    remote_auth_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

    try:
        # Push master branch to main on GitHub
        push(r, remote_auth_url, refspecs=[b"refs/heads/master:refs/heads/main"])
        print("Successfully pushed to 'main' branch on GitHub!")
    except Exception as e:
        print(f"Push to main encountered: {e}. Retrying to master...")
        try:
            push(r, remote_auth_url, refspecs=[b"refs/heads/master:refs/heads/master"])
            print("Successfully pushed to 'master' branch on GitHub!")
        except Exception as e2:
            print("Push failed:", e2)
            return False

    print("\nStep 3: Enabling GitHub Pages...")
    pages_payload = json.dumps({
        "build_type": "workflow"
    }).encode("utf-8")

    req = urllib.request.Request(
        f"https://api.github.com/repos/{username}/{repo_name}/pages",
        data=pages_payload,
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            print("GitHub Pages successfully enabled with GitHub Actions!")
    except urllib.error.HTTPError as e:
        # 409 means Pages is already enabled or queued
        if e.code == 409:
            print("GitHub Pages already enabled.")
        else:
            print(f"Pages configuration note ({e.code}): Will be handled automatically by the workflow.")

    print(f"\nSUCCESS! Project is published and live at:")
    print(f"Repository: https://github.com/{username}/{repo_name}")
    print(f"Live Site:  https://{username}.github.io/{repo_name}/")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/auto_publish.py <GITHUB_TOKEN>")
        sys.exit(1)
    auto_publish(sys.argv[1].strip())
