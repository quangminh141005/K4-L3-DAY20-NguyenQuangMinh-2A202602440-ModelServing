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


## Which N16-N19 pieces are real

| Day | Component used in this run | Real or stub |
|---|---|---|
| N16 Cloud/IaC | Local processes; no cloud infrastructure integration | Stub |
| N17 Data pipeline | Six hard-coded toy documents | Stub |
| N18 Lakehouse | In-memory Python document list; no persistent lakehouse | Stub |
| N19 Vector + features | Keyword-overlap retrieval; no embedding model or vector index | Stub |
| N20 Serving | Actual HTTP completions from local llama-server | Real |

All three queries completed and the pipeline printed the retrieved contexts and returned answers. Mean LLM time was 2361.5 ms out of 2361.6 ms total, effectively 100%. This is expected because embedding is skipped and keyword retrieval searches only six documents. Their reported 0.0 ms values are rounded timings of toy/skipped operations, not evidence that real embedding and vector retrieval would be free.

To target a 2× reduction, focus on generation rather than these stub stages. First reduce unnecessary output length and remeasure while checking that answers remain complete; faster inference is another candidate. Keeping the system prompt identical can enable prefix reuse when supported, but no cache speedup was measured here. Halving the token limit is not guaranteed to halve total latency because prompt processing and other overhead remain.

Execution success does not establish answer correctness. In the goodput answer, the model incorrectly says goodput ignores SLOs and expands TTFT/TPOT incorrectly. Goodput counts requests meeting SLOs; TTFT means time to first token and TPOT means time per output token. The model-generated answers above are preserved as actual outputs, including their errors.
