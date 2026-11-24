# Eternal Voyage documentation

This Zensical site documents Eternal Voyage for Minecraft Java Edition 1.20.1 and Forge. The Markdown pages are in `docs/` and the navigation is in `zensical.toml`.

## Preview locally

From the project directory in PowerShell, use the existing virtual environment or create it with Python 3.12.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\zensical.exe serve --open
```

Run `.\.venv\Scripts\zensical.exe build --clean` to generate the static files in `site/`.

## Publish to GitHub Pages

1. Put the documentation project in your GitHub repository. The ignore file keeps the local `pack/` inputs, virtual environment, and generated output out of Git.
2. Open the repository’s **Settings → Pages** and select **GitHub Actions** as the source.
3. Push a documentation change to the default branch or run **Publish documentation** manually from **Actions**. The workflow builds the site, derives its canonical URL from Pages, and deploys the `site/` artifact. It supports both an account site and a repository subpath.

## Update the pack guides

Check the running world’s server settings as well as the new-world defaults. Review KubeJS loot and scripts together with the FTB quest chapters, and update the mod inventory when the shipped JARs change.

With the pack snapshot in `pack/`, refresh the quest, loot, mod, bloodline and combat references with `.\.venv\Scripts\python.exe tools/build_pack_reference.py`. Pass `--javap` with the path to Java 17’s `javap` to refresh the individual fruit, awakening, race and discipline pages, move stats, Haki tree and playable icons. GitHub Pages builds from the generated Markdown and PNGs, so the pack files can stay local.
