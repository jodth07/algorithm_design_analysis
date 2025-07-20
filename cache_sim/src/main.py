# from cache import Cache
from experiment import run_experiment


# if __name__ == '__main__':

if __name__ == "__main__":
    # cache = Cache(size=3, policy='LRU')
    # trace = [1, 2, 3, 1, 4, 2, 5, 1]
    #
    # for addr in trace:
    #     hit = cache.access(addr)
    #     print(f"Accessing {addr} → {'HIT' if hit else 'MISS'}")
    #
    # print("\nStats:")
    # print(cache.stats())
    run_experiment()
