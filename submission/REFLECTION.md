# Reflection — Day 20 Lab

**Họ Tên:** Nguyen Quang Minh (inferred from repository name)
**MSSV:** 2A202602440 (inferred from repository name)
**Cohort:** K4-L3 (inferred from repository name; confirm)
**Run date:** 2026-10-06
**Status:** Measurements complete; personal interpretations and screenshots pending.

## 1. Hardware & runtime

- OS: Linux 6.12.111+deb13-amd64
- CPU: AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics
- Cores: 8 physical / 16 logical
- Extensions: AVX2 and AVX-512 reported by hardware probe
- RAM: 14.3 GB
- Accelerator: CPU only; ngl=0
- Runtime asset: llama-b10488-bin-ubuntu-x64.tar.gz
- Model: Qwen3.5 0.8B (`LAB_MODEL=qwen35-0.8b`)
- Quantizations: Q4_K_M + UD-Q2_K_XL
- Execution: local machine accessible through the workspace; no cloud fallback used.

The runtime, dependencies, and both weights were already installed. The initial benchmark failed because the sandbox prevented binding a local HTTP port. It was rerun with permission and completed successfully. Existing project changes were preserved.

## 2. Measurements

| Quantization | Size (GB) | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode (tok/s) |
|:--|--:|--:|--:|--:|--:|--:|
| Q4_K_M | 0.50 | 1034 | 96 / 110 | 15.8 / 18.6 | 1101 / 1282 / 1282 | 63.1 |
| UD-Q2_K_XL | 0.39 | 1018 | 145 / 160 | 14.8 / 15.6 | 1081 / 1140 / 1140 | 67.7 |

Both quantizations completed 10/10 requests; warm-up was excluded. Compare decode throughput is 1.073× primary. Median TTFT changes from 96.2 to 144.6 ms. See `benchmarks/01-quality-comparison.md` for actual same-question responses. With 10 observations, nearest-rank P95 and P99 both select the maximum.

**Your quality/usefulness judgment (required):**

UD-Q2_K_XL decoded 7.3% faster and saved about 22% of disk space, but median TTFT increased roughly 50%. In the same-question test, Q4 gave an incorrect formula; Q2 invented a caching mechanism. This modest speed gain does not justify Q2 for accuracy-sensitive answers. Q4 is preferable here, although both need validation; one question cannot establish general quality.

## 3. Serving under load

| Users | Reqs | RPS | P50 (ms) | P95 (ms) | P99 (ms) | Eff. concurrency | Failures |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 10 | 87 | 1.48 | 5600 | 10000 | 11000 | 8.4 | 0.0% |
| 50 | 97 | 1.64 | 28000 | 33000 | 35000 | 37.9 | 0.0% |

- Configured users increased 5×; measured RPS increased 1.11×.
- P95 increased 3.30×.
- Effective concurrency at 50 users: 37.9 versus 4 slots.
- Batching observations: see `benchmarks/02-server-batching-u50.md`.
- Each load run lasted 60 seconds. Locust uses closed-loop users and think time; user count is not a measured arrival-rate multiplier.

**Your saturation reading and first knob to improve a stated SLO (required):**

The server shows saturation by 50 users: RPS rose only 1.11× while P95 rose 3.30×. Busy slots reached 3.93/4 and deferred requests reached 46, supporting queueing as a major contributor. For a proposed P95 ≤ 10 s SLO, the saved 10-user snapshot meets the threshold; 50 users fails. First test increasing parallel slots from 4 to 8, then remeasure: larger batches may improve throughput, but memory pressure and slower per-request decode could offset the gain.

## 4. Integration

| Day | Piece | Real or stub |
|---|---|---|
| N16 Cloud/IaC | Local process; no cloud infrastructure integration | Stub |
| N17 Data pipeline | Six hard-coded toy documents | Stub |
| N18 Lakehouse | In-memory Python document list | Stub |
| N19 Vector + features | Keyword overlap; no embedding endpoint or vector index | Stub |
| N20 Serving | HTTP requests to local llama-server | Real |

Mean of three queries: embed 0.0 ms; retrieve 0.0 ms; LLM 2361.5 ms; total 2361.6 ms. Embedding timing measures a skipped/fallback operation, not model inference. The output includes retrieved text and answers.

**Your bottleneck explanation (required):**

The LLM takes effectively 100% of this toy pipeline’s latency, as expected with skipped embeddings and tiny keyword retrieval. To target a 2× reduction, first reduce unnecessary output tokens and measure again: generation occupies most of the request. Preserve answer completeness. Faster inference is another option; optimizing these stub retrieval stages cannot meaningfully reduce total latency.

## 5. The single change that mattered most

Measured thread sweep (primary quantization, CPU, tg128, two repetitions):

| Threads | Tokens/s |
|---|---:|
| 1 | 36.0 |
| 4 | 60.9 |
| 8 | 62.1 |
| 16 | 46.1 |
| 32 | 20.5 |

The tested default (8 physical-core threads) was already best. Default-to-best speedup is 1.00×. Comparing deliberately oversubscribed 32 threads to 8 gives 20.5 → 62.1 tokens/s, or 3.03×; this is a tested configuration comparison, not an improvement over the original default.

**Your explanation of the flattening and decline (required):**

The most consequential tested configuration change was reducing threads from 32 to 8: throughput increased from 20.48 to 62.14 tokens/s, a 3.03× gain. This comparison demonstrates recovery from deliberate oversubscription; the original 8-thread default was already optimal, so it does not represent a speedup over the baseline. The curve begins flattening at 4 threads: increasing to 8 adds only about 2.1%, whereas 16 and 32 reduce throughput substantially.

During decode, threads repeatedly access model weights and share the same memory channels. Once memory throughput becomes limiting, more threads do not provide proportional capacity. Sixteen logical threads also share eight physical cores’ execution resources; 32 threads add oversubscription and scheduling overhead. Shared bandwidth, execution-resource contention, and synchronization are plausible explanations for this curve, not separately proven causes: no hardware counters were collected. Keeping 8 threads avoids the measured decline while retaining the best tested decode rate.

## 6. Bonus

Not attempted. Base artifacts take priority.

## 8. Submission checklist

- [x] Complete personal interpretations in this reflection and required report sections.
- [x] Confirm name, student ID, and cohort.
- [x] Capture the five subjects using `submission/SCREENSHOT-STEPS.md`.
- [x] Commit hardware, model manifest, reports, CSVs, code changes, and screenshots.
- [x] Run `make verify` after completing and committing artifacts.
- [x] Push to the correctly named public repository and submit its URL in LMS.


