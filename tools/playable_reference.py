"""Read playable-content registries and explicit move stats from the shipped builds."""

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
import tomllib
from zipfile import ZipFile

from mod_cards import MOD_CARDS


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack"
DOCS = ROOT / "docs"
REGISTRIES = {
    "mineminenomi": "xyz.pixelatedw.mineminenomi.init.ModFruits",
    "inofruits": "com.inovactio.inofruits.init.InoItems",
    "inomissing": "com.inovactio.inomissing.init.MissingItems",
    "akuma": "net.blitz.akuma.init.AkumaFruits",
    "blitzutility": "net.blitz.blitzutility.init.BlitzUtilityFruits",
    "cartaddon": "net.brachiobombastudios.cartaddon.init.CartFruits",
    "awakenawakennomi": "com.inovactio.awakenawakennomi.util.AwakenFruitsData",
}
DIRECT = {"inofruits", "inomissing"}
STAT_NAME = re.compile(r"^(?:(?:[A-Z0-9]+_)*(?:DAMAGE|COOLDOWN)(?:_TICKS)?|[A-Z0-9_]*(?:DURATION|BLEED)_TICKS)$")
INSTRUCTION = re.compile(r"^\s*\d+:\s+(.*)$", re.M)
FIELD = re.compile(r"// Field ([\w/$]+)\.([\w$]+):Lnet/minecraftforge/registries/RegistryObject;")
LANG_FORMAT = re.compile(r"§[0-9a-fk-or]", re.IGNORECASE)
REPLACED_MOVES = {
    "mineminenomi:gear_fifth", "mineminenomi:gomu_gomu_no_gigant", "mineminenomi:gomu_gomu_no_dawn_whip",
    "mineminenomi:fishman_passive_bonuses", "mineminenomi:fishman_damage", "mineminenomi:fishman_swim_speed",
    "mineminenomi:eleclaw", "mineminenomi:sulong", "mineminenomi:electrical_missile",
    "mineminenomi:electrical_tempesta", "mineminenomi:electrical_luna", "mineminenomi:electrical_shower",
}
DAWN_MODES = {
    "pistol": ("pistol", "Dawn Pistol", "Fire a giant stretched punch. The area effect has no separate damage hit.",
               [("PROJECTILE_HIT_DAMAGE", 25), ("COOLDOWN_TICKS", 120)]),
    "gatling": ("gatling", "Dawn Gatling", "Fire 12 punches at intervals of 3 ticks. Damage is listed per projectile.",
                [("PROJECTILE_HIT_DAMAGE", 8.75), ("COOLDOWN_TICKS", 400)]),
    "bazooka": ("cymbal", "Dawn Cymbal", "Charge a giant two-handed strike that flattens targets it catches.",
                [("PROJECTILE_HIT_DAMAGE", 80), ("COOLDOWN_TICKS", 320), ("CHARGE_TICKS", 20),
                 ("FLATTEN_TICKS", 60)]),
    "rocket": ("rocket", "Dawn Rocket", "Launch yourself toward a point within 100 blocks. The launch itself deals no direct damage.",
               [("COOLDOWN_TICKS", 280)]),
}
VERIFIED_STATS = {
    "racenomi:lunarian_blood": [
        ("Bare-handed damage at all times", "+1 HP"),
        ("Damage taken with the flame lit", "50% of eligible damage"),
        ("Movement speed with the flame out", "+40%"),
        ("Attack speed with the flame out", "+25%"),
        ("Additional bare-handed damage with the flame out", "+2 HP"),
        ("Jump height with the flame out", "+0.5 block"),
    ],
    "inofruits:blood_spear": [("Blood cost", "2"), ("Direct hit at standard size", "6 HP + 3% of maximum HP")],
    "racenomi:ray_body": [("Armour toughness", "+1"), ("Bare-handed damage", "+2 HP"), ("Bare-handed attack speed", "+25% of base")],
    "racenomi:garfish_body": [("Swim speed", "+100% of base")],
    "racenomi:octopus_body": [("Attack speed (armed or unarmed)", "+30% of base")],
    "racenomi:whale_shark_body": [("Armour toughness", "+2"), ("Maximum health from passive", "+4 HP")],
    "racenomi:pufferfish_body": [("Spine damage on an eligible hit", "2 HP"), ("Poison chance", "25%"),
                                ("Poison duration", "3 s (60 ticks)")],
    "racenomi:hammerhead_body": [("Melee damage", "+2 HP"), ("Knockback strength", "1.5")],
    "awakenawakennomi:gomu_gomu_no_dawn_whip": [("Sweep reach", "9 blocks"), ("Sweep duration", "0.4 s (8 ticks)")],
    "awakenawakennomi:gomu_gomu_no_dawn_gatling": [("Projectiles per cast", "12"), ("Interval", "0.15 s (3 ticks)")],
    "awakenawakennomi:gomu_gomu_no_dawn_rocket": [("Maximum reach", "100 blocks")],
    "awakenawakennomi:gear_fifth": [("Maximum duration", "180 s"), ("Damage taken from eligible hits", "50%"),
                                   ("Air running per takeoff", "3 s")],
    "awakenawakennomi:gomu_gomu_no_gigant": [("Maximum duration", "30 s")],
}
AWAKENING_STATS = {
    "ao_no_rakka": [("Hits per enemy", "1"), ("Healing per enemy, first three hit", "20 HP")],
    "ancient_spine_saw": [("Hits per enemy", "1")],
    "horn_drill": [("Hits per enemy", "1")],
    "ivory_catastrophe": [("Hits per enemy", "1")],
    "reverse_slow_smash": [("Hits per enemy", "1"), ("Damage by stored attacks", "20 / 40 / 70 / 120 HP")],
    "diosa_fleur": [("Clone duration", "60 s"), ("Clone damage", "20 HP")],
    "living_feast": [("Golem duration", "60 s")],
    "anesthesia": [("Minimum interval between hits to one target", "2 s")],
    "loves_punishment": [("Minimum interval between petrifications", "10 s")],
    "drought_siphon": [("Enemies that provide healing", "First 3 hit")],
    "inga_samsara": [("Maximum reflected damage per enemy", "200 HP")],
}
FORM_STATS = {
    "awakenawakennomi:gomu_gomu_no_gigant": [
        ("Punch damage", "+10 HP"), ("Armour", "+8"), ("Toughness", "+2"),
        ("Entity reach", "+6 blocks"), ("Block reach", "+6 blocks"),
        ("Step height", "+1.5 blocks"), ("Knockback resistance", "+1"),
    ],
}
MORPH_STATS = {
    "armor": ("Armour", ""), "armorToughness": ("Armour toughness", ""), "punch": ("Punch damage", " HP"),
    "toughness": ("Toughness", ""), "movementSpeed": ("Movement speed", "% of base"), "jump": ("Jump", ""),
    "stepHeight": ("Step height", " blocks"), "gravity": ("Gravity", ""), "health": ("Maximum health", "%"),
}


@dataclass
class Move:
    id: str
    title: str
    description: str
    category: str = ""
    icon: str | None = None
    stats: list[tuple[str, float]] = field(default_factory=list)
    damage_key: str | None = None
    kind: str = ""
    form_stats: list[tuple[str, str]] = field(default_factory=list)
    extra_stats: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class Entry:
    id: str
    title: str
    owner: str
    section: str
    moves: list[str]
    kind: str = ""
    tier: int | None = None
    description: str = ""
    parent: str | None = None
    quest: str | None = None

    @property
    def path(self):
        if self.section in {"fruits", "races", "styles"} and not self.parent:
            return f"characters/{self.section}/{self.id.split(':')[1]}.md"
        return self.legacy_path

    @property
    def legacy_path(self):
        return f"reference/content/{self.owner}/{self.section}/{self.id.split(':')[1]}.md"


def mod_metadata(jar):
    if "META-INF/mods.toml" in jar.namelist():
        return tomllib.loads(jar.read("META-INF/mods.toml").decode("utf-8-sig"))["mods"][0]
    metadata = json.loads(jar.read("fabric.mod.json"))
    return {"modId": metadata["id"], "version": metadata["version"], "logoFile": metadata.get("icon")}


def load_mod(path):
    with ZipFile(path) as jar:
        modid = mod_metadata(jar)["modId"]
        lang = {}
        for name in jar.namelist():
            if name.startswith("assets/") and name.endswith("/lang/en_us.json"):
                lang.update(json.loads(jar.read(name)))
        classes = []
        for name in jar.namelist():
            if not name.endswith(".class"):
                continue
            is_registry = name[:-6].replace("/", ".") == REGISTRIES.get(modid)
            gameplay = any(part in name for part in ("/abilities/", "/ability/", "/projectiles/", "/school/"))
            if is_registry or name.endswith(("/LawRule.class", "/Sole.class")) or gameplay and any(term in jar.read(name) for term in
                                               (b"registerAbility", b"setDamage", b"startCooldown", b"AbilityCore", b"Damage;")):
                classes.append(name[:-6].replace("/", "."))
        textures = sorted(n for n in jar.namelist() if n.startswith("assets/") and n.endswith(".png"))
    return modid, path, lang, classes, textures


def disassemble(javap, source):
    modid, jar, _, classes, _ = source
    checksum = hashlib.sha256(jar.read_bytes())
    checksum.update("\n".join(classes).encode())
    digest = checksum.hexdigest()[:16]
    cache = ROOT / ".cache" / "playable" / f"{modid}-{digest}.txt"
    if not cache.exists():
        chunks = []
        batch = []
        length = 0
        for name in classes:
            if length + len(name) > 16000:
                chunks.append(batch)
                batch, length = [], 0
            batch.append(name)
            length += len(name) + 1
        if batch:
            chunks.append(batch)
        command = [javap, "-J-Dfile.encoding=UTF-8", "-p", "-c", "-constants", "-classpath", str(jar)]
        outputs = [subprocess.check_output([*command, *items], encoding="utf-8") for items in chunks]
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text("".join(outputs), encoding="utf-8")
    text = cache.read_text(encoding="utf-8")
    result = {}
    for fragment in re.split(r'(?m)^Compiled from .*\n', text):
        header = re.search(r"(?m)^(?:public |protected |abstract |final )*(?:class|interface|enum) ([\w.$]+)", fragment)
        if header:
            result[header[1].replace(".", "/")] = fragment
    return result


def stat_number(op):
    if m := re.match(r"[ifd]const_(m1|\d)", op):
        return float(-1 if m[1] == "m1" else m[1])
    if m := re.match(r"(?:bi|si)push\s+(-?\d+)", op):
        return float(m[1])
    if m := re.search(r"// (?:float|double|int|long) (-?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?)", op):
        return float(m[1])
    return None


def string(op):
    if "// String " in op:
        return op.split("// String ", 1)[1].replace("\\'", "'")
    return None


def describe(key, locale):
    return " ".join(value for k, value in locale.items()
                    if k == key + ".description" or k.startswith(key + ".description.")
                    or k in (key + ".desc", key + ".tip"))


def racial_tooltip_stats(ops):
    """Read fixed numerical racial stats exposed by the in-game tooltip."""
    labels = {
        "STAT_SWIM_SPEED": "Swim speed",
        "STAT_ATTACK_SPEED": "Attack speed",
        "STAT_DAMAGE": "Bare-handed damage",
        "STAT_TOUGHNESS": "Armor toughness",
        "STAT_HEALTH": "Maximum health",
        "STAT_KNOCKBACK": "Knockback resistance",
        "STAT_JUMP": "Additional jump height",
        "STAT_SPEED": "Movement speed",
        "STAT_FALL": "Additional fall resistance",
    }
    for i, op in enumerate(ops[1:-1], 1):
        field = re.search(r"// Field (\w+):", ops[i + 1])
        if "RaceRegistry.stat:" in op and field and (name := string(ops[i - 1])):
            labels[field[1]] = name
    rows = []
    for i, op in enumerate(ops[3:], 3):
        if "RaceRegistry.statLine:" not in op:
            continue
        field = re.search(r"// Field (\w+):", ops[i - 3])
        value = stat_number(ops[i - 2])
        if not field or value is None or not (name := labels.get(field[1])):
            continue
        prefix = (string(ops[i - 1]) or "").removesuffix("%")
        name = name.replace("Bare hand", "Bare-handed")
        normalized = name.lower()
        if normalized.startswith("health healed"):
            unit = " HP"
        elif "seconds" in normalized:
            unit = " s"
        elif any(word in normalized for word in ("reach", "range", "jump", "fall without harm")):
            unit = " blocks"
        elif any(word in normalized for word in ("speed", "taken", "knockback", "gained", "resistance")) and "fall resistance" not in normalized:
            unit = "%"
        elif normalized in {"fall damage", "through armour"} or normalized.startswith(("damage per", "damage under", "damage for", "damage with", "first blow damage")):
            unit = "%"
        elif ("health" in normalized or "damage" in normalized) and "toughness" not in normalized:
            unit = " HP"
        else:
            unit = ""
        rows.append((name, f"{prefix}{value:.5g}{unit}"))
    return rows


def move_from_class(modid, code, locale, known=None):
    ops = INSTRUCTION.findall(code)
    registered = []
    for i, op in enumerate(ops):
        if "registerAbility:(Ljava/lang/String;Ljava/lang/String;" not in op:
            continue
        values = [s for item in ops[max(0, i - 6):i] if (s := string(item))]
        if len(values) >= 2 and re.fullmatch(r"[a-z0-9_]+", values[-2]):
            registered.append((values[-2], values[-1]))
    if known:
        move_id, title = known
    elif len(set(registered)) == 1:
        move_id, title = registered[0]
    else:
        return None
    key = f"ability.{modid}.{move_id}"
    description = describe(key, locale)
    if not description:
        for i, op in enumerate(ops):
            if "registerDescriptionText:" not in op:
                continue
            values = [s for item in ops[max(0, i - 75):i] if (s := string(item)) and len(s) > 32]
            if values:
                description = values[-1]
                break
    category = re.search(r"AbilityCategory\.([A-Z_]+):", code)
    stats = {}
    for name, value in re.findall(r"\b([A-Z0-9_]+) = (-?\d+(?:\.\d+)?)(?:[fFdDlL])?;", code):
        if STAT_NAME.fullmatch(name) and 0 < float(value) < 100000:
            stats[name] = float(value)
    cooldowns = set()
    hits = set()
    for i, op in enumerate(ops[1:], 1):
        num = stat_number(ops[i - 1])
        if not num or num < 0:
            continue
        if "CooldownComponent.getTooltip:(F)" in op:
            stats.setdefault("COOLDOWN", num)
        if "CooldownComponent.startCooldown:(Lnet/minecraft/world/entity/LivingEntity;F)" in op:
            cooldowns.add(num)
        if "DealDamageComponent.getTooltip:(F)" in op:
            stats.setdefault("DAMAGE", num)
        if ".m_6469_:(Lnet/minecraft/world/damagesource/DamageSource;F)Z" in op:
            hits.add(num)
    for method, value in re.findall(
        r"(?m)^  (?:public|protected) (?:float|int|double) (getDamage|getPunchCooldown|getCooldown)\(\);"
        r"\n +Code:\n +0: (.*?)\n +\d+: [fid]return", code,
    ):
        num = stat_number(value)
        if num is not None and num > 0:
            stats.setdefault("DAMAGE" if method == "getDamage" else "COOLDOWN", num)
    named_cooldowns = {value for name, value in stats.items() if "COOLDOWN" in name}
    for num in sorted(cooldowns - named_cooldowns):
        stats[f"COOLDOWN_VARIANT_{num:g}"] = num
    if len(hits) == 1 and not any(name.endswith("DAMAGE") for name in stats):
        stats["FIXED_HIT_DAMAGE"] = hits.pop()
    if move_id == "sawshark_body" and modid == "racenomi":
        stats = {"ADDED_MELEE_DAMAGE": 3, "BLEED_CHANCE_PERCENT": 5, "BLEED_TICKS": 60}
    identity = f"{modid}:{move_id}"
    kind = ""
    if "AbilityType.PASSIVE:" in code:
        kind = "Passive"
    elif "getTransformation();" in code:
        kind = "Active · Transformation"
    elif "AbilityCore$Builder.\"<init>\":" in code:
        kind = "Active"
    form = list(FORM_STATS.get(identity, ()))
    for i, op in enumerate(ops[1:], 1):
        match = re.search(r"akumalib/util/MorphStats\.(\w+):\(D\)", op)
        if match and match[1] in MORPH_STATS and (value := stat_number(ops[i - 1])) is not None:
            label, unit = MORPH_STATS[match[1]]
            if match[1] in ("movementSpeed", "health"):
                value *= 100
            row = label, f"{value:+g}{unit}"
            if row not in form:
                form.append(row)
    return Move(identity, locale.get(key, title), description, category[1] if category else "",
                stats=list(stats.items()), kind=kind, form_stats=form)


def registered_fruits(all_code):
    results = {}
    awakening = {}
    for modid, cls in REGISTRIES.items():
        code = all_code[modid][cls.replace(".", "/")]
        functions, static = code.split("  static {};", 1)
        ops = INSTRUCTION.findall(static)
        if modid == "awakenawakennomi":
            fruit_field = None
            moves = []
            for op in ops:
                match = FIELD.search(op)
                if match and match[1].endswith("/ModFruits"):
                    fruit_field, moves = match[2], []
                elif match and fruit_field:
                    moves.append(move_ref(*match.groups()))
                elif fruit_field and "putstatic" in op and "FruitsData;" in op:
                    awakening[fruit_field] = moves
                    fruit_field = None
            continue

        lambdas = {int(num): INSTRUCTION.findall(body) for num, body in re.findall(
            r"(?ms)^  private static .*? lambda\$static\$(\d+)\(\);\n(.*?)(?=^  \S|\Z)", functions)}
        start = 0
        for i, op in enumerate(ops[:-1]):
            if ".registerFruitItem:" not in op:
                continue
            next_op = ops[i + 1]
            identity = re.search(r"putstatic .*// Field ([A-Z0-9_]+):Lnet/minecraftforge/registries/RegistryObject;", next_op)
            window = ops[start:i]
            start = i + 2
            if not identity:
                continue
            field_id = identity[1]
            strings = [s for item in window if (s := string(item))]
            if not strings:
                continue
            if modid in DIRECT:
                body = window
            else:
                dynamic = [int(m[1]) for item in window if (m := re.search(r"InvokeDynamic #(\d+):get:", item))]
                body = lambdas.get(dynamic[-1], []) if dynamic else []
            fruit_type = next(((i, m[1]) for i, item in enumerate(body)
                               if (m := re.search(r"FruitType\.([A-Z_]+):", item))), None)
            if not fruit_type:
                continue
            position, category = fruit_type
            tier = stat_number(body[position - 1])
            moves = [move_ref(*m.groups()) for item in body[position + 1:] if (m := FIELD.search(item))]
            results[(modid, field_id)] = (strings[-1], int(tier), category, moves)
    return results, awakening


def move_ref(cls, field_name):
    return f"{cls}.{field_name}" if field_name != "INSTANCE" else cls


def read_sources(javap):
    ids = set(REGISTRIES) | {"racenomi", "hakirework", "blackhaki", "infusion"}
    sources = {}
    for path in (PACK / "mods").glob("*.jar"):
        with ZipFile(path) as jar:
            key = mod_metadata(jar)["modId"]
        if key in ids:
            sources[key] = load_mod(path)
    with ThreadPoolExecutor(max_workers=3) as executor:
        pending = {key: executor.submit(disassemble, javap, source) for key, source in sources.items()}
        codes = {key: task.result() for key, task in pending.items()}
    return sources, codes


RACE_FAMILIES = {
    "fishman": ("Fish-Man", "fishman", "r_fishman", {
        "fishman_sawshark": ("Saw-shark Fish-Man", "sawshark_body", "mineminenomi"),
        "fishman_ray": ("Ray Fish-Man", "ray_body", "mineminenomi"),
        "fishman_garfish": ("Garfish Fish-Man", "garfish_body", "mineminenomi"),
        "fishman_octopus": ("Octopus Fish-Man", "octopus_body", "racenomi"),
        "fishman_whale_shark": ("Whale Shark Fish-Man", "whale_shark_body", "racenomi"),
        "fishman_pufferfish": ("Pufferfish Fish-Man", "pufferfish_body", "racenomi"),
        "fishman_hammerhead": ("Hammerhead Fish-Man", "hammerhead_body", "racenomi"),
    }),
    "mink": ("Mink", "mink", "r_mink", {
        "mink_dog": ("Dog Mink", "dog_mink_pack", "mineminenomi"),
        "mink_lion": ("Lion Mink", "lion_mink_body", "mineminenomi"),
        "mink_bunny": ("Bunny Mink", "bunny_mink_legs", "mineminenomi"),
        "mink_cat": ("Cat Mink", "cat_mink_eyes", "racenomi"),
        "mink_jaguar": ("Jaguar Mink", "jaguar_mink_claws", "racenomi"),
        "mink_polar_bear": ("Polar Bear Mink", "polar_bear_mink_fur", "racenomi"),
        "mink_bull": ("Bull Mink", "bull_mink_charge", "racenomi"),
    }),
    "giant": ("Giant", "giant", "r_giant", {
        "elbaf_giant": ("Elbaf Giant", "elbaf_pride", "racenomi"),
        "ancient_giant": ("Ancient Giant", "ancient_blood", "racenomi"),
    }),
    "wotan": ("Wotan", "wotan", "r_wotan", {
        f"wotan_{slug}": (f"{name} Wotan", power, "racenomi")
        for slug, name, power in (("sawshark", "Saw-shark", "sawshark_body"), ("ray", "Ray", "ray_body"),
                                  ("garfish", "Garfish", "garfish_body"), ("octopus", "Octopus", "octopus_body"),
                                  ("whale_shark", "Whale Shark", "whale_shark_body"),
                                  ("pufferfish", "Pufferfish", "pufferfish_body"), ("hammerhead", "Hammerhead", "hammerhead_body"))
    }),
    "sky_people": ("Sky People", "sky", "r_sky_people", {
        "skypiean": ("Skypiean", "skypiean_body", "racenomi"),
        "birkan": ("Birkan", "birkan_body", "racenomi"),
        "wingless_birkan": ("Wingless Birkan", "wingless_birkan_body", "racenomi"),
        "shandia": ("Shandia", "shandia_body", "racenomi"),
    }),
    "human": ("Human", "human", "r_human", {
        "human_ordinary": ("Ordinary Human", "human_will", "racenomi"),
        "human_hidden_modified": ("Hidden Modified Human", "", "racenomi"),
        "modified_human": ("Modified Human", "modified_body", "racenomi"),
    }),
    "cyborg": ("Cyborg", "cyborg", "r_cyborg", {}),
    "oni": ("Oni", "oni", "r_oni", {}),
    "tontatta": ("Tontatta", "tontatta", "r_tontatta", {}),
    "lunarian": ("Lunarian", "lunarian", "r_lunarian", {}),
    "buccaneer": ("Buccaneer", "buccaneer", "r_buccaneer", {
        f"{slug}_buccaneer": (f"{slug.title()} Buccaneer", "buccaneer_blood", "racenomi")
        for slug in ("broad", "stout", "great")
    }),
    "merfolk": ("Merfolk", "merfolk", "r_merfolk", {
        "mermaid": ("Mermaid", "swift_tail", "racenomi"),
        "great_merfolk": ("Great Merfolk", "great_merfolk_body", "racenomi"),
    }),
}
RACE_NOTES = {
    "fishman": "Fish-Men breathe underwater and train Fishman Karate. Their standard body size starts at 1.25×. The Whale Shark variant uses a 1.50× body.",
    "fishman_whale_shark": "The largest Fish-Man variant starts at 1.50× body size. The extra size helps with reach and damage but takes more room aboard ship.",
    "elbaf_giant": "A Giant with a standard size of 4× and Pride of Elbaf. You have more room to manoeuvre in buildings than an Ancient Giant.",
    "ancient_giant": "A Giant with a standard size of 6×, Ancient Blood and Continent Puller. Your larger body makes tight spaces harder to navigate.",
    "mink": "Train Electro for charged strikes and Sulong for full-moon fights. Each variant adds a body trait and its own Electro techniques.",
    "mink_dog": "Fight alongside crewmates to gain the most from Pack damage. Inu Odoshi is a charging kick.",
    "mink_lion": "Choose Lion for the strongest flat damage bonus among Minks and a lightning cone that handles groups.",
    "mink_bunny": "Choose Bunny for speed, jumps and safe falls of up to 12 blocks. Its moves close distance along the ground or from above.",
    "mink_cat": "Choose Cat for night vision and faster attacks. Aka Byobu picks out the first target you hit in a rush.",
    "mink_jaguar": "Choose Jaguar for higher damage and an occasional bleed with bare fists. Juken Karajishi hits harder with a sword.",
    "mink_polar_bear": "Choose Polar Bear for cold protection, faster swimming, toughness and a grab. Its 1.50× body needs more room to move.",
    "mink_bull": "Choose Bull for a strong running hit and knockback. Its 1.25× body is larger than most Minks.",
    "skypiean": "Choose Skypiean for running speed and the largest Dial damage bonus. Breath Gale and Dial Blend extend your Dial moveset.",
    "wotan": "Wotans combine Giant techniques and Fishman Karate. Their fish subtype supplies an additional passive.",
    "cyborg": "Fit body parts and accessories and use Cola to power your moves. The quest chapter tracks head, arm, chest, leg and shoulder upgrades, and the techniques available depend on what you have fitted.",
    "human_hidden_modified": "Play twenty hours as a Hidden Modified Human and reach 5,000 Doriki to wake the modification.",
    "modified_human": "Equip a Raid Suit with the Germa 66 Ration Box. Sneak and use it to pick the suit colour. Suit-specific moves require the corresponding suit.",
    "lunarian": "Light your flame to take 50% less eligible damage, or extinguish it for faster movement and attacks. Flame Switch controls the stance. Your flame starts out after login or respawn and goes out in water. Fire and lava do no damage in either stance. A Lunarian starts at 1.5× body size and can crouch to fit through a normal doorway.",
    "buccaneer": "Broad, Stout and Great are cosmetic choices with the same body size, passive and moves. Sneak to hunch through ordinary doorways.",
    "mermaid": "Choose Swift Tail for faster swimming. At 1× body size, you trade Great Merfolk’s extra toughness for speed.",
    "great_merfolk": "Choose Great Body for more toughness and a 1.25× body. Mermaid’s Swift Tail is the faster option in water.",
    "merfolk": "Merfolk swim quickly and have legs on land. They can learn Fishman Karate alongside their own aquatic techniques.",
    "tontatta": "Tontatta have a very small body, with reach, movement and maximum health affected by their racial shape.",
    "wingless_birkan": "Stronger grounded Mantra with no altitude bonus. You can buy Sky Leap to meet later unlock requirements, but need wings to use it.",
    "birkan": "Mantra is stronger up high. Wings let you use Sky Leap.",
    "shandia": "Choose Shandia for a winged melee fighter with tougher armour and the War Cry and Berserker branch.",
    "kuja": "An archer who can train snake-arrow techniques. Armament and Observation awaken on entering the Grand Line.",
    "three_eye": "Observation awakens when you enter the Grand Line. Train techniques to reveal and anticipate enemies. The third eye can reveal the Voice of All Things.",
    "long_arm": "Use bare hands to strike or grab enemies from farther away.",
    "long_leg": "Use long-reaching kicks and leaps to control where you fight.",
}
RACIAL_FACTORS = {
    "human": "akumalib:human_lineage",
    "modified_human": "inomissing:lineage_steel_skin inomissing:lineage_regeneration inomissing:lineage_superhuman_strength",
    "mink": "akumalib:mink_lineage",
    "fishman": "inomissing:lineage_fishman_strength",
    "giant": "inomissing:lineage_giant_lineage",
    "elbaf_giant": "racenomi:elbaf_lineage",
    "ancient_giant": "racenomi:ancient_lineage",
    "lunarian": "inomissing:lineage_lunarian",
    "tontatta": "racenomi:tontatta_lineage inomissing:lineage_dwarf_lineage",
    "wingless_birkan": "racenomi:birkan_lineage",
}
VARIANT_TECHNIQUES = {
    "ancient_giant": ("continent_puller",),
    "mink_dog": ("inu_odoshi",),
    "mink_lion": ("electro_roar",),
    "mink_bunny": ("moon_rabbit", "comet_rabbit"),
    "mink_cat": ("aka_byobu",),
    "mink_jaguar": ("juken_karajishi",),
    "mink_polar_bear": ("bear_hug",),
    "mink_bull": ("mo_golova",),
    "skypiean": ("breath_gale", "dial_blend"),
    "birkan": ("mantra_mark", "divine_stride"),
    "wingless_birkan": ("mantra_mark",),
    "shandia": ("war_cry", "berserker"),
}
MINK_TECHNIQUE_STATS = {
    "eleclaw": (10, 8, 1),
    "mink_assault": (8, 9, 1),
    "electrical_luna": (14, 10, 2),
    "electrical_tempesta": (8, 8, 1),
    "electrical_shower": (4, 12, 2),
    "inu_odoshi": (16, 13, 2),
    "electro_roar": (8, 11, 1),
    "moon_rabbit": (10, 12, 1),
    "comet_rabbit": (14, 14, 2),
    "aka_byobu": (14, 13, 2),
    "juken_karajishi": (14, 10, 2),
    "bear_hug": (3, 15, 1),
    "mo_golova": (12, 8, 1),
}
RACE_BASE = {"fishman": "fishmankarate", "merfolk": "fishmankarate", "human": "rokushiki"}
STYLE_SPECS = {
    "swordsman": ("Swordsman", "mineminenomi", ("ittoryu", "nitoryu", "santoryu"), "st_swordsman"),
    "brawler": ("Brawler", "mineminenomi", ("brawler",), "st_brawler"),
    "sniper": ("Sniper", "mineminenomi", ("sniper",), "st_sniper"),
    "doctor": ("Doctor", "mineminenomi", ("doctor",), "st_doctor"),
    "art_of_weather": ("Art of Weather", "mineminenomi", ("artofweather",), "st_art_of_weather"),
    "black_leg": ("Black Leg", "mineminenomi", ("blackleg",), "st_black_leg"),
    "okama_kenpo": ("Okama Kenpo", "blitzutility", ("okama",), "st_okama_kenpo"),
    "nitoryu": ("Nitoryu", "blitzutility", ("nitoryu",), "st_nitoryu"),
    "axe": ("Axe Style", "blitzutility", ("axe", "axestyle"), "st_weapon_arts"),
    "bisento": ("Bisento Style", "blitzutility", ("bisento",), "st_weapon_arts"),
    "bludgeon": ("Bludgeon Style", "cartaddon", ("bludgeon",), "st_weapon_arts"),
    "twin_barrel": ("Twin Barrel Style", "cartaddon", ("twinbarrel",), "st_weapon_arts"),
}


def stats_from_projectile(move, code, codes):
    """Keep fixed projectile damage only when the move names a single fixed-damage projectile."""
    candidates = set()
    for cls in re.findall(r"// class ([\w/$]+)", code):
        projectile = codes.get(cls, "")
        if not projectile or "/projectiles/" not in cls:
            continue
        ops = INSTRUCTION.findall(projectile)
        values = {n for i, op in enumerate(ops[1:], 1)
                  if ".setDamage:(F)" in op and (n := stat_number(ops[i - 1])) and n > 0}
        if len(values) == 1:
            candidates.add((cls, values.pop()))
    if len(candidates) == 1:
        move.stats.append(("PROJECTILE_HIT_DAMAGE", candidates.pop()[1]))


def normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def collect_moves(sources, all_code, locked):
    by_class, by_id = {}, {}
    for mod, codes in all_code.items():
        _, _, locale, _, textures = sources[mod]
        icons = {Path(p).stem: p for p in textures if "/abilities/" in p}
        names = {normalize(key.split(".")[-1]): (key.split(".")[-1], label)
                 for key, label in locale.items() if key.startswith(f"ability.{mod}.") and key.count(".") == 2}
        for cls, code in codes.items():
            move = move_from_class(mod, code, locale)
            if move is None and mod in {"hakirework", "racenomi"}:
                simple = cls.split("/")[-1].split("$")[-1].removesuffix("Ability")
                if (known := names.get(normalize(simple))) and "extends " in code.splitlines()[0]:
                    move = move_from_class(mod, code, locale, known=known)
            if move is None or move.id in locked or move.id in REPLACED_MOVES:
                continue
            stats_from_projectile(move, code, codes)
            if mod == "racenomi" and move.id not in VERIFIED_STATS:
                rows = racial_tooltip_stats(INSTRUCTION.findall(code))
                if rows:
                    move.extra_stats.extend(rows)
                    if move.kind == "Passive" and any("damage" in name.lower() for name, _ in rows):
                        move.stats = [(key, val) for key, val in move.stats if key not in {"DAMAGE", "FIXED_HIT_DAMAGE"}]
            if mod == "awakenawakennomi":
                move.extra_stats.extend(AWAKENING_STATS.get(move.id.split(":")[1], ()))
            if mod == "racenomi" and (mink_stats := MINK_TECHNIQUE_STATS.get(move.id.split(":")[1])):
                damage, cooldown, charges = mink_stats
                slug = move.id.split(":")[1]
                unit = " per bolt" if slug == "electrical_shower" else " per catch or squeeze" if slug == "bear_hug" else ""
                move.kind = "Active"
                move.stats = [("DAMAGE", damage), ("COOLDOWN", cooldown)]
                move.extra_stats += [
                    ("Electro charges", str(charges)),
                    ("Sulong damage" + unit, f"{damage * 1.5:g} HP"),
                    ("Sulong cooldown", f"{cooldown if slug == 'bear_hug' else cooldown / 2:g} s"),
                    ("Sulong Electro charges", "0"),
                ]
                if unit:
                    move.stats.remove(("DAMAGE", damage))
                    move.extra_stats.insert(0, ("Damage" + unit, f"{damage:g} HP"))
                if slug == "juken_karajishi":
                    move.extra_stats += [("Damage with a sword", "17.5 HP"), ("Sulong damage with a sword", "26.25 HP")]
            move.icon = icons.get(move.id.split(":")[1])
            if not move.icon:
                alternatives = [p for p in textures if "/abilities/" in p and Path(p).stem == normalize(
                    move.id.split(":")[1])]
                if len(alternatives) == 1:
                    move.icon = alternatives[0]
            by_class[cls] = move
            by_id[move.id] = move
        if mod == "hakirework":
            for move_id, title in names.values():
                key = f"ability.{mod}.{move_id}"
                identity = f"{mod}:{move_id}"
                if identity not in locked:
                    by_id.setdefault(identity, Move(identity, title, describe(key, locale), icon=icons.get(move_id)))
    add_enum_moves(sources["inofruits"], all_code["inofruits"], by_class, by_id)
    add_dawn_modes(by_id)
    return by_class, by_id


def add_dawn_modes(moves):
    for original, (slug, title, description, stats) in DAWN_MODES.items():
        damage_key = f"mineminenomi:gomu_gomu_no_{original}"
        base = moves[damage_key]
        base.stats = [(key, value) for key, value in base.stats if not key.startswith("FIFTH_GEAR_")]
        move_id = f"awakenawakennomi:gomu_gomu_no_dawn_{slug}"
        icon = f"assets/awakenawakennomi/textures/abilities/gomu/gomu_gomu_no_dawn_{slug}.png"
        moves[move_id] = Move(move_id, title, description, "DEVIL_FRUITS", icon, stats,
                              damage_key if original != "rocket" else None, kind="Active")
    whip = moves.get("awakenawakennomi:gomu_gomu_no_dawn_whip")
    if whip:
        whip.stats = [(key, value) for key, value in whip.stats if key != "PROJECTILE_HIT_DAMAGE"]
        whip.stats.append(("PROJECTILE_HIT_DAMAGE", 60))


def add_enum_moves(source, codes, by_class, by_id):
    _, _, locale, _, textures = source
    descriptions = codes["com/inovactio/inofruits/abilities/okioki/OkiLaws"]
    rule_desc = {key.lower(): line.replace("\\'", "'") for key, line in re.findall(
        r"LawRule\.([A-Z_]+):[^\n]+\n[^\n]+// String ([^\n]+)", descriptions)}
    for root, prefix in (("okioki/LawRule", "law_"), ("kutsukutsu/Sole", "")):
        class_name = f"com/inovactio/inofruits/abilities/{root}"
        ops = INSTRUCTION.findall(codes[class_name].split("  static {};", 1)[1])
        for i, op in enumerate(ops):
            if 'Method "<init>":(Ljava/lang/String;ILjava/lang/String;Ljava/lang/String;' not in op:
                continue
            labels = [s for v in ops[max(0, i - 14):i] if (s := string(v))]
            if len(labels) < 3:
                continue
            slug, title = labels[-2:] if prefix else labels[-3:-1]
            slug = prefix + slug
            identity = f"inofruits:{slug}"
            notes = describe(f"ability.inofruits.{slug}", locale)
            stats = []
            if prefix:
                notes = rule_desc.get(slug.removeprefix(prefix), notes)
                stats = [("DURATION_TICKS", stat_number(ops[i - 2])), ("COOLDOWN", stat_number(ops[i - 1]))]
            else:
                notes = labels[-1]
                stats = [("COOLDOWN", 40)]
            icon = next((path for path in textures if "/abilities/" in path and Path(path).stem == slug), None)
            move = Move(identity, title, notes, "DEVIL_FRUITS", icon,
                        [(key, value) for key, value in stats if value is not None], kind="Active")
            by_class[f"{class_name}/{slug}"] = by_id[identity] = move


def fruit_keys(registry, locale, mod):
    by_title = {}
    for item, value in locale.items():
        if item.startswith(f"item.{mod}.") and len(item.split(".")) == 3:
            by_title.setdefault(normalize(value), item.split(".")[2])
    for (owner, field_id), (title, tier, kind, refs) in registry.items():
        if owner == mod:
            yield field_id, by_title.get(normalize(title), field_id.lower()), (title, tier, kind, refs)


def from_packages(classes, mod, packages):
    return [move.id for cls, move in classes.items() if move.id.startswith(f"{mod}:")
            and any(f"/{package}/" in cls for package in packages)]


def unique(ids):
    return list(dict.fromkeys(ids))


def fruit_entries(registry, awakenings, sources, classes, by_id, pools, removed):
    entries = []
    box_contents = {fruit for pool in pools.values() for fruit in pool}
    for mod in REGISTRIES.keys() - {"awakenawakennomi"}:
        locale = sources[mod][2]
        for field_id, slug, (title, tier, kind, refs) in fruit_keys(registry, locale, mod):
            fruit_id = f"{mod}:{slug}"
            if fruit_id in removed or (mod == "cartaddon" and fruit_id not in box_contents):
                continue
            moves = [classes[cls].id for cls in refs if cls in classes]
            if mod == "inofruits" and slug in {"oki_oki_no_mi", "kutsu_kutsu_no_mi"}:
                moves.extend(from_packages(classes, mod, ("okioki" if slug.startswith("oki") else "kutsukutsu",)))
            description = describe(f"item.{mod}.{slug}", locale)
            if not description and slug == "hito_hito_no_mi":
                description = "This Human fruit has no active move in its base registration. Its awakening adds Brain Point."
            entry = Entry(fruit_id, title, mod, "fruits", unique(moves), kind, tier, description)
            entries.append(entry)
            if mod == "mineminenomi" and field_id in awakenings:
                moves = [classes[cls].id for cls in awakenings[field_id] if cls in classes]
                if slug == "gomu_gomu_no_mi":
                    moves.extend(f"awakenawakennomi:gomu_gomu_no_dawn_{mode[0]}" for mode in DAWN_MODES.values())
                entries.append(Entry(f"awakenawakennomi:{slug}", f"{title} Awakening", "awakenawakennomi",
                                     "awakenings", unique(moves), kind, tier, parent=entry.path))
    return entries


def race_entries(sources, classes, by_id):
    entries = []
    race_lang = sources["racenomi"][2]
    for slug, (title, family, quest, variants) in RACE_FAMILIES.items():
        variant_moves = {f"racenomi:{move}" for _, move, _ in variants.values()}
        variant_moves.update(f"racenomi:{move}" for variant in variants for move in VARIANT_TECHNIQUES.get(variant, ()))
        if slug == "wotan":
            variant_moves.add("racenomi:continent_puller")
        moves = from_packages(classes, "racenomi", (family,))
        if slug in RACE_BASE:
            moves.extend(k for k in from_packages(classes, "mineminenomi", (RACE_BASE[slug],))
                         if not k.endswith(("fishman_passive_bonuses", "fishman_damage", "fishman_swim_speed")))
        if slug == "wotan":
            moves.extend(from_packages(classes, "mineminenomi", ("fishmankarate",)))
            moves.extend(from_packages(classes, "racenomi", ("giant", "fishman")))
            variant_moves.update(f"racenomi:{m}" for _, m, _ in RACE_FAMILIES["giant"][3].values())
        if slug == "fishman":
            moves.extend(f"racenomi:{move}" for move in ("fishman_body", "fishman_passive") if f"racenomi:{move}" in by_id)
        if slug == "human":
            moves.extend(from_packages(classes, "racenomi", ("human",)))
        family_entry = Entry(f"racenomi:{slug}", title, "racenomi", "races",
                             unique(k for k in moves if k not in variant_moves and k in by_id),
                             description=RACE_NOTES.get(slug) or describe(f"race.racenomi.{slug}", race_lang),
                             quest=quest)
        entries.append(family_entry)
        for variant, (name, ability, namespace) in variants.items():
            key = f"{namespace}:{variant}"
            moves = [f"racenomi:{ability}"] if f"racenomi:{ability}" in by_id else []
            if variant == "modified_human":
                moves += from_packages(classes, "racenomi", ("modified",))
            moves.extend(f"racenomi:{move}" for move in VARIANT_TECHNIQUES.get(variant, ()))
            description = RACE_NOTES.get(variant) or describe(f"race.racenomi.{variant}", race_lang)
            entries.append(Entry(key, name, "racenomi", "races", unique(m for m in moves if m in by_id),
                                 description=description, parent=family_entry.path, quest=quest))
    for slug, title in (("long_arm", "Long-Arm"), ("long_leg", "Long-Leg"), ("three_eye", "Three-Eye"), ("kuja", "Kuja")):
        entries.append(Entry(f"hakirework:{slug}", title, "hakirework", "races", [],
                             description=RACE_NOTES[slug], quest="r_tribes"))
    return entries


def quest_move_groups():
    runtime = (PACK / "kubejs/server_scripts/eternal_voyage_quests.js").read_text(encoding="utf-8")
    tasks = json.loads(re.search(r"(?m)^  EV\.TASKS = (.+)$", runtime)[1])
    groups = {}
    for page in (PACK / "config/ftbquests/quests/chapters").glob("*.snbt"):
        chapter = page.stem
        if not chapter.startswith(("st_", "r_")):
            continue
        group = groups.setdefault(chapter, defaultdict(list))
        active = ""
        for task in re.findall(r'(?m)^\t{5}id: "(\w+)"', page.read_text(encoding="utf-8")):
            step = tasks.get(task, {})
            kind, val = step.get("c"), step.get("v")
            if kind == "school":
                active = f"school/{val}"
            elif kind == "style" and isinstance(val, list) and len(val) == 1:
                active = f"style/{val[0]}"
            elif kind == "race" and isinstance(val, list) and len(val) == 1 and chapter == "r_tribes":
                active = f"race/{val[0]}"
            elif kind == "ability":
                group[active].extend(v if ":" in v else f"mineminenomi:{v}" for v in val)
    return groups


SCHOOLS = {
    "oden_nitoryu": "Oden Two-Sword Style", "kitsunebi": "Fox Fire Style", "hanauta": "Humming Fencing",
    "hawk_eye": "Hawk-Eye Style", "shimotsuki": "Shimotsuki Style", "asura": "Kyutoryu Asura",
    "red_hair": "Red-Hair Style", "ryusoken": "Ryusoken", "hasshoken": "Hasshoken", "sumo": "Sumo",
    "fishman_jujutsu": "Fishman Jujutsu", "dial_arts": "Dial Arts",
}
def discipline_entries(classes, by_id, quests):
    entries = []
    for slug, (title, mod, packages, chapter) in STYLE_SPECS.items():
        moves = from_packages(classes, mod, packages)
        if chapter != "st_weapon_arts":
            for group, tracked in quests.get(chapter, {}).items():
                if not group.startswith("school/"):
                    moves.extend(tracked)
        entries.append(Entry(f"{mod}:{slug}", title, mod, "styles",
                             unique(m for m in moves if m in by_id), quest=chapter))
    for chapter, groups in quests.items():
        for key, moves in groups.items():
            if not key.startswith("school/"):
                continue
            slug = key.split("/")[-1]
            if slug in SCHOOLS:
                entries.append(Entry(f"hakirework:{slug}", SCHOOLS[slug], "hakirework", "schools",
                                     unique(m for m in moves if m in by_id), quest=chapter))
    return entries


def clean(text):
    return LANG_FORMAT.sub("", text).replace("\\n", " ").replace("OMPWorld", "One Piece World")


def relative(page, target):
    return posixpath.relpath(target, posixpath.dirname(page))


def link(page, target, title):
    return f"[{title}]({relative(page, target)})"


def display_stat(key, value):
    name = key.removesuffix("_TICKS").replace("_", " ").capitalize()
    if key.startswith("COOLDOWN_VARIANT_"):
        name = "Conditional cooldown"
    elif key == "DAMAGE":
        name = "Base damage"
    elif key == "PROJECTILE_HIT_DAMAGE":
        name = "Projectile hit"
    if key == "BLEED_CHANCE_PERCENT":
        return "Bleed chance on an eligible hit", f"{value:g}%"
    if key.endswith("_TICKS") or "COOLDOWN" in key:
        return name, f"{value / 20:g} s ({value:g} ticks)"
    if key.endswith("DAMAGE"):
        return name, f"{value:g} HP"
    return name, f"{value:g}"


def stat_table(rows):
    return ['<div class="entry-stats" markdown="1">', "", "| Stat | Value |", "| --- | --- |",
            *(f"| {name} | {value} |" for name, value in rows), "", "</div>", ""]


def entry_icon(entry, sources, moves, installed):
    slug = entry.id.split(":")[1]
    if entry.section == "awakenings":
        for move_id in entry.moves:
            move = moves[move_id]
            if move.icon:
                return installed(move.id.split(":")[0], move.icon)
    if entry.section in ("fruits", "awakenings"):
        source = entry.owner if entry.section == "fruits" else "mineminenomi"
        candidates = [p for p in sources[source][4] if Path(p).stem == slug and "/textures/item" in p]
    elif entry.section == "races":
        source = entry.owner
        aliases = {slug, slug.replace("fishman_", ""), slug.replace("wotan_", "fishman_")}
        candidates = [p for p in sources[source][4] if "/gui/icons/" in p and Path(p).stem in aliases]
    else:
        candidates = []
    if candidates:
        return installed(source, candidates[0])
    for move_id in entry.moves:
        move = moves[move_id]
        if move.icon:
            return installed(move.id.split(":")[0], move.icon)
    return f"assets/mods/{entry.owner}.png"


def render_move(page, lines, move, tuning, installed, fruit_peak=None, heading="##", anchor_prefix=""):
    icon = installed(move.icon.split("/")[1], move.icon) if move.icon else None
    anchor = f" {{ #{anchor_prefix}-{move.id.split(':')[1].replace('_', '-')} }}" if anchor_prefix else ""
    lines.extend(["", f"<!-- move {move.id} -->", "", f"{heading} {clean(move.title)}{anchor}", ""])
    marker = f'![]({relative(page, icon)}){{ .entry-move-icon loading=lazy }}' if icon else ""
    tags = f"*{move.kind}*" if move.kind else ""
    if marker or tags:
        lines.extend([" ".join(filter(None, (marker, tags))), ""])
    if move.description:
        lines.extend([clean(move.description), ""])
    stats = [display_stat(k, v) for k, v in move.stats]
    if move.id == "inofruits:blood_spear":
        lines.extend(["The health-based part of the direct hit accounts for size before pack and Doriki modifiers. "
                      "The short recovery applies when there is too little blood to cast.", ""])
        stats = [("Failed cast recovery" if value == "0.5 s (10 ticks)" else name, value) for name, value in stats]
    stats.extend(VERIFIED_STATS.get(move.id, ()))
    stats.extend(move.extra_stats)
    factor = tuning.get(move.damage_key or move.id, 1)
    if factor != 1:
        stats.append(("Pack multiplier when dealing damage", f"{factor:g}×"))
    if fruit_peak is not None and move.category == "DEVIL_FRUITS":
        fixed = next((value for key, value in move.stats if key == "PROJECTILE_HIT_DAMAGE"), None)
        if fixed is not None:
            stats.append(("Projectile hit at 50,000 Doriki with pack multiplier", f"{fixed * factor * fruit_peak:g} HP"))
    if move.id == "mineminenomi:gomu_gomu_no_pistol":
        stats.extend([("Hit at 50,000 Doriki, no gear", "19.8 HP"), ("Hit at 50,000 Doriki, Gear Second", "33 HP")])
    if stats:
        lines.extend(stat_table(stats))
    if move.form_stats:
        lines.extend(["**Stats while transformed**", "", *stat_table(move.form_stats)])


def render_entry(entry, entries, moves, tuning, pools, icons, installed, sources, awakened_damage, write):
    page = entry.path
    owner_page = f"reference/content/{entry.owner}.md"
    section_index = f"reference/content/{entry.owner}/{entry.section}/index.md"
    if entry.section in {"fruits", "races", "styles"}:
        section_index = f"characters/{entry.section}/index.md"
    lines = [
        f"# {clean(entry.title)}", "",
        f'![]({relative(page, icons[page])}){{ .entry-page-icon }}', "",
        f'{link(page, section_index, "All fighting styles" if entry.section == "styles" else entry.section.title())} · {link(page, owner_page, MOD_CARDS[entry.owner][0])}',
        "",
    ]
    if entry.description:
        lines.extend([clean(entry.description), ""])
    if entry.section == "fruits":
        lines.append(f"<!-- fruit {entry.id} -->")
        if entry.id == "mineminenomi:yami_yami_no_mi":
            lines.extend(["", "Black Hole can hold up to **30,000 absorbed blocks** for Liberation.", ""])
    curve = None
    if entry.section in ("fruits", "awakenings"):
        curve = [2.25, 2, 1.75, 1.75][min(max(entry.tier, 1), 4) - 1]
        overview = [("Type", entry.kind.replace("_", " ").title()), ("Tier", entry.tier),
                    ("Fruit damage scaling", f"1.00× at 10,000 Doriki → {curve:g}× at 50,000 Doriki")]
        if entry.moves:
            kinds = [moves[move].kind for move in entry.moves]
            gomu_awakening = entry.id == "awakenawakennomi:gomu_gomu_no_mi"
            if gomu_awakening:
                kinds = kinds[:-len(DAWN_MODES)]
            count = str(len(kinds))
            if all(kinds):
                passive = kinds.count("Passive")
                count += f" ({len(kinds) - passive} active, {passive} passive)"
            overview.append(("Abilities", count))
            if gomu_awakening:
                overview.append(("Gear Fifth variants", ", ".join(f"[{title}](#{title.lower().replace(' ', '-')})"
                                                                for _, title, _, _ in DAWN_MODES.values())))
        if entry.section == "fruits":
            boxes = [tier.replace("_", " ").title() for tier, values in pools.items() if entry.id in values]
            if boxes:
                overview.append(("Fruit boxes", link(page, "characters/fruit-boxes.md", ", ".join(boxes))))
        else:
            overview.extend([("Awakening Doriki requirement", "40,000"),
                             ("Active online time with this fruit", "About 24 hours (1,728,000 ticks)")])
        lines.extend(stat_table(overview))
        lines.extend([f"See {link(page, 'characters/combat-stats.md#damage-from-doriki', 'damage calculations')}.", ""])
        if entry.id == "awakenawakennomi:gomu_gomu_no_mi":
            lines.extend(["In Gear Fifth, Pistol, Gatling, Bazooka and Rocket take the Dawn forms described below. "
                          "Each damaging form uses the pack multiplier for its original move.", ""])
    if entry.parent:
        parent = entries[entry.parent]
        lines.extend([f"See {link(page, parent.path, parent.title)} for the shared moves and progression.", ""])
    children = [other for other in entries.values() if other.parent == page]
    for child in children:
        if child.section == "awakenings":
            lines.extend(["[Jump to awakening](#awakening)", ""])
    if entry.section == "fruits" and any(child.section == "awakenings" for child in children):
        lines.extend([f"After awakening, this fruit’s original damaging moves deal **{awakened_damage:g}× damage**. "
                      "The awakening techniques below have their own values.", ""])
        if "zoan" in entry.kind.lower():
            guide = link(page, "characters/devil-fruits.md#what-changes-after-awakening", "awakened Zoan form stats")
            lines.extend([f"Keep using your normal combat forms after awakening. See the {guide} for the upgrade.", ""])
    variants = [child for child in children if child.section == "races"]
    if variants:
        lines.extend(["**Variants**", "", *[f"- [{child.title}](#{variant_anchor(child)})" for child in variants], ""])
    if entry.section == "races":
        lines.extend(stat_table([("Racial damage scaling", "1.00× at 10,000 Doriki → 1.40× at 50,000 Doriki")]))
    elif entry.section == "styles":
        lines.extend(stat_table([("Style damage at 10,000 Doriki", "1.00×"),
                                 ("At 50,000 Doriki with a fruit", "1.50×"),
                                 ("At 50,000 Doriki while fruitless", "2.50×"),
                                 ("At 50,000 Doriki with an eligible all-fruitless crew", "2.75×")]))
    elif entry.section == "schools":
        lines.extend(["The school master and lesson requirements govern when these techniques unlock. "
                      "Haki or fighting-style damage scaling applies when the attack uses that category.", ""])
    if entry.section in ("races", "styles", "schools"):
        lines.extend([f"{link(page, 'characters/combat-stats.md', 'See combat stats')}.", ""])
    if entry.moves:
        lines.extend(['!!! note "Reading the stats"',
                      "    Listed base damage is for the named part of the move. Pack and Doriki multipliers "
                      "are shown separately. Times assume 20 ticks per second.", ""])
    for move_id in entry.moves:
        render_move(page, lines, moves[move_id], tuning, installed, curve)
    if variants:
        lines.extend(["", "## Variants", ""])
        for child in variants:
            anchor = variant_anchor(child)
            lines.extend([f"### {child.title} {{ #{anchor} }}", "",
                          f"![]({relative(page, icons[child.path])}){{ .entry-move-icon }}", ""])
            if child.description:
                lines.extend([clean(child.description), ""])
            for move_id in child.moves:
                render_move(page, lines, moves[move_id], tuning, installed, heading="####", anchor_prefix=anchor)
    if entry.section == "races":
        render_racial_factors(page, lines, [entry, *variants], sources, installed)
    for child in children:
        if child.section != "awakenings":
            continue
        lines.extend(["", "## Awakening", "", f"**Source** · {MOD_CARDS[child.owner][0]}", "",
                      *stat_table([("Doriki", "40,000"), ("Active time with the fruit", "About 24 hours (1,728,000 ticks)")])])
        if child.id == "awakenawakennomi:gomu_gomu_no_mi":
            lines.extend(["Gear Fifth gives Pistol, Gatling, Bazooka and Rocket the Dawn forms below.", ""])
        for move_id in child.moves:
            render_move(page, lines, moves[move_id], tuning, installed, curve, heading="###", anchor_prefix="awakening")
    if entry.quest:
        chapter = f"reference/quests/{entry.quest}.md"
        lines.extend(["", "## Quests", "", f"See {link(page, chapter, 'the quest chapter')} for milestones and rewards.", ""])
    write(page, lines)


def variant_anchor(entry):
    return entry.id.split(":")[1].replace("_", "-")


def render_racial_factors(page, lines, entries, sources, installed):
    factors = []
    for entry in entries:
        slug = entry.id.split(":")[1]
        subtype = slug.removeprefix("fishman_").removeprefix("wotan_")
        if subtype.startswith("mink_"):
            subtype = subtype.removeprefix("mink_") + "_mink"
        for identity in RACIAL_FACTORS.get(slug, f"racenomi:{subtype}_lineage").split():
            owner, name = identity.split(":")
            locale, textures = sources[owner][2], sources[owner][4]
            key = f"ability.{owner}.{name}"
            if key in locale and not any(row[0] == identity for row in factors):
                icon = next((p for p in textures if p.endswith(f"/abilities/{name}.png")), None)
                marker = f"![]({relative(page, installed(owner, icon))}){{ .entry-move-icon }} " if icon else ""
                effect = locale.get(key + ".description.0", "")
                factors.append((identity, marker + locale[key], clean(effect).replace("|", "&#124;"), MOD_CARDS[owner][0]))
    lines.extend(["", "## Lineage Factors", ""])
    if factors:
        lines.extend(["| Graft | Effect | Source |", "| --- | --- | --- |",
                      *(f"| {title} | {effect} | {owner} |" for _, title, effect, owner in factors), ""])
    else:
        lines.extend(["See the [graft guide](../bloodlines/index.md#grafted-lineage-factors) for factors you can add to this character.", ""])
    if factors:
        lines.extend(["See [grafting and capacity](../bloodlines/index.md#grafted-lineage-factors) before choosing a factor.", ""])


def weather_moves(entries, moves, config, locked):
    if not config.get("weather2"):
        return
    linked = {
        "mineminenomi:rain_tempo": "Calls rain in the area around the weather cloud.",
        "mineminenomi:thunderstorm_tempo": "Creates a local thunderstorm at the weather cloud for 60 seconds.",
        "mineminenomi:raigo": "Requires a thunderstorm at your location. A successful cast reinforces local thunder for 60 seconds.",
        "inomissing:seiryu_storm": "Calls a local thunderstorm for 60 seconds.",
        "mineminenomi:fubuki": "Creates a local snowstorm for 20 seconds.",
        "mineminenomi:grande_sables": "Creates a local sandstorm for 15 seconds.",
        "inomissing:kogosei": "The sunlight check accounts for local precipitation.",
        "blitzutility:lightning_reign": "Uses local thunder for both the cast and the ongoing storm check.",
        "awakenawakennomi:storm_sovereign": "The local thunder check affects the form’s tier and its response to damage.",
        "racenomi:sulong": "A Mink under the Chemist’s Rumble effect can enter Sulong without a full moon.",
    }
    for identity, note in linked.items():
        if identity in moves:
            comes_from_fruit = identity in {"mineminenomi:raigo", "inomissing:seiryu_storm",
                                            "mineminenomi:fubuki", "mineminenomi:grande_sables"}
            if not comes_from_fruit or config.get("fruitWeather"):
                moves[identity].description += "\n\n" + note
    if config.get("weatherTempos"):
        _, _, locale, _, _ = load_mod(next((PACK / "mods").glob("eternalvoyage-companion-*.jar")))
        style = next(entry for entry in entries if entry.id == "mineminenomi:art_of_weather")
        icon = "assets/mineminenomi/textures/abilities/tempo.png"
        tempos = (
            ("tornado", "Cool → Heat → Cool", "Cyclone Tempo", 3500, 10,
             [("Duration", f"{config['tornadoTempoSeconds']} s"),
              ("Base damage per eligible hit", f"{config['tornadoTempoDamage']:g} HP"),
              ("Firenado bonus per eligible hit", f"+{config['firenadoDamage']:g} HP"),
              ("Sandstorm damage", f"{config['sandstormTornadoDamage']:g} HP"),
              ("Blizzard damage", f"{config['frostTornadoDamage']:g} HP"),
              ("Lightning strike damage", f"{config['thunderTornadoBoltDamage']:g} HP")]),
            ("blizzard", "Cool → Cool → Thunder", "Cyclone Tempo", 4500, 10,
             [("Duration", f"{config['blizzardTempoSeconds']} s"), ("Base damage per eligible hit", f"{config['blizzardTempoDamage']:g} HP")]),
            ("supercell", "Heat → Cool → Thunder", "Thunderstorm Tempo", 6000, 15,
             [("Duration", "48 s"), ("Thunder begins", "4 s after casting"), ("Hail begins", "28 s after casting"),
              ("Base lightning damage", f"{config['supercellBoltDamage']:g} HP"),
              ("Base hail damage", f"{config['supercellHailDamage']:g} HP")]),
        )
        for tempo, sequence, prerequisite, doriki, points, stats in tempos:
            identity = f"eternalvoyage:{tempo}_tempo"
            if identity in locked:
                continue
            key = f"ability.eternalvoyage.{tempo}_tempo"
            details = [("Weather Ball sequence", sequence), ("Required technique", prerequisite),
                       ("Doriki to learn", f"{doriki:,}"), ("Technology points", str(points)),
                       ("Cooldown from cast", f"{config[tempo + 'TempoRest']} s"), *stats]
            moves[identity] = Move(identity, locale[key], describe(key, locale), icon=icon,
                                   kind="Active", extra_stats=details)
            style.moves.append(identity)
    for identity in ("mineminenomi:thunderbolt_tempo", "mineminenomi:thunderstorm_tempo",
                     "mineminenomi:thunder_lance_tempo", "eternalvoyage:supercell_tempo"):
        if identity in moves:
            moves[identity].extra_stats.append(("Damage with local thunder over caster", f"{config['stormBonus']:g}×"))


def playable_reference(javap, pools, removed, locked, write):
    sources, codes = read_sources(javap)
    classes, moves = collect_moves(sources, codes, locked)
    registry, awakenings = registered_fruits(codes)
    quests = quest_move_groups()
    entries = fruit_entries(registry, awakenings, sources, classes, moves, pools, removed)
    race_pages = race_entries(sources, classes, moves)
    for entry in race_pages:
        if entry.owner == "hakirework":
            slug = entry.id.split(":")[1]
            entry.moves = unique(m for m in quests["r_tribes"][f"race/{slug}"] if m in moves)
    entries.extend(race_pages)
    entries.extend(discipline_entries(classes, moves, quests))
    sources["akumalib"] = load_mod(next((PACK / "mods").glob("akumalib-*.jar")))
    config = json.loads((PACK / "config/eternalvoyage-companion.json").read_text(encoding="utf-8-sig"))
    weather_moves(entries, moves, config, locked)
    by_path = {entry.path: entry for entry in entries}
    assert len(by_path) == len(entries), "Two entries share a documentation path"

    assets = {}

    def install(source, asset):
        key = source, asset
        if key not in assets:
            path = f"assets/playable/{source}/{asset.split('/textures/', 1)[-1]}"
            destination = DOCS / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            with ZipFile(sources[source][1]) as jar:
                destination.write_bytes(jar.read(asset))
            assets[key] = path
        return assets[key]

    icons = {entry.path: entry_icon(entry, sources, moves, install) for entry in entries}
    tuning = config["moveDamage"]
    server = PACK / "serverconfig"
    lib_config = tomllib.loads((server / "akumalib-server.toml").read_text(encoding="utf-8-sig"))
    awakened_damage = lib_config.get("awakenedFruits", {}).get("awakenedDamage", 1.5)
    grouped = defaultdict(list)
    canonical = [entry for entry in entries if not entry.parent]
    for entry in canonical:
        render_entry(entry, by_path, moves, tuning, pools, icons, install, sources, awakened_damage, write)
        if entry.section not in {"fruits", "races", "styles"}:
            grouped[(entry.owner, entry.section)].append(entry)

    for section, title in (("fruits", "Devil Fruit catalogue"), ("races", "Race guide"),
                           ("styles", "Fighting style catalogue")):
        page = f"characters/{section}/index.md"
        guide = {"fruits": "devil-fruits.md", "races": "races-and-styles.md", "styles": "fighting-styles.md"}[section]
        lines = [f"# {title}", "", f"[How it works](../{guide})", ""]
        groups = defaultdict(list)
        for entry in canonical:
            if entry.section == section:
                label = entry.kind.replace("_", " ").title()
                if section == "styles":
                    label = "Weapon arts" if entry.quest == "st_weapon_arts" else "Core styles"
                if label.startswith("Zoan"):
                    label = "Zoan"
                groups[label].append(entry)
        for label, group in sorted(groups.items()):
            if label:
                lines.extend([f"## {label}", ""])
            lines.extend(["| Name | Source |", "| --- | --- |"])
            for entry in sorted(group, key=lambda item: item.title.casefold()):
                icon = f"![]({relative(page, icons[entry.path])}){{ .entry-move-icon loading=lazy }}"
                lines.append(f"| {icon} {link(page, entry.path, entry.title)} | {MOD_CARDS[entry.owner][0]} |")
            lines.append("")
        write(page, lines)
    master = ["# Playable content", "", "- [Devil Fruit catalogue](../../characters/fruits/index.md)",
              "- [Race guide](../../characters/races/index.md)",
              "- [Fighting style catalogue](../../characters/styles/index.md)",
              "- [Schools and martial arts](../../characters/schools.md)"]
    for (owner, section), group in sorted(grouped.items()):
        page = f"reference/content/{owner}/{section}/index.md"
        title = f"{MOD_CARDS[owner][0]} · {section.title()}"
        master.append(f"- [{title}](../{page.removeprefix('reference/')}) · {len(group)} entries")
        lines = [f"# {title}", "", f"[{MOD_CARDS[owner][0]} overview](../../{owner}.md)", ""]
        buckets = defaultdict(list)
        for entry in group:
            kind = entry.kind.replace("_", " ").title() if entry.kind else "Entries"
            buckets[kind].append(entry)
        for label, bucket in sorted(buckets.items()):
            lines.extend(["", f"## {label}", "", '<div class="entry-grid" markdown="1">', ""])
            for entry in sorted(bucket, key=lambda item: item.title.casefold()):
                lines.extend([f"[![]({relative(page, icons[entry.path])}){{ loading=lazy }} "
                              f"**{entry.title}**]({relative(page, entry.path)})", ""])
            lines.extend(["</div>", ""])
        write(page, lines)
    write("reference/playable/index.md", master)
    generated = {entry.path for entry in canonical} | {
        f"reference/content/{owner}/{section}/index.md" for owner, section in grouped
    } | {f"characters/{section}/index.md" for section in ("fruits", "races", "styles")}
    old_files = list((DOCS / "reference/content").glob("*/*/*.md"))
    for section in ("fruits", "races", "styles"):
        old_files.extend((DOCS / f"characters/{section}").glob("*.md"))
    for old in old_files:
        if old.relative_to(DOCS).as_posix() not in generated and old.read_text(encoding="utf-8").startswith(
                "<!-- Generated by tools/build_pack_reference.py."):
            old.unlink()
    migrate_playable_links(entries)
    print(f"Indexed {len(canonical)} playable pages and extracted {len(assets)} content textures.")
    return by_path, grouped


def migrate_playable_links(entries):
    targets = {}
    for entry in entries:
        if entry.section not in {"fruits", "awakenings", "races", "styles"}:
            continue
        page = entry.parent or entry.path
        anchor = "awakening" if entry.section == "awakenings" else variant_anchor(entry) if entry.parent else ""
        targets[entry.legacy_path] = (page, anchor)
        index = f"reference/content/{entry.owner}/{entry.section}/index.md"
        section = "fruits" if entry.section == "awakenings" else entry.section
        targets[index] = (f"characters/{section}/index.md", "")
    for path in DOCS.rglob("*.md"):
        page = path.relative_to(DOCS).as_posix()
        original = path.read_text(encoding="utf-8")

        def replace(match):
            old, _, fragment = match[1].partition("#")
            target = targets.get(posixpath.normpath(posixpath.join(posixpath.dirname(page), old)))
            if not target:
                return match[0]
            target_page, anchor = target
            return f"]({relative(page, target_page)}" + (f"#{anchor or fragment}" if anchor or fragment else "") + ")"

        text = re.sub(r"\]\(([^()\s]+\.md(?:#[\w-]+)?)\)", replace, original)
        if text != original:
            path.write_text(text, encoding="utf-8")
