# Representative Held Item Implementation Guide

This document lists a concise but exhaustive set of **held items** whose implementation will exercise **every major item–driven effect pathway** in the battle engine.
Each item name exactly matches the entry in _data/items.json_ and excludes medicines, Poké Balls, and other non-battle gear.

---

## 1. Passive Healing Items

| Item             | Trigger                   | Exact Effect                                                     | Effect Class                                            |
| ---------------- | ------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- |
| **leftovers**    | End of each turn          | Heals 1/16 of holder’s max HP.                                   | `ResidualHeal(fraction=1/16)`                           |
| **black-sludge** | End of turn               | Heals Poison-type holders by 1/16 HP; damages others by 1/16 HP. | `ConditionalResidualHeal` & `ConditionalResidualDamage` |
| **shell-bell**   | After holder deals damage | Restores HP equal to ⅛ of damage inflicted.                      | `OnDamageDealtHeal(ratio=0.125)`                        |

_Implementation note_: Residual effects tie into the `TurnEnd` phase; on-damage trigger hooks into `after_damage` event.

---

## 2. Damage Modification Items

| Item            | Scope                                      | Exact Effect                                                     | Effect Class                                            |
| --------------- | ------------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------- |
| **life-orb**    | Holder’s damaging moves                    | +30 % damage; holder loses 10 % max HP after each damaging move. | `MultiplyMoveDamage(1.3)` + `RecoilFixedFraction(0.10)` |
| **expert-belt** | Holder’s moves vs. super-effective targets | Damage × 1.2                                                     | `ConditionalDamageBoost(super_effective, 1.2)`          |
| **muscle-band** | Holder’s _physical_ moves                  | Damage × 1.1                                                     | `TaggedMovePowerBoost(category=PHYSICAL, 1.1)`          |

---

## 3. Stat Boosting Items

| Item             | Trigger | Exact Effect                          | Effect Class                                  |
| ---------------- | ------- | ------------------------------------- | --------------------------------------------- |
| **wise-glasses** | Passive | Holder’s _special_ moves × 1.1 power. | `TaggedMovePowerBoost(category=SPECIAL, 1.1)` |
| **razor-claw**   | Passive | Holder’s critical-hit ratio +1 stage. | `CritStageBoost(+1)`                          |
| **scope-lens**   | Passive | Same as Razor Claw (alt item).        | Re-uses `CritStageBoost`                      |

---

## 4. Choice Items (-Lock Mechanics)

| Item             | Boost         | Lock Rule                                                    | Effect Class                         |
| ---------------- | ------------- | ------------------------------------------------------------ | ------------------------------------ |
| **choice-band**  | Attack × 1.5  | Locks holder into first move used until it leaves the field. | `ChoiceLock(stat_boost=ATTACK, 1.5)` |
| **choice-specs** | Sp. Atk × 1.5 | Same lock.                                                   | `ChoiceLock(stat_boost=SP_ATK, 1.5)` |
| **choice-scarf** | Speed × 1.5   | Same lock.                                                   | `ChoiceLock(stat_boost=SPEED, 1.5)`  |

_Implementation note_: store `locked_move_id` in Pokémon state; prevent selection of other moves while item is held and Pokémon remains active.

---

## 5. Type Enhancement Items

| Item             | Type   | Exact Effect                 | Effect Class                    |
| ---------------- | ------ | ---------------------------- | ------------------------------- |
| **flame-plate**  | Fire   | Fire-type moves × 1.2 (20 %) | `TypeMovePowerBoost(FIRE, 1.2)` |
| **splash-plate** | Water  | Water moves × 1.2            | Same class (`WATER`)            |
| **sky-plate**    | Flying | Flying moves × 1.2           | Same class (`FLYING`)           |

All 17 plates map to the same effect class with a `type` parameter.

---

## 6. Status-Related Items

| Item             | Trigger                            | Exact Effect                          | Effect Class                  |
| ---------------- | ---------------------------------- | ------------------------------------- | ----------------------------- |
| **lum-berry**    | When holder gains any major status | Consumed; cures status.               | `ConsumeOnStatus(CURE_ALL)`   |
| **flame-orb**    | End of turn                        | Burns holder if not already statused. | `SelfInflictStatus(BURN)`     |
| **toxic-orb**    | End of turn                        | Badly poisons holder.                 | `SelfInflictStatus(TOXIC)`    |
| **chesto-berry** | When holder is asleep              | Consumed; wakes up.                   | `ConsumeOnStatus(SLEEP_CURE)` |

---

## 7. Conditional Trigger Items

| Item                | Condition                                      | Effect                                    | Effect Class                                     |
| ------------------- | ---------------------------------------------- | ----------------------------------------- | ------------------------------------------------ |
| **focus-sash**      | Holder at full HP & attacked for lethal damage | Survive with 1 HP; item consumed.         | `DamagePreventionOnce(condition=full_hp)`        |
| **weakness-policy** | Hit by super-effective move                    | +2 Attack & Sp. Atk; item consumed.       | `OnSuperEffectiveStatStageBoost(+2, ATK+SP_ATK)` |
| **custap-berry**    | HP ≤ 25 % at turn start                        | Acts first in priority bracket; consumed. | `LowHPPriorityBoost(once=True)`                  |
| **eject-button**    | Hit by damaging move (survive)                 | Holder switches out immediately.          | `OnHitForcedSwitch(self_switch=True)`            |

---

## 8. Contact / Recoil Items

| Item                | Trigger                                | Effect                                                                        | Effect Class                                |
| ------------------- | -------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------- |
| **rocky-helmet**    | When holder is hit by a _contact_ move | Attacker takes 1/6 max HP damage.                                             | `ContactRecoil(damage_frac=1/6)`            |
| **sticky-barb**     | Passive / contact                      | Damages holder 1/8 HP each turn; transfers to attacker on contact hit.        | `ResidualDamage(1/8)` + `TransferOnContact` |
| **protective-pads** | Passive                                | Prevents **all** contact side-effects on holder (e.g., Rocky Helmet, Static). | `ContactEffectNegation`                     |

---

## 9. Weather / Terrain Extension Items

| Item                 | Affected Move/Ability      | Effect                             | Effect Class                                     |
| -------------------- | -------------------------- | ---------------------------------- | ------------------------------------------------ |
| **damp-rock**        | _Rain Dance_ / **drizzle** | Rain lasts 8 turns instead of 5.   | `WeatherDurationModifier(weather=RAIN, turns=8)` |
| **heat-rock**        | Sunlight moves/abilities   | Sunshine 8 turns.                  | Same class (`SUN`)                               |
| **icy-rock**         | Hail                       | 8 turns.                           | Same class (`HAIL`)                              |
| **terrain-extender** | Any terrain set            | Extends terrain from 5 to 8 turns. | `TerrainDurationModifier(8)`                     |

---

## 10. Complex Conditional Items

| Item               | Complexity                | Exact Effect                                                                        | Effect Class Notes                             |
| ------------------ | ------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------- |
| **quick-claw**     | Random priority           | 3/16 chance each turn to move first in its priority bracket.                        | `RandomPriorityBoost(prob=3/16)`               |
| **red-card**       | Reactive switch           | When holder is hit by a damaging move, attacker is forcibly switched out. Consumed. | `OnHitForceOpponentSwitch`                     |
| **lagging-tail**   | Always acts last          | Holder moves last within its priority bracket.                                      | `PriorityOverride(to_last=True)`               |
| **white-herb**     | Stat reset                | At end of turn, if any stat is negative, resets all negative stages; consumed.      | `EndTurnStatReset(negatives_only=True)`        |
| **safety-goggles** | Hazard & weather immunity | Holder immune to damage from sandstorm/hail and to powder moves (e.g., Spore).      | `WeatherDamageImmunity` + `PowderMoveImmunity` |

---

### Coverage Matrix

| Effect Class                           | Demonstrated By               |
| -------------------------------------- | ----------------------------- |
| ResidualHeal / ConditionalResidualHeal | leftovers, black-sludge       |
| OnDamageDealtHeal                      | shell-bell                    |
| MultiplyMoveDamage / Power             | life-orb, expert-belt         |
| ChoiceLock                             | choice items                  |
| TypeMovePowerBoost                     | plates                        |
| CritStageBoost                         | razor-claw                    |
| ConsumeOnStatus                        | lum-berry, chesto-berry       |
| SelfInflictStatus                      | flame-orb                     |
| DamagePreventionOnce                   | focus-sash                    |
| OnSuperEffectiveStatStageBoost         | weakness-policy               |
| ContactRecoil / ContactEffectNegation  | rocky-helmet, protective-pads |
| Weather/TerrainDurationModifier        | damp-rock, terrain-extender   |
| RandomPriorityBoost / PriorityOverride | quick-claw, lagging-tail      |
| OnHitForceOpponentSwitch               | red-card                      |
| TransferOnContact                      | sticky-barb                   |
| EndTurnStatReset                       | white-herb                    |

Implementing these **40 held items** will activate every significant item-related mechanic required by the battle engine; the remainder of the item list can then be added by simple data mapping with these effect classes.
