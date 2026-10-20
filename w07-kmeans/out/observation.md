# Observations · Week 7

## Task 1

R3: an empty cluster **keeps its previous centroid**. Jumping it to the furthest point would yank it into another blob and steal points. Over 40 seeds, random recovered the three blobs **24/40** times; k-means++ recovered them **40/40** (mean sse 0.120 vs 38.5). ++ spends O(kn) distances before iteration 1 to spread the seeds — worth it when a bad local optimum is cheap to avoid and expensive to keep; skip it if you already have good seeds or k is huge. SSE always falls as k grows (k=n gives SSE=0), so you cannot choose k by minimising it.

R3: 빈 클러스터는 **이전 중심을 유지**한다. 가장 먼 점으로 옮기면 다른 blob을 훔친다. 시드 40개에서 random은 **24/40**, ++는 **40/40**. ++는 시작 전 O(kn) 거리를 써서 시드를 벌려 두고, 나쁜 국소해 비용이 클 때 이득이다. SSE는 k가 늘면 항상 줄어 k=n이면 0이므로 k를 SSE 최소로 고를 수 없다.

## Task 2

At n=1000, contrast dropped **below 1 at d≈50** (0.982) and below 0.5 between 100 and 200. A6: n matters — at d=20, contrast rose 1.79 → 2.45 as n went 200 → 2000, because a closer pair becomes likelier. A8: this does **not** threaten week-3 LSH. That was Jaccard on sets, not ℓ₂ in a cube; minhash still estimates overlap in a large vocabulary.

n=1000에서 contrast는 **d≈50에서 1 미만**(0.982), 0.5 아래는 100–200 사이. A6: n도 중요하다. d=20에서 n=200→2000이면 contrast 1.79→2.45. A8: 3주차 LSH는 위협하지 않는다. Jaccard/집합이지 큐브의 유클리드가 아니다.

## Task 3

Per point I store one upper bound and k lower bounds — **k+1 extra numbers** (here 13). The **upper bound vs half the nearest other centroid** (Elkan's `u ≤ s(c)` / `u ≤ ½ d(c,c')`) does most of the pruning; maintaining it costs k centroid–centroid distances and k shifts per iteration. SSE difference is **exactly 0** because we only skip distances we can prove, then assign with the same tie-break. First iteration cannot prune: **240,066 / 498,746 ≈ 48%** of all remaining distance calls happen there. Cut 95.2% → strong.

점마다 상한 1개와 하한 k개, **추가로 k+1개 숫자**. 대부분을 줄이는 것은 자기 중심 상한과 다른 중심까지 거리의 절반을 비교하는 부등식이다. SSE 차이는 **정확히 0** — 증명 가능한 거리만 건너뛴다. 첫 반복은 가지치기가 없어 전체의 약 **48%**가 거기에서 나온다.
