# Doriki and Haki

## Doriki and health

The baseline Doriki cap is **50,000**. The pack’s curved base-health scale reaches **250 HP** at 10,000 Doriki and **500 HP** at the cap. See [Combat stats and Doriki scaling](combat-stats.md) for intermediate HP values and all damage curves.

## Awaken and train Haki

**Haki first awakens in the Grand Line.** You cannot unlock or train it in the Blues or the Calm Belt. When you first enter **Paradise**, Kuja awaken Armament and Observation and Three-Eye characters awaken Observation. If you already met the conditions for a deferred awakening during your time in the Blues, it takes effect on entry.

Once you reach Paradise, choose a combat awakening or train with a mentor. Combat awakening generally needs **500 Doriki**, a foe configured to count as at least twice your strength, and a drop to **20% health**. Survive for 30 seconds or defeat the foe sooner. Mentors and training can awaken Haki without that Doriki minimum.

### Mentors, sparring and meditation

Mentors can teach a Haki type once they have **50% of its XP limit**, and can take up to three apprentices. An apprentice can wake Armament with **40 hits landed** on a mentor, or Observation with **25 hits taken while blind**. The mentor technique lesson requires **20 qualifying hits**. Apprentices get double sparring XP. Nearby mentors earn 10% of an apprentice’s Haki XP. You can use `/haki mentor` and `/haki accept` to set up a player apprenticeship.

Meditation trains Observation. A blindfold doubles its gain, and waterfall training can train both Armament and Observation. A session lasts up to one minute, with a three-minute rest. The configured base is **0.15 XP per 10 seconds** and a daily limit of **6 XP per Haki kind** through that training.

### Branches, limits and surges

| Kind | Branches | What to train for |
| --- | --- | --- |
| Armament (Busoshoku) | Hardening, Imbuing, Emission | Defend and fight with hardened fists, coat weapons and shots, or strike with projected Haki. |
| Observation (Kenbunshoku) | Sense, Evasion, Foresight | Track targets, sidestep attacks, or develop Future Sight. |
| Conqueror’s (Haoshoku) | Presence, Domination, Coating | Broaden or sustain your presence, overpower enemy wills, or coat your strikes. Coating starts growing after Presence and Domination total **40 mastery**. |

| Character | Branch maximum | Budget per Haki kind |
| --- | ---: | ---: |
| Fruitless | 60 | 140 |
| Devil Fruit user | 52 | 100 |

Fork choices at **20 and 40** and keystones at **60** shape your build. Mastery pauses at the surge thresholds until a qualifying fight. The active conditions include a qualifying foe when you drop to half health, fighting a boss, three enemies on you at once, or a 45-second fight against a foe at least half as strong. A surge lasts 60 seconds, refills the Haki bar, and halves the branch’s cooldowns during the surge. Nearby crewmates can gain **1.5 mastery** in their strongest branch. Formations use at least three nearby crewmates with different strongest branches.

Techniques also require Doriki. A technique at mastery 60 targets **80% of the baseline Doriki limit** (40,000 here), with lower steps scaling proportionally. Base techniques can have higher floors. For example, Hardening and Imbuing have a **4,000 Doriki** minimum, and Internal Destruction has an **8,000 Doriki** minimum. Passive nodes use mastery. Resetting branch forks through a mentor costs **100,000 Belly**, loses half the branch mastery, and has a **24-real-hour** cooldown. A Kokuto Forge also supports resetting forks.

See the [Haki tree techniques](haki-tree.md) for every branch and node. **Kamusari** sits at **30 Coating** with Rayleigh, **Galaxy Impact** at **40** and **Galaxy Divide** at **48** with Garp, and **Ragnaraku** at **50** with Kaido. **Observation Killer** opens at **30 Domination**. Player Galaxy Impact lifts you into the air before you aim and dive toward the impact point. Aim within **48 blocks**.

### Haki in combat

- **Guard.** Sneak while hardened or holding an imbued sword to block frontal hits. The configured block scales from **20% up to 70%** with Armament XP and costs Haki. The separate Armament Guard tree technique has a short window for stopping the next hit.
- **Observation.** Aura gives a configured sidestep chance from **5% to 25%** as Observation grows. Blindness or Darkness grants a **3×** XP bonus to applicable Observation training. Burning, poison, withering, nausea, or losing 30% of your health within two seconds can cloud Observation and prevent sidesteps or Future Sight.
- **Stacked defence.** Haki Realm’s cap on combined post-armour player buffs is **80% reduction**. The companion has a corresponding player-defence cap. The [move damage table](../reference/settings/move-damage.md) gives the configured per-move adjustments.

### Haki clashes

When two Haki-coated hits meet within **0.5 seconds**, the stronger side gains an edge. A normal clash shifts damage by up to **50%** and awards **0.05 Armament XP** to each side before growth modifiers.

When Conqueror’s coatings meet or active Conqueror’s bursts overlap, both fighters can lock into a contest of wills. Conqueror’s level, Armament, and remaining health affect pressure. Press attack to push the contest in your favour. A decisive loss can knock you out.

| Contest rule | Pack value |
| --- | --- |
| Time limit | 6 s |
| Attack presses counted | Up to 6 per second |
| Pressure per press | +4 |
| Haki overuse per press | +30 |
| Haki drained from the loser | 30% |
| Knockout after a crushing loss | 3 s |
| Conqueror’s level for both fighters to split the sky | 60 |
| Cooldown for another overlapping-burst clash between the same players | 30 s |

Legend opponents put up more pressure while fighting seriously, and less after they are wounded. Hard fights add pressure. See [Willpower](willpower.md) for Haki capacity, refill, and knockout resistance passives.

### Fruitless crew scaling

At **50,000 Doriki**, eligible Haki damage, Haki’s added damage on qualifying hits, and fighting-style damage scale to **1.50×** for a fruit user, **2.50×** for a fruitless player, or **2.75×** for a member of an entirely fruitless crew. The crew bonus begins above **10,000 Doriki** and adds **0.125×** at **30,000** and **0.25×** at the cap. See the [full damage table](combat-stats.md#damage-from-doriki).

The roster must have **at least three members**, and every member must be fruitless. Offline members count using their last recorded status. Crewmates can be anywhere. If even one member has a fruit, the fruitless members use their individual **2.50×** cap instead.

Haki Realm gives each fruitless player a **1.5× Haki bar**, **1.5× Armament and Observation XP**, and the larger branch budget described above. The crew damage rule adds to none of those values. **Crew formations** use nearby members with different strongest branches. The [surge and formation rules](#branches-limits-and-surges) explain that mechanic.

## Conqueror’s Haki

Haki Realm handles who can awaken Conqueror’s Haki. Its base birth chance is **5%**. A character who was born with it has a faster growth rate and can draw it out through a mentor or the natural awakening conditions.

A character born with Conqueror’s Haki can awaken it naturally in a crisis once Armament and Observation are awake and they reach **30% of the Doriki cap** (15,000 on the baseline). They can also take a mentor’s **15-second** King’s Test. They gain Conqueror’s mastery **1.5×** as fast.

To earn it, sail into the New World, reach **70%** of your limits in both Armament and Observation, defeat **Rayleigh**, and defeat a qualifying Emperor or Admiral. The config lists Whitebeard, Big Mom, Kaido, Shanks, Blackbeard, Aokiji, Kizaru, and Akainu. The King’s Test for an earned candidate lasts **60 seconds**, with a blackout threshold of **10% health**. An additional secret unlock condition is open to any player. Follow [The Haki of Kings](../reference/quests/h_kings.md). See [Bloodlines](bloodlines/index.md) for the extra birth rolls from Will of D. and Figarland.

## Voice of All Things

This is an Observation-related gift with a **5%** configured birth chance. The Sense tree also offers it as a mastery-40 fork. The Eternal Voyage settings enable treasure and fruit listening, Sea King detection, and a calming interaction. The configured ranges are **32 blocks** for treasure, **96** for Sea Kings and **64** for crew. Calm lasts **30 seconds**, with a **20-second** cooldown setting. The Blind trait can train its linked Observation feature.

**Pack sources:** `mineminenomi-server.toml`, `hakirework-server.toml`, `ompworld/doriki-health.toml`, `eternalvoyage-companion.json`, and `hakirework_ev_kings.json`.
