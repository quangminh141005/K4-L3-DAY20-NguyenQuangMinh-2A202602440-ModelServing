# Take the five required screenshots

Open terminals in this repository. Capture genuine terminal output with Print Screen → rectangular selection; save PNG files directly in `submission/screenshots/`. Keep text legible and crop to the terminal. Do not photograph generated mock terminal images.

1. **Hardware:** run `LAB_MODEL=qwen35-0.8b make probe`. Include CPU, physical/logical cores, RAM, backend, and build. Save `01-hardware-probe.png`.
2. **Benchmark:** measurements are already in `benchmarks/01-quickstart-results.md`. Run `cat benchmarks/01-quickstart-results.md` and capture the model, settings, completed-request counts, and complete table showing both quantizations, TTFT, TPOT, and E2E percentiles. Save `02-bench.png`. If you rerun `make bench`, it overwrites the report and its observation section; update the reflection to the new numbers.
3. **Serve and smoke:** terminal A: `make serve`. Leave it running. Once it says it is listening, terminal B: `make smoke`. Arrange A and B side by side, showing the listening address, completion, and nonzero `llamacpp:tokens_predicted_total`. Save `03-serve-and-smoke.png` (or two images, `03a-serve.png` and `03b-smoke.png`). If port 8080 is already occupied by the assistant's server, use `LAB_SERVER_PORT=8090 make serve` and `LAB_SERVER_PORT=8090 make smoke`.
4. **10 users:** keep server A running. Terminal B: `make load-10` (add `LAB_SERVER_PORT=8090` if using that port). Wait for the 60-second run to finish. Include the final request counts/RPS table AND the response-time percentile table with 50%, 95%, and 99%. Save `04-locust-10.png`.
5. **50 users:** terminal B: `make load-50`. Immediately, terminal C: `make metrics`. Both must run together. Use the same port environment variable for both if needed. After the load finishes, capture the final counts/RPS and percentile tables. Save `05-locust-50.png`.

Rerunning load tests changes the CSV measurements. Afterwards run `make load-report` and update the load table in `submission/REFLECTION.md` to match. The reports have personal observation sections which you must complete.

Optional: capture `make tune`, batching report, and `make pipeline` output. These do not replace the five required subjects.

After your own explanations and screenshots are complete, commit the submission artifacts and run `make verify`. Never add `.env`, `.venv`, runtime binaries, or model weights.

## Capture the already completed load runs without rerunning

Use `tail -n 22 benchmarks/load-10.log` for screenshot 4 and `tail -n 22 benchmarks/load-50.log` for screenshot 5. These are genuine logs of the completed 60-second runs. Maximize the terminal and decrease its font size enough to fit the percentile columns. The final console counts differ slightly from the last periodic CSV snapshots used in the reports; do not edit either source.
