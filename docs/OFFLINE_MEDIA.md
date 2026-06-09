# Offline media and large binaries

Large audio, video, PDF, and generated plot assets were **removed from git** to keep clone size small for active development.

## What stayed in the repo

- Markdown scores, prompts, and music subsystem docs under `docs/music/` (except `audio/`)
- All narrative `.md` papers and architecture docs
- Source code, tests, and small CSV trajectory samples in `results/`

## What moved offline

| Former path | Contents | Approx. size |
|-------------|----------|--------------|
| `docs/music/audio/` | MP3 score renders | ~110 MB |
| `docs/videos/` | MP4 section videos | ~43 MB |
| `docs/Other_papers/` | Reference PDFs | ~54 MB |
| `core/revenge_pdf.npz` | Revenge PDF grid cache | ~11 MB (regenerated on first `revenge_core` use) |
| `results/*.png` | Scenario plot outputs | regenerable via `simulations/` |
| `tests/revenge/*.png` | Test plot outputs | regenerable via `tests/revenge/` |

## Restore locally

- **revenge grid:** run any script that imports `core.revenge_core` — it regenerates `core/revenge_pdf.npz` automatically.
- **scenario plots:** run scenarios under `simulations/` or `tests/run_all_scenarios.py`.
- **revenge test plots:** run scripts in `tests/revenge/`.
- **MP3/MP4/PDF:** restore from your pre-cleanup backup, release bundle, or cloud copy if you still need them for presentation.

## Policy

Do not commit MP3, MP4, PDF, NPZ, or generated PNG artifacts to this repository. Use external storage or release assets instead.