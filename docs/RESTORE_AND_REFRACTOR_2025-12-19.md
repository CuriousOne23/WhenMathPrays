# Repository Restore and Refactor Guide (2025-12-19)

## Overview
This document summarizes the process used to restore the local repository to a previous stable state (from late last night), and how to make that state the current version on GitHub for the `phase3` branch. It also covers best practices for safe restoration and force-pushing to a remote branch.

---

## Steps to Restore Local Repository to a Previous Commit

1. **View Recent Commits:**
   ```sh
   git log --since='1 day ago' --oneline
   ```
   Identify the commit hash from the desired point in history (e.g., `5203be4`).

2. **Check for Uncommitted Changes:**
   ```sh
   git status
   ```
   If you have uncommitted changes, stash them:
   ```sh
   git stash push -m "backup before restore"
   ```

3. **Checkout the Target Commit:**
   ```sh
   git checkout <commit-hash>
   # Example:
   git checkout 5203be4
   ```
   This puts you in a detached HEAD state at the chosen commit.

4. **Switch to the Target Branch:**
   ```sh
   git switch phase3
   ```

5. **Reset the Branch to the Desired Commit:**
   ```sh
   git reset --hard <commit-hash>
   # Example:
   git reset --hard 5203be4
   ```

---

## Force-Push Local State to GitHub

1. **Push the Local Branch to GitHub (Overwriting Remote):**
   ```sh
   git push origin phase3 --force
   ```
   This will make the remote `phase3` branch match your local repository exactly.

**Warning:** This will overwrite the remote branch history. Only use `--force` if you are sure this is what you want.

---

## Additional Notes
- Your previous changes are safely stashed and can be reapplied with `git stash pop` if needed.
- After force-pushing, collaborators should re-clone or reset their local branches to avoid conflicts.
- Always communicate with your team before force-pushing shared branches.

---

*Document generated on 2025-12-19 by GitHub Copilot (GPT-4.1)*
