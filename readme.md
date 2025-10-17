Repository: HHA504

What I changed
- Removed two large video files from history:
  - `504_serverless_functions/zoom/Severless_part1.mp4` (~75.5 MB)
  - `504_serverless_functions/zoom/Severless_part2.mp4` (~106.3 MB)
- Rewrote local history to drop the blobs and ran garbage collection.
- Force-pushed the cleaned history to `origin/main` (as requested).

Why
- GitHub rejects files larger than 100 MB and recommends staying below 50 MB. The second file exceeded 100 MB and prevented pushes.

How to verify
1. Check the remote main ref from your machine:

```powershell
git ls-remote origin refs/heads/main
```

2. Compare local and remote SHAs:

```powershell
git fetch origin
git rev-parse --short HEAD
git rev-parse --short origin/main
```

3. Confirm the large files are no longer in history:

```powershell
git rev-list --objects --all | findstr /I "Severless_part"
```

Optional: Keep the videos with Git LFS
- If you want to retain the large media files in the repository, use Git LFS. Example steps:

```powershell
# install git-lfs from https://git-lfs.github.com/ or using your package manager
git lfs install
git lfs track "504_serverless_functions/zoom/*.mp4"
# recommit large files (after adding them back to the working tree)
git add .gitattributes
git add 504_serverless_functions/zoom/Severless_part1.mp4
git add 504_serverless_functions/zoom/Severless_part2.mp4
git commit -m "Add videos tracked by LFS"
git push origin main
```

Notes and warnings
- Rewriting history changes commit SHAs. Any collaborators who pulled before the rewrite will need to re-clone or reset their local branches to avoid conflicts.
- If you did not intend to force-push or want the rewrite reversed, contact repository collaborators and/or restore from a backup before proceeding.

Contact
- If you want me to also add the videos back using Git LFS or push a separate branch with the video files, tell me and I will do it.
