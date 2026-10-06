# 02 - Serve: load test + saturation reading

Host `Linux-x86_64` · llama.cpp `b10488` ·
`--parallel 4` · `ctx=2048` · `threads=8` ·
`ngl=0`

| Users | Reqs | RPS | P50 (ms) | P95 (ms) | P99 (ms) | Eff. concurrency | Failures |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 10 | 113 | 1.93 | 4000 | 6600 | 6900 | 8.1 | 0.0% |
| 50 | 115 | 1.96 | 24000 | 28000 | 29000 | 38.9 | 0.0% |

*Effective concurrency = RPS x average latency (Little's Law) -- how many requests were
really in flight, regardless of how many users locust simulated. It counts queued requests
too, so the occupancy/slot ratio can legitimately exceed 1.0; it is occupancy, not
utilisation. For true slot utilisation use the server's own gauges (`make metrics`).*

## What these two runs say

| Going from 10 to 50 users | |
|:--|--:|
| Offered load | 5x |
| Throughput actually delivered | **1.02x** (20% of linear) |
| P95 latency | **4.24x** |
| Effective concurrency at 50 users | 38.9 vs `--parallel 4` slots (occupancy/slot ratio 9.73) |

**Saturated.** Throughput delivered only 1.02x for 5x the offered load, and effective concurrency (38.9) is at or above all 4 decode slots. Saturation sets in somewhere at or below 50 users; the load you added beyond that point became queue time rather than throughput.

Throughput moved 1.02x while P95 moved 4.24x. That gap is the goodput argument: past saturation you buy throughput by spending latency, and if your SLO is a P95 target then the requests you added are no longer being served within it. (This lab does not fix an SLO number for you -- pick one in your write-up and state how much goodput you keep at it.)

## Your reading

Throughput is already close to its observed plateau at 10 users: moving to 50 users changes RPS from 1.93 to 1.96 (1.02×), while P95 rises from 6.6 to 28 seconds (4.24×). The precise knee cannot be located with only two user counts, but these runs show that adding users in this range mostly increases waiting rather than completed throughput. Fifty users are clearly beyond the useful operating point for a tight latency target.

Effective concurrency is 38.9 versus four slots. The separately sampled metrics show up to 3.81 average busy slots per decode step and 46 deferred requests. Together these support queueing as a major contributor to the latency increase. They do not directly separate queue time from compute time; mixed prompts and batch contention can also change service time. Five times as many closed-loop users is not necessarily five times the offered request rate.

For a proposed P95 ≤ 10-second SLO, the 10-user snapshot meets the target and the 50-user snapshot fails it. Exact goodput cannot be calculated from these aggregate percentiles alone; it needs per-request success and latency records. First test increasing `--parallel` from 4 to 8 and remeasure the same workload: additional slots may improve batching and reduce waiting. This is a proposed experiment, not a measured improvement; memory pressure and slower per-request decode may offset the benefit. Thread count is already at the best tested setting, while changing quantization has an observed quality tradeoff.
