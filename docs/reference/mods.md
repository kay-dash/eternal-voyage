# Mod inventory

The supplied snapshot contains **50 JARs** for Eternal Voyage. This inventory records the builds in that snapshot.

The [Mods directory](content/index.md) gives each mod its own overview, gameplay guides and content reference.

## One Piece systems

| Mod | Build |
| --- | --- |
| Akuma no Mi | `0.0.6-1.20.1` |
| AkumaLib | `6.8.1` |
| Awaken Awaken no Mi | `3.0.3` |
| Black Blades & Fists | `1.9.0-beta-1.20.1` |
| Blitz Utility | `0.0.6-1.20.1` |
| Cart Addon | `0.9.0-1.20.1` |
| Devil Fruit Lives | `1.2.0-1.20.1` |
| Eternal Voyage Companion | `1.15.0` |
| Haki Realm (Eternal Voyage build) | `2.0.0-1.20.1` |
| Infusion no Mi | `0.0.5-1.20.1` |
| Cruise Cruise no Mi | `0.8.0` |
| InoFruits | `4.0.0` |
| Mine Mine no Mi: Impel Down | `0.1.0` |
| Missing Missing no Mi | `8.1.0` |
| Mine Mine no Mi: Sky Island | `1.0.2` |
| Mine Mine no Mi | `0.11.6` |
| Awaken Path | `2.3.1` |
| One Piece World | `2.0.0-phase6c.4` |
| Race Race no Mi | `0.5.0` |
| Transponder Snails | `1.20.1-2.1.0` |

## World, ships and survival

| Mod | Build |
| --- | --- |
| Aquamirae | `7.1.14` |
| L_Ender's Cataclysm | `3.31` |
| Corpse | `1.20.1-1.0.23` |
| When Dungeons Arise | `2.1.58-1.20.x` |
| When Dungeons Arise: Seven Seas | `1.0.2` |
| Mowzie's Mobs | `1.8.2` |
| PlayerRevive | `2.0.31` |
| Tough As Nails | `9.2.0.171` |
| Upgrade Aquatic | `6.0.3` |
| Valkyrien Skies 2 | `2.4.11` |
| Eureka! Ships! | `1.6.4` |
| Ship In A Bottle | `1.20.1-2.0.0` |
| Ship Retrieval Service | `1.0.0` |
| Valkyrien Icebreakers | `1.1.0` |
| Respawning Structures | `1.20.1-4.4` |
| Weather2 | `1.20.1-2.8.3` |

## Maps, quests and support

| Mod | Build |
| --- | --- |
| AA4 Atlas | `1.1.2` |
| Antique Atlas | `3.1.2+1.20` |
| ExtraLib | `3.3.1` |
| ExtraQuests | `2.0.1` |
| FTB Library | `2001.2.13` |
| FTB Quests | `2001.4.22` |
| FTB Teams | `2001.3.2` |
| FTB XMod Compat | `2.1.3` |
| GlitchCore | `0.0.1.1` |
| KubeJS | `2001.6.5-build.26` |
| Rhino | `2001.2.3-build.10` |
| Proximity Chat | `1.1.6` |
| VLib | `1.20.1-0.1.1` |
| Surveyor Map Framework | `1.1.2+1.20` |

## Dependencies declared by the JARs

Some required mod IDs declared in the supplied Forge metadata have no matching top-level JAR in this snapshot. If assembling an instance, resolve them from the full pack distribution and use the loader to verify compatibility.

| Supplied mod | Required mod IDs missing from the snapshot |
| --- | --- |
| AA4 Atlas, Antique Atlas, Surveyor | `connector` or `connectormod` as declared by each build, and `fabric_api` |
| Aquamirae | `fragmentum`, `geckolib` |
| FTB Library, FTB Quests, FTB Teams, FTB XMod Compat, KubeJS | `architectury` |
| Haki Realm, Mowzie's Mobs | `geckolib` |
| L_Ender's Cataclysm | `lionfishapi` |
| PlayerRevive | `creativecore` |
| Transponder Snails | `voicechat` |
| Respawning Structures | `cupboard` |
| Ship In A Bottle | `architectury`, `fabric_api` |
| VLib | `architectury` |
| Upgrade Aquatic | `blueprint` |
| Ship In A Bottle | `1.20.1-2.0.0` |
| Ship Retrieval Service | `1.0.0` |
| Valkyrien Icebreakers | `1.1.0` |
| Respawning Structures | `1.20.1-4.4` |
| Weather2 | `coroutil` |

## Configuration-only integrations

The snapshot includes settings for **Lootr**. Those settings apply when the server has Lootr installed.
