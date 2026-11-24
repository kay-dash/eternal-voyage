# Factions and professions

## Factions

The quest book has chapters for **Pirates**, **Marines**, **Bounty Hunters**, **Revolutionary Army**, **World Government**, and **Seven Warlords of the Sea**. The active faction or Warlord status controls access to the chapter. Cruise also has civilian start enabled.

Crews affect the [Atlas](../voyage/navigation.md#log-pose-and-atlas), conquest, and shared Road Poneglyph readings. Each crewmate tracks and claims their own [quest book](../voyage/quest-book.md) progress.

### Ranks, faction quests and wars

Haki Realm keeps **four** quests on each faction’s in-game board and refreshes them every **two real hours**. The FTB faction chapters track a separate set of milestones. High ranks can have limited seats, including one Fleet Admiral, three Admirals, five Vice Admirals and seven Warlords. A seat can fill automatically after three real days vacant. Fourteen real days of inactivity can cost a limited seat.

Faction switching costs **100,000 Belly** and has a **seven-real-day** cooldown. Joining from no faction is free. Looting your own side’s structure chests can cost Loyalty for the listed factions and ranks, and Marines and Bounty Hunters can lose Loyalty for killing their own side’s NPCs. Eligible wanted-player payouts are **2% of bounty**, capped at **1,000,000 Belly**.

Haki Realm faction wars last **three real days** with a **two-real-day** truce. These wars are scored by kills. The [island conquest and crew wars](../world/conflict.md#siege-and-war) have separate objectives and timing.

### Rank fruit rewards

Check your faction finale for fruit rewards and use the chat menu or `/fruitreward` after you qualify. The Four Emperors’ choices are for captains. The King of the World’s fruit and the Five Elders’ fruits are first-come rewards. If you claim an Admiral fruit and later qualify as Fleet Admiral, or claim an Elder fruit and then qualify as King of the World, you cannot claim a second fruit from the higher post.

## Professions

Choose **two trades** on the server. Your second slot opens when your first trade reaches **level 1**. Profession XP is retained on death. Spread trades across your crew so you can share tools, gear, food and boat upgrades.

The FTB quest book gives every trade a chapter with its own level, crafting, gathering and travel objectives.

| Profession | Activities and equipment |
| --- | --- |
| [Blacksmith](../reference/quests/blacksmith.md) | Forge and improve weapons. Follow the quest’s forged-item milestones. |
| [Carpenter](../reference/quests/carpenter.md) | Make boats and ship fittings. A Carpenter can also mend a Cruise hull afloat. |
| [Chemist](../reference/quests/chemist.md) | Compound materials, powders and specialist recipes. |
| [Cook](../reference/quests/cook.md) | Prepare dishes and level up through food milestones. |
| [Farmer](../reference/quests/farmer.md) | Grow crops and specialize in harvests. |
| [Fisher](../reference/quests/fisher.md) | Fish, discover catches, and pursue Calm Belt Sea Kings beginning at level 44. |
| [Hunter](../reference/quests/hunter.md) | Track game and progress through creature hunts. |
| [Inventor](../reference/quests/inventor.md) | Craft devices and advanced dials. |
| [Lumberjack](../reference/quests/lumberjack.md) | Work different woods and harvest materials for other trades. |
| [Merchant](../reference/quests/merchant.md) | Trade, take orders and build a commerce route. |
| [Miner](../reference/quests/miner.md) | Prospect, mine metals, and follow rare-resource milestones. |
| [Musician](../reference/quests/musician.md) | Play instruments to develop songs and support abilities. |
| [Navigator](../reference/quests/navigator.md) | Make navigation tools and charts, check the weather, and develop open-water abilities. |
| [Tailor](../reference/quests/tailor.md) | Sew equipment and flags. At level 10 craft heat or cold linings, and at 50 craft [All-Weather Lining](../world/weather.md#armour-linings). |

Cruise’s Log Book tracks profession progress and the game exposes its talents alongside the trade. Every supplied profession curve has base XP **20** and exponent **1.25**. Use the [Trade talents](trade-talents.md) tables for entry nodes, effects and connected nodes, and the [Cruise content index](../reference/content/inocruise.md) for items, recipes, creature entries and trade-specific datapack IDs.

### Rumble Ball and dial recipes

Use the Chemist or Inventor workstation to make these items.

| Item | Trade level | Materials | Yield |
| --- | --- | --- | ---: |
| Rumble Ball | Chemist 42 | Golden Egg, Golden Fruit, Golden Hercules | 1 |
| Jet Dial | Inventor 36 | 7 Dial Fragments, 2 Balloon Catfish | 3 |
| Burst Dial | Inventor 42 | Jet Dial, 3 Mysterious Parts, 3 iron ingots, 2 Iron Scrap | 1 |
| Tone Dial | Inventor 44 | Mysterious Dial, note block, 2 Iron Scrap | 1 |

Rumble lasts **three minutes**. It clears Devil Fruit cooldowns when taken and makes transformed Zoan users stronger, tougher, and faster. A Mink can take it to use Sulong without waiting for a full moon. Taking a second ball while the first is active ends Rumble and inflicts nausea, weakness, and slowness.

The **Jet Dial** launches you in the direction you look. The **Tone Dial** rings when a creature or player approaches it. Both come from [Sky Island](../reference/content/inosky.md). The **Burst Dial** fits a Cruise boat at the Upgrade Bench and runs on Cola. Cyborgs can use Mine Mine no Mi’s **Ultra Cola** and **Cola Backpack**.

**Pack sources:** `akumalib-server.toml`, `hakirework-server.toml`, `inocruise-server.toml`, and the faction and profession quest chapters.
