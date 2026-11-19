"""Merge the per-sample SQANTI-browser hubs in hubs/* into one hub, zfand2b_hub/.
Groups: FLAIR filtered (open), FLAIR unfiltered (open), TAMA per-sample unfiltered (closed).
Every track is labelled with its tool, age, sample and filter state. Run from mouse_zfand2b/."""
import os, re, shutil
order = ["Young_B31", "Young_B32", "Young_B33", "Young_B34", "Young_B35",
         "Old_B151", "Old_B152", "Old_B153", "Old_B154"]
out = "zfand2b_hub"; shutil.rmtree(out, ignore_errors=True); os.makedirs(f"{out}/mm39")
open(f"{out}/hub.txt", "w").write(
    "hub Zfand2b_mouse_brain\nshortLabel Zfand2b young vs old\n"
    "longLabel SQANTI-browser: Zfand2b locus, FLAIR merged (per-sample FL) and TAMA per-sample, 5 young and 4 old mouse brains\n"
    "genomesFile genomes.txt\nemail sqanti3_user@users.noreply.github.com\ndescriptionUrl README.md\n")
open(f"{out}/genomes.txt", "w").write("genome mm39\ntrackDb mm39/trackDb.txt\ngroups mm39/groups.txt\n")
open(f"{out}/mm39/groups.txt", "w").write(
    "name flair_filtered\nlabel FLAIR filtered (CAGE<=50bp, FL>=2, canonical, no RTS, no NMD)\npriority 1\ndefaultIsClosed 0\n\n"
    "name flair_unfiltered\nlabel FLAIR unfiltered\npriority 2\ndefaultIsClosed 0\n\n"
    "name tama\nlabel TAMA per-sample, unfiltered\npriority 3\ndefaultIsClosed 1\n")
shutil.copy("README.md", f"{out}/README.md")
ABBR = {"full-splice_match": "FSM", "incomplete-splice_match": "ISM", "novel_in_catalog": "NIC",
        "novel_not_in_catalog": "NNC"}
plan = [(f"FLAIR_{s}_filtered", "flair_filtered", i) for i, s in enumerate(order)] + \
       [(f"FLAIR_{s}", "flair_unfiltered", i) for i, s in enumerate(order)] + \
       [(f"TAMA_{s}", "tama", i) for i, s in enumerate(order)]
blocks = []
for hub, group, i in plan:
    src = f"hubs/{hub}/mm39"
    shutil.copytree(src, f"{out}/mm39/{hub}", ignore=shutil.ignore_patterns("trackDb.txt", "groups.txt"))
    tool, age, sample = hub.split("_")[:3]; filt = hub.endswith("_filtered")
    for blk in open(f"{src}/trackDb.txt").read().strip().split("\n\n"):
        name = re.search(r"^track (\S+)", blk, re.M).group(1)
        main = name == "mm39_sqanti3"; cat = "" if main else name[len("mm39_sqanti3_"):]
        short = f"{tool} {age} {sample}{' filt' if filt else ''} {ABBR.get(cat, cat) if cat else 'all'}"
        long = f"{tool} {age} {sample} ({'filtered' if filt else 'unfiltered'}): " + (f"SQANTI3 {cat} transcripts" if cat else "all SQANTI3 transcripts")
        blk = re.sub(r"^track (\S+)", lambda m: f"track {hub}_{m.group(1)}", blk, flags=re.M)
        blk = re.sub(r"^(bigDataUrl|html|searchTrix) (\S+)", lambda m: f"{m.group(1)} {hub}/{m.group(2)}", blk, flags=re.M)
        blk = re.sub(r"^group \S+", f"group {group}", blk, flags=re.M)
        blk = re.sub(r"^priority \S+", f"priority {i + 1 + (0 if main else 0.5)}", blk, flags=re.M)
        blk = re.sub(r"^visibility \S+", f"visibility {'pack' if main and group != 'tama' else 'hide'}", blk, flags=re.M)
        blk = re.sub(r"^shortLabel .*$", f"shortLabel {short}", blk, flags=re.M)
        blk = re.sub(r"^longLabel .*$", f"longLabel {long}", blk, flags=re.M)
        blocks.append(blk)
open(f"{out}/mm39/trackDb.txt", "w").write("\n\n".join(blocks) + "\n")
print(len(blocks), "tracks ->", out)
