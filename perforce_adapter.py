import os
import subprocess
import logging
from typing import List, Dict, Any
from base_engine import AbstractVCSProvider

logger = logging.getLogger("VCSBridgeCore")

class PerforceProvider(AbstractVCSProvider):
    """
    Perforce Helix Core (P4) server implementation utilizing workspace mapping rules.
    """
    def initialize_repository(self) -> bool:
        try:
            os.environ["P4PORT"] = self.remote_url
            os.environ["P4USER"] = self.auth_creds.get("username", "")
            if "password" in self.auth_creds:
                os.environ["P4PASSWD"] = self.auth_creds["password"]

            cmd = ["p4", "sync", "..."]
            subprocess.run(cmd, cwd=self.local_path, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Perforce client syncing fatal loop: {e.stderr}")
            return False

    def fetch_latest_changes(self) -> List[Dict[str, Any]]:
        try:
            cmd = ["p4", "changes", "-m", "10", "..."]
            result = subprocess.run(cmd, cwd=self.local_path, capture_output=True, text=True, check=True)
            
            changesets = []
            for line in result.stdout.strip().split("\n"):
                if not line: continue
                parts = line.split(" ", 6)
                if len(parts) >= 6:
                    changesets.append({"id": parts[1], "author": parts[3], "timestamp": parts[5], "message": parts[6].strip("'")})
            return changesets
        except subprocess.CalledProcessError:
            return []

    def push_changeset(self, commit_metadata: Dict[str, Any]) -> bool:
        try:
            subprocess.run(["p4", "reconcile", "..."], cwd=self.local_path, check=True, capture_output=True)
            desc = commit_metadata.get("message", "Automated Git-to-P4 Gateway Sync")
            spec = f"Change:\tnew\nDescription:\n\t{desc}\nFiles:\n"
            
            p = subprocess.Popen(["p4", "change", "-i"], cwd=self.local_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = p.communicate(input=spec)
            
            if p.returncode != 0:
                return False
                
            cl_id = "".join(filter(str.isdigit, stdout))
            subprocess.run(["p4", "submit", "-c", cl_id], cwd=self.local_path, capture_output=True, text=True, check=True)
            return True
        except Exception as e:
            logger.error(f"Perforce execution exception workflow failure: {str(e)}")
            return False
