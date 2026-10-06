# 01 - Measure: latency baseline

Model `Qwen3.5 0.8B` · host `Linux-x86_64` · llama.cpp `b10488`
Settings: `threads=8` `ngl=0` `ctx=2048`
`max_tokens=64` · warm-up discarded
Completed requests: `Q4_K_M` 10/10 · `UD-Q2_K_XL` 10/10

| Quantization | Size (GB) | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode (tok/s) |
|:--|--:|--:|--:|--:|--:|--:|
| Q4_K_M | 0.50 | 1029 | 102 / 116 | 14.7 / 14.9 | 1019 / 1048 / 1048 | 67.9 |
| UD-Q2_K_XL | 0.39 | 1021 | 136 / 155 | 14.1 / 14.4 | 1029 / 1049 / 1049 | 70.8 |

- **TTFT** = prefill. Short prompts keep it small; long-context RAG is where it explodes.
- **TPOT** = per-output-token decode cost, bounded by memory bandwidth. `decode tok/s = 1000 / TPOT_p50`.
- `UD-Q2_K_XL` decodes **1.04x faster** than `Q4_K_M` here, for 0.11 GB less on disk.

## Your observation

UD-Q2_K_XL increased decode throughput from 67.9 to 70.8 tokens/s (about 4.3%) and reduced the reported file size from 0.50 to 0.39 GB (about 22%). However, median TTFT increased from 102 to 136 ms, and median end-to-end latency increased slightly from 1019 to 1029 ms. The smaller quantization therefore does not improve every part of responsiveness.

The same-question responses in `01-quality-comparison.md` favor Q4 for this example: Q4 recognizes the relationship between goodput and SLOs but invents an incorrect formula; Q2 invents a proprietary caching mechanism and a false expansion of SLO, then reaches the output limit. Goodput@SLO means the rate of successful requests that meet the specified service-level targets. For accuracy-sensitive answers, the modest decode gain does not justify the worse response in this test, so Q4 is the preferable choice here. Both require answer validation, and one question does not establish general accuracy.

Only 10 requests were measured per quantization. With nearest-rank percentiles, P95 and P99 both select the maximum observation; these results are useful for this local comparison, not a reliable production-tail estimate. TTFT is measured client-side and includes HTTP and scheduling overhead as well as prompt processing.
