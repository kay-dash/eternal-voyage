"""Render profession tables from the installed trade data and pack overrides."""

from collections import Counter, defaultdict
import json
from pathlib import Path
from zipfile import ZipFile


TRADES = {
    "blacksmith": ("Forge", "forging", "Weapons, ammunition, and forged gear."),
    "carpenter": ("Shipyard", "shipbuilding", "Cruise boats, hull repairs, lockers, and building plans."),
    "chemist": ("Laboratory", "chemistry", "Medicine, powders, thrown concoctions, and Rumble Balls."),
    "cook": ("Kitchen", "cooking", "Meals that feed, heal, and improve training."),
    "farmer": (None, None, "Orchards, crops, and higher-quality produce."),
    "fisher": (None, None, "Fish, shellfish, rare catches, and Calm Belt Sea Kings."),
    "hunter": ("Tannery", "tanning", "Nets, traps, small creatures, and big-game hunts."),
    "inventor": ("Workshop", "inventing", "Tools, instruments, dials, and upgrade parts."),
    "lumberjack": (None, None, "Speciality woods and timber for the crew’s boatbuilder."),
    "merchant": (None, None, "Sales, contracts, auctions, and buried treasure."),
    "miner": ("Masonry", "masonry", "Ore, rare finds, stonework, and refined materials."),
    "musician": ("Music Stand", "composing", "Scores and trade, travel, or combat buffs for your crew."),
    "navigator": ("Chart Table", "charting", "Charts, bearings, weather forecasts, and exploration."),
    "tailor": ("Sewing Table", "tailoring", "Clothing, flags, sails, and temperature linings."),
}
FRUIT_PERKS = {
    "extra_output": "Can yield an extra item",
    "ingredient_back": "Can preserve an ingredient",
    "faster_techniques": "Shorter profession ability cooldowns",
    "faster_gathering": "Faster gathering",
}


def load_trade_data(pack):
    data, lang = {}, {}
    for prefix in ("mine-mine-no-mi", "inomissing", "inosky", "inocruise", "eternalvoyage"):
        with ZipFile(next((pack / "mods").glob(f"{prefix}-*.jar"))) as jar:
            for name in jar.namelist():
                if name.endswith("/lang/en_us.json") and name.startswith("assets/"):
                    lang.update(json.loads(jar.read(name)))
                if name.startswith(("data/inocruise/", "data/eternalvoyage/recipes/tailoring/")) and name.endswith(".json"):
                    section = name.split("/")[2]
                    if section in {"recipes", "talent_webs", "fishing", "hunting", "big_game",
                                   "creature_spawns", "trapping", "mining", "fruit_trades", "professions"}:
                        data[name] = json.loads(jar.read(name))
    root = pack / "kubejs"
    for path in sorted((root / "data").rglob("*.json")):
        name = path.relative_to(root).as_posix()
        if name in data or name.startswith(("data/inocruise/recipes/", "data/inocruise/fishing/")):
            data[name] = json.loads(path.read_text(encoding="utf-8-sig"))
    return data, lang


def namespaced_name(key, lang):
    namespace, _, name = key.lstrip("#").partition(":")
    fallback = name.removeprefix("is_").replace("_", " ").title()
    if key.startswith("#"):
        return "Any " + fallback
    return next((lang[k] for category in ("item", "block", "entity", "biome")
                 if (k := f"{category}.{namespace}.{name}") in lang), fallback)


def ingredient_name(ingredient, lang):
    if isinstance(ingredient, list):
        return " or ".join(ingredient_name(item, lang) for item in ingredient)
    return namespaced_name(ingredient.get("item") or "#" + ingredient["tag"], lang)


def recipe_lines(data, lang, workstation, kind, banned, table, label):
    recipe_name = "masonry_bench" if kind == "masonry" else workstation.lower().replace(" ", "_")
    raw = data[f"data/inocruise/recipes/{recipe_name}.json"]
    row = lambda pattern: " · ".join("—" if ch == " " else ingredient_name(raw["key"][ch], lang)
                                    for ch in pattern.ljust(3))
    lines = ["", f"## {workstation}", "", "Craft the workstation at a crafting table."]
    lines.extend(table(("Top row", "Middle row", "Bottom row"), [tuple(row(pattern) for pattern in raw["pattern"])]))
    rows = []
    for recipe in data.values():
        if recipe.get("type") != f"inocruise:{kind}":
            continue
        output = recipe["result"]
        ingredients = recipe["ingredients"]
        if any(item in banned for item in item_ids(recipe)):
            continue
        counts = Counter(ingredient_name(it, lang) for it in ingredients)
        materials = ", ".join(f"{n} × {name}" if n > 1 else name for name, n in counts.items())
        name = namespaced_name(output["item"], lang)
        if recipe.get("learned"):
            name += " (learn from a Score Recipe)"
        rows.append((label(name), recipe["level"], output.get("count", 1), recipe["xp"], label(materials)))
    lines.extend(["", "### Recipes"])
    lines.extend(table(("Makes", "Level", "Yield", "XP", "Ingredients"),
                       sorted(rows, key=lambda r: (r[1], r[0].casefold()))))
    return lines


def item_ids(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "item" and isinstance(child, str):
                yield child
            yield from item_ids(child)
    elif isinstance(value, list):
        for child in value:
            yield from item_ids(child)


def region_names(ids, lang):
    return ", ".join(namespaced_name(key.lstrip("#"), lang) for key in ids) or "Any eligible area"


def field_tables(trade, data, lang, table, label):
    collections = defaultdict(dict)
    for path, row in data.items():
        parts = path.split("/")
        collections[parts[2]][parts[-1].removesuffix(".json")] = row
    if trade == "fisher":
        rows = []
        for key, fish in collections["fishing"].items():
            name = namespaced_name(fish["item"], lang)
            if fish.get("summons"):
                name = {"sea_king_large": "Sea King", "sea_king_extra_large": "Extra-large Sea King",
                        "sea_king_goldfish": "Goldfish Sea King"}.get(key, name)
            waters = region_names(fish.get("biomes", []), lang)
            for key, title in (("min_y", "Y at least"), ("max_y", "Y at most")):
                if key in fish:
                    waters += f" · {title} {fish[key]}"
            if fish.get("fluid") == "lava" or fish.get("fluid") == "minecraft:lava":
                waters += " · Lava"
            depth = f"{fish.get('min_depth', 1)}–{fish['max_depth']}" if "max_depth" in fish else f"{fish.get('min_depth', 1)}+"
            size = fish.get("size", {})
            length = f"{size['min']:g}–{size['max']:g}" if size else "—"
            rows.append((label(name), fish.get("min_level", 1), label(waters),
                         depth, f"{fish['chance']:.2%}",
                         length, f"{fish['xp']} / {fish.get('first_catch_xp', 0)}"))
        return ["", "## Catch catalogue", "",
                "Chances are base entry values. The place, depth and your level determine which catches can roll. "
                "Special conditions such as weather, dimension and fishing in lava still apply.",
                *table(("Catch", "Level", "Waters", "Depth", "Chance", "Size (cm)", "XP / first"), sorted(rows, key=lambda r: (r[1], r[0])))]
    if trade == "hunter":
        rows = []
        for key, animal in collections["hunting"].items():
            spawn = collections["creature_spawns"].get(key, {})
            rows.append((label(namespaced_name(animal["entity"], lang)), animal.get("min_level", 1),
                         label(region_names(spawn.get("biomes", []), lang)) if spawn else "See the Bestiary",
                         animal.get("tool", "").split(":")[-1].replace("_", " ").title() or "Net",
                         f"{animal['xp']} / {animal.get('first_capture_xp', 0)}",
                         f"{animal.get('rare_variant_multiplier', 1)}×"))
        game = [(label(namespaced_name(animal["entity"], lang)), animal["min_level"],
                 f"{animal['xp']} / {animal['first_kill_xp']}") for animal in collections["big_game"].values()]
        traps = [(label(namespaced_name(animal["entity"], lang)), label(region_names(animal.get("biomes", []), lang)),
                  "Yes" if animal.get("requires_sky") else "No",
                  "Enhanced" if animal.get("traps") else "Standard or enhanced")
                 for animal in collections["trapping"].values()]
        return ["", "## Small creatures",
                *table(("Creature", "Level", "Habitat", "Tool", "XP / first", "Rare XP"), sorted(rows, key=lambda r: (r[1], r[0]))),
                "## Trapping",
                *table(("Creature", "Habitat", "Open sky", "Trap"), sorted(traps)),
                "## Big game",
                *table(("Beast", "Level", "XP / first"), sorted(game, key=lambda r: (r[1], r[0])))]
    if trade == "miner":
        rows = []
        finds = []
        for vein in collections["mining"].values():
            blocks = label(region_names(vein["blocks"], lang))
            rows.append((blocks, vein.get("xp", 0)))
            for find in vein.get("finds", ()):
                finds.append((blocks, label(namespaced_name(find["item"], lang)), find.get("min_level", 1),
                              f"{find['chance']:.2%}", find.get("xp", 0)))
        return ["", "## Mining XP", *table(("Block", "XP"), sorted(rows, key=lambda r: (-r[1], r[0]))),
                "## Finds in the rock", *table(("Mine", "Find", "Level", "Chance", "Extra XP"),
                                              sorted(finds, key=lambda r: (r[2], r[0], r[1])))]
    return []


def talent_table(trade, web, lang, table, label):
    neighbors = defaultdict(list)
    display = {}
    for a, b in web["links"]:
        neighbors[a].append(b)
        neighbors[b].append(a)
    flat_bonuses = {"salvager", "hearty_meals", "sea_king_hunter", "collector", "light_step",
                    "still_air", "sharp_teeth", "planting_xp"}
    for node_id, node in web["nodes"].items():
        key = f"talent.inocruise.{trade}.{node['bonus']}"
        name = lang.get(key, node_id.replace("_", " ").title())
        value = node["value"]
        shown_value = f"{value:g}" if node["bonus"] in flat_bonuses else f"{value:.0%}"
        description = lang.get(f"{key}.desc", "").replace("%s", shown_value)
        display[node_id] = (name, description)
    duplicate_names = Counter(name for name, _ in display.values())
    occurrences = Counter()
    for node_id, (name, description) in display.items():
        occurrences[name] += 1
        if duplicate_names[name] > 1:
            display[node_id] = (f"{name} {occurrences[name]}", description)
    rows = []
    for node_id, node in web["nodes"].items():
        name, effect = display[node_id]
        kind = node["kind"].title() + (" · Start" if node_id in web["starts"] else "")
        adjacent = ", ".join(display[other][0] for other in neighbors[node_id])
        rows.append((label(name), kind, label(effect or "See the ability or talent in your profession book."), label(adjacent)))
    return table(("Talent", "Kind", "Effect", "Connects to"), rows)


def profession_reference(pack, docs, banned, table, label, write):
    data, lang = load_trade_data(pack)
    catalogue = ["# Professions", "", "[Choosing your two trades](../factions-and-trades.md#professions)", "",
                 "Choose a trade for its controls, progression, crafting and talents. The quest chapter is linked from each guide."]
    catalogue_rows = []
    talent_index = ["# Trade talents", "", "[Profession catalogue](professions/index.md)", "",
                    "Each trade has its own talent web. Start at an entry node and work through connected talents. "
                    "Equip any unlocked combat techniques from the **Profession** tab of the ability screen."]
    with ZipFile(next((pack / "mods").glob("inocruise-*.jar"))) as jar:
        icons = {trade: jar.read(f"assets/inocruise/textures/gui/profession/{trade}.png") for trade in TRADES}
    for trade, (station, kind, summary) in TRADES.items():
        title = lang.get(f"profession.inocruise.{trade}", trade.title())
        icon = f"gui/profession/{trade}.png"
        dest = docs / "assets/playable/inocruise" / icon
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(icons[trade])
        catalogue_rows.append((f"![](../../assets/playable/inocruise/{icon}){{ .entry-move-icon }} [{title}]({trade}.md)", summary))
        talent_index.extend(["", f'<a id="{trade}"></a>', f"- [{title} talents](professions/{trade}.md#talents)"])
        lines = field_tables(trade, data, lang, table, label)
        if station:
            lines.extend(recipe_lines(data, lang, station, kind, banned, table, label))
        perks = []
        for name, fruit in data.items():
            if name.startswith("data/inocruise/fruit_trades/") and (perk := fruit["trades"].get(f"inocruise:{trade}")):
                if fruit["fruit"] in banned:
                    continue
                title = namespaced_name(fruit["fruit"], lang)
                slug = fruit["fruit"].split(":")[1]
                if (docs / f"characters/fruits/{slug}.md").is_file():
                    title = f"[{title}](../fruits/{slug}.md)"
                perks.append((title, FRUIT_PERKS[perk]))
        if perks:
            lines.extend(["", "## Devil Fruit bonuses", "", "These fruits also grant **15% more XP** in this trade."])
            lines.extend(table(("Fruit", "Additional effect"), sorted(perks)))
        lines.extend(["", "## Talents", "", "Spend your talent points in the profession book. Techniques open in the **Profession** tab of the ability screen."])
        web = data[f"data/inocruise/talent_webs/{trade}.json"]
        lines.extend(talent_table(trade, web, lang, table, label))
        lines.extend(["", "## Quest chapter", "", f"[{title} milestones and rewards](../../reference/quests/{trade}.md)."])
        p = docs / f"characters/professions/{trade}.md"
        marker = "<!-- Pack profession tables -->"
        source, _, _ = p.read_text(encoding="utf-8").partition(marker)
        p.write_text(source.rstrip() + "\n\n" + marker + "\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")
    catalogue.extend(table(("Profession", "What you do"), catalogue_rows))
    write("characters/professions/index.md", catalogue)
    write("characters/trade-talents.md", talent_index)
