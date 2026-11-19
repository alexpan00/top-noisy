# Zfand2b intron retention: young vs old mouse brain

Locus: chr1:75,145,290-75,148,270 (+ strand). Window used: chr1:75,144,500-75,149,000.
Young = B31–B35 (ENA PRJEB85167 YoungWT). Old = B151–B154 (assumed).

1. `python3 scripts/make_inputs.py` builds the inputs.
   - FLAIR merged transcriptome (../mouse/flair_JC): one set per mouse, keeping isoforms with FL.<sample> > 0 and setting FL = FL.<sample>. Each set has an unfiltered and a filtered version.
   - Per-sample TAMA runs (../mouse/{gtf,classifications}): unfiltered only.
   - Filters: |dist_to_CAGE_peak| ≤ 50 (NA fails), FL ≥ 2, all canonical, no RTS, NMD not TRUE.
2. `sqanti_browser.py --genome mm39` runs once per input set and writes to hubs/<TOOL>_<Age>_<sample>[_filtered]. Logs are in logs/.
3. `python3 scripts/merge_hubs.py` writes the combined hub to zfand2b_hub/. It has 27 sub-hubs: FLAIR filtered (open), FLAIR unfiltered (open) and TAMA (closed).

What it shows (2026-11-19):
- FLAIR: the IR NIC isoforms G768.3 (3 exons) and G768.5 (2 exons) pass the filters in B151, B153 and B154 and have FL 0 in every young mouse. G768.4 (8 exons, retains intron 2) passes in B152 and B153 and has FL 1 in B31 and B35.
- TAMA per-sample: young B31 (G1257.7), B32 (G1533.4, G1533.8), B34 (G1196.7) and B35 (G1054.5) also have FL 1 isoforms that retain chr1:75,146,561-75,147,010. FLAIR's zero in young is therefore a collapse/quantification effect.
- IsoQuant (../mouse/isoquant_JC) reports no Zfand2b IR isoform.
