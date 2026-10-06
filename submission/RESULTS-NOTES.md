# Reading your results

These are coaching notes, not your personal reflection. Use your own words for the required observation sections.

- TTFT is the client time to the first content chunk. It includes HTTP overhead, scheduling, prompt processing, and any queueing; it is not an isolated prefill measurement.
- TPOT measures the time after the first token divided by remaining output tokens. The server token count is used when available.
- The baseline has only 10 prompts per quantization. Nearest-rank P95 and P99 both select the largest observation; identical P95/P99 is expected and does not establish a reliable production tail estimate.
- The smaller quantization improves decode throughput from 63.1 to 67.7 tokens/s (1.073×), while median TTFT increases from 96.2 to 144.6 ms. File sizes in the report use GiB even though the column says GB. A disk-size reduction is not a measured peak-RAM reduction.
- Tuning: 4 threads achieves 60.9 tokens/s, 8 achieves 62.1, 16 achieves 46.1, and 32 achieves 20.5. The curve starts flattening around 4 threads and peaks at 8. Extra SMT threads share physical execution resources and memory bandwidth; oversubscription adds scheduling/synchronization cost. These are plausible mechanisms, not hardware-counter measurements proving a single cause.
- The default is already 8 threads. Do not claim a 3.03× improvement over the default. 3.03× compares the deliberately oversubscribed 32-thread configuration with 8 threads; default-to-best improvement is 1.00×. A measured alternative comparison is 1 thread → 8 threads.
- Under load, RPS × average latency estimates requests in the system, including queued requests. It is not active decode-slot utilization. The metrics sampler is the evidence of batching.
- Locust uses a closed-loop user population with think time: 50 versus 10 users is 5× configured users, not necessarily 5× offered requests/s. A 60-second run also excludes unfinished requests from completed-request percentiles.
- Goodput counts successful requests meeting a stated latency SLO. Aggregate CSV percentiles do not supply exact goodput or separate queue time from compute time. Increased latency with little throughput growth and saturated slots supports a queueing explanation; it is not a direct queue-time measurement.
- Integration uses local toy documents, keyword retrieval, and no embedding model by default. N16–N19 are stubbed in this run. N20 is a real HTTP call to the local llama-server. Stub embedding/retrieval timing cannot predict your full earlier-days stack.

Actual load results (CSV snapshots): 10 users → 87 completed requests, 1.48 RPS, P95 10 seconds; 50 users → 97, 1.64 RPS, P95 33 seconds. The final console summaries include a few more requests than the last periodic CSV snapshot. Preserve both sources; do not manually make their counts match. The highest sampled average busy-slot count was 3.93/4 and the peak deferred gauge was 46. These are consistent with heavy queueing. The two runs cannot identify the precise saturation knee.

Actual integration result: all three queries completed; mean LLM time was 2361.5 ms of 2361.6 ms total. Embedding and retrieval rounded to 0.0 ms because they are skipped/toy operations. The serving stage accounts for effectively all this toy pipeline's latency.

Quality evidence: the deterministic primary response contains a false formula (“dividing the total throughput by the SLOs”). The compare response wrongly calls goodput a proprietary caching mechanism and invents “Synchronous Load On Rate”; it is also truncated at the output limit. Both answers need correction. In this one test, the smaller quantization is less faithful to the concept. This single question cannot establish a general accuracy gap.
