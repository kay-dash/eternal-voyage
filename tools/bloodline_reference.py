"""Generate player bloodline pages using the pack's configured birth rolls."""

from playable_reference import stat_table


# Names and perks from Haki Realm's Lineage, Lineages, BloodPerks, Growth and Professions.
LINEAGES = {
    "will_of_d": ("willOfDChance", "Will of D.", "Roger, Luffy, Garp and Teach",
                  "A killing blow can leave you standing at 2 HP, clearing Poison and Wither. The World Government will turn you away.",
                  [("Health after surviving a killing blow", "2 HP"), ("Survival cooldown", "10 min"),
                   ("Resistance IV on survival", "3 s"), ("Regeneration II on survival", "5 s")]),
    "kozuki": ("kozukiChance", "Kozuki Clan", "Oden, Momonosuke and Hiyori",
               "You inherit the [Voice of All Things](../haki.md#voice-of-all-things) and can read Poneglyphs "
               "with an empty hand. This includes the Road Poneglyph readings tracked by the pack.",
               [("Doriki required for Oden Two-Sword Style lessons", "25% less")]),
    "vinsmoke": ("vinsmokeChance", "Vinsmoke Lineage Factor", "Sanji, Ichiji, Niji and Yonji",
                 "An engineered exoskeleton helps you stay standing, and food helps you heal. Black Leg kicks hit harder.",
                 [("Armour", "+4"), ("Armour toughness", "+2")]),
    "shimotsuki": ("shimotsukiChance", "Shimotsuki Clan", "Ryuma, Koshiro, Kuina and Zoro",
                   "Sword hits are stronger with a sword in your main hand. The lesson discount applies to "
                   "[sword schools](../schools.md), including Oden Two-Sword Style.",
                   [("Sword damage bonus", "+8%"), ("Doriki required for sword-school lessons", "25% less")]),
    "charlotte": ("charlotteChance", "Charlotte Family", "Katakuri, Smoothie and Cracker",
                  "You gain maximum health and resist knockback. Food restores extra hunger, based on how much it normally restores.",
                  [("Maximum health", "+4 HP"), ("Knockback resistance", "+0.30"),
                   ("Extra hunger points", "25% of the food's hunger value, rounded, minimum 1")]),
    "figarland": ("figarlandChance", "Figarland Family", "Shanks, Garling and Shamrock",
                  "This line gives you another chance to be born with Conqueror’s Haki. Sword hits are stronger "
                  "with a sword in your main hand, and your Conqueror’s Haki grows faster once awakened.",
                  [("Extra birth roll for Conqueror’s Haki", "15% if the regular roll misses"),
                   ("Conqueror’s Haki XP", "1.25×"), ("Sword damage bonus", "+5%")]),
    "nefertari": ("nefertariChance", "Nefertari Family", "Vivi, Cobra and Lili",
                  "You restore health to nearby injured crewmates who have enough hunger. "
                  "Nearby villagers also grant you Hero of the Village.",
                  [("Crew healing radius", "24 blocks"), ("Healing per crewmate", "1 HP every 6 s"),
                   ("Crewmate hunger requirement", "6 hunger points (3 drumsticks)"),
                   ("Villager check", "16 blocks"), ("Hero of the Village duration", "10 s, refreshed near villagers")]),
    "kurozumi": ("kurozumiChance", "Kurozumi Clan", "Orochi, Kanjuro, Higurashi and Semimaru",
                 "While sneaking, you are harder for mobs to acquire as a new target. The clan also takes reduced fall damage.",
                 [("New target acquisition while sneaking", "Blocked beyond 6 blocks"),
                  ("Fall damage taken", "67% of normal")]),
    "monkey": ("monkeyChance", "Monkey Family", "Garp, Dragon and Luffy",
               "Your bare-handed hits deal more damage and your [Hardening branch](../haki-tree.md#hardening) grows faster.",
               [("Bare-handed damage", "1.10×"), ("Hardening mastery gain", "1.20×")]),
    "riku": ("rikuChance", "Riku Family", "Riku Dold III, Viola and Rebecca",
             "Observation’s Aura reaches further and [Sense](../haki-tree.md#sense) grows faster.",
             [("Aura range", "1.25×"), ("Sense mastery gain", "1.20×")]),
    "portgas": ("portgasChance", "Portgas Line", "Rouge and Ace",
                "You take less fire damage and hit harder when badly injured.",
                [("Fire damage taken", "50% of normal"), ("Outgoing damage below one-third health", "1.10×")]),
    "ryugu": ("ryuguChance", "Ryugu Royal Line", "Neptune, Shirahoshi and Fukaboshi",
              "Sea Kings, Guardians, Drowned and other aquatic animals that use the same target check leave you alone. "
              "Underwater, you receive Water Breathing and Dolphin’s Grace.",
              [("Water effects", "3 s, refreshed every 2 s while in water")]),
    "silvers": ("silversChance", "Silvers Line", "Rayleigh",
                "[Emission](../haki-tree.md#emission) grows faster and damaging techniques on its branch hit harder.",
                [("Emission mastery gain", "1.20×"), ("Ryuo damage", "1.05×")]),
}


def bloodline_reference(config, akuma_traits, grafts, docs, write):
    directory = "characters/bloodlines"
    akuma_active = akuma_traits.get("enabled", True)
    akuma_share = akuma_traits.get("chanceOnFirstJoin", 10) / 200 if akuma_active else 0
    index = ["# Bloodlines", "",
             "A bloodline is rolled once per player when they first join and can belong to any race. "
             "It appears in the **Trait** line of your character stats. You can be born without one.", ""]
    rows = []
    published = {"index"}

    def publish(slug, title, owner, description, stats):
        icon = "../../assets/mods/" + ("hakirework.png" if owner == "Haki Realm" else "akuma.png")
        lines = [f"# {title}", "", f"![]({icon}){{ .entry-page-icon }}", "",
                 "[All bloodlines](index.md)", "", description, "", *stat_table(stats)]
        write(f"{directory}/{slug}.md", lines)
        published.add(slug)

    if config["enabled"]:
        for slug, (key, title, examples, description, stats) in LINEAGES.items():
            odds = config[key]
            if odds <= 0:
                continue
            info = [("Haki Realm birth roll", f"{100 * odds:g}%"), ("Known carriers", examples), *stats]
            if slug == "will_of_d":
                info.extend([("Extra birth roll for Conqueror’s Haki", f"{100 * config['willOfDConquerorChance']:g}% if the regular roll misses")])
                if akuma_active:
                    info.extend([("Akuma birth roll", f"{akuma_share:.1%}"),
                                 ("Haki XP and bounty from eligible gains", "1.25× each")])
                description += " Follow the [Inherited Will quests](../../reference/quests/r_traits.md)."
            if slug == "kozuki":
                description += " See [Oden Two-Sword Style](../../reference/content/hakirework/schools/oden_nitoryu.md)."
            publish(slug, title, "Haki Realm", description, info)
            chance = f"{100 * odds:g}% Haki Realm"
            if slug == "will_of_d" and akuma_active:
                chance += f" or {akuma_share:.1%} on Akuma’s roll"
            rows.append((f"[{title}]({slug}.md)", chance, examples))
    if akuma_active:
        celestial_odds = akuma_share
        upgrade_percent = akuma_traits.get("celestialDragonBoxUpgradeChance", 20)
        bounty = akuma_traits.get("heavenlyDemonBounty", 500_000)
        if "will_of_d" not in published:
            publish("will_of_d", "Will of D.", "Akuma no Mi",
                    "The World Government will turn you away. Follow the "
                    "[Inherited Will quests](../../reference/quests/r_traits.md).",
                    [("Akuma birth roll", f"{akuma_share:.1%}"),
                     ("Haki XP and bounty from eligible gains", "1.25× each")])
            rows.append(("[Will of D.](will_of_d.md)", f"{akuma_share:.1%} Akuma", "Roger, Luffy, Garp and Teach"))
        publish("celestial_dragon", "Celestial Dragon Blood", "Akuma no Mi",
                "World Noble heritage increases Belly gains and can improve a fruit box when you open it. "
                "Follow the [Celestial Blood quest](../../reference/quests/r_traits.md#q-7a786fd8c1865132).",
                [("Akuma birth roll", f"{celestial_odds:.1%}"), ("Belly from eligible gains", "1.25×"),
                 ("Chance of upgrading an eligible fruit box by one tier", f"{upgrade_percent}%")])
        publish("heavenly_demon", "Heavenly Demon", "Akuma no Mi",
                "First reach Celestial Dragon rank in the World Government with Celestial Dragon Blood. "
                "After leaving the World Government, become a pirate captain and meet the bounty requirement, "
                "or join a crew whose captain is online and carries Will of D.",
                [("Birth roll", "Earned in play"), ("Bounty needed when captaining your own crew", f"{bounty:,}"),
                 ("Haki XP and Belly from eligible gains", "1.15× each")])
        rows.extend([("[Celestial Dragon Blood](celestial_dragon.md)", f"{celestial_odds:.1%} Akuma", "World Nobles"),
                     ("[Heavenly Demon](heavenly_demon.md)", "Earned in play", "Donquixote Doflamingo")])
    if rows:
        index.extend(["## Bloodline catalogue", "", "Each percentage applies to the named birth roll. "
                      "An already assigned Akuma bloodline carries through to your character stats.", "",
                      "| Bloodline | How to get it | Known carriers |", "| --- | --- | --- |",
                      *(f"| {name} | {odds} | {examples} |" for name, odds, examples in rows), ""])
    index.extend(["## Grafted Lineage Factors", "",
                  "A player with the [Nomi Nomi no Mi](../fruits/nomi_nomi_no_mi.md) "
                  "can graft Lineage Factors onto another player. Grafts have their own capacity and can coexist "
                  "with a bloodline. See [Borrowed Blood](../../reference/quests/r_traits.md#q-29161f26afbbc28c).", "",
                  *stat_table([("Stable grafts", grafts["stableTraits"]),
                               ("Maximum HP loss per excess graft", f"{grafts['unstableHealthLoss']:.0%}"),
                               ("Weakening of every graft per excess graft", f"{grafts['unstableWeakening']:.0%}"),
                               ("Grafts persist through death", "Yes" if grafts["traitsKeptOnDeath"] else "No")])])
    write(f"{directory}/index.md", index)
    for stale in (docs / directory).glob("*.md"):
        if stale.stem not in published and stale.read_text(encoding="utf-8").startswith("<!-- Generated by"):
            stale.unlink()
