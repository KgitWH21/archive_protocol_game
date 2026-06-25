# Archive Protocol — Field Manual

*Classified Document // User: Jinhua_Ma // Clearance Level: SHADE*

---

## Overview

Archive Protocol is a turn-based card game set inside a military containment simulation. You play as **Shade**, an operative moving through three escalating sectors. Each sector contains a threat that must be neutralized before you can advance. The decisions you make between fights — and the cards you build your deck around — determine whether you make it out.

---

## Running the Game

```bash
pip install rich
python main.py
```

---

## The Run

A run consists of **3 sectors** played in sequence. Your HP carries over between sectors — damage you take in Sector 1 follows you into Sector 2. After clearing a sector you choose between resting or scavenging before the next fight.

### Enemies

| Sector | Enemy | HP | Attack Range |
|--------|-------|----|--------------|
| 1 | Awakened Cultist | 30 | 4–9 |
| 2 | Archive Sentinel | 45 | 6–13 |
| 3 | Okinawa Core Fragment | 65 | 8–18 |

---

## Combat

Each turn follows this sequence:

1. **You draw 3 cards** from your deck
2. **You play cards** until you run out of energy or choose to end your turn
3. **Unplayed cards** go to the discard pile
4. **The enemy attacks**
5. Energy and block reset; next turn begins

### Resources

- **HP** — you start at 50. Reach 0 and the run ends.
- **Energy** — you have 3 per turn. Each card costs energy to play.
- **Block** — absorbs incoming damage before HP. Resets to 0 at the end of each turn.

### Enemy Intent

Before you make a single decision, the enemy shows you exactly how hard it plans to hit. Use this to decide whether to prioritize dealing damage or stacking block.

- **Yellow intent** — light hit (under 10 damage)
- **Red intent** — heavy hit (10+ damage)

### Block Math

If an enemy hits for 9 and you have 6 block: you take 3 damage, block drops to 0.
If an enemy hits for 9 and you have 12 block: you take 0 damage, block drops to 3.

### Status Effects

Cards can apply persistent effects to enemies that last multiple turns.

- **Burn** — at the start of the enemy's turn, they take damage equal to their current Burn stacks, then Burn decreases by 1. Stacks accumulate if you apply it multiple times.
- **Vulnerable** — while active, your attacks deal **+50% damage** to that enemy. Decreases by 1 each turn.

The enemy panel shows active stacks in real time. A good combo: apply Vulnerable first, then follow up with a high-damage card the same turn to get the bonus immediately.

### Controls

| Input | Action |
|-------|--------|
| `1`, `2`, `3` | Play the corresponding card from your hand |
| `0` | End your turn |
| `d` | View your full deck, hand, and discard pile |

---

## The Deck

You start with 5 cards:

| Card | Cost | DMG | BLK | Notes |
|------|------|-----|-----|-------|
| CQB Strike | 1 | 8 | — | Bread and butter. You have two. |
| Suppressive Fire | 2 | 14 | — | Efficient damage at medium cost. |
| Stealth Protocol | 1 | — | 10 | Best block per energy in the starter deck. |
| Temporal Resonance | 2 | 5 | 5 | Split value. Good when you need both. |

Cards you play go to the **discard pile**. Unplayed cards also go to discard at end of turn. When your deck is empty, the discard reshuffles into a new deck automatically.

---

## Between Sectors

After clearing Sectors 1 and 2, you choose one of two options — you cannot take both.

| Choice | Effect |
|--------|--------|
| **REST** | Recover 15 HP |
| **SCAVENGE** | Choose one card from 3 random rewards to add to your deck |

Your current HP is shown alongside the REST option so you can make an informed call. If you're near full health, scavenging costs you nothing meaningful. If you took a beating, skipping a card to survive Sector 3 is often the right move.

## Card Rewards

When you Scavenge, you are shown **3 random cards** from the reward pool. Pick one to permanently add to your deck, or skip.

Adding a card makes your deck larger — which means more options but also more turns before you see any one card again. Choose cards that support how you're already playing, not just the highest numbers.

### Reward Pool

| Card | Cost | DMG | BLK | Burn | Vuln | Notes |
|------|------|-----|-----|------|------|-------|
| Frag Grenade | 2 | 18 | — | — | — | High damage, no frills. |
| Neural Disruptor | 2 | 10 | 5 | — | — | Solid hybrid. |
| Ghost Step | 1 | — | 15 | — | — | Best block in the pool. |
| Overcharge | 3 | 25 | — | — | — | Massive damage, expensive. |
| Reactive Armor | 2 | — | 12 | — | — | Pure defense at good value. |
| Tactical Reload | 0 | 4 | 4 | — | — | Free card. Always playable. |
| Cipher Blade | 1 | 11 | — | — | — | High damage per energy. |
| EMP Burst | 2 | 12 | 6 | — | — | Well-rounded. |
| Dead Drop | 1 | — | 8 | — | — | Cheap block. |
| Kinetic Surge | 3 | 20 | 8 | — | — | Best total value, highest cost. |
| Incendiary Round | 2 | 6 | — | 4 | — | Sets up sustained damage over next 4 turns. |
| Marked Target | 1 | 4 | — | — | 2 | Cheap setup. Play before a big damage card. |
| Napalm Protocol | 3 | 10 | — | 6 | — | Expensive but Burn 6 is devastating on tanky enemies. |
| Exploit Weakness | 2 | — | — | — | 3 | Pure setup. Pairs with Overcharge or Kinetic Surge for huge turns. |

---

## Strategy Notes

**Watch the intent every turn.** If the enemy is about to hit for 15 and you have Stealth Protocol in hand, playing it first changes the math entirely. If they're hitting for 5, you can ignore block and go pure offense.

**Tactical Reload is never a bad play.** It costs 0 energy and still puts value on the board. If you have leftover energy after your real plays, Tactical Reload turns dead turns into chip damage and block.

**The Sentinel and Core Fragment can two-shot you** if you're not managing block. By Sector 3 you should know whether your deck is offense-heavy or defense-heavy and lean into it rather than splitting.

**Bigger deck ≠ better deck.** Every card you add also dilutes your best cards. A focused 6-card deck that sees Overcharge twice per fight beats a 10-card deck where Overcharge appears once.

**Burn wins long fights, Vulnerable wins short ones.** Against the Core Fragment (65 HP), Burn 6 deals 21 damage over 6 turns for free. Against the Cultist (30 HP), you might kill it before Burn ticks twice — Vulnerable and a big hit is faster.

**Rest vs Scavenge isn't always obvious.** If you're at 40+ HP heading into Sector 2, Scavenge is almost always correct — the heal would be wasted. If you're at 20 HP, a bad Sector 2 can end the run before you even see your new card.

**Use `d` before committing to a plan.** If Exploit Weakness is in your discard and Overcharge is two cards deep in your deck, the combo isn't coming this fight. Knowing that early changes what you play now.

---

*End of Field Manual // Archive Protocol v0.1*
