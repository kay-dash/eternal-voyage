# Devil Fruits and awakenings

## Finding and keeping a fruit

Look for [fruit boxes](fruit-boxes.md) in [regional treasure](../world/loot.md#treasure-box-rolls), arena rewards, and the quest book. Leaves do not drop fruit. Each fruit can have only **one copy in circulation at a time** under the server’s **Simple** fruit rules. You can carry more than three different uneaten fruits.

**Uneaten fruits rot after seven real days**, including time when the server is offline. Chests and handoffs keep the original timer. You get warnings with **24 hours**, **1 hour**, and **5 minutes** left while carrying it. A rotten fruit returns to the pool, so decide promptly whether to eat it, trade it, or pass it to a crewmate. Holding the fruit in your other hand when you use **Juno’s Blessing** adds 24 hours, up to seven days remaining. The timer excludes eaten fruits, SMILEs, and fruits already bound to Infusion weapons.

Browse the [Devil Fruit catalogue](fruits/index.md) by fruit type. Each fruit’s page shows its moves, stats, and awakening moveset where available.

## Fruit mastery

Haki Realm enables **five mastery levels**. Its base for the first level-up is 20 mastery XP, with the cost rising linearly by current level. Using a move gives a configured **6 XP**, with the same move able to teach once every three seconds. Zoans can also train through active time in form, at a configured **20 XP per minute**. Standing still for more than ten seconds pauses that form gain.

Mastery gates later moves, with fruit-specific starter pairs in the [core settings](../reference/settings/core.md#hakirework-servertoml). Ope Ope, for example, gets Room and Injection Shot as its starter pair. The shipped low-mastery power and cooldown multipliers are both **1.0**, and full mastery is not required for a Logia body. See [combat scaling](combat-stats.md#damage-from-doriki) for each fruit tier’s late-voyage damage and the [move damage multipliers](../reference/settings/move-damage.md) for individual attacks.

## Awakening

For fruits that can awaken, reach **40,000 Doriki** plus **1,728,000 online ticks** with that fruit, roughly 24 hours at 20 ticks per second. Time stops counting after 6,000 ticks without moving, roughly five minutes. Watch for chat progress at 50%, 75%, and 90%. Open your fruit’s page in the [catalogue](fruits/index.md) to see its awakening and move stats.

## Fruit lives

The shipped build gives a fruit user **three lives**. A qualifying PvP death spends one life. The third removes your Devil Fruit powers. Deaths to mobs or the environment do not use a life unless another player is credited for the kill. Deaths in protected fights where stat loss is disabled are exempt.

Infused weapons carry **three lives of their own**. If you carry one when you suffer a qualifying PvP death, it loses a life. At zero, the weapon shatters and releases the fruit inside. Trading the weapon passes on its remaining lives.

## Water and Logia

Staying in water as a fruit user is dangerous. The pack targets roughly **25 seconds** to die if you stay submerged, with a damage interval of 20 ticks. [Bubble supplies](../world/survival.md#fruit-users-and-bubbles) make underwater travel easier.

Eligible attacks from hostile Mine Mine no Mi mobs can hit a Logia body in late Paradise, the New World, the Red Line, and the Nether.

**Pack sources:** `ompworld/fruit-rot.toml`, `ompworld/devil-fruit-water.toml`, `mineminenomi-server.toml`, `mineminenomiawakenpath-common.toml`, `eternalvoyage-companion.json`, `hakirework-server.toml`, and the KubeJS fruit script and box data.
