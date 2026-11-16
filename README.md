# Top 500 pool1 genes: young vs old mouse brain hub

The genes are ranks 1–500 of ../pool1.csv, sorted by old_minus_young (the difference in noisy-transcript ratio). They run from Ddx39b (0.340) down to 1110059G10Rik (0.069). The list is in tables/top500_genes.txt.
Ages come from ENA PRJEB85167, where B31–B35 are labelled YoungWT. B151–B154 are assumed to be old (not confirmed).

1. `scripts/subset_genes.py`: keeps the transcripts whose associated_gene is in the list (a fusion "A_B" counts if either part is listed). It runs on each of ../mouse/{gtf,classifications}. The output goes to input/<sample>_{corrected.gtf,classification.txt} plus the matching *_filtered_* files. The filters are the same as in the paper and in the Zc3h8 analysis: |dist_to_CAGE_peak| ≤ 50, FL ≥ 2, all canonical, no RTS, NMD not TRUE. The merged transcriptome has no FL, so it is unfiltered only.
2. `sqanti_browser.py --genome mm39` (no --chrom-sizes, because the hub uses the public UCSC mm39 assembly) runs once per input and writes to hubs/<Young|Old>_<sample>[_filtered] and hubs/Merged. The unfiltered runs and Merged also use `--tables`. Logs are in logs/.
   Merged is built with `--no-trix`, because its trix.ix (109 MB) is over GitHub's 100 MB file limit. Search by name works in the per-sample tracks.
3. `python3 scripts/merge_hubs.py` writes the combined hub to top500_hub/ (hub.txt). It has 19 sub-hubs and 138 tracks. The filtered group shows by default and the merged group starts closed.

Counts of transcripts (unfiltered / filtered):
B31 18,454 / 2,383; B32 19,995 / 2,553; B33 20,300 / 2,614; B34 16,298 / 2,139; B35 16,255 / 2,150; B151 20,131 / 2,467; B152 22,297 / 2,730; B153 17,040 / 2,306; B154 15,038 / 2,043; Merged 38,156.
Each sample's unfiltered set contains all 500 genes. The filtered sets contain 449–475 of them.
