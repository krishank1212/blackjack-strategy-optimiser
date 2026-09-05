# About the project

This project implements a full blackjack game engine from first principles and uses stochastic local search to test whether a strategy can be improved through direct simulation, starting from a deliberately poor policy, rather than by looking up a published strategy table. The aim was not to build a card-counting or advantage-play system, but to see whether hill-climbing over the space of possible strategies can rediscover something close to known-optimal basic strategy purely from simulated outcomes, and to understand precisely where such a search spends its budget when it falls short.

The game engine supports 6-deck shoes (configurable), splits (including re-splitting), doubling, blackjack payouts, and soft/hard hand tracking, all implemented without an external blackjack library.

---

# How it's made

## Game representation

A hand is represented by `Hand`, which tracks cards and computes its value with Ace soft/hard adjustment: an Ace counts as 11 unless that would bust the hand, in which case it counts as 1. A hand is `soft` if it still holds an Ace counted as 11.

A game state for strategy purposes is encoded as:

$$(\text{hand\_type}, \text{value}, \text{dealer\_upcard})$$

where `hand_type` is one of `hard`, `soft`, or `pair`. Pairs are encoded by rank rather than total value, since the optimal action for a pair depends on the rank, not the numeric total (a pair of 8s and a hard 16 share a total but call for very different decisions). There are 390 such states in total.

## Legal action pruning

`legal_actions` never offers `stand` at a hard total of 11 or below. This is not a house-rule restriction; it's a provably correct pruning of a dominated action. Since the highest single card value is 10, any hard total ≤ 11 cannot bust on the next card, so hitting can only leave the total unchanged or higher, and never introduces bust risk that wasn't already possible at the current total. Given the dealer's play is fixed, a weakly higher total can only tie or beat at least as many dealer outcomes as a lower one. Standing below 12 is therefore strictly dominated by hitting, and excluding it from the legal action set removes a portion of the search space that could never contain an optimal policy, rather than constraining what the optimiser can discover.

## Hill-climbing optimisation

`optimise.py` performs stochastic local search directly on the strategy dictionary:

1. Start from a deliberately poor policy (`always_hit_strategy`, which hits at every state including pairs) rather than an approximate basic-strategy baseline, so any improvement found is attributable to the search itself rather than inherited from a good starting point.
2. At each iteration, `mutate_strategy` changes the action at exactly one randomly chosen state to a different legal alternative.
3. The candidate is screened on a small sample (`num_games / 10`). If it beats the current EV by more than $\epsilon_1 = 1/\sqrt{N/10}$, it's re-evaluated on the full sample size against a tighter threshold $\epsilon_2 = 1/\sqrt{N}$.
4. Only mutations clearing both thresholds are accepted and folded into the running strategy.

The two-stage screen exists because a single hand resolves to roughly ±1 or ±2 units, so accepting on a single small-sample comparison would let through a large number of spurious improvements. The thresholds approximate a standard error scale rather than a formal confidence interval.

The optimised strategy and its EV history (an `(iteration, ev)` pair recorded on every accepted mutation) are returned by `optimise_strategy` and explicitly captured and pickled by the caller, rather than being saved from inside the function itself.

---

# Implementation

- `cards.py`: `Card` and `Deck`. The deck stores its own `no_of_decks` at construction and reshuffles by reinitialising with that same value, so an internally triggered reshuffle (the shoe running out mid-draw) rebuilds the original shoe size rather than silently collapsing to a single deck.
- `hand.py`: `Hand`, with soft/hard value tracking and blackjack/bust detection.
- `play_strategy.py`: state encoding, the pruned legal-action set, the always-hit seed strategy, and an approximate basic-strategy baseline used only for validating the engine.
- `game.py`: full round logic, including split handling (new hands are appended to a list and processed sequentially), doubling, and blackjack payouts.
- `simulation.py`: `evaluate_ev`, a flat-bet Monte Carlo evaluator used inside optimisation.
- `strategy_optimiser.py`: single-state mutation logic for hill-climbing.
- `optimise.py`: the hill-climbing loop described above.

---

# Experimental setup

- Shoe size: 6 decks
- Betting: flat £1 per hand throughout (no bet-sizing or card-counting component)
- Hill-climbing: seeded from `always_hit_strategy`, 1,000 iterations, screening sample of 20,000 games, confirmation sample of 200,000 games
- Baseline validation: approximate basic-strategy policy evaluated over 10,000,000 games

---

# Quantitative results

| Strategy | EV per £ wagered | Sample size |
|---|---|---|
| Always-hit (hill-climbing seed) | -0.884598 | 200,000 |
| Hill-climbing result (1,000 iterations) | -0.234884 | 200,000 |
| Baseline (approximate basic strategy) | -0.0040 | 10,000,000 |

The baseline figure sits within the range of published house-edge estimates for 6-deck blackjack under comparable rules, which serves as the sanity check that the engine itself is implemented correctly, independent of anything the optimiser does.

## State-level breakdown

To understand *why* the gap to baseline remains large, the final optimised strategy was compared state-by-state against both the seed and the basic-strategy baseline, across all 390 states:

| Category | Count | Share |
|---|---|---|
| Untouched, and happens to match baseline ("lucky") | 127 | 32.6% |
| Untouched, and disagrees with baseline | 201 | 51.5% |
| Mutated, and now matches baseline | 43 | 11.0% |
| Mutated, but still disagrees with baseline | 19 | 4.9% |

Combining the first two rows: **328 of 390 states (84.1%) were never successfully mutated away from the seed action at all.** Of the remaining 62 states that were changed, 43 landed on the correct action and 19 did not, roughly a 70/30 split. This is consistent with the 66 accepted mutations recorded across the full run (66 accepted mutations producing 62 states differing from the seed implies a small number of states, likely one or two, were mutated more than once, with a later mutation landing back on the original seed action; the exact path can't be recovered from the final strategy alone, only from a per-state log recorded during the run itself).

<img width="1256" height="500" alt="EV vs iteration during hill-climbing" src="ev_convergence.png" />

*EV per £ wagered against iteration number, plotted from the `history` list returned by `optimise_strategy` (66 points, one per accepted mutation). Notably, the curve is still stepping upward at iteration ~970 with no visible plateau, indicating the search had not stalled at a local optimum by the end of the run.*

---

# Analysis

The state-level breakdown reframes what limits this optimiser, and the reframing matters: it is not primarily a **coverage** problem (not enough of the 390 states were ever attempted), it is primarily an **acceptance-rate** problem. Only 66 of 1,000 proposed mutations were ever accepted, meaning the overwhelming majority of iterations proposed a change that failed to clear the screening threshold, the confirmation threshold, or both. Given each hand resolves to roughly ±1 to ±2 units and a single-state action change typically shifts EV by a small fraction of a percentage point, most single-state effects at this sample size are genuinely close to the noise floor the thresholds are designed to filter out, so a low acceptance rate is largely expected behaviour rather than a bug. The roughly 70/30 split between correctly and incorrectly mutated states (43 vs 19) suggests that when a mutation does clear both thresholds, it is right considerably more often than not, though a nontrivial minority of accepted mutations still move a state to an action that is still wrong, consistent with the thresholds being an approximate standard-error scale rather than a rigorous test, as noted above.

The convergence plot supports the acceptance-rate framing further: EV is still stepping upward at iteration ~970, with no flat plateau where acceptance visibly drops to zero. This indicates the search had not stalled at a local optimum by the end of the run; it was simply proposing improving mutations at a low and roughly steady rate throughout. Had the plot flattened out well before iteration 1000, that would instead point toward the search being stuck (no further single-state change could clear the threshold, even though multi-state changes might), which would call for a different remedy than more compute.

Because the plot rules out a stall, the natural next step is comparatively low-risk: run the same procedure for more iterations, or increase the sample sizes used at the screening/confirmation stages to raise statistical power (which should both increase the acceptance rate for genuinely improving mutations and reduce the fraction of accepted mutations that land on a still-incorrect action). Distinguishing which of these two changes matters more would be a natural follow-up experiment.

---

# Limitations

- **No card counting or bet variation**: the engine and optimiser use flat betting throughout, so no advantage-play mechanism is modelled.
- **Heuristic significance thresholds**: the hill-climbing acceptance criterion approximates a standard error scale rather than a formal statistical test, so individual accepted mutations may still occasionally reflect sampling noise rather than genuine improvement, as reflected in the 25 states mutated to a still-incorrect action.
- **Single mutation per iteration, low acceptance rate**: only one state's action is proposed per iteration, and only 66 of 1,000 proposals were ever accepted. This is the dominant constraint on how far the search progresses within a fixed iteration budget, more so than the size of the state space itself.
- **Mutation history not logged per state**: the final pickled strategy only records the end state, not the sequence of mutations applied to each state. A state that ends at the seed action is consistent with, but not proof of, having never been selected for mutation; a small number of states may have been mutated more than once. Confirming this precisely would require logging the mutated state at every accepted step during the run, not just the resulting EV.

---

# Lessons learnt

This project reinforced the importance of:

- validating a simulation engine against a known external benchmark (published basic-strategy house edge) before trusting any result built on top of it,
- distinguishing a genuinely dominated action from an arbitrary house-rule constraint, and proving the former rather than assuming it,
- guarding against noise-driven acceptance in an optimisation loop when the underlying signal (a single hand's outcome) is high-variance relative to the effect size being searched for,
- breaking down an aggregate result into its state-level components before drawing conclusions about *why* a search fell short, since the same overall gap to baseline can arise from very different underlying causes (insufficient coverage vs. an overly strict or noisy acceptance criterion), and only a state-level check can distinguish between them,
- being explicit about what a result does and doesn't prove: the final pickled strategy alone could not confirm whether "untouched" states were truly never selected for mutation, only that they ended up back at the seed action, which needed to be stated as a limitation rather than assumed away.