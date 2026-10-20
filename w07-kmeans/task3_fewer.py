#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out


class YourKMeans:
    """Your k-means.

        __init__(k, max_iter=50)
        run(points, initial_centroids, distance) -> (labels, centroids)

    Same starting centroids, same `distance` function - which is counted. That
    counter is your score.

    The idea, from §7.3 and the triangle inequality:

        if a point is much closer to its current centroid than that centroid
        moved, and than any other centroid could have come, then it cannot have
        changed cluster, and you do not have to measure anything

    Keeping enough bookkeeping to make that test cheap, without keeping so much
    that the bookkeeping costs more than the distances, is the task.

    You may call `distance` on two centroids, and those calls are counted too -
    which is the correct accounting, since that is real work. There are k of
    them and n points, and k is much smaller than n. That asymmetry is the
    whole opening.
    """

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter
        self.iterations = 0
        self.first_iter_calls = 0
        self.total_calls = 0

    def run(self, points, initial_centroids, distance):
        """Elkan-style bounds: upper bound to own centroid, lower bounds to
        the others, updated from the k centroid shifts."""
        n = len(points)
        k = self.k
        centroids = [tuple(c) for c in initial_centroids]
        labels = [0] * n
        upper = [float("inf")] * n
        lower = [[0.0] * k for _ in range(n)]
        tight = [False] * n
        calls0 = getattr(distance, "calls", 0)

        for self.iterations in range(1, self.max_iter + 1):
            cc = [[0.0] * k for _ in range(k)]
            sep = [float("inf")] * k
            for j in range(k):
                for m in range(j + 1, k):
                    d = distance(centroids[j], centroids[m])
                    cc[j][m] = cc[m][j] = d
                    if d < sep[j]:
                        sep[j] = d
                    if d < sep[m]:
                        sep[m] = d
            for j in range(k):
                sep[j] *= 0.5

            changed = False
            first = self.iterations == 1
            for i, p in enumerate(points):
                a = labels[i]
                if not first and upper[i] <= sep[a]:
                    continue
                if not first and not tight[i]:
                    d_own = distance(p, centroids[a])
                    lower[i][a] = d_own
                    upper[i] = d_own
                    tight[i] = True
                    if upper[i] <= sep[a]:
                        continue

                best_j = a
                best_d = None if first else upper[i]
                for j in range(k):
                    if not first and j == a:
                        continue
                    if not first and best_d is not None:
                        if best_d <= lower[i][j] or best_d <= 0.5 * cc[a][j]:
                            continue
                    d = distance(p, centroids[j])
                    lower[i][j] = d
                    if best_d is None or d < best_d - 1e-12:
                        best_d, best_j = d, j
                upper[i] = best_d
                tight[i] = True
                if labels[i] != best_j:
                    labels[i] = best_j
                    changed = True

            if first:
                self.first_iter_calls = getattr(distance, "calls", 0) - calls0

            old = centroids
            centroids = _means(points, labels, k, centroids)
            if not changed:
                break
            for j in range(k):
                shift = distance(old[j], centroids[j])
                if shift == 0.0:
                    continue
                for i in range(n):
                    lower[i][j] = max(0.0, lower[i][j] - shift)
                    if labels[i] == j:
                        upper[i] += shift
                        tight[i] = False

        self.total_calls = getattr(distance, "calls", 0) - calls0
        return labels, centroids
