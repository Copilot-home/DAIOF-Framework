import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger("GitHubWorker")

class GitHubWorker:
    """
    Worker service for GitHub operations.
    Acts as the 'best worker' for repository management and sync.
    """

    @staticmethod
    async def execute(action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "list_repos":
            return await GitHubWorker._list_repos()
        elif action == "sync_logic":
            return await GitHubWorker._sync_logic(payload)
        elif action == "audit_repo":
            return await GitHubWorker._audit_repo(payload.get("repo", ""))
        else:
            raise ValueError(f"Unknown GitHub action: {action}")

    @staticmethod
    async def _list_repos() -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ["gh", "repo", "list", "NguyenCuong1989", "--limit", "100", "--json", "name,url,updatedAt"],
                capture_output=True, text=True, check=True
            )
            import json
            repos = json.loads(result.stdout)
            return {"status": "success", "count": len(repos), "repos": repos}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def _sync_logic(payload: Dict[str, Any]) -> Dict[str, Any]:
        # Reuse the synaptic_orchestrator logic but as a service call
        repo = payload.get("repo")
        logger.info(f"🔄 Syncing logic for {repo}")
        # In a real scenario, this would trigger the synaptic_orchestrator script
        return {"status": "success", "repo": repo, "synced": True}

    @staticmethod
    async def _audit_repo(repo: str) -> Dict[str, Any]:
        logger.info(f"🔍 Auditing {repo}")
        # Simulated audit logic
        return {"status": "success", "repo": repo, "health_score": 0.95}
