"""ARC-P13-8: assemble paper/zenodo/ — H GeoTIFFs, stage5 result tables, figure code, README.
Builds the folder and writes MANIFEST.txt with sizes and sha256. Uploads nothing.
"""
import hashlib, os, shutil, pathlib

ROOT = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
Z = ROOT / "paper" / "zenodo"
for sub in ("products", "tables", "code"):
    (Z / sub).mkdir(parents=True, exist_ok=True)

copied = []

# 1. gridded H products
for f in sorted((ROOT / "data" / "products").glob("*.tif")):
    dst = Z / "products" / f.name
    shutil.copy2(f, dst); copied.append(dst)

# 2. stage5 result tables (CSV) and the result documents that describe them
for f in sorted((ROOT / "stage5").rglob("*")):
    if f.is_file() and f.suffix in (".csv", ".md"):
        dst = Z / "tables" / f"{f.parent.name}_{f.name}" if f.parent.name != "stage5" else Z / "tables" / f.name
        shutil.copy2(f, dst); copied.append(dst)

# 3. figure code, including the helpers it imports
CODE = [ROOT / "scratch/P9/p10_figs.py",
        ROOT / "scratch/P13/p13_fig03.py",
        ROOT / "scratch/P13/p13_graphical_abstract.py",
        ROOT / "scratch/P3/cells.py",
        ROOT / "scratch/P2/regions.py",
        ROOT / "scratch/P13/bib.py",
        ROOT / "scratch/P13/render_refs.py",
        ROOT / "scratch/P13/make_rse.py",
        ROOT / "scratch/P13/p13_zenodo.py"]
for f in CODE:
    if f.exists():
        dst = Z / "code" / f.name
        shutil.copy2(f, dst); copied.append(dst)

# manifest
lines, total = [], 0
for f in sorted(copied):
    n = f.stat().st_size; total += n
    h = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
    lines.append(f"{n:>10}  {h}  {f.relative_to(Z)}")
(Z / "MANIFEST.txt").write_text(
    "ARC-P13-8 Zenodo deposit manifest\n"
    "size (bytes)  sha256 (first 16 hex)  path relative to paper/zenodo/\n"
    + "-" * 78 + "\n" + "\n".join(lines)
    + f"\n{'-'*78}\n{len(lines)} files, {total} bytes ({total/1048576:.2f} MiB)\n")
print(f"{len(lines)} files, {total/1048576:.2f} MiB")
for sub in ("products", "tables", "code"):
    fs = list((Z / sub).iterdir())
    print(f"  {sub:9s} {len(fs):3d} files  {sum(f.stat().st_size for f in fs)/1048576:6.2f} MiB")
