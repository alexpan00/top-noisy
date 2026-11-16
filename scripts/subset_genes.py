"""Subset a SQANTI3 corrected GTF + classification to transcripts whose associated_gene
is in a gene list (fusion names "A_B" match if any component is listed). Writes the
unfiltered subset and a filtered subset that passes the paper filters
(|dist_to_CAGE_peak| <= 50, FL >= 2, all canonical, RTS FALSE, NMD not TRUE).
usage: subset_genes.py GTF CLASSIFICATION GENE_LIST OUT_PREFIX"""
import sys, re
gtf, cls, genes, out = sys.argv[1:]
genes = {l.strip() for l in open(genes) if l.strip()}

def passes(r):
    d, fl = r["dist_to_CAGE_peak"], r["FL"]
    return (d not in ("NA", "") and abs(float(d)) <= 50 and fl not in ("NA", "") and int(fl) >= 2
            and r["all_canonical"] == "canonical" and r["RTS_stage"] == "FALSE" and r["predicted_NMD"] != "TRUE")

keep, keep_f = set(), set()
with open(cls) as f, open(out + "_classification.txt", "w") as o, \
        open(out + "_filtered_classification.txt", "w") as of:
    header = f.readline(); o.write(header); of.write(header)
    cols = header.rstrip("\n").split("\t")
    for l in f:
        r = dict(zip(cols, l.rstrip("\n").split("\t")))
        if genes.isdisjoint(r["associated_gene"].split("_")):
            continue
        keep.add(r["isoform"]); o.write(l)
        if passes(r):
            keep_f.add(r["isoform"]); of.write(l)

tid = re.compile(r'transcript_id "([^"]+)"')
with open(gtf) as f, open(out + "_corrected.gtf", "w") as o, \
        open(out + "_filtered_corrected.gtf", "w") as of:
    for l in f:
        m = tid.search(l)
        if not m: continue
        t = m.group(1)
        if t in keep:
            o.write(l)
            if t in keep_f: of.write(l)
print(out, len(keep), "transcripts,", len(keep_f), "pass filters")
