# from cache import Cache
from cache_sim.src.experiment import run_experiment

if __name__ == "__main__":
    cache_sizes_32 = [4, 8, 16, 32]
    cache_sizes_512 = [64, 128, 256, 512]
    run_experiment(cache_sizes_32)
    run_experiment(cache_sizes_512)
