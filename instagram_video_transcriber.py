import os
import subprocess
from instaloader import Instaloader
import time

def login_and_save_session(username, password):
    """Login and save session file."""
    L = Instaloader()
    session_file = f"session-{username}"
    try:
        L.load_session_from_file(username, session_file)
        print("Session loaded.")
        return True  # Session loaded, no need to log in
    except FileNotFoundError:
        print("No session file found. Logging in...")
        L.login(username, password)
        L.save_session_to_file(session_file)
        print("Session saved.")
        return False  # Session created

def download_saved_posts_cli(username, session_loaded):
    """Use CLI to download saved posts."""
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print("Downloading one saved post...")
    command = [
        "instaloader",
        "--dirname-pattern", "downloads",
        ":saved"
    ]
    if not session_loaded:
        command.insert(1, "--login")
        command.insert(2, username)

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during download: {result.stderr}")
        print("If this is a rate limit issue, please wait and try again later.")
    else:
        print("Downloaded saved posts.")
        time.sleep(60)  # Delay to avoid rate limits

def main():
    username = input("Enter Instagram username: ")
    password = input("Enter Instagram password: ")

    try:
        # Login and save session
        session_loaded = login_and_save_session(username, password)

        # Download saved posts using CLI
        download_saved_posts_cli(username, session_loaded)

        print("Check the 'downloads' folder for saved posts.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
