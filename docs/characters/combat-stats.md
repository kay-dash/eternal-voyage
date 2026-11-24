# Combat stats and Doriki scaling

Damage is measured in **HP**. Two HP equal one heart. Eternal Voyage adjusts individual moves and then scales supported player attacks with Doriki. Use the damage listed on your move’s page and the tables below to estimate how hard it will hit as you train.

## Base health

Up to 10,000 Doriki, base health is **Doriki ÷ 40**, with a floor of **20 HP**. After 10,000, each additional 160 Doriki gives **1 HP**, up to **500 HP at 50,000 Doriki**. Racial size, equipment, transformations and buffs can affect your final maximum.

| Doriki | Base health | Hearts |
| ---: | ---: | ---: |
| 0–800 | 20 HP | 10 |
| 1,000 | 25 HP | 12.5 |
| 5,000 | 125 HP | 62.5 |
| 10,000 | 250 HP | 125 |
| 20,000 | 312.5 HP | 156.25 |
| 30,000 | 375 HP | 187.5 |
| 40,000 | 437.5 HP | 218.75 |
| 50,000 | 500 HP | 250 |

## Damage from Doriki

Doriki starts adding damage above **10,000**. By **30,000**, you gain half the bonus available at **50,000**.

| Attack or Haki component | 10,000 or less | 20,000 | 30,000 | 40,000 | 50,000 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tier 1 Devil Fruit | 1.00× | 1.31× | 1.63× | 1.94× | 2.25× |
| Tier 2 Devil Fruit | 1.00× | 1.25× | 1.50× | 1.75× | 2.00× |
| Tier 3 or 4 Devil Fruit | 1.00× | 1.19× | 1.38× | 1.56× | 1.75× |
| Haki or fighting style, fruit user | 1.00× | 1.13× | 1.25× | 1.38× | 1.50× |
| Haki or fighting style, fruitless | 1.00× | 1.38× | 1.75× | 2.13× | 2.50× |
| Haki or fighting style, eligible fruitless crew | 1.00× | 1.44× | 1.88× | 2.31× | 2.75× |
| Racial ability | 1.00× | 1.10× | 1.20× | 1.30× | 1.40× |

Use your fruit’s tier for fruit moves. Kamusari and qualifying Armament and Conqueror’s Coating damage use the Haki rows.

### All-fruitless crew bonus

A Mine Mine no Mi crew needs **at least three members** and the server must know that **every member is fruitless**. Offline members count through their last recorded fruit status. One fruit user, or an offline member whose status is unknown to the server, makes the crew ineligible. Your crewmates can be elsewhere when you attack.

An eligible crew adds **0.25** to the fruitless **cap multiplier**, taking it from **2.50× to 2.75×** for Haki and fighting-style damage. At 30,000 Doriki the extra crew contribution is **0.125×**. For example, a 20 HP style hit at that Doriki, with no per-move adjustment or other modifiers, scales to **35 HP** while fruitless and **37.5 HP** with an eligible crew. At the cap those values are **50 HP** and **55 HP**. See [Haki](haki.md#fruitless-crew-scaling) for Haki XP, capacity and the separate formation mechanic.

## Individual move damage

The pack applies the move’s listed adjustment to the incoming ability damage before the usual bonuses. Then the Doriki curve scales the move. These examples isolate the direct damage of the named hit. Armor, Haki, move phases, explosions and other effects can change what actually lands.

| Move | Base projectile hit | Pack adjustment | Through 10,000 Doriki | At 30,000 | At 50,000 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gomu Gomu no Pistol · tier 2 | 6 HP | 1.65× | 9.9 HP | 14.85 HP | 19.8 HP |
| Gomu Gomu no Bazooka · tier 2 | 20 HP | 1.65× | 33 HP | 49.5 HP | 66 HP |
| Hiken · tier 3 | 50 HP | 1.55× | 77.5 HP | 106.56 HP | 135.63 HP |

**Kamusari** has its own mastery calculation before Doriki adds to it. Its direct slash starts at **20 HP plus 40 HP × (Coating mastery ÷ 60)**. At **30 Coating mastery**, that gives **40 HP** before scaling. An eligible fruitless crew member with **30,000 Doriki** gets **75 HP** for that direct component. At **50,000 Doriki and 60 Coating mastery**, the direct component reaches **165 HP** with the crew bonus. The area effect and other Haki damage are separate from this example.

For other examples, **Anaconda Press** has a **2.70×** per-move factor, **Hurricane** has **0.40×**, and **Ragna Izuchi** has **0.20×**. Check the full [move-by-move tables](../reference/settings/move-damage.md) for the names and values shipped with the pack. An untuned move starts at 1.00× for this part of the calculation.

NPCs receive **half of the increase above 1.00×** for a boosted move. For example, a **2.70×** player factor becomes **1.85×** for an NPC. Factors below 1.00× are applied in full. NPCs have their own [regional stats](../world/encounter-stats.md).

## Haki techniques and body size

Haki Realm attacks that follow body size gain reach across areas, lines, and targeted attacks. A **size-4** body reaches about **twice as far** under the shared size rule. Individual attacks can have their own reach calculations. Galaxy Impact’s blast and crater also grow. Pure Haki techniques, including 27 Conqueror’s, Observation, and guard moves, keep their usual reach.

| Technique | Standard body | Size 4 |
| --- | ---: | ---: |
| Ryuo Spear | 14 blocks | 30 blocks |
| Kingly Fist | 12 blocks | 30 blocks |
| Punch of a King | 8 blocks | 16 blocks |
| Black Fist Barrage | 4 blocks | 8 blocks |

<a id="defence-size-and-logia"></a>

## Defense, size and Logia

- **Player defense.** The configured cap on combined protection in the post-armor layer is 80%. For a hit with 50 HP remaining after armor, the capped layer by itself can reduce it to 10 HP. Guards, dodges, invulnerability and special move rules can affect whether a hit reaches that layer.
- **Size.** A larger body can multiply melee damage and the damage of size-sensitive moves. Eligible attacks follow a square-root damage curve up to **3×**.
- **Logia.** Hostile Mine Mine no Mi mobs in **late Paradise, the New World, the Red Line, and the Nether** can bypass Logia intangibility on eligible attacks. The [Devil Fruits guide](devil-fruits.md) covers the broader fruit rules.
