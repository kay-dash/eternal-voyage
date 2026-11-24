"""Use American English in player prose while preserving identifiers and links."""

import re


WORD_PAIRS = """
armour armor armours armors armoured armored armourer armorer
defence defense defences defenses offence offense
colour color colours colors coloured colored colouring coloring colourful colorful
centre center centres centers centred centered harbour harbor harbours harbors
behaviour behavior behaviours behaviors flavour flavor flavours flavors
favour favor favours favors favoured favored favouring favoring
favourite favorite favourites favorites neighbour neighbor neighbours neighbors neighbouring neighboring
honour honor honours honors honoured honored labour labor rumour rumor rumours rumors
catalogue catalog catalogues catalogs dialogue dialog
metre meter metres meters centimetre centimeter centimetres centimeters kilometre kilometer kilometres kilometers
travelling traveling travelled traveled traveller traveler travellers travelers levelling leveling levelled leveled
cancelled canceled cancelling canceling signalling signaling signalled signaled
labelled labeled labelling labeling modelled modeled modelling modeling fuelled fueled fuelling fueling
recognise recognize recognises recognizes recognised recognized recognising recognizing
organise organize organised organized specialise specialize specialisation specialization
specialises specializes specialised specialized specialising specializing customise customize customised customized
paralyse paralyze paralyses paralyzes paralysed paralyzed paralysing paralyzing
realise realize realises realizes realised realized stabilise stabilize neutralise neutralize
crystallise crystallize crystallised crystallized
practise practice practises practices practised practiced practising practicing
manoeuvre maneuver manoeuvres maneuvers manoeuvring maneuvering
artefact artifact artefacts artifacts mould mold moulds molds moustache mustache
grey gray greys grays greyed grayed towards toward whilst while amongst among
ageing aging jewellery jewelry aluminium aluminum aeroplane airplane
""".split()
SPELLINGS = dict(zip(WORD_PAIRS[::2], WORD_PAIRS[1::2]))
WORD = re.compile(r"\b(?:" + "|".join(SPELLINGS) + r")\b", re.I)
PROTECTED = re.compile(r"(\x60{3}[\s\S]*?\x60{3}|\x60[^\x60\n]*\x60|\]\([^\n)]*\)|https?://[^\s<>)]+|<[^>\n]*>)")
LOCAL_ANCHORS = {
    "armor-linings": "armour-linings",
    "bloodline-catalog": "bloodline-catalogue",
    "defense-size-and-logia": "defence-size-and-logia",
}


def american_english(text):
    def replace(match):
        word = match[0]
        american = SPELLINGS[word.lower()]
        if word.isupper():
            return american.upper()
        return american.capitalize() if word[0].isupper() else american

    parts = PROTECTED.split(text)
    for i, part in enumerate(parts):
        if not i % 2:
            parts[i] = WORD.sub(replace, part)
        elif part.startswith("](") and "://" not in part and ".md#" in part:
            for current, old in LOCAL_ANCHORS.items():
                parts[i] = parts[i].replace(f".md#{old})", f".md#{current})")
    return "".join(parts)
