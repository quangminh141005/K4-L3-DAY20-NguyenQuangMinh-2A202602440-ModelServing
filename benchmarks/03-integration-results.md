# 03 - Integrate: RAG pipeline run

Host `Linux-x86_64` · llama.cpp `b10488` ·
retrieval backend: **keyword overlap** · 3 queries

| Query | Contexts retrieved | embed (ms) | retrieve (ms) | llm (ms) | total (ms) |
|:--|--:|--:|--:|--:|--:|
| Why is goodput more useful than raw throughp... | goodput, paged, radix | 0.0 | 0.0 | 3338.6 | 3338.6 |
| What problem does PagedAttention actually so... | paged, radix, disagg | 0.0 | 0.0 | 1126.5 | 1126.5 |
| When does splitting prefill and decode help?... | disagg, radix, batching | 0.0 | 0.0 | 2619.5 | 2619.6 |

Mean per stage (ms): embed **0.0** · retrieve **0.0** ·
llm **2361.5** · total **2361.6**
Dominant stage: **llm** (100% of total)

## Answers returned

**Why is goodput more useful than raw throughput?**

> Based on the context provided, **Goodput** is more useful than raw throughput primarily because it **ignores SLOs (Service Level Objectives) at saturation**.

While raw throughput measures the total requests per second (requests/sec), Goodput specifically counts only the requests that met the Target Time-to-Fullness (TTFT) and Target Time-to-Poll (TPOT) targets. This means Goodput focuses on the a

**What problem does PagedAttention actually solve?**

> PagedAttention solves the problem of **internal fragmentation in GPU memory** by storing the KV cache in non-contiguous pages.

This allows the engine to utilize unused memory regions more effectively than a contiguous array, thereby reducing wasted GPU memory.

**When does splitting prefill and decode help?**

> Based on the provided context, splitting prefill and decode helps to **reduce compute and memory bandwidth costs**.

The context explains that prefill is compute-bound (requires more CPU power), while decode is memory-bandwidth-bound (requires more GPU memory). By splitting these operations into separate pools:
1.  **Prefill** is performed on separate pools, avoiding the compute-bound nature of th


## Which N16-N19 pieces are real (required -- replace this line)

_List each of N16, N17, N18, N19 as real or stubbed. Stubbing costs no points;
misrepresenting it does. Then answer: is the dominant stage above what you expected?
If you had to halve this pipeline's latency, which stage would you attack and why?_
