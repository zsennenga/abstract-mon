# Effect Classes & Battle System Roadmap

This document scopes the remaining effect infrastructure for `abstract-mon`.
The analysis is derived from _data/moves.json_, _data/abilities.json_, and _data/items.json_.
Exclusions: catching mechanics, overworld/party effects, form change, and generation-specific gimmicks.

---

## 1. Effect Class Catalogue

### 1.1 Damage Modification

| Effect Class         | Applied By                                                                                                               | Notes                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| `MultiplyMovePower`  | Items (type-boost orbs/plates/berries), Abilities (e.g. **technician**, **solar-power**), Moves (conditional power mods) | Multiplier may depend on type, weather, HP, etc. Should stack multiplicatively. |
| `MultiplyMoveDamage` | Items (**Life Orb** exists), Abilities (**sniper**, **reckless**), Weather/Terrain                                       | Runs after power modifier, before random factor.                                |
| `RecoilDamage`       | Moves (**Take Down**, **Flare Blitz**), Items (**Life Orb**)                                                             | Accepts ratio (¼, ⅓, etc.) and whether it can KO the user.                      |
| `CrashDamage`        | Moves that damage user on miss (**Jump Kick**)                                                                           | Requires miss detection hook.                                                   |
| `FlinchChance`       | Abilities (**Stench**), Moves with secondary flinch chance                                                               | Needs interaction with move priority.                                           |
| `CriticalRateStage`  | Moves (**Karate Chop**), Items (**Scope Lens** later)                                                                    | Grants stage increments on use.                                                 |

### 1.2 Multi-Hit / Turn Sequencing

| Effect Class        | Applied By                               | Notes                                                              |
| ------------------- | ---------------------------------------- | ------------------------------------------------------------------ |
| `MultiHit`          | Moves (**Double Slap**, **Fury Swipes**) | Generates 2-5 hit loop, each hit independent accuracy & crit.      |
| `GuaranteedTwoTurn` | Moves (**Solar Beam**, **Skull Bash**)   | Stores "charging" state, executes next turn; handles weather skip. |
| `MustRecharge`      | Moves (**Hyper Beam**)                   | Marks user as unable to act next turn.                             |
| `TrapBind`          | Moves (**Bind**, **Wrap**)               | Adds residual damage and switch prevention for 2-5 turns.          |
| `SemiInvulnerable`  | Moves (**Dig**, **Fly**, **Dive**)       | Adds untargetable state with specific move exceptions.             |

### 1.3 Stat Stage Manipulation

| Effect Class        | Applied By                                                                   | Notes                                             |
| ------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------- |
| `ModifyStatStage`   | Dozens of status moves, abilities (**Intimidate**), items (X-items if added) | Supports ± stages, multiple stats, self/target.   |
| `SwapStatStage`     | Moves (**Power Swap**, **Guard Swap**)                                       | Swaps entire stage arrays between Pokémon.        |
| `TransferStatStage` | Moves (**Heart Swap**)                                                       | Copies from target to user.                       |
| `ResetEvasion`      | Move (**Chip Away** style)                                                   | Sets evasion stage to 0 and locks further boosts. |

### 1.4 Status Conditions

| Effect Class    | Applied By                                                                             | Notes                                   |
| --------------- | -------------------------------------------------------------------------------------- | --------------------------------------- |
| `InflictStatus` | Moves with burn/paralyze/freeze chance, Abilities (**Static**), Items (status berries) | Accepts status type and probability.    |
| `HealStatus`    | Items (Full Heal), Moves (**Aromatherapy**)                                            | For held-item triggers at end of turn.  |
| `PreventStatus` | Abilities (**Limber**), Items (**Safety Goggles** style)                               | Hooks into status application pipeline. |

### 1.5 Weather & Terrain

| Effect Class            | Applied By                                     | Notes                                                        |
| ----------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| `SetWeather`            | Abilities (**Drizzle**), Moves (**Sunny Day**) | Duration infinite/turn-based. Adds callbacks on damage calc. |
| `WeatherDamageImmunity` | Abilities (**Sand Veil** immunity portion)     | Cancels residual damage for holder.                          |
| `WeatherEvasionBoost`   | Abilities (**Sand Veil**)                      | Multiplies evasion 1.25× without stage.                      |

### 1.6 Field Hazards & Side Conditions

| Effect Class    | Applied By                                             | Notes                                        |
| --------------- | ------------------------------------------------------ | -------------------------------------------- |
| `LayerHazard`   | Moves (**Spikes**, **Toxic Spikes**, **Stealth Rock**) | Tracks layers, applies entry damage/effects. |
| `EntryDamage`   | System callback when Pokémon switches in               | Uses hazard state.                           |
| `HazardRemoval` | Moves (**Rapid Spin**, **Defog**)                      | Clears hazards.                              |

### 1.7 Switching & Turn Control

| Effect Class    | Applied By                                 | Notes                                         |
| --------------- | ------------------------------------------ | --------------------------------------------- |
| `ForceSwitch`   | Moves (**Roar**, **Whirlwind**)            | Ignores substitute, fails vs. Soundproof etc. |
| `UserSwitchOut` | Moves (**U-turn**, **Volt Switch**)        | Executes damage then opens selection UI.      |
| `PreventEscape` | Trap moves and abilities (**Shadow Tag**). |

### 1.8 Healing & Drain

| Effect Class      | Applied By                                        | Notes                                                              |
| ----------------- | ------------------------------------------------- | ------------------------------------------------------------------ |
| `PercentHealUser` | Moves (**Recover**, **Roost**), Items (Leftovers) | Accepts fraction.                                                  |
| `DrainDamage`     | Moves (**Absorb**, **Leech Life**)                | Heals user by % of damage dealt.                                   |
| `LeechSeed`       | Move of same name                                 | End-turn HP transfer; cancels if grass-type or flying when seeded. |

### 1.9 Type & Immunity Alteration

| Effect Class         | Applied By                           | Notes                                                 |
| -------------------- | ------------------------------------ | ----------------------------------------------------- |
| `TypeImmunityAbsorb` | Abilities (**Volt Absorb**, berries) | Converts would-be damage into healing or zero damage. |
| `GroundedState`      | Move (**Smack Down**), Gravity       | Removes levitation and Flying immunity.               |

---

## 2. Battle System State Extensions

1. **TurnPhase Tracker**
   Supports multi-step moves (`charging`, `recharging`, `semi_invulnerable`) with remaining turn counter.
2. **SideCondition Container**
   Stores hazards, Tailwind, screens, etc., per trainer side.
3. **Weather / Terrain Object**
   Already started; requires `duration` and `source` fields plus callback registry.
4. **ResidualEffect Registry**
   Generic structure holding per-Pokemon effects that tick at end of turn (Leech Seed, Bind, etc.).
5. **MoveLock State**
   Records forced move usage (Encore, Outrage) and move disable status.
6. **Flinch Flag**
   Boolean reset each turn; if set, Pokémon skips action.
7. **Recharge Flag**
   Marks Pokémon that must skip turn due to `MustRecharge`.

---

## 3. Odd Moves Requiring Special Treatment

Analysis identified approximately 141+ complex moves that require special implementation beyond standard effect classes. These are organized by complexity category below.

### 3.1 Turn Structure Manipulation

Moves that fundamentally alter the normal flow of turns:

| Move                                            | Complexity                                                                         |
| ----------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Bide**                                        | Stores accumulated damage for two turns, then deals double. Ignores type.          |
| **Hyper Beam** / **Giga Impact**                | User must recharge (skip turn) after use.                                          |
| **Outrage** / **Thrash** / **Petal Dance**      | Forces user to repeat move for 2-3 turns, then confuses.                           |
| **Uproar**                                      | Forces user to repeat move for 2-5 turns, prevents sleep.                          |
| **Fly** / **Dig** / **Dive** / **Shadow Force** | Two-turn move with semi-invulnerable state in between.                             |
| **Solar Beam** / **Skull Bash**                 | Two-turn charge move (first turn setup, second turn attack).                       |
| **Sky Drop**                                    | Carries target into air for one turn, both Pokémon can't act.                      |
| **Razor Wind** / **Sky Attack**                 | Charges for one turn before attacking.                                             |
| **Future Sight** / **Doom Desire**              | Delayed damage that hits 3 turns later, bypassing type matchups at time of impact. |
| **Perish Song**                                 | All Pokémon faint after 3 turns unless switched out.                               |
| **Destiny Bond**                                | If user faints before next turn, the attacker also faints.                         |

### 3.2 Move Copying/Selection

Moves that use, copy, or select other moves:

| Move            | Complexity                                                                      |
| --------------- | ------------------------------------------------------------------------------- |
| **Metronome**   | Randomly selects and uses any move except a limited exclusion list.             |
| **Sleep Talk**  | Randomly uses one of user's other moves while asleep.                           |
| **Assist**      | Uses random move from party members.                                            |
| **Copycat**     | Uses the last move used in battle.                                              |
| **Mirror Move** | Uses the last move used by the target.                                          |
| **Me First**    | Copies and uses target's selected move with 1.5× power if it's a damaging move. |
| **Sketch**      | Permanently replaces itself with target's last used move.                       |
| **Transform**   | Copies target's species, type, stats, moves (with 5PP each).                    |
| **Mimic**       | Temporarily replaces itself with target's last used move.                       |

### 3.3 Complex Damage Calculations

Moves with non-standard damage formulas:

| Move                                  | Complexity                                                                  |
| ------------------------------------- | --------------------------------------------------------------------------- |
| **Counter** / **Mirror Coat**         | Inflicts 2× the damage of the last physical/special move that hit the user. |
| **Metal Burst**                       | Returns 1.5× damage received.                                               |
| **Endeavor**                          | Reduces target's HP to match user's current HP.                             |
| **Pain Split**                        | Averages current HP between user and target.                                |
| **Super Fang** / **Nature's Madness** | Reduces target's HP by half of current.                                     |
| **Final Gambit**                      | Deals damage equal to user's current HP; user faints.                       |
| **Psywave**                           | Damage based on user's level (50-150%).                                     |
| **Dragon Rage**                       | Fixed 40 HP damage.                                                         |
| **Sonic Boom**                        | Fixed 20 HP damage.                                                         |
| **Night Shade** / **Seismic Toss**    | Damage equal to user's level.                                               |
| **Gyro Ball**                         | Power based on target's Speed relative to user's.                           |
| **Electro Ball**                      | Power based on user's Speed relative to target's.                           |
| **Low Kick** / **Grass Knot**         | Power based on target's weight.                                             |
| **Heavy Slam** / **Heat Crash**       | Power based on user's weight relative to target's.                          |
| **Flail** / **Reversal**              | Power inversely proportional to user's remaining HP percentage.             |
| **Crush Grip** / **Wring Out**        | Power directly proportional to target's remaining HP percentage.            |
| **Return**                            | Power based on friendship (max 102).                                        |
| **Frustration**                       | Power based on lack of friendship (max 102).                                |
| **Stored Power**                      | Power increases with user's stat boosts.                                    |
| **Punishment**                        | Power increases with target's stat boosts.                                  |
| **Weather Ball**                      | Type and power change based on active weather.                              |
| **Magnitude**                         | Random power between 10-150.                                                |

### 3.4 State Management [NOT IN SCOPE]

Moves that track complex state over multiple turns:

| Move                          | Complexity                                                  |
| ----------------------------- | ----------------------------------------------------------- |
| **Substitute**                | Creates HP-based decoy that blocks damage and status.       |
| **Disable**                   | Prevents target from using its last move for 4-7 turns.     |
| **Encore**                    | Forces target to repeat its last move for 4-8 turns.        |
| **Taunt**                     | Target can only use damaging moves for 3-5 turns.           |
| **Torment**                   | Target cannot use the same move twice in a row.             |
| **Stockpile**                 | Stores up to 3 levels of energy for Spit Up/Swallow.        |
| **Spit Up**                   | Power based on Stockpile count, then resets it.             |
| **Swallow**                   | Healing based on Stockpile count, then resets it.           |
| **Rollout** / **Ice Ball**    | Five-turn move that doubles in power each consecutive turn. |
| **Fury Cutter**               | Power doubles each consecutive successful hit.              |
| **Rage**                      | Attack raises each time user is hit.                        |
| **Grudge**                    | If user faints, the move that caused it loses all PP.       |
| **Lock-On** / **Mind Reader** | Next move will hit target regardless of accuracy/evasion.   |

### 3.5 Item/Berry Interactions

Moves that interact with held items:

| Move                       | Complexity                                                     |
| -------------------------- | -------------------------------------------------------------- |
| **Fling**                  | Power and effect based on user's held item, which is consumed. |
| **Natural Gift**           | Power and type based on user's held berry, which is consumed.  |
| **Recycle**                | Recovers user's last used/consumed item.                       |
| **Trick** / **Switcheroo** | Swaps held items between user and target.                      |
| **Bestow**                 | Gives user's held item to target.                              |
| **Incinerate**             | Destroys target's berry so it can't be used.                   |
| **Pluck** / **Bug Bite**   | Consumes and gains effect of target's berry.                   |
| **Belch**                  | Can only be used if user has consumed a berry.                 |

### 3.6 Protection/Blocking

Complex protection moves:

| Move                     | Complexity                                                                         |
| ------------------------ | ---------------------------------------------------------------------------------- |
| **Protect** / **Detect** | Blocks all moves for one turn, with decreasing success rate if used consecutively. |
| **Endure**               | Ensures user survives with 1 HP if it would be KO'd this turn.                     |
| **Spiky Shield**         | Blocks moves and damages contact attackers.                                        |
| **Baneful Bunker**       | Blocks moves and poisons contact attackers.                                        |
| **King's Shield**        | Blocks moves and lowers Attack of contact attackers.                               |
| **Obstruct**             | Blocks moves and sharply lowers Defense of contact attackers.                      |
| **Quick Guard**          | Protects team from priority moves.                                                 |
| **Wide Guard**           | Protects team from multi-target moves.                                             |
| **Mat Block**            | Protects team from damaging moves (first turn only).                               |
| **Crafty Shield**        | Protects team from status moves.                                                   |

### 3.7 Multi-Hit Complex

Multi-hit moves with special mechanics:

| Move                                               | Complexity                                                     |
| -------------------------------------------------- | -------------------------------------------------------------- |
| **Triple Kick**                                    | Three hits in one turn with increasing power (1×, 2×, 3×).     |
| **Triple Axel**                                    | Three hits with increasing power and separate accuracy checks. |
| **Double Iron Bash**                               | Hits twice with separate flinch chances.                       |
| **Water Shuriken**                                 | 2-5 hits with priority.                                        |
| **Bullet Seed** / **Rock Blast** / **Pin Missile** | 2-5 hits with complex probability distribution.                |
| **Beat Up**                                        | Hits once for each conscious Pokémon in party.                 |
| **Dual Chop** / **Double Hit** / **Double Kick**   | Always hits exactly twice.                                     |

### 3.8 Field/Party Effects

Moves affecting multiple Pokémon or field state:

| Move                                             | Complexity                                                |
| ------------------------------------------------ | --------------------------------------------------------- |
| **Aromatherapy** / **Heal Bell**                 | Cures all status conditions in party.                     |
| **Safeguard**                                    | Prevents status conditions for 5 turns.                   |
| **Light Screen** / **Reflect**                   | Reduces damage from physical/special attacks for 5 turns. |
| **Aurora Veil**                                  | Reduces all damage for 5 turns (requires Hail).           |
| **Tailwind**                                     | Doubles Speed for team for 3 turns.                       |
| **Trick Room**                                   | Reverses Speed order for 5 turns.                         |
| **Gravity**                                      | Grounds Flying types, disables levitation for 5 turns.    |
| **Heal Block**                                   | Prevents healing moves/effects for 5 turns.               |
| **Fairy Lock**                                   | Prevents switching for all Pokémon next turn.             |
| **Stealth Rock** / **Spikes** / **Toxic Spikes** | Places hazards that damage/affect Pokémon on entry.       |
| **Defog**                                        | Removes hazards, screens, and terrain.                    |
| **Rapid Spin**                                   | Removes hazards from user's side.                         |
| **Follow Me** / **Rage Powder**                  | Redirects all single-target moves to user.                |
| **Helping Hand**                                 | Boosts power of ally's move.                              |

---

## 4. Implementation Priority

1. **Core Damage & Stat Effects (High)**
   • `MultiplyMovePower`, `MultiplyMoveDamage`, `ModifyStatStage`, `InflictStatus`, `RecoilDamage`
   Enables majority of standard offensive/defensive interactions.

2. **Residual & Hazard System (High)**
   • `TrapBind`, `LayerHazard`, `ResidualEffect Registry`, Entry hazard damage.
   Needed for common competitive moves.

3. **Weather Framework (Medium)**
   • `SetWeather`, weather callbacks, immunity & modifiers.

4. **Multi-Hit & Two-Turn Mechanics (Medium)**
   • `MultiHit`, `GuaranteedTwoTurn`, `MustRecharge`, `SemiInvulnerable`.

5. **Switching & Turn Control (Medium)**
   • `UserSwitchOut`, `ForceSwitch`, `Flinch Flag`, `PreventEscape`.

6. **Healing & Drain (Low)**
   • `PercentHealUser`, `DrainDamage`, end-turn passive items.

7. **Odd Move Specials (Low / Separate Milestone)**
   Tackle moves in §3 individually once core systems are solid.

---

## 5. Recommended Next Steps

1. Extend `BattleState` with **TurnPhase**, **ResidualEffect**, and **SideCondition** containers.
2. Implement generic **ModifierContainer** hooks for power & damage multipliers.
3. Create unit tests for `MultiplyMovePower` and `TrapBind` as representative complex effects.
4. Iterate through data to map each move/ability/item to exactly one (or composite) effect class, adding missing variants as discovered.
5. Document effect application order in the battle loop to avoid future ambiguity.
6. Revisit "Odd Moves" list after core phases to design tailored mini-engines or scripted effects.

---

## 6. Abilities Analysis

Analysis of the 233 abilities in the dataset revealed 225 battle-relevant abilities with diverse effects.

### 6.1 Ability Categories

| Category             | Count | Examples                                                | Notes                                         |
| -------------------- | ----- | ------------------------------------------------------- | --------------------------------------------- |
| Weather Setters      | 43    | **Drizzle**, **Sand Stream**, **Drought**               | Includes weather immunity and boost abilities |
| Type Immunity        | 17    | **Volt Absorb**, **Flash Fire**, **Water Absorb**       | Nullifies or absorbs specific types           |
| Stat Modifiers       | 27    | **Speed Boost**, **Intimidate**, **Moody**              | Changes stats of self or opponents            |
| Contact Effects      | 15    | **Static**, **Rough Skin**, **Effect Spore**            | Triggers when hit by contact moves            |
| Damage Modifiers     | 41    | **Technician**, **Tinted Lens**, **Iron Fist**          | Multiplies damage for specific move types     |
| Healing Effects      | 18    | **Regenerator**, **Rain Dish**, **Dry Skin**            | Restores HP under specific conditions         |
| Status Preventers    | 15    | **Limber**, **Immunity**, **Insomnia**                  | Prevents specific status conditions           |
| On-Enter Effects     | 25    | **Intimidate**, **Drizzle**, **Frisk**                  | Triggers when Pokémon enters battle           |
| Turn-End Effects     | 15    | **Speed Boost**, **Shed Skin**, **Harvest**             | Activates at end of each turn                 |
| Move Modifiers       | 47    | **Serene Grace**, **Sheer Force**, **Prankster**        | Changes move properties (not just damage)     |
| Priority Changers    | 6     | **Gale Wings**, **Prankster**, **Triage**               | Modifies move priority                        |
| Field Effects        | 7     | **Electric Surge**, **Psychic Surge**, **Grassy Surge** | Sets or modifies terrain                      |
| Complex Conditionals | 28    | **Moxie**, **Wimp Out**, **Emergency Exit**             | Has complex activation conditions             |

### 6.2 Complex Abilities Requiring Special Implementation

#### 6.2.1 Type & Form Changing (Excluded from Scope)

- **Forecast**: Changes type based on weather
- **Multitype**: Changes type based on held plate
- **Zen Mode**: Changes form when below 50% HP
- **Schooling**: Changes form based on level and HP
- **Shields Down**: Changes form based on HP threshold
- **Battle Bond**: Changes form after KOing an opponent
- **Power Construct**: Changes form when below 50% HP
- **Stance Change**: Changes form when using specific moves

#### 6.2.2 Battle Entry Effects

| Ability                                     | Complexity                                              |
| ------------------------------------------- | ------------------------------------------------------- |
| **Intimidate**                              | Lowers opponent's Attack on entry                       |
| **Drizzle** / **Drought** / **Sand Stream** | Sets permanent weather on entry                         |
| **Electric/Psychic/Grassy/Misty Surge**     | Sets terrain on entry                                   |
| **Frisk**                                   | Reveals opponent's held item                            |
| **Forewarn**                                | Reveals opponent's highest-power move                   |
| **Imposter**                                | Transforms into opponent on entry (like Transform move) |
| **Trace**                                   | Copies random opponent's ability                        |

#### 6.2.3 Damage Calculation Modifiers

| Ability                                          | Complexity                                             |
| ------------------------------------------------ | ------------------------------------------------------ |
| **Wonder Guard**                                 | Only takes damage from super-effective moves           |
| **Unaware**                                      | Ignores opponent's stat changes for damage calculation |
| **Mold Breaker** / **Teravolt** / **Turboblaze** | Ignores abilities that would prevent move effects      |
| **Scrappy**                                      | Ignores Ghost immunity to Normal/Fighting moves        |
| **Tinted Lens**                                  | Doubles damage of not-very-effective moves             |
| **Technician**                                   | Boosts moves with base power ≤60 by 50%                |
| **Water Bubble**                                 | Doubles Water move power, halves Fire damage received  |
| **Huge Power** / **Pure Power**                  | Doubles Attack stat                                    |

#### 6.2.4 Conditional Triggers

| Ability                           | Complexity                                                                   |
| --------------------------------- | ---------------------------------------------------------------------------- |
| **Moxie**                         | Raises Attack after KOing opponent                                           |
| **Wimp Out** / **Emergency Exit** | Forces switch when HP drops below 50%                                        |
| **Berserk**                       | Raises Special Attack when hit below 50% HP                                  |
| **Stakeout**                      | Double damage against Pokémon that switched in this turn                     |
| **Moody**                         | Randomly raises one stat by 2 stages and lowers another by 1 stage each turn |
| **Speed Boost**                   | Raises Speed by one stage after each turn                                    |
| **Innards Out**                   | When KO'd, deals damage equal to last HP amount                              |
| **Color Change**                  | Changes type to match move that hit it                                       |

#### 6.2.5 Move/Effect Redirection

| Ability                             | Complexity                                                       |
| ----------------------------------- | ---------------------------------------------------------------- |
| **Lightning Rod** / **Storm Drain** | Redirects Electric/Water moves to self and boosts Special Attack |
| **Dancer**                          | Copies dance moves used by other Pokémon                         |
| **Receiver**                        | Gains ability of fainted ally                                    |
| **Synchronize**                     | When statused, inflicts same status on attacker                  |
| **Pressure**                        | Makes opponent's moves use 1 extra PP                            |
| **Magic Bounce**                    | Reflects status and stat-lowering moves back to user             |

### 6.3 Ability Effect Priorities

**High Priority:**

- Type immunities (**Volt Absorb**, **Flash Fire**)
- Weather setters (**Drizzle**, **Drought**)
- Entry effects (**Intimidate**)
- Damage modifiers (**Technician**, **Huge Power**)

**Medium Priority:**

- Status prevention (**Limber**, **Immunity**)
- Stat modifiers (**Speed Boost**, **Moxie**)
- Contact effects (**Static**, **Rough Skin**)

**Low Priority:**

- Complex conditionals (**Moody**, **Stakeout**)
- Redirection abilities (**Lightning Rod**)
- Form-changing abilities (excluded from scope)

---

## 7. Items Analysis

Analysis of the 954 items in the dataset identified 843 battle-relevant items, with many having complex effects.

### 7.1 Item Categories

| Category              | Count | Examples                                              | Notes                              |
| --------------------- | ----- | ----------------------------------------------------- | ---------------------------------- |
| Held Damage Modifiers | 114   | **Life Orb**, **Choice Band**, **Expert Belt**        | Modifies damage output             |
| Held Stat Boosters    | 60    | **Choice Scarf**, **Muscle Band**, **Wise Glasses**   | Boosts specific stats              |
| Held Type Resistors   | 19    | **Occa Berry**, **Passho Berry**, **Chilan Berry**    | Reduces damage from specific types |
| Held Healing Items    | 4     | **Leftovers**, **Shell Bell**, **Black Sludge**       | Restores HP over time              |
| Held Status Items     | 8     | **Flame Orb**, **Toxic Orb**, **Mental Herb**         | Inflicts or cures status           |
| Held Misc Battle      | 99    | **Focus Sash**, **Red Card**, **Eject Button**        | Various battle effects             |
| Consumable Berries    | 18    | **Sitrus Berry**, **Lum Berry**, **Liechi Berry**     | One-time use effects               |
| Choice Items          | 3     | **Choice Band**, **Choice Scarf**, **Choice Specs**   | Locks into one move, boosts stat   |
| Form Change Items     | 10    | **Prison Bottle**, **Griseous Orb**                   | Changes form (excluded)            |
| Complex Held Items    | 56    | **Weakness Policy**, **Focus Sash**, **Eject Button** | Conditional triggers               |
| Z-Crystal Items       | 35    | **Normalium Z**, **Firium Z**                         | Z-move enablers (excluded)         |

### 7.2 Complex Items Requiring Special Implementation

#### 7.2.1 Choice Items (High Complexity)

| Item             | Complexity                                               |
| ---------------- | -------------------------------------------------------- |
| **Choice Band**  | Boosts Attack by 50%, locks into first move used         |
| **Choice Scarf** | Boosts Speed by 50%, locks into first move used          |
| **Choice Specs** | Boosts Special Attack by 50%, locks into first move used |

#### 7.2.2 Conditional Trigger Items

| Item                | Complexity                                                                     |
| ------------------- | ------------------------------------------------------------------------------ |
| **Focus Sash**      | If at full HP, survives with 1 HP from attacks that would KO                   |
| **Weakness Policy** | When hit by super-effective move, raises Attack and Special Attack by 2 stages |
| **White Herb**      | Removes all stat reductions at end of turn                                     |
| **Mental Herb**     | Cures infatuation, taunt, encore, disable, and torment                         |
| **Eject Button**    | Forces switch out when hit by a damaging move                                  |
| **Red Card**        | Forces opponent to switch out when holder is hit                               |
| **Quick Claw**      | 20% chance to move first in priority bracket                                   |

#### 7.2.3 Consumable Effect Items

| Item                                          | Complexity                                                       |
| --------------------------------------------- | ---------------------------------------------------------------- |
| **Sitrus Berry**                              | Restores 25% HP when below 50% HP                                |
| **Lum Berry**                                 | Cures any status condition                                       |
| **Type-Resist Berries** (Occa, Passho, etc.)  | Halves damage from super-effective moves of specific type        |
| **Stat-Boost Berries** (Liechi, Ganlon, etc.) | Raises stat when below 25% HP                                    |
| **Custap Berry**                              | Grants priority when below 25% HP                                |
| **Kee Berry** / **Maranga Berry**             | Raises Defense/Special Defense when hit by physical/special move |

#### 7.2.4 Passive Effect Items

| Item                                 | Complexity                                                  |
| ------------------------------------ | ----------------------------------------------------------- |
| **Leftovers**                        | Restores 1/16 max HP each turn                              |
| **Rocky Helmet**                     | Damages contact attackers for 1/6 their max HP              |
| **Sticky Barb**                      | Damages holder each turn, transfers to attackers on contact |
| **Black Sludge**                     | Heals Poison types, damages non-Poison types                |
| **Terrain Extender**                 | Extends terrain duration to 8 turns                         |
| **Heat Rock** / **Damp Rock** / etc. | Extends weather duration to 8 turns                         |

#### 7.2.5 Type & Move Modifiers

| Item                                    | Complexity                                 |
| --------------------------------------- | ------------------------------------------ |
| **Type-Enhancing Items** (Plates, etc.) | Boosts moves of specific type by 20%       |
| **Muscle Band**                         | Boosts physical moves by 10%               |
| **Wise Glasses**                        | Boosts special moves by 10%                |
| **Expert Belt**                         | Boosts super-effective moves by 20%        |
| **Life Orb**                            | Boosts all moves by 30%, user loses 10% HP |
| **Wide Lens**                           | Increases move accuracy by 10%             |

### 7.4 Item Effect Priorities

**High Priority:**

- Passive healing (**Leftovers**)
- Damage modifiers (**Life Orb**, **Choice Band**)
- Type-enhancing items (Plates, type gems)

**Medium Priority:**

- Status berries (**Lum Berry**, **Cheri Berry**)
- Conditional triggers (**Focus Sash**, **Weakness Policy**)
- Stat boosters (**Choice Scarf**, **Muscle Band**)

**Low Priority:**

- Complex conditional items (**Custap Berry**, **Quick Claw**)
- Weather/terrain extenders
- Z-Crystals (excluded from scope)

---

## 8. Implementation Priority

1. **Core Damage & Stat Effects (High)**
   • `MultiplyMovePower`, `MultiplyMoveDamage`, `ModifyStatStage`, `InflictStatus`, `RecoilDamage`
   • Ability damage modifiers (**Technician**, **Tinted Lens**)
   • Item damage modifiers (**Life Orb**, **Choice Band**)
   Enables majority of standard offensive/defensive interactions.

2. **Residual & Hazard System (High)**
   • `TrapBind`, `LayerHazard`, `ResidualEffect Registry`, Entry hazard damage.
   • Passive healing items (**Leftovers**)
   • End-turn ability effects (**Speed Boost**, **Poison Heal**)
   Needed for common competitive moves.

3. **Weather Framework (Medium)**
   • `SetWeather`, weather callbacks, immunity & modifiers.
   • Weather-setting abilities (**Drizzle**, **Drought**)
   • Weather-dependent abilities (**Swift Swim**, **Chlorophyll**)

4. **Multi-Hit & Two-Turn Mechanics (Medium)**
   • `MultiHit`, `GuaranteedTwoTurn`, `MustRecharge`, `SemiInvulnerable`.

5. **Switching & Turn Control (Medium)**
   • `UserSwitchOut`, `ForceSwitch`, `Flinch Flag`, `PreventEscape`.
   • Switch-triggering items (**Eject Button**, **Red Card**)
   • Switch-triggering abilities (**Emergency Exit**, **Wimp Out**)

6. **Status & Type Immunity (Medium)**
   • Status prevention abilities (**Limber**, **Immunity**)
   • Type immunity abilities (**Volt Absorb**, **Flash Fire**)
   • Status-curing items (**Lum Berry**, **Chesto Berry**)

7. **Healing & Drain (Low)**
   • `PercentHealUser`, `DrainDamage`, end-turn passive items.

8. **Complex Ability Effects (Low)**
   • Entry effects (**Intimidate**, **Trace**)
   • Conditional triggers (**Moxie**, **Berserk**)

9. **Odd Move/Ability/Item Specials (Low / Separate Milestone)**
   Tackle complex cases individually once core systems are solid.

---
