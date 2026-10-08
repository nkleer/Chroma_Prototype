"""The core idea of each color and color combination, from Magic: The Gathering's own writing (Mark Rosewater's
color pie articles; the Ravnica guilds, the Alara shards and the Tarkir clans). Reference data for naming eras,
writing two- and three-color options, and explaining a person's identity. Nothing here is a force in the engine."""

IDEAS = {
    # single colors: goal through means (Rosewater, "Mechanical Color Pie" and the color philosophy articles)
    "W": ("White", "peace through structure: morality, order, community, the group above the self"),
    "U": ("Blue", "perfection through knowledge: learning, reason, improvement, thinking before acting"),
    "B": ("Black", "power through opportunity: self-interest, ambition, using whatever works"),
    "R": ("Red", "freedom through action: emotion, impulse, passion, living in the moment"),
    "G": ("Green", "acceptance through wisdom: nature, tradition, instinct, what is meant to be"),
    # ally pairs (Ravnica guilds)
    "WU": ("Azorius", "law and procedure: order kept by rules, deliberation and institutions"),
    "UB": ("Dimir", "secrets: information as power, working unseen"),
    "BR": ("Rakdos", "indulgence: pleasure, performance and freedom from restraint"),
    "RG": ("Gruul", "primal freedom: instinct and strength against the constraints of civilisation"),
    "WG": ("Selesnya", "harmony: community, belonging and growing together as one"),
    # enemy pairs (Ravnica guilds)
    "WB": ("Orzhov", "institutional power: wealth, obligation and hierarchy that serves those on top"),
    "UR": ("Izzet", "invention: curiosity driven by passion, experiment over caution"),
    "BG": ("Golgari", "the cycle of life and death: decay feeds growth, nothing is wasted"),
    "WR": ("Boros", "righteous action: justice enforced with zeal and courage"),
    "UG": ("Simic", "adaptation: improving on nature through understanding it"),
    # ally triads (Alara shards)
    "WUG": ("Bant", "honour and order: nobility, faith and duty to all"),
    "WUB": ("Esper", "perfection through control: refining self and world"),
    "UBR": ("Grixis", "power without restraint: ambition with no conscience"),
    "BRG": ("Jund", "survival of the fittest: strength, appetite, the food chain"),
    "WRG": ("Naya", "vitality: life lived fully, with heart, body and community"),
    # enemy triads (Tarkir clans, each with its virtue)
    "WBG": ("Abzan", "endurance: family, ancestry and holding ground"),
    "WUR": ("Jeskai", "cunning: discipline and enlightenment of mind and body"),
    "UBG": ("Sultai", "ruthlessness: patience, luxury and using what others discard"),
    "WBR": ("Mardu", "speed: decisive action and honour in the fight"),
    "URG": ("Temur", "savagery: instinct, endurance and wisdom of the wild"),
}

def mix(key):
    """Equal color mix for a combination key, e.g. 'WB' -> 'W.5 B.5'."""
    share = round(1 / len(key), 2)
    return " ".join(f"{c}{share}" for c in key)

ERA_COMBOS = [k for k in IDEAS]          # single colors, all ten pairs and all ten triads, drawn evenly
