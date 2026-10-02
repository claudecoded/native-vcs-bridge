import subprocess
import logging
from typing import List, Dict, Any
from base_engine import AbstractVCSProvider, VCSProviderException

logger = logging.getLogger("VCSBridgeCore")

class MercurialProvider(AbstractVCSProvider):
    """
    Mercurial (Hg) implementation strategy managing native decentralized states.
    """
    def initialize_repository(self) -> bool:
        try:
            logger.info(f"Cloning Mercurial repository from {self.remote_url}")
            cmd = ["hg", "clone", self.remote_url, self.local_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            raise VCSProviderException(f"Mercurial clone sequence interrupted: {e.stderr}")

    def fetch_latest_changes(self) -> List[Dict[str, Any]]:
        try:
            cmd = ["hg", "log", "--template", "{node}\\|{author}\\|{date|isodate}\\|{desc}\\n", "-l", "10"]
            result = subprocess.run(cmd, cwd=self.local_path, capture_output=True, text=True, check=True)
            
            changesets = []
            for line in result.stdout.strip().split("\n"):
                if not line: continue
                parts = line.split("\\|", 3)
                if len(parts) == 4:
                    changesets.append({"id": parts[0], "author": parts[1], "timestamp": parts[2], "message": parts[3]})
            return changesets
        except subprocess.CalledProcessError as e:
            logger.error(f"Could not retrieve hg changesets: {e.stderr}")
            return []

    def push_changeset(self, commit_metadata: Dict[str, Any]) -> bool:
        try:
            subprocess.run(["hg", "addremove"], cwd=self.local_path, check=True, capture_output=True)
            commit_cmd = ["hg", "commit", "-u", commit_metadata.get("author", "Bridge"), "-m", commit_metadata.get("message", "Sync Engine Integration")]
            subprocess.run(commit_cmd, cwd=self.local_path, check=True, capture_output=True)
            subprocess.run(["hg", "push", self.remote_url], cwd=self.local_path, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Mercurial synchronization deployment failed: {e.stderr}")
            return False
