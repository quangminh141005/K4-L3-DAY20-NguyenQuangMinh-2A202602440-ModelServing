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

## Your explanation (required -- replace this line)

_Where is the knee, and why there? If the peak sits at your physical core count
and drops above it, say what the extra threads are competing for. If your curve
does something else -- flat, or still climbing at 2x logical cores -- say that
instead and reason about why. A result that contradicts the expected shape is
worth more than one that matches it, as long as you explain it._
