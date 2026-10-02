import subprocess
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from base_engine import AbstractVCSProvider, VCSProviderException

logger = logging.getLogger("VCSBridgeCore")

class SVNProvider(AbstractVCSProvider):
    """
    Subversion (SVN) bridge implementation using native command line interface pipelines.
    """
    def initialize_repository(self) -> bool:
        try:
            logger.info(f"Checking out SVN repository from {self.remote_url} into {self.local_path}")
            cmd = ["svn", "checkout", self.remote_url, self.local_path, "--non-interactive"]
            if "username" in self.auth_creds:
                cmd.extend(["--username", self.auth_creds["username"], "--password", self.auth_creds.get("password", "")])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            raise VCSProviderException(f"SVN initialization failed: {e.stderr}")

    def fetch_latest_changes(self) -> List[Dict[str, Any]]:
        try:
            logger.info("Fetching incoming changes via 'svn log --xml'...")
            cmd = ["svn", "log", self.local_path, "--revision", "HEAD:1", "--limit", "10", "--xml"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            changesets = []
            root = ET.fromstring(result.stdout)
            for logentry in root.findall("logentry"):
                changesets.append({
                    "id": logentry.get("revision"),
                    "author": logentry.find("author").text if logentry.find("author") is not None else "Unknown",
                    "timestamp": logentry.find("date").text if logentry.find("date") is not None else "",
                    "message": logentry.find("msg").text.strip() if logentry.find("msg") is not None else ""
                })
            return changesets
        except Exception as e:
            logger.error(f"Failed to parse SVN historical logs: {str(e)}")
            return []

    def push_changeset(self, commit_metadata: Dict[str, Any]) -> bool:
        try:
            subprocess.run(["svn", "add", "--force", "."], cwd=self.local_path, check=True, capture_output=True)
            cmd = ["svn", "commit", "-m", commit_metadata.get("message", "Sync from Git Bridge"), "--non-interactive"]
            if "username" in self.auth_creds:
                cmd.extend(["--username", self.auth_creds["username"], "--password", self.auth_creds.get("password", "")])
            
            result = subprocess.run(cmd, cwd=self.local_path, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"SVN structural commit failed: {e.stderr}")
            return False
