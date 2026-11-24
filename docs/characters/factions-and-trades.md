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

Open the **Professions** tab in the character book. Choose a trade to see its unlocks and recipes. The **Guide** plank opens its Cruise Guide chapter. Fishers and Hunters can open the Bestiary from here, and Navigators can open the Log Book. Each trade guide below also links to its quest chapter.

| Profession | Activities and equipment |
| --- | --- |
| [Blacksmith](professions/blacksmith.md) | Forge and improve weapons. Follow the quest’s forged-item milestones. |
| [Carpenter](professions/carpenter.md) | Make boats and ship fittings. A Carpenter can also mend a Cruise hull afloat. |
| [Chemist](professions/chemist.md) | Compound materials, powders and specialist recipes. |
| [Cook](professions/cook.md) | Prepare dishes and level up through food milestones. |
| [Farmer](professions/farmer.md) | Grow crops and specialize in harvests. |
| [Fisher](professions/fisher.md) | Fish, discover catches, and pursue Calm Belt Sea Kings beginning at level 44. |
| [Hunter](professions/hunter.md) | Track game and progress through creature hunts. |
| [Inventor](professions/inventor.md) | Craft devices and advanced dials. |
| [Lumberjack](professions/lumberjack.md) | Work different woods and harvest materials for other trades. |
| [Merchant](professions/merchant.md) | Trade, take orders and build a commerce route. |
| [Miner](professions/miner.md) | Prospect, mine metals, and follow rare-resource milestones. |
| [Musician](professions/musician.md) | Play instruments to develop songs and support abilities. |
| [Navigator](professions/navigator.md) | Make navigation tools and charts, check the weather, and develop open-water abilities. |
| [Tailor](professions/tailor.md) | Sew equipment and flags. At level 10 craft heat or cold linings, and at 50 craft [All-Weather Lining](../world/weather.md#armour-linings). |

### Experience and talents

Every trade starts at **level 1** and reaches **level 100**. Advancing costs **20 × current level¹·²⁵ XP** before rounding. Workstation XP is listed for every recipe in the guides. Away from a bench, you earn XP by doing the trade’s work. The Bestiary and Log Book also reward collection milestones.

You gain a **talent point every five levels** in each trade. Open **Talents** from its page or press **J** with default controls. Spend points on a starting node or one adjacent to a talent you already own. The technique nodes grant moves you can equip from the **Profession** ability tab. A Chemist’s **Potion of Second Thoughts** refunds all the points in one trade. See [Trade talents](trade-talents.md) to jump to any web.

A meal’s **Appetite** boosts one trade for ten minutes. A Musician’s **Craftsman’s Song** boosts every trade and can stack with Appetite. Sleeping at a town inn grants **Rested**, a 10% trade XP bonus until next dusk.

### Crew trade pairs

Work within **16 blocks** of a crewmate with the paired trade for a **15%** bonus.

| Pair | What improves |
| --- | --- |
| Fisher + Cook | Dishes last longer. |
| Farmer + Cook | The Cook earns more XP. |
| Miner + Blacksmith | More scrap is recovered. |
| Hunter + Chemist | Remedies last longer. |
| Carpenter + Navigator | Cruise boats sail faster. |

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
