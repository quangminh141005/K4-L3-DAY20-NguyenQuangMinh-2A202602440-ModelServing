# 02 - Continuous batching under load (u50)

Host `Linux-x86_64` · `--parallel 4` · 30 samples over
60s at 2.0s intervals · raw CSV: `02-server-metrics-u50.csv`

| Gauge | Peak observed |
|:--|--:|
| `n_busy_slots_per_decode` (avg/decode) | 3.81 of 4 slots (95%) |
| `requests_processing` | 4 |
| `requests_deferred` | 46 |
| `kv_cache_usage_ratio` | n/a — not exported by llama.cpp `b10488` |
| `tokens_predicted_total` (final) | 32062 |

Highest sampled value was **3.81 of 4** slots. Note this gauge is llama.cpp's *average* busy slots per decode step, so the number below is the highest average we sampled, not an instantaneous maximum batch width. A peak near 1 means
requests were served one at a time -- either the load was too light to overlap, or
they arrived too far apart. A peak approaching `--parallel` means the scheduler was
genuinely packing concurrent requests into shared decode steps.
`requests_deferred` went above zero: more requests arrived than there were slots, so some waited. That wait is the queue time in your P95.

## Your observation

The highest sampled average busy-slot count was 3.81 out of 4 (about 95%), with a peak of 4 processing requests and 46 deferred requests. Multiple slots were contributing to shared decode steps, so continuous batching was observed under load. The 3.81 value is the highest sampled average per decode step, not a directly measured instantaneous maximum batch width.

The load report estimates effective concurrency at 38.9, much larger than four slots. These values measure different quantities: RPS × mean response time estimates requests in the system, including queued requests, whereas the server gauge describes active decode work. The deferred-request peak supports this queueing interpretation. For batching, the server metric is the relevant evidence; for overall in-flight occupancy, Little’s Law provides an estimate. Neither metric invalidates the other.

The 60-second run is finite and excludes unfinished requests from completed-request latency statistics. Effective concurrency is therefore approximate, and the peaks of separate gauges need not occur at the same instant.
