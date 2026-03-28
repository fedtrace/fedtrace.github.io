"""Shared helpers for Colab notebooks in this repo."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

REPO_URL = "https://github.com/fedtrace/fedtrace.github.io.git"
DEFAULT_REPO_DIR = Path("/content/fedtrace.github.io")
NOTEBOOK_DEPS_SENTINEL_VERSION = "v1"


def bootstrap_colab_repo(
    repo_dir: str | Path = DEFAULT_REPO_DIR,
    repo_url: str = REPO_URL,
) -> Path:
    """Clone the repo into the Colab workspace if needed."""
    repo_path = Path(repo_dir)
    if not repo_path.exists():
        repo_path.parent.mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"}
        subprocess.run(
            ["git", "clone", "--depth=1", repo_url, str(repo_path)],
            check=True, env=env,
        )

    if str(repo_path) not in sys.path:
        sys.path.insert(0, str(repo_path))

    os.chdir(repo_path)
    return repo_path


def get_repo_paths(repo_root: str | Path = DEFAULT_REPO_DIR) -> dict[str, Path]:
    """Return canonical paths used across notebooks."""
    repo_path = Path(repo_root)
    return {
        "repo_root": repo_path,
        "notebooks_dir": repo_path / "notebooks",
        "scripts_dir": repo_path / "scripts",
        "data_root": repo_path / "data",
        "raw_dir": repo_path / "data" / "raw",
        "outputs_dir": repo_path / "data" / "outputs",
    }


def prepare_notebook(
    repo_root: str | Path = DEFAULT_REPO_DIR,
    *,
    pull_latest: bool = False,
) -> tuple[Path, dict[str, Path]]:
    """Bootstrap the repo and optionally pull latest main."""
    repo_path = bootstrap_colab_repo(repo_root)

    if pull_latest:
        try:
            from google.colab import userdata
            token = userdata.get("GITHUB_TOKEN_FEDTRACE")
        except Exception:
            token = None

        if token:
            authed_url = f"https://x-access-token:{token}@github.com/fedtrace/fedtrace.github.io.git"
            subprocess.run(["git", "remote", "set-url", "origin", authed_url], check=True, cwd=repo_path)
            # Shallow clones can't push; unshallow before any pull that may be followed by push.
            if (repo_path / ".git" / "shallow").exists():
                subprocess.run(["git", "fetch", "--unshallow", "origin", "main"], check=True, cwd=repo_path)

        try:
            subprocess.run(["git", "pull", "origin", "main"], check=True, cwd=repo_path)
        except subprocess.CalledProcessError:
            print("Warning: git pull failed — continuing with local repo state.")

    return repo_path, get_repo_paths(repo_path)


def ensure_notebook_requirements(
    notebook_name: str,
    *,
    requirements_path: str | Path = "../requirements.txt",
) -> None:
    """Install notebook dependencies once per session and restart runtime.

    The runtime restart ensures packages load against correct binaries.
    Without this, imports can silently fail on Colab after pip upgrades.
    """
    sentinel = Path(f"/tmp/fedtrace_{notebook_name}_deps_{NOTEBOOK_DEPS_SENTINEL_VERSION}")
    if sentinel.exists():
        print(f"Dependencies ready for {notebook_name}.")
        return

    subprocess.run(
        [
            sys.executable, "-m", "pip", "install", "-q", "-U",
            "--upgrade-strategy", "only-if-needed",
            "-r", str(requirements_path),
        ],
        check=True,
    )
    sentinel.write_text("ok")
    print("Dependencies updated. Restarting runtime...")
    os.kill(os.getpid(), 9)


def publish_artifacts(
    paths: Iterable[str | Path],
    message: str,
    repo_dir: str | Path = DEFAULT_REPO_DIR,
    dry_run: bool = False,
) -> bool:
    """Commit and push generated artifacts from Colab back to GitHub.

    Requires a Colab secret named ``GITHUB_TOKEN_FEDTRACE`` with write access
    to the fedtrace org. Add it via the key icon in the Colab left sidebar.

    Returns True when a commit was created and pushed.
    """
    try:
        from google.colab import userdata
    except ImportError as exc:
        raise RuntimeError("publish_artifacts only works from Google Colab.") from exc

    token = userdata.get("GITHUB_TOKEN_FEDTRACE")
    if not token:
        raise RuntimeError(
            "Missing Colab secret GITHUB_TOKEN_FEDTRACE. "
            "Add it via the key icon in the Colab left sidebar."
        )

    repo_path = Path(repo_dir)
    rel_paths = [str(Path(p)) for p in paths]

    missing = [p for p in rel_paths if not (repo_path / p).exists()]
    if missing:
        raise FileNotFoundError(
            "Cannot publish — files not found: " + ", ".join(missing)
        )

    repo_url = f"https://x-access-token:{token}@github.com/fedtrace/fedtrace.github.io.git"

    subprocess.run(["git", "config", "user.email", "noreply@anthropic.com"], check=True, cwd=repo_path)
    subprocess.run(["git", "config", "user.name", "Claude"], check=True, cwd=repo_path)
    subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True, cwd=repo_path)

    # Shallow clones can't push; unshallow if needed.
    if (repo_path / ".git" / "shallow").exists():
        subprocess.run(["git", "fetch", "--unshallow", "origin", "main"], check=True, cwd=repo_path)

    try:
        subprocess.run(["git", "pull", "--ff-only", "origin", "main"], check=True, cwd=repo_path)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "git pull --ff-only failed before publishing — remote has diverged. "
            "Re-run prepare_notebook(pull_latest=True) and retry."
        ) from exc

    subprocess.run(["git", "add", "--", *rel_paths], check=True, cwd=repo_path)

    # git diff --cached misses brand-new files with no HEAD entry; use status instead
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", *rel_paths],
        cwd=repo_path, capture_output=True, text=True, check=True,
    )
    staged = [l for l in status.stdout.splitlines() if l and l[0] not in (" ", "?")]
    if not staged:
        print("No artifact changes to commit.")
        return False

    if dry_run:
        print(f"[dry_run] Would commit: {', '.join(rel_paths)}")
        print(f"[dry_run] Message: {message}")
        return False

    subprocess.run(["git", "commit", "-m", message], check=True, cwd=repo_path)

    push = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=repo_path, capture_output=True, text=True,
    )
    if push.returncode != 0:
        raise RuntimeError(
            f"git push failed (exit {push.returncode}):\n"
            + (push.stderr or push.stdout)
        )
    print(f"Pushed: {', '.join(rel_paths)}")
    return True
