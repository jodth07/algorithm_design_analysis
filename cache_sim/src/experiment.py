import csv
import os
import tracemalloc

from cache_sim.src.cache import Cache  # Legacy fallback for FIFO/LRU wrapper
from cache_sim.src.arc_cache import ARCCache
from cache_sim.src.clock_cache import ClockCache
from cache_sim.src.parser import SyntheticParser, ZipfianParser


def get_cache(policy, size):
    if policy == "FIFO" or policy == "LRU":
        return Cache(size=size, policy=policy)
    elif policy == "CLOCK":
        return ClockCache(size=size)
    elif policy == "ARC":
        return ARCCache(size=size)
    else:
        raise ValueError(f"Unsupported cache policy: {policy}")


def run_experiment(cache_sizes: list[int]):
    policies = ["FIFO", "LRU", "CLOCK", "ARC"]
    trace_types = ["Synthetic", "Zipfian"]
    trials = 3
    results = []

    for trace_type in trace_types:
        for size in cache_sizes:
            for policy in policies:
                avg_hit_rate = 0
                avg_miss_rate = 0
                avg_eviction_rate = 0
                avg_memory_kb = 0

                for t in range(trials):
                    seed = 42 + t
                    if trace_type == "Synthetic":
                        parser = SyntheticParser(
                            num_accesses=10000, address_space=50, seed=seed
                        )
                    else:
                        parser = ZipfianParser(
                            num_accesses=10000, address_space=50, skew=1.2, seed=seed
                        )
                    trace = parser.load()
                    tracemalloc.start()
                    cache = get_cache(policy, size)
                    for addr in trace:
                        cache.access(addr)
                    _, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    stats = cache.stats()
                    avg_hit_rate += stats["Hit Rate"]
                    avg_miss_rate += stats["Miss Rate"]
                    avg_eviction_rate += stats["Eviction Rate"]
                    avg_memory_kb += round(peak / 1024, 2)

                results.append(
                    {
                        "TraceType": trace_type,
                        "CachePolicy": policy,
                        "CacheSize": size,
                        "AvgHitRate": round(avg_hit_rate / trials, 4),
                        "AvgMissRate": round(avg_miss_rate / trials, 4),
                        "AvgEvictionRate": round(avg_eviction_rate / trials, 4),
                        "AvgMemoryUsedKB": round(avg_memory_kb / trials, 2),
                    }
                )

    file_name = f"cache_experiment_results_arc_clock_{cache_sizes[-1]}.csv"
    # Save to CSV
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "results",
        file_name,
    )

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Experiment complete. Results saved to results/{file_name}")
