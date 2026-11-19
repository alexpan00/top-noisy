# Hdac1 intron retention: young vs old mouse brain (FL >= 3)

Locus: Hdac1, chr4:129,409,896-129,436,465 (− strand). Window used: chr4:129,409,000-129,437,500.
Young = B31–B35 (ENA PRJEB85167 YoungWT). Old = B151–B154 (assumed).

1. `python3 scripts/make_inputs.py chr4 129409000 129437500 3` builds the inputs.
   - FLAIR merged transcriptome (../mouse/flair_JC): one set per mouse, keeping isoforms with FL.<sample> > 0 and setting FL = FL.<sample>. Each set has an unfiltered and a filtered version.
   - Per-sample TAMA runs: unfiltered only.
   - Filters: |dist_to_CAGE_peak| ≤ 50 (NA fails), **FL ≥ 3**, all canonical, no RTS, NMD not TRUE. The paper text says FL ≥ 2. At FL ≥ 2, young B33 would keep G19644.6.
2. `sqanti_browser.py --genome mm39` runs once per input set and writes to hubs/. Logs are in logs/.
3. `python3 scripts/merge_hubs.py` writes the combined hub to hdac1_hub/. It has 27 sub-hubs: FLAIR filtered (open), FLAIR unfiltered (open) and TAMA (closed).

The event: G19644.6 (FLAIR IR NIC: 12 exons, coding, NMD FALSE, CAGE −33, polyA motif) retains chr4:129,415,304-129,416,155 and also 129,416,298-129,416,755.

| | B151 | B152 | B153 | B154 | B31 | B32 | B33 | B34 | B35 |
|---|---|---|---|---|---|---|---|---|---|
| G19644.6 FL | 6 | 3 | 4 | 4 | 1 | 1 | 2 | 1 | 0 |
| Hdac1 gene FL | 104 | 142 | 299 | 277 | 108 | 123 | 131 | 233 | 194 |

- At FL ≥ 3, G19644.6 passes in all 4 old mice. It is present before filtering in 4 of 5 young mice and passes in none.
- Retention of 129,415,304-129,416,155, all reads: FLAIR old 17/789 vs young 5/759 (p = 0.017). TAMA per-sample old 17/807 vs young 6/783 (p = 0.03). IsoQuant has no Hdac1 IR model.
- Another IR NIC, G19644.2, retains only 129,416,298-129,416,755, which shows no age difference. It passes in all old mice and in young B34 and B35, so the young filtered tracks are not FSM-only in every mouse.
  - Filtered contents per mouse: B31 has only the FSM. B32 and B33 have no IR (B32: FSM, NIC .4, .7, ISM .8; B33: FSM, NIC .4, ISM .8).
  - The cleanest young/old pairs for the figure are B31 or B33 against any old mouse.
