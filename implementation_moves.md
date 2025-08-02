# Representative Move Implementation Guide

This guide lists a compact move set that, once implemented, exercises **every major Effect class** identified for the battle engine. Each move below appears verbatim in _data/moves.json_.

---

## 1. Basic Damage Moves

| Move             | Pwr / Acc | Type · Cat        | Effect                      | Effect Classes                      |
| ---------------- | --------- | ----------------- | --------------------------- | ----------------------------------- |
| **Pound**        | 40 / 100  | Normal · Physical | Inflicts regular damage.    | `DoMoveDamage`                      |
| **Flamethrower** | 90 / 100  | Fire · Special    | 10 % chance to burn target. | `DoMoveDamage`, `InflictStatus`     |
| **Stone Edge**   | 100 / 80  | Rock · Physical   | High critical-hit ratio.    | `DoMoveDamage`, `CriticalRateStage` |

_Implementation notes_: Baseline damage, elemental typing, critical stage increase.

---

## 2. Priority Moves

| Move             | Pwr / Acc | Type · Cat        | Priority | Effect                                           | Effect Classes                 |
| ---------------- | --------- | ----------------- | -------- | ------------------------------------------------ | ------------------------------ |
| **Quick Attack** | 40 / 100  | Normal · Physical | +1       | Inflicts regular damage with increased priority. | `DoMoveDamage`, `PriorityMove` |

_Implementation notes_: Moves with priority values execute before normal-priority moves, regardless of Speed stat.

---

## 3. Secondary-Effect Moves

| Move              | Pwr / Acc | Type     | Effect                         | Effect Classes                    |
| ----------------- | --------- | -------- | ------------------------------ | --------------------------------- |
| **Thunder Punch** | 75 / 100  | Electric | 10 % chance to paralyze.       | `DoMoveDamage`, `InflictStatus`   |
| **Shadow Ball**   | 80 / 100  | Ghost    | 20 % chance to ↓ Sp. Def (-1). | `DoMoveDamage`, `ModifyStatStage` |
| **Poison Fang**   | 50 / 100  | Poison   | 50 % chance to badly poison.   | `DoMoveDamage`, `InflictStatus`   |

---

## 4. Multi-Hit Moves

| Move            | Pwr / Acc | Hits | Effect                   | Effect Classes                    |
| --------------- | --------- | ---- | ------------------------ | --------------------------------- |
| **Double Slap** | 15 / 85   | 2-5  | Standard multi-hit.      | `MultiHit`, `DoMoveDamage`        |
| **Triple Kick** | 10 / 90   | 3    | Each hit ×1,×2,×3 power. | `MultiHit` (variable power logic) |
| **Tail Slap**   | 25 / 85   | 2-5  | Skill-Link synergy.      | `MultiHit`                        |

_Implementation notes_: Requires per-hit accuracy & crit.

---

## 5. Two-Turn Moves

| Move           | Pwr / Acc | Flow                                      | Effect Classes                          |
| -------------- | --------- | ----------------------------------------- | --------------------------------------- |
| **Solar Beam** | 120 / 100 | Charge 1 → Attack 2 (skip charge in Sun). | `GuaranteedTwoTurn`                     |
| **Fly**        | 90 / 95   | Semi-invulnerable turn 1, hit turn 2.     | `SemiInvulnerable`, `GuaranteedTwoTurn` |
| **Hyper Beam** | 150 / 90  | Attack, then recharge (skip turn).        | `DoMoveDamage`, `MustRecharge`          |

---

## 6. Stat Manipulation Moves

| Move             | Category | Effect                                | Effect Classes    |
| ---------------- | -------- | ------------------------------------- | ----------------- |
| **Swords Dance** | Status   | Raise Attack +2 (self).               | `ModifyStatStage` |
| **Charm**        | Status   | Lowers target Attack -2.              | `ModifyStatStage` |
| **Power Swap**   | Status   | Swaps Atk/SpA stage mods with target. | `SwapStatStage`   |

---

## 7. Field Hazards

| Move             | Effect                                                    | Effect Classes                 |
| ---------------- | --------------------------------------------------------- | ------------------------------ |
| **Stealth Rock** | Damages Pokémon on switch-in (1/8-1/2 based on weakness). | `LayerHazard`, `EntryDamage`   |
| **Spikes**       | Up to 3 layers; 1/8 / 1/6 / 1/4 entry damage.             | `LayerHazard`, `EntryDamage`   |
| **Toxic Spikes** | Poison(s) grounded Pokémon on entry.                      | `LayerHazard`, `InflictStatus` |

---

## 8. Weather / Terrain Setting Moves

| Move                 | Turns | Effect                                                      | Effect Classes |
| -------------------- | ----- | ----------------------------------------------------------- | -------------- |
| **Rain Dance**       | 5     | Sets rain weather.                                          | `SetWeather`   |
| **Sunny Day**        | 5     | Sets harsh sunlight.                                        | `SetWeather`   |
| **Electric Terrain** | 5     | Creates electric terrain (prevents sleep, boosts Electric). | `SetTerrain`   |

---

## 9. Healing / Drain Moves

| Move           | Type   | Effect                                    | Effect Classes                  |
| -------------- | ------ | ----------------------------------------- | ------------------------------- |
| **Recover**    | Normal | Heals user 50 % max HP.                   | `PercentHealUser`               |
| **Giga Drain** | Grass  | Damages & heals 50 % of damage dealt.     | `DoMoveDamage`, `DrainDamage`   |
| **Leech Seed** | Grass  | Seeds target; heal user 1/8 HP each turn. | `ResidualEffect`, `DrainDamage` |

---

## 10. Switching Moves

| Move            | Pwr / Acc | Effect                                                 | Effect Classes                  |
| --------------- | --------- | ------------------------------------------------------ | ------------------------------- |
| **U-turn**      | 70 / 100  | After damage, user switches out.                       | `DoMoveDamage`, `UserSwitchOut` |
| **Volt Switch** | 70 / 100  | Same as U-turn for Electric type.                      | `DoMoveDamage`, `UserSwitchOut` |
| **Whirlwind**   | — / —     | Forces target to switch; fails vs. Substitute/protect. | `ForceSwitch`                   |

---

### Coverage Matrix

| Effect Class              | Covered By                                     |
| ------------------------- | ---------------------------------------------- |
| DoMoveDamage              | Pound, Thunder Punch, etc.                     |
| PriorityMove              | Quick Attack                                   |
| InflictStatus             | Thunder Punch, Poison Fang, Toxic Spikes       |
| ModifyStatStage           | Shadow Ball, Swords Dance, Charm               |
| CriticalRateStage         | Stone Edge                                     |
| MultiHit                  | Double Slap, Triple Kick                       |
| GuaranteedTwoTurn         | Solar Beam, Fly                                |
| MustRecharge              | Hyper Beam                                     |
| SemiInvulnerable          | Fly                                            |
| SwapStatStage             | Power Swap                                     |
| LayerHazard / EntryDamage | Stealth Rock, Spikes                           |
| SetWeather / Terrain      | Rain Dance, Electric Terrain                   |
| PercentHealUser           | Recover                                        |
| DrainDamage               | Giga Drain, Leech Seed                         |
| ResidualEffect            | Leech Seed, TrapBind via Bind (multi-category) |
| UserSwitchOut             | U-turn                                         |
| ForceSwitch               | Whirlwind                                      |

With these 28 representative moves implemented, every high-priority effect pathway is exercised, ensuring the battle engine supports the full spectrum of mechanics before scaling to the remaining 800+ moves.

**Note on Data Structure:** The data structure in _data/moves.json_ now includes priority values, which should be used to determine move execution order. For a complete implementation, the data would still need to be extended to include:

1. Move tags (punch, sound, etc.) for ability interactions
2. Contact flags for abilities like Static, Flame Body
