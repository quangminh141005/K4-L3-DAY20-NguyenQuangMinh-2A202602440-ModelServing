#!/usr/bin/env python3
"""Save actual same-question responses from both installed quantizations."""
import json
import pathlib
import sys
import httpx
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'lib'))
import labkit

prompt = 'What is goodput@SLO? Define it in two sentences and distinguish it from raw throughput.'
active = labkit.load_active()
rows = []
for role in ('primary', 'compare'):
    model = str(labkit.repo_root() / active[f'{role}_model'])
    with labkit.serve_bg(model, port=8098) as base:
        response = httpx.post(f'{base}/v1/chat/completions', json={
            'model': 'local', 'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0, 'seed': 42, 'max_tokens': 160,
        }, timeout=300)
        response.raise_for_status()
        body = response.json()
        rows.append({'quant': active[f'{role}_quant'],
                     'answer': body['choices'][0]['message']['content'],
                     'finish_reason': body['choices'][0]['finish_reason'],
                     'timings': body.get('timings')})
        print(rows[-1]['quant'], rows[-1]['answer'], flush=True)
labkit.write_report('01-quality-comparison.md',
    '# Same-question quality check\n\n'
    + f'Prompt: {prompt}\n\nTemperature: 0; seed: 42; max_tokens: 160. One sample per quantization; this is not a general quality evaluation.\n\n'
    + '\n\n'.join(f"## {r['quant']}\n\n{r['answer']}\n\nFinish reason: `{r['finish_reason']}`" for r in rows),
    {'prompt': prompt, 'temperature': 0, 'seed': 42, 'max_tokens': 160, 'results': rows})
