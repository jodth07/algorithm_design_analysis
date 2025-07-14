import csv
import os

from cache import Cache
from parser import SyntheticParser, ZipfianParser


def run_experiment():
    cache_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    policies = ["FIFO", "LRU"]
    trace_types = ["Synthetic", "Zipfian"]
    trials = 3
    results = []

    for trace_type in trace_types:
        for size in cache_sizes:
            for policy in policies:
                avg_hit_rate = 0
                avg_miss_rate = 0
                avg_eviction_rate = 0

                for t in range(trials):
                    seed = 42 + t
                    if trace_type == "Synthetic":
                        parser = SyntheticParser(
                            num_accesses=1000, address_space=50, seed=seed
                        )
                    else:
                        parser = ZipfianParser(
                            num_accesses=1000, address_space=50, skew=1.2, seed=seed
                        )

                    trace = parser.load()
                    cache = Cache(size=size, policy=policy)
                    for addr in trace:
                        cache.access(addr)

                    stats = cache.stats()
                    avg_hit_rate += stats["Hit Rate"]
                    avg_miss_rate += stats["Miss Rate"]
                    avg_eviction_rate += stats["Eviction Rate"]

                results.append(
                    {
                        "TraceType": trace_type,
                        "CachePolicy": policy,
                        "CacheSize": size,
                        "AvgHitRate": round(avg_hit_rate / trials, 4),
                        "AvgMissRate": round(avg_miss_rate / trials, 4),
                        "AvgEvictionRate": round(avg_eviction_rate / trials, 4),
                    }
                )

    # Save to CSV
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "results",
        "cache_experiment_results4.csv",
    )

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(
        "✅ Experiment complete. Results saved to results/cache_experiment_results.csv"
    )
