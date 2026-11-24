# Towns and island claims

Once your crew can defend itself, decide where you’ll spend time between voyages. A village with a **village flag** grows through trade, errands, and defense. An **unheld island with a hall** can become a crew claim after an assault.

## Cruise towns and villages

Make landfall at the village, find the **notice board** for errands, and visit the workshops or market to trade. If you’re trying to grow the town, offer Belly at the **town hall** and help with raid defense. Higher prosperity brings more trades and services for the whole port.

Village damage is set to **Mend**. Damaged blocks start returning when the village has been left in peace for three minutes. Village blocks give no drops, and player blocks placed inside can be returned during repair. Natural hostile spawns are suppressed in living villages. Mobs can still enter from outside and spawners can still operate.

| Prosperity | What the village gains |
| ---: | --- |
| 30 | More housing and inhabitants, barracks and guards |
| 80 | Missing trades’ workshops, an inn, warehouse and market hall |
| 150 | Walls, bank, bounty office, colosseum and plots |

A peaceful in-game day adds one point. Trade adds one per 1,000 Belly, gifts at the town hall one per 500 Belly, errands five, and successful raid defense ten. A lost raid costs twenty. The supplied settings give a village two guards and permit Marine aid from within 1,000 blocks with a 30-second delay after a villager is killed. A dead village can repopulate after seven in-game days. The notice-board revival fee is 2,000 Belly per original resident.

Wiping out villages adds escalating bounty and can close nearby villages to the offender. The hunt starts after two villages within the configured memory window. The ban applies within 1,000 blocks for 30 in-game days. Bounty escalation doubles per additional village. The configured chance for bounty hunters to arrive instead of Marines starts at 30% and increases with bounty.

## Claim an island

1. Pick an unheld island with a hall. Bring food and enough crewmates to clear the waves.
2. Move to the hall and declare an assault with `/island assault`. Defeat **three waves** within **five minutes**.
3. The island changes hands **as soon as the last defender falls**. A bell rings and the new holder’s flag rises in about **two seconds**. If the assault fails, the same crew can try again after **three in-game days**.

### Read the hall flag

A spruce pole at the hall’s center shows the island’s holder. It flies the crew’s **9×6 Jolly Roger** in the captain’s faction colors, or the Marines’ or Revolutionaries’ flag. An unheld hall has a bare pole. Sieges, raid outcomes, wars, and surrenders update the flag when ownership changes.

Flags are visible up to **160 blocks** away, including Cruise town flags. The hall pole and banner resist breaking and explosions. Any section displaced by an ability returns within about **two seconds**, and flags yield no items. Existing halls gain their pole when a player approaches. Older hand-placed banners serve as decoration.

Held islands can face raids. The supplied normal raid window is **20 to 30 in-game days**, with a **five-minute** defense window. Failed defenses lower the hold score. The flag comes down if that score reaches zero.

The starting hold score is **three**. The configured retake window is **five to ten in-game days**. The hall has a four-block clear radius for fighting. The wider build-protection radius is set to **64 blocks** in the shipped world rules.

## Siege and war

In a siege, the captain declares at an opposing island’s hall. The scheduled fight has a five-minute muster and a five-minute battle. Attackers need to hold the hall continuously for **60 seconds** without holders on it. Repeated no-shows can forfeit a siege after seven eligible postponements and at least 24 real hours.

Crew wars open after one in-game day. Surrender or capture of the other crew’s home island ends the war, with **10%** of the losing crew’s bank account paid to the winner.

| Held island sea | Crew income per in-game day |
| --- | ---: |
| Blues | 500 Belly |
| Early Paradise | 1,000 Belly |
| Late Paradise | 2,000 Belly |
| New World | 4,000 Belly |

## Markets and island events

The Auction House charges a **2% listing fee**, holds a listing up to **30 in-game days**, and allows **ten listings** per seller. Cruise’s merchant ships, concerts, feasts, traveling swordsmiths, restaurants, fishing tournaments and other events remain active under the supplied settings. At sea, watch for schools of fish, migrations, ships in distress, ghost ships, falling stars and wrecks. The [core settings](../reference/settings/core.md#inocruise-servertoml) list their timing and duration.

**Pack sources:** `ompworld/conflict.toml` and `inocruise-server.toml`.

Next, [cross Reverse Mountain](../voyage/paradise.md) or check [Impel Down](../voyage/impel-down.md) if a raid or fight ended in an arrest.
