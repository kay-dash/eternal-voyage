# Encounter stats

Eternal Voyage sets enemy strength by region, role and encounter. Use these values to judge what your next sea will ask of you. HP is health in Minecraft damage units. Two HP equal one heart.

## Faction enemies

Each cell shows **HP / Doriki**. Brutes and snipers that use the same role row share its values.

| Role | Blues | Early Paradise | Late Paradise | New World |
| --- | ---: | ---: | ---: | ---: |
| Grunt | 40 / 1,500 | 120 / 4,000 | 180 / 8,000 | 250 / 15,000 |
| Brute or sniper | 75 / 3,000 | 200 / 6,000 | 300 / 12,000 | 400 / 22,000 |
| Captain | 150 / 6,000 | 400 / 10,000 | 600 / 18,000 | 800 / 35,000 |
| Admiral | 300 / 8,000 | 700 / 16,000 | 1,000 / 25,000 | 1,400 / 48,000 |
| Attack attribute multiplier | 1.00× | 1.50× | 2.00× | 3.00× |
| Added armour toughness | +0 | +2 | +4 | +6 |

Eligible enemies can use advanced Haki from the second row onward. Cruise’s arena fighters use the row selected by their assigned Doriki, and certain garrisons have individual placement rules. See [arena tiers](../reference/datapack/arena_tiers.md) for every listed fighter, Haki value, and prize.

## Other regional enemies

| Region | Generic health multiplier | Generic attack multiplier |
| --- | ---: | ---: |
| Blues | 1.00× | 1.00× |
| Paradise | 3.00× | 1.50× |
| New World | 6.00× | 2.00× |
| Nether | 4.00× | 1.75× |

These are for eligible mobs with the normal max-health and attack attributes. Dedicated enemy systems such as the faction tables, Cataclysm boss settings and Mowzie’s combat settings have their own values.

## Cataclysm and Mowzie’s Mobs

Cataclysm’s **Ancient Remnant** and **Modern Remnant** have 1.00× base health. **Maledictus** is at 1.50×, **the Leviathan** at 1.75×, and **the Harbinger**, **Scylla**, **Ignis**, **Ender Guardian**, and **Netherite Monstrosity** at 2.00×. Their configured attack multipliers are 1.00×. Some Cataclysm attacks add a share of the target’s maximum health. For example, the Ender Guardian’s configured Gravity Punch share is **5%** and its Uppercut share is **10%**. A 500 HP target contributes 25 HP or 50 HP respectively to the relevant calculation.

The **Ferrous Wroughtnaut** uses **1.50× health** and **1.00× attack**. **Frostmaw**, **Umvuthi**, **Sculptor**, **Naga**, **Umvuthana**, **Bluff**, and **Elokosa** use **3.00× health** and **1.50× attack**. Grottol, Lantern and Foliaath use 1.00× for both.

The [boss and gear values](../reference/settings/survival.md) include the other entities and the configured weapon and ability damage. For example, the Incinerator’s base weapon attack setting is **14 HP**, the Ceraunus wave is **6 HP**, and the Phantom Halberd is **12 HP**.

## Impel Down

Prison guards and beasts use the pack’s Doriki-to-health curve and deal **2×** configured damage before other combat modifiers. Uniformed jailers range from **50–125 HP** at the entrance to **375–415.625 HP** on Level 6. Hooded guards roll **30%** more Doriki.

The **Warden** on Level 6 has **37,500 configured Doriki**, **3,375 effective HP**, **16 armour**, and **425 Haki**. The **Sphinx** on Level 2 has **120,000 configured Doriki**, **1,200 effective HP**, **14 armour**, and **300 Haki**. The [prison encounter tables](../reference/settings/encounters.md#impel-down-guards-and-wardens) list every floor, including the Chief of the Guard and the great beasts. See [Impel Down](../voyage/impel-down.md#impel-down) for travel and arrests.

## Challenge and Overworld bosses

Normal challenge stages run from **1,000 Doriki** for Higuma to **12,500** for Enel. The configured Hard rematches are at **50,000**, with **3.875×** the encounter’s base HP. Arlong, Kuroobi, and Chew have their own Overworld stages for fights outside the challenge arenas. See the [boss tables](../reference/settings/encounters.md#challenge-bosses) for the per-fight stages and multipliers.

Legend bounties have a **20-real-hour rematch cooldown**. Hard Legend rematches remove the usual fruit-box reward.
