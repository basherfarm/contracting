import sys, signal, resource
from seneca.constants.config import MEMORY_LIMIT, RECURSION_LIMIT, CPU_TIME_LIMIT

def set_resources():
    # resource.setrlimit(resource.RLIMIT_STACK, (MEMORY_LIMIT, MEMORY_LIMIT))
    # resource.setrlimit(resource.RLIMIT_CPU, (CPU_TIME_LIMIT, CPU_TIME_LIMIT))
    sys.setrecursionlimit(RECURSION_LIMIT)
