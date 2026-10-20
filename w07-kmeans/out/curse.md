# Task 2 · contrast curve (this machine)

**Machine:** AMD Ryzen 7 6800H, 16 GB RAM, Windows 11, Python 3.14.2.
Cursor and a browser were open.

Default: 1,000 uniform points in the unit cube, 20,000 random pairs.

## A2 · contrast against dimension

| d | mean | min | max | contrast | rel. sd | time |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.521 | 0.003 | 1.326 | 488.6 | 0.476 | 0.05 s |
| 5 | 0.884 | 0.111 | 1.687 | 14.26 | 0.282 | 0.07 s |
| 10 | 1.274 | 0.438 | 2.159 | 3.93 | 0.193 | 0.09 s |
| 20 | 1.815 | 0.821 | 2.670 | 2.25 | 0.135 | 0.15 s |
| 50 | 2.867 | 1.909 | 3.785 | 0.982 | 0.083 | 0.33 s |
| 100 | 4.068 | 3.206 | 4.954 | 0.545 | 0.060 | 0.50 s |
| 200 | 5.776 | 4.871 | 6.682 | 0.372 | 0.041 | 1.05 s |
| 500 | 9.126 | 8.099 | 10.176 | 0.256 | 0.026 | 2.47 s |
| 1000 | 12.909 | 11.970 | 13.806 | 0.153 | 0.019 | 6.03 s |

## A3 · when contrast dies

Contrast falls fast, then slowly. It drops **below 1 at d ≈ 50** (0.982) and **below 0.5 between 100 and 200** (0.545 → 0.372). By d=200, the furthest pair is only 37% farther than the nearest.

## A4 · mean vs d

Mean grows like **√d**, not linearly. For two independent Uniform[0,1]^d points, E[‖X−Y‖²] = d/6, so mean ≈ √(d/6):

| d | measured mean | √(d/6) |
|---:|---:|---:|
| 2 | 0.521 | 0.577 |
| 20 | 1.815 | 1.826 |
| 200 | 5.776 | 5.774 |
| 1000 | 12.909 | 12.910 |

The numbers sit on the square-root curve.

## A5 · relative stdev

stdev stays ~0.24 while the mean climbs, so rel.sd falls 0.476 → 0.019. Contrast (A3) better captures "nearest stopped meaning anything": it is exactly the gap you use to pick a neighbour. Rel.sd says the distribution is concentrating, which is the same phenomenon in a milder statistic.

## A6 · does n matter?

Fixed d=20, 20,000 pair samples:

| n | min | max | contrast |
|---:|---:|---:|---:|
| 200 | 0.946 | 2.636 | 1.79 |
| 1,000 | 0.821 | 2.670 | 2.25 |
| 2,000 | 0.821 | 2.830 | 2.45 |

Yes. More points make a closer pair more likely, so min falls and contrast rises. The curse is about the **sample**, not just the dimension.

## A7 · machine / largest run

AMD Ryzen 7 6800H, 16 GB, Windows 11, Python 3.14.2. Largest run (d=1000, n=2000) took **6.03 s**.

## A8 · does this threaten week-3 LSH?

No, not directly. Week 3 used **Jaccard on shingle sets**, not Euclidean distance in a unit cube. Minhash estimates set overlap; two documents can still have a meaningful 0.6 Jaccard in a huge vocabulary. The curse here is a fact about ℓ₂ on uniform cubes. It would threaten Euclidean LSH / k-NN in high-d feature space, not bag-of-shingles Jaccard.
