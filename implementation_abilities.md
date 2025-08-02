# Representative Ability Implementation Guide

This document specifies a compact yet comprehensive subset of abilities whose implementation will exercise **every major ability-driven effect class** needed by the battle engine. Abilities are grouped by the pattern they demonstrate. Each ability name appears exactly as in _data/abilities.json_.

---

## 1. Weather-Setting Abilities (on entry)

| Ability          | Trigger                        | In-Game Effect                                                                          | Implementation Notes                                       |
| ---------------- | ------------------------------ | --------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **drizzle**      | When the Pokémon enters battle | Sets rain that persists until another weather replaces it.                              | Effect Class: `SetWeather(on_enter, weather=RAIN)`         |
| **drought**      | On entry                       | Sets harsh sunlight until replaced.                                                     | Same as above with `SUN`                                   |
| **sand-stream**  | On entry                       | Sets a sandstorm until replaced.                                                        | Same pattern → `SANDSTORM`                                 |
| **snow-warning** | On entry                       | Sets hail (snow) until replaced.                                                        | `HAIL` weather constant                                    |
| **delta-stream** | On entry / ability gain        | Starts "mysterious air current" (no super-effective Flying weakness) until user leaves. | Requires custom `SetWeather` variant & damage-mod override |

---

## 2. Type Immunity / Absorption Abilities

| Ability           | Effect                                                                                 | Implementation Notes                                                    |
| ----------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **volt-absorb**   | When an Electric move hits, heal ¼ max HP; move has no other effect.                   | `TypeAbsorb(heal_fraction=0.25, type=ELECTRIC)`                         |
| **water-absorb**  | Heals versus Water moves.                                                              | Same class with `WATER`                                                 |
| **flash-fire**    | Grants immunity to Fire moves and boosts own Fire move power by 50 % after activation. | Combine `TypeAbsorb(boost_flag=True)` + `MultiplyMovePower` conditional |
| **lightning-rod** | Redirects single-target Electric moves to self and raises Sp. Atk by 1 stage.          | `MoveRedirection(type=ELECTRIC)` + `ModifyStatStage`                    |
| **storm-drain**   | Same for Water moves, boosts Sp. Atk.                                                  | Reuse with `WATER`                                                      |

---

## 3. Damage Modification Abilities

| Ability         | Scope                           | Effect                                    | Implementation Notes                                 |
| --------------- | ------------------------------- | ----------------------------------------- | ---------------------------------------------------- |
| **technician**  | User's moves                    | 1.5× power if base power ≤ 60.            | `MultiplyMovePower` with conditional `power≤60`      |
| **tinted-lens** | User's moves                    | Doubles power of not-very-effective hits. | `MultiplyMoveDamage` after type effectiveness        |
| **huge-power**  | User                            | Doubles Attack stat.                      | `StatMultiplier(ATTACK, 2.0)` applied in stat getter |
| **sniper**      | User's moves                    | Crit damage × 2.25 instead of × 1.5.      | `CritModifier(multiplier=2.25)`                      |
| **iron-fist**   | Punching moves gain 1.2× power. | `TaggedMovePowerBoost(tag=PUNCH, 1.2)`    |

---

## 4. Stat Modification Abilities

### 4.1 On-Entry

| Ability        | Effect                                            | Notes                                                       |
| -------------- | ------------------------------------------------- | ----------------------------------------------------------- |
| **intimidate** | Lowers adjacent foes' Attack by 1 stage on entry. | `ModifyStatStage(targets=opponents, stat=ATTACK, delta=-1)` |

### 4.2 Turn-End

| Ability         | Effect                                           | Notes                                   |
| --------------- | ------------------------------------------------ | --------------------------------------- |
| **speed-boost** | Raises Speed by 1 stage after each turn.         | `TurnEndStatStage(+1, SPEED)`           |
| **moody**       | Each turn: +2 to one random stat, –1 to another. | Custom `TurnEndRandomStageShift` effect |

### 4.3 Conditional

| Ability      | Condition                       | Effect                                      |
| ------------ | ------------------------------- | ------------------------------------------- |
| **moxie**    | After this Pokémon KOs a foe    | +1 Attack stage (`OnKOStatStage`)           |
| **berserk**  | HP drops below 50 % from damage | +1 Sp. Atk (`HPThresholdStatStage`)         |
| **stakeout** | Target switched-in this turn    | Damage dealt × 2 (`ConditionalDamageBoost`) |

---

## 5. Contact Effect Abilities

| Ability          | Effect                                               | Implementation                                 |
| ---------------- | ---------------------------------------------------- | ---------------------------------------------- |
| **static**       | 30 % chance to paralyze attacker on contact.         | `ContactStatusChance(status=PARALYSIS, p=0.3)` |
| **rough-skin**   | Attacker takes 1/8 max HP damage on contact.         | `ContactRecoil(damage_frac=0.125)`             |
| **flame-body**   | 30 % chance to burn attacker on contact.             | Same class with BURN                           |
| **effect-spore** | 30 % chance: random PARALYSIS/BURN/SLEEP on contact. | `ContactRandomStatus`                          |
| **iron-barbs**   | Same recoil as rough-skin (Steel flavor).            | Reuse `ContactRecoil`                          |

---

## 6. Status Prevention Abilities

| Ability          | Prevents                   | Extra Detail                                                            | Implementation              |
| ---------------- | -------------------------- | ----------------------------------------------------------------------- | --------------------------- |
| **limber**       | Paralysis                  | Heals if already paralyzed upon gaining ability.                        | `StatusImmunity(PARALYSIS)` |
| **immunity**     | Poison / Badly Poison      | Same comments.                                                          | `StatusImmunity(POISON)`    |
| **insomnia**     | Sleep                      |                                                                         | `StatusImmunity(SLEEP)`     |
| **water-bubble** | Burn + halves Fire damage. | Combines `StatusImmunity(BURN)` + `MultiplyDamageTaken(type=FIRE, 0.5)` |
| **own-tempo**    | Confusion                  |                                                                         | `StatusImmunity(CONFUSION)` |

---

## 7. Move Modification Abilities

| Ability          | Modification                                            | Implementation                                   |
| ---------------- | ------------------------------------------------------- | ------------------------------------------------ |
| **prankster**    | User's status moves get +1 priority.                    | `ModifyMovePriority(condition=STATUS, delta=+1)` |
| **serene-grace** | Doubles chance of secondary effects.                    | `SecondaryEffectChanceMultiplier(2.0)`           |
| **sheer-force**  | Removes secondary effects but +30 % power.              | `RemoveSecondaries+MultiplyMovePower(1.3)`       |
| **normalize**    | All user moves become Normal type & get 1.2× power.     | `ChangeMoveType(NORMAL)` + booster               |
| **color-change** | After taking damage, user's type becomes attack's type. | `PostHitTypeChange` (complex)                    |

---

## 8. Priority Changing Abilities

| Ability             | Effect                                                  | Notes                                     |
| ------------------- | ------------------------------------------------------- | ----------------------------------------- |
| **gale-wings**      | Flying moves get +1 priority when user at full HP.      | `ConditionalPriorityBoost(type=FLYING)`   |
| **triage**          | Healing moves get +3 priority.                          | `TaggedPriorityBoost(tag=HEAL, delta=+3)` |
| **stall**           | User's moves act last in priority bracket.              | `PriorityOverride(to_last=True)`          |
| **dazzling**        | Prevents opponents' priority moves from hitting allies. | `PriorityBlock(opponent_moves)`           |
| **queenly-majesty** | Prevents opponents' priority moves from hitting allies. | `PriorityBlock(opponent_moves)`           |

---

## 9. Field / Terrain Abilities

| Ability            | Trigger      | Effect                                                          | Implementation                                      |
| ------------------ | ------------ | --------------------------------------------------------------- | --------------------------------------------------- |
| **electric-surge** | On entry     | Creates electric terrain for 5 turns.                           | `SetTerrain(ELECTRIC, 5)`                           |
| **psychic-surge**  | On entry     | Creates psychic terrain (blocks priority on grounded foes).     | `SetTerrain(PSYCHIC)` + affects `PriorityCheck`     |
| **grassy-surge**   | On entry     | Grassy terrain: heals 1/16 HP each turn, boosts Grass moves.    | Terrain system + heal residual                      |
| **misty-surge**    | On entry     | Misty terrain: halves Dragon damage, prevents status on ground. | Terrain hooks for damage & status                   |
| **aura-break**     | While active | Reverses power of Dark/Fairy aura abilities.                    | `GlobalAuraModifier(multiplier=2/3)` (special case) |

---

## 10. Complex Conditional Abilities

| Ability                       | Complexity     | Key Behaviours                                                     | Implementation Concepts                                                   |
| ----------------------------- | -------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| **wonder-guard**              | Damage filter  | Takes damage only from super-effective moves & fixed-damage moves. | `DamageFilter(require_super_effective=True)`                              |
| **trace**                     | Ability copy   | On entry, copies a random opponent's ability.                      | `AbilityReplace(copy_target)`; needs event after ability activation order |
| **imposter**                  | Auto-Transform | On entry, transforms into random opponent.                         | Re-use move _transform_ logic in ability                                  |
| **moody**                     | Stat lottery   | End-turn +2 random stat, –1 different random stat.                 | `TurnEndRandomStageShift`                                                 |
| **wimp-out / emergency-exit** | HP threshold   | Switches user out when HP drops below 50 % after being hit.        | `ForcedSelfSwitch(once_when_hp<0.5)`                                      |

---

### Effect-Class Coverage Recap

| Effect Class                                           | Demonstrated By                  |
| ------------------------------------------------------ | -------------------------------- |
| `SetWeather`                                           | drizzle, drought                 |
| `TypeAbsorb`                                           | volt-absorb                      |
| `MultiplyMovePower/Damage`                             | technician, tinted-lens          |
| `StatMultiplier / ModifyStatStage`                     | huge-power, speed-boost          |
| `ContactRecoil / ContactStatusChance`                  | rough-skin, static               |
| `StatusImmunity`                                       | limber, immunity                 |
| `ModifyMovePriority`                                   | prankster, gale-wings            |
| `PriorityBlock`                                        | queenly-majesty                  |
| `SetTerrain`                                           | electric-surge                   |
| `DamageFilter`                                         | wonder-guard                     |
| Advanced (copy/transform, forced switch, random shift) | trace, imposter, moody, wimp-out |

Implementing the 40 abilities in this guide will activate **all major ability-driven pathways** in the engine, ensuring subsequent abilities can be added by simple data mapping or small extensions.

**Note on Missing Data Fields:** The current data structure in _data/abilities.json_ does not include certain fields that may be needed for complete implementation:

1. Move tags that abilities interact with (punch, sound, contact, etc.)
2. Ability activation conditions (on entry, on hit, etc.)
3. Priority modification values
4. Stat modification values and targets

These additional fields should be added to the data model or inferred from effect text before implementing the corresponding effect classes.
