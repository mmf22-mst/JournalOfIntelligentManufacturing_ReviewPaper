"""Online Resource 2.
Article: How Much Ontology Does a Manufacturing Knowledge Graph Need? A Construction Ladder,
a Cost Model, and a Decision Framework for Process Engineers. Journal of Intelligent Manufacturing.
Authors: Michael J. McNary, Jian Liu, Donald C. Wunsch II. Corresponding author: mmf22@mst.edu.

Reproduces every figure in Table 4 and Section 6.6 from the stated assumptions.

Run:  python cost_check.py
All token counts and rates are the ones stated in Sections 6.1, 6.2, and 6.5.
Change an assumption here and the printed table changes with it.
"""

# ---- Corpus and call structure (Section 6.5) ----
T = 50_000_000          # tokens in the construction collection
c = 8_000               # chunk size, tokens
prompt_in = 30_000      # construction prompt per call, including the chunk
construct_out = 2_000   # output tokens per construction call
calls = T // c          # 6,250 calls

# ---- Population call (Section 6.5) ----
pop_in = c + 6_000      # chunk plus schema, grounding vocabulary, and instructions
pop_out = 2_000         # extracted triples per chunk

# ---- Per-answer tokens (Section 6.2 and 6.5) ----
q = 200                 # question
x_graph = 9_800         # retrieved context, graph rungs (Han et al. 2025, Table 31)
x_plain = 3_600         # retrieved context, L1 (Han et al. 2025, Table 31)
a = 500                 # generated answer

# ---- Price scenarios, USD per million tokens (Table 4) ----
scenarios = {
    "Low":  (0.20, 0.60),
    "Base": (1.00, 4.00),
    "High": (3.00, 15.00),
}

# ---- People (Section 6.6) ----
engineer_month = 20_000
engineer_day = engineer_month / 20

M = 1_000_000
print(f"calls = {calls:,}; construction input = {calls*prompt_in/M:.1f}M, output = {calls*construct_out/M:.1f}M tokens")
print(f"population input = {calls*pop_in/M:.1f}M, output = {calls*pop_out/M:.1f}M tokens\n")

hdr = f"{'Scenario':8s} {'Construct':>10s} {'Populate':>10s} {'Build':>8s} {'Per ans graph':>14s} {'Per ans L1':>11s} {'Eng-days':>9s} {'People/Build':>13s} {'Build/Answer':>13s}"
print(hdr)
for name, (p_in, p_out) in scenarios.items():
    construct = calls * (prompt_in * p_in + construct_out * p_out) / M
    populate = calls * (pop_in * p_in + pop_out * p_out) / M
    build = construct + populate
    ans_graph = ((q + x_graph) * p_in + a * p_out) / M
    ans_plain = ((q + x_plain) * p_in + a * p_out) / M
    print(f"{name:8s} {construct:10.0f} {populate:10.0f} {build:8.0f} {ans_graph:14.4f} {ans_plain:11.4f} "
          f"{build/engineer_day:9.2f} {engineer_month/build:13.0f}x {build/ans_graph:13,.0f}x")

print("\nOrders of magnitude (log10) between steps, people -> build -> per answer:")
import math
for name, (p_in, p_out) in scenarios.items():
    construct = calls * (prompt_in * p_in + construct_out * p_out) / M
    populate = calls * (pop_in * p_in + pop_out * p_out) / M
    build = construct + populate
    ans_graph = ((q + x_graph) * p_in + a * p_out) / M
    print(f"{name:8s} people/build = {math.log10(engineer_month/build):.1f}   build/answer = {math.log10(build/ans_graph):.1f}")
