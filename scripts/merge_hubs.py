"""Merge per-sample SQANTI-browser hubs (hubs/*) into one hub (top500_hub).
Track names get the sample prefix; files go to mm39/<hub>/. Run from locus_hub/."""
import os, re, shutil
order = ["Young_B31", "Young_B32", "Young_B33", "Young_B34", "Young_B35",
         "Old_B151", "Old_B152", "Old_B153", "Old_B154"]
out = "top500_hub"; shutil.rmtree(out, ignore_errors=True); os.makedirs(f"{out}/mm39")
open(f"{out}/hub.txt", "w").write(
    "hub Pool1_top500_mouse_brain\nshortLabel Top500 young vs old\n"
    "longLabel SQANTI-browser: top 500 pool1 genes (old-young noisy ratio), 5 young and 4 old mouse brains\n"
    "genomesFile genomes.txt\nemail sqanti3_user@users.noreply.github.com\ndescriptionUrl README.md\n")
open(f"{out}/genomes.txt", "w").write("genome mm39\ntrackDb mm39/trackDb.txt\ngroups mm39/groups.txt\n")
open(f"{out}/mm39/groups.txt", "w").write(
    "name filtered\nlabel Top500 filtered (CAGE<=50bp, FL>=2, canonical, no RTS, no NMD)\npriority 1\ndefaultIsClosed 0\n\n"
    "name unfiltered\nlabel Top500 unfiltered\npriority 2\ndefaultIsClosed 0\n\n"
    "name merged\nlabel Merged transcriptome (all samples, no FL)\npriority 3\ndefaultIsClosed 1\n")
shutil.copy("hubs/Old_B151/README.md", f"{out}/README.md")
plan = [(f"{s}_filtered", "filtered", i) for i, s in enumerate(order)] + \
       [(s, "unfiltered", i) for i, s in enumerate(order)] + [("Merged", "merged", 0)]
blocks = []
ABBR = {"full-splice_match": "FSM", "incomplete-splice_match": "ISM", "novel_in_catalog": "NIC",
        "novel_not_in_catalog": "NNC", "antisense": "antisense", "genic": "genic", "fusion": "fusion",
        "intergenic": "intergenic", "genic_intron": "genic_intron"}
def labels(hub, name):
    tag = hub.replace("_filtered", "").replace("_", " ") + (" filt" if hub.endswith("_filtered") else "")
    long_tag = hub.replace("_filtered", "").replace("_", " ") + (" (filtered)" if hub.endswith("_filtered") else " (unfiltered)")
    cat = name[len("mm39_sqanti3_"):] if name != "mm39_sqanti3" else ""
    short = f"{tag} {ABBR.get(cat, cat)}".strip() if cat else f"{tag} all"
    long = f"{long_tag}: SQANTI3 {cat} transcripts" if cat else f"{long_tag}: all SQANTI3 transcripts"
    return short, long
for hub, group, i in plan:
    src = f"hubs/{hub}/mm39"
    shutil.copytree(src, f"{out}/mm39/{hub}", ignore=shutil.ignore_patterns("trackDb.txt", "groups.txt"))
    for blk in open(f"{src}/trackDb.txt").read().strip().split("\n\n"):
        name = re.search(r"^track (\S+)", blk, re.M).group(1)
        main = name == "mm39_sqanti3"
        blk = re.sub(r"^track (\S+)", lambda m: f"track {hub}_{m.group(1)}", blk, flags=re.M)
        blk = re.sub(r"^(bigDataUrl|html|searchTrix) (\S+)", lambda m: f"{m.group(1)} {hub}/{m.group(2)}", blk, flags=re.M)
        blk = re.sub(r"^group \S+", f"group {group}", blk, flags=re.M)
        blk = re.sub(r"^priority \S+", f"priority {i + 1 + (0 if main else 0.5)}", blk, flags=re.M)
        blk = re.sub(r"^visibility \S+", f"visibility {'pack' if main and group != 'merged' else 'hide'}", blk, flags=re.M)
        short, long = labels(hub, name)
        blk = re.sub(r"^shortLabel .*$", f"shortLabel {short}", blk, flags=re.M)
        blk = re.sub(r"^longLabel .*$", f"longLabel {long}", blk, flags=re.M)
        blocks.append(blk)
open(f"{out}/mm39/trackDb.txt", "w").write("\n\n".join(blocks) + "\n")
print(len(blocks), "tracks ->", out)
