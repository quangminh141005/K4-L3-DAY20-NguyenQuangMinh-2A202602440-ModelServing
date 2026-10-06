# 01 - Tune: thread-count sweep

Model `Qwen3.5-0.8B-Q4_K_M.gguf` · host `Linux-x86_64` · llama.cpp `b10488`
CPU: **8 physical · 16 logical** cores · `ngl=0` · metric `tg128`

| threads (-t) | tg128 (tok/s) | vs best |
|:--|--:|--:|
| 1 | 36.0 | 58% |
| 4 | 60.9 | 98% |
| 8 | 62.1 | 100% |
| 16 | 46.1 | 74% |
| 32 | 20.5 | 33% |

**Best**: `-t 8` at 62.1 tok/s
**Slowest tested**: `-t 32` at 20.5 tok/s (3.03x spread)
**Against the physical-core default** (`-t 8`, 62.1 tok/s): 1.00x

Use this in your run:

```bash
LAB_N_THREADS=8 make bench
```

## Your explanation

The curve starts flattening around 4 threads: throughput rises only about 2% from 60.9 tokens/s at 4 threads to the peak of 62.1 at 8. Above the eight physical cores, it falls to 46.1 at 16 threads and 20.5 at 32. The practical choice is therefore 8 threads; 4 is already close to the best tested throughput.

Decode repeatedly accesses model weights through shared memory channels. Once memory throughput limits progress, additional threads cannot supply proportional bandwidth. SMT threads share physical-core execution resources, and 32 threads oversubscribe the 16 logical CPUs, adding scheduling and synchronization costs. These mechanisms plausibly explain the plateau and decline; this sweep did not collect hardware counters to isolate their individual contributions.

Reducing the deliberately oversubscribed setting from 32 to 8 threads gives a measured 3.03× improvement. The original physical-core default was already 8, so the improvement over that default is 1.00×. The data supports avoiding excessive threads, not claiming an unmeasured speedup over the baseline.
