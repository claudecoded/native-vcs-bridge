import argparse
import sys
from base_engine import VCSBridgeDaemon
from svn_adapter import SVNProvider
from mercurial_adapter import MercurialProvider
from perforce_adapter import PerforceProvider

def main():
    parser = argparse.ArgumentParser(
        description="Universal VCS Bridge Engine - Connect non-Git systems to Git workflows."
    )
    parser.add_argument(
        "--provider", 
        choices=["svn", "hg", "p4"], 
        required=True, 
        help="Select the external Version Control System provider."
    )
    parser.add_argument("--remote-url", required=True, help="The remote repository service endpoint URL.")
    parser.add_argument("--local-path", required=True, help="Target local working directory directory path.")
    parser.add_argument("--git-repo", default=".", help="Path to your internal target Git tracking repository.")
    parser.add_argument("--username", help="Authentication identity credential username.")
    parser.add_argument("--password", help="Authentication identity credential secret password token.")

    args = parser.parse_args()
    creds = {"username": args.username, "password": args.password} if args.username else {}

    print(f"[+] Initializing structural bridge mapping sequence for provider: {args.provider.upper()}")
    
    if args.provider == "svn":
        provider = SVNProvider(args.remote_url, args.local_path, creds)
    elif args.provider == "hg":
        provider = MercurialProvider(args.remote_url, args.local_path, creds)
    elif args.provider == "p4":
        provider = PerforceProvider(args.remote_url, args.local_path, creds)
    else:
        print("[-] Fatal: Unsupported orchestration adapter signature framework context.")
        sys.exit(1)

    daemon = VCSBridgeDaemon(provider, args.git_repo)
    success = daemon.run_synchronization_cycle()
    
    if success:
        print("[+] Synchronization automation thread executed successfully.")
    else:
        print("[-] Critical: Interface bridging execution cycle failure encountered.")
        sys.exit(1)

if __name__ == "__main__":
    main()
