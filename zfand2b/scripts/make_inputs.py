"""Build SQANTI-browser inputs for the Zfand2b locus (chr1:75,144,500-75,149,000, + strand).

FLAIR merged transcriptome (../mouse/flair_JC): for each mouse, keep the isoforms with
FL.<sample> > 0, set FL = FL.<sample>, and write an unfiltered set and a filtered set
(paper filters). Output: input/flair_<sample>[_filtered]_{corrected.gtf,classification.txt}.
TAMA per-sample runs (../mouse/{gtf,classifications}): the transcripts overlapping the
window, unfiltered only. Output: input/tama_<sample>_*.
Paper filters: |dist_to_CAGE_peak| <= 50 (NA fails), FL >= 2, all canonical, RTS FALSE, NMD not TRUE.
Run from mouse_zfand2b/."""
import csv, re, os
CHROM, START, END = "chr1", 75144500, 75149000
S = ["B151", "B152", "B153", "B154", "B31", "B32", "B33", "B34", "B35"]
tid = re.compile(r'transcript_id "([^"]+)"')
os.makedirs("input", exist_ok=True)

def passes(r):
    d, fl = r["dist_to_CAGE_peak"], r["FL"]
    return (d not in ("NA", "") and abs(float(d)) <= 50 and fl not in ("NA", "") and int(fl) >= 2
            and r["all_canonical"] == "canonical" and r["RTS_stage"] == "FALSE" and r["predicted_NMD"] != "TRUE")

def window_gtf(gtf):
    keep, lines = set(), []
    for l in open(gtf):
        p = l.split("\t")
        if len(p) < 9 or p[0] != CHROM or p[2] == "gene": continue
        if p[2] == "transcript" and int(p[3]) <= END and int(p[4]) >= START:
            keep.add(tid.search(p[8]).group(1))
        lines.append(l)
    return keep, [l for l in lines if tid.search(l.split("\t")[8]).group(1) in keep]

def write(prefix, gtf_lines, header, rows, ids):
    with open(f"input/{prefix}_corrected.gtf", "w") as o:
        o.writelines(l for l in gtf_lines if tid.search(l.split("\t")[8]).group(1) in ids)
    with open(f"input/{prefix}_classification.txt", "w") as o:
        w = csv.DictWriter(o, header, delimiter="\t", lineterminator="\n"); w.writeheader()
        w.writerows(r for r in rows if r["isoform"] in ids)
    return len(ids)

# FLAIR merged, one set per sample
keep, gl = window_gtf("../mouse/flair_JC/merged.gtf")
with open("../mouse/flair_JC/flair_JC_classification.txt") as f:
    rd = csv.DictReader(f, delimiter="\t"); header = rd.fieldnames
    base = [r for r in rd if r["isoform"] in keep]
for s in S:
    rows = []
    for r in base:
        if int(r[f"FL.{s}"]) > 0:
            r2 = dict(r); r2["FL"] = r[f"FL.{s}"]; rows.append(r2)
    ids = {r["isoform"] for r in rows}
    n = write(f"flair_{s}", gl, header, rows, ids)
    nf = write(f"flair_{s}_filtered", gl, header, rows, {r["isoform"] for r in rows if passes(r)})
    print("flair", s, n, "isoforms,", nf, "pass")

# TAMA per-sample
for s in S:
    keep, gl = window_gtf(f"../mouse/gtf/{s}_tama_models_corrected.gtf")
    with open(f"../mouse/classifications/{s}_tama_models_classification.txt") as f:
        rd = csv.DictReader(f, delimiter="\t"); header = rd.fieldnames
        rows = [r for r in rd if r["isoform"] in keep]
    print("tama", s, write(f"tama_{s}", gl, header, rows, keep), "isoforms")
