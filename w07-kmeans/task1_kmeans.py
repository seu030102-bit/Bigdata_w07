#!/usr/bin/env python3
"""Week 7 · Task 1 — k-means, and the thing that decides the answer.

Textbook §7.1 (clustering, the curse of dimensionality), §7.3 (k-means).

k-means is four lines: pick centroids, assign every point to the nearest one,
move each centroid to the mean of its points, repeat. It always converges.

It converges to a **local** optimum, and which one depends entirely on where you
started. That is not a footnote - it is the difference between a clustering that
means something and one that does not, and you can watch it happen on nine points.

    python3 task1_kmeans.py --verify
"""
import argparse, math, random

# Three obvious blobs of three points each. Any sensible clustering finds them.
BLOBS = [(0.0, 0.0), (0.2, 0.1), (0.1, 0.2),
         (8.0, 8.0), (8.2, 8.1), (8.1, 8.2),
         (0.0, 8.0), (0.2, 8.1), (0.1, 8.2)]


def euclidean(a, b):
    """Distance between two points of any dimension."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _sqdist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def assign(points, centroids):
    """Nearest centroid for each point. Return a list of centroid indices.

    Ties go to the lower index, so that everybody's answer is the same.
    """
    labels = []
    for p in points:
        best_d, best_j = None, 0
        for j, c in enumerate(centroids):
            d = euclidean(p, c)
            if best_d is None or d < best_d - 1e-12:
                best_d, best_j = d, j
        labels.append(best_j)
    return labels


def update(points, labels, k, previous=None):
    """Move each centroid to the mean of its points.

    Empty cluster (R3): keep the previous centroid if we have one, otherwise
    reuse points[j]. The alternative — jump to the furthest point — would yank
    the empty centre across the space and often steal another blob.
    """
    dim = len(points[0])
    sums = [[0.0] * dim for _ in range(k)]
    counts = [0] * k
    for p, lab in zip(points, labels):
        counts[lab] += 1
        for d, v in enumerate(p):
            sums[lab][d] += v
    centroids = []
    for j in range(k):
        if counts[j]:
            centroids.append(tuple(s / counts[j] for s in sums[j]))
        elif previous is not None:
            centroids.append(tuple(previous[j]))
        else:
            centroids.append(tuple(points[j % len(points)]))
    return centroids


def _init_random(points, k, rng):
    return [tuple(p) for p in rng.sample(list(points), k)]


def _init_plusplus(points, k, rng):
    pts = list(points)
    centroids = [tuple(pts[rng.randrange(len(pts))])]
    closest = [_sqdist(p, centroids[0]) for p in pts]
    for _ in range(1, k):
        total = sum(closest)
        if total <= 0:
            centroids.append(tuple(pts[rng.randrange(len(pts))]))
            continue
        r = rng.random() * total
        acc = 0.0
        chosen = 0
        for i, d in enumerate(closest):
            acc += d
            if acc >= r:
                chosen = i
                break
        centroids.append(tuple(pts[chosen]))
        c = centroids[-1]
        for i, p in enumerate(pts):
            d = _sqdist(p, c)
            if d < closest[i]:
                closest[i] = d
    return centroids


def kmeans(points, k, init="random", seed=246, max_iter=100):
    """Run to convergence. Return (labels, centroids, sse)."""
    rng = random.Random(seed)
    if init == "++":
        centroids = _init_plusplus(points, k, rng)
    else:
        centroids = _init_random(points, k, rng)

    labels = [None] * len(points)
    used = 0
    for it in range(1, max_iter + 1):
        new_labels = assign(points, centroids)
        used = it
        if new_labels == labels:
            labels = new_labels
            break
        labels = new_labels
        centroids = update(points, labels, k, previous=centroids)
    kmeans.iterations = used
    return labels, centroids, sse_of(points, labels, centroids)


def sse_of(points, labels, centroids):
    """Sum of squared distances from each point to its assigned centroid."""
    return sum(_sqdist(p, centroids[lab]) for p, lab in zip(points, labels))


# ------------------------------------------------------------------- harness
def verify():
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<50} {detail}")
        fails += not ok

    try:
        check("distance in 2d", abs(euclidean((0, 0), (3, 4)) - 5) < 1e-9)
        check("distance in 5d",
              abs(euclidean((0,) * 5, (1,) * 5) - math.sqrt(5)) < 1e-9)
    except NotImplementedError:
        print("  euclidean is still a stub"); return 1

    try:
        labels, cents, sse = kmeans(BLOBS, 3, init="++", seed=1)
    except NotImplementedError:
        print("  kmeans is still a stub"); return 1

    groups = {}
    for p, l in zip(BLOBS, labels):
        groups.setdefault(l, []).append(p)
    check("three clusters of three", sorted(len(g) for g in groups.values()) == [3, 3, 3],
          sorted(len(g) for g in groups.values()))
    check("the three blobs were recovered",
          all(max(q[0] for q in g) - min(q[0] for q in g) < 1 and
              max(q[1] for q in g) - min(q[1] for q in g) < 1
              for g in groups.values()))
    check("sse is small when clusters are right", sse < 1.0, f"sse {sse:.4f}")

    # Bad luck with random starts should sometimes be visibly worse.
    randoms = [kmeans(BLOBS, 3, init="random", seed=s)[2] for s in range(40)]
    plusplus = [kmeans(BLOBS, 3, init="++", seed=s)[2] for s in range(40)]
    check("random init sometimes lands badly", max(randoms) > min(randoms) * 5,
          f"sse from {min(randoms):.3f} to {max(randoms):.3f}")
    check("k-means++ is more reliable than random",
          sum(plusplus) / len(plusplus) <= sum(randoms) / len(randoms),
          f"mean sse: ++ {sum(plusplus) / len(plusplus):.3f} vs "
          f"random {sum(randoms) / len(randoms):.3f}")

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())
