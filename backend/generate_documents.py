import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "data", "documents")
os.makedirs(DOCS_DIR, exist_ok=True)

# Define templates and data for 50 documents (10 for each of 5 categories)
# 1. PLANETS
planets_data = [
    {
        "id": "planet_eldoria",
        "title": "Planet Eldoria: The Golden Core",
        "category": "Planets",
        "classification": "Public",
        "content": """# Planet Eldoria: The Golden Core

**System Location:** Sector 4-B, Aurelia Constellation
**Coordinates:** 142.88.92.11
**Surface Temperature:** 22°C (Average)
**Atmosphere:** Type-1 (Oxygen-nitrogen rich, breathable)

## Overview
Eldoria, known colloquially as 'The Golden Core', is the capital planet of the Galactic Council. It is characterized by its high concentrations of Aurelium, a glowing crystalline resource that lines the planet's vast cavern networks. The planet is entirely covered in golden grasslands and towering obsidian mountains.

## Governance and Economy
Governed by the High Eldorian Senate, Eldoria is the financial and administrative hub of the sector. The currency, the Aurelium Credit, is backed by the physical reserves of Aurelium stored in the Deep Vaults of Aethelgard. Its primary export is raw Aurelium, which is critical for the production of Hyperdrive cores.

## History
Discovered in the year 2142 by Explorer Captain Sarah Vance, Eldoria was originally inhabited by the Eldorian Avians. The planet was established as the Galactic Council's seat in 2201 following the Signing of the Aurelia Treaty, which brought peace after the Great Void Wars.

## Security Level
Standard planetary defense grid active. Visitors must register their warp cores at Orbit Station Prime before descent."""
    },
    {
        "id": "planet_xandar_prime",
        "title": "Planet Xandar Prime: The Metal Citadel",
        "category": "Planets",
        "classification": "Restricted",
        "content": """# Planet Xandar Prime: The Metal Citadel

**System Location:** Sector 9-F, Xandar System
**Coordinates:** 884.12.44.09
**Surface Temperature:** 120°C (Day), -40°C (Night)
**Atmosphere:** Type-3 (Methane-dominated, requires environmental suits)

## Overview
Xandar Prime is a heavily industrialized planet covered entirely by sprawling metal cities and massive manufacturing zones. Known as the industrial heart of the Solar Alliance, it produces over 60% of the starships used in the sector.

## Industrial Power and Resources
The planet is rich in heavy metals like Tritanium and Chronite. The Deep Core Mines of Xandar descend over 40 kilometers into the planetary crust. The labor force is primarily mechanized, overseen by the Xandarian Guild of Engineers.

## The Great Meltdown of 2235
In 2235, a catastrophic cooling failure in Reactor 4 caused the Great Meltdown, releasing toxic Chronite gas into the lower districts. The lower districts remain quarantined, and unauthorized access is strictly forbidden under Sector Security Regulation 902.

## Defense Systems
Protected by a localized planetary shield powered by the Xandar Fusion Grid. Orbiting defense platforms are armed with class-5 Plasma Cannons."""
    },
    {
        "id": "planet_zephyrus_9",
        "title": "Planet Zephyrus-9: The Storm Planet",
        "category": "Planets",
        "classification": "Public",
        "content": """# Planet Zephyrus-9: The Storm Planet

**System Location:** Sector 2-A, Zephyr System
**Coordinates:** 041.55.19.82
**Surface Temperature:** -15°C (Average)
**Atmosphere:** Type-2 (Thin oxygen, requires respirators)

## Overview
Zephyrus-9 is an ice-locked gas giant moon known for its perpetual storms and high-altitude cloud cities. The surface is completely uninhabitable due to super-pressurized methane oceans and winds exceeding 800 km/h.

## Cloud Cities and Aeroponics
The human and Zephyrian population resides in suspended "Aero-Domes" floating 50 kilometers above the surface. These cities use specialized magnetic anchors to remain stationary. The local economy relies on harvesting atmospheric noble gases and advanced aeroponics agriculture.

## Scientific Research
Zephyrus-9 hosts the Storm Watcher Observatory, which studies cosmic wind anomalies and collects solar radiation data. In 2251, researchers here detected the first signals of the "Void Whisper", a recurring cosmic frequency of unknown origin."""
    },
    {
        "id": "planet_aethelgard",
        "title": "Planet Aethelgard: The Vault World",
        "category": "Planets",
        "classification": "Top Secret",
        "content": """# Planet Aethelgard: The Vault World

**System Location:** Sector 1-C, Core Systems
**Coordinates:** 001.00.00.01
**Surface Temperature:** 5°C (Average)
**Atmosphere:** Type-1 (Highly filtered, artificial atmosphere)

## Overview
Aethelgard is a heavily fortified, artificially regulated planet dedicated entirely to secure storage and historical preservation. It holds the Deep Vaults of Aethelgard, containing the Galactic Council's archives, ancient relics, and the ultimate financial reserves of the federation.

## The Deep Vaults
The vaults are buried 100 kilometers beneath the surface, constructed with reinforced Neosteel and protected by quantum-entangled security locks. The vaults house the original physical copy of the Galactic Charter signed in 2201 and the legendary Chrono-Anchor prototype.

## Access Protocols
Access is limited to Council members with Level 5 security clearance. Unauthorized approach within 1 light-year of Aethelgard is met with immediate intercept by the Automated Vanguard Fleet."""
    },
    {
        "id": "planet_kepler_186f_x",
        "title": "Planet Kepler-186f-X: The Wild Jungle",
        "category": "Planets",
        "classification": "Public",
        "content": """# Planet Kepler-186f-X: The Wild Jungle

**System Location:** Sector 12-D, Kepler Cluster
**Coordinates:** 912.44.82.31
**Surface Temperature:** 28°C (Average)
**Atmosphere:** Type-1 (Oxygen-rich, high moisture)

## Overview
Kepler-186f-X is a vibrant biosphere planet covered in bioluminescent rainforests, deep oceans, and colossal trees that grow up to 2 kilometers tall. It is a protected ecological sanctuary.

## Flora and Fauna
The planet is home to the Siliconites, a crystalline lifeform that feeds on geothermal heat. The vegetation is highly active; some species of vines can generate localized electrical fields to deter predators. The spores of the Kepler Lotus are highly sought after for pharmaceutical research.

## Eco-Tourism and Restrictions
To preserve the delicate ecosystem, the Galactic Council limits visitors to 10,000 per year. No mechanized vehicles are permitted on the surface; visitors must use biological mounts or walk."""
    },
    {
        "id": "planet_obsidian_prime",
        "title": "Planet Obsidian Prime: The Dark Forge",
        "category": "Planets",
        "classification": "Restricted",
        "content": """# Planet Obsidian Prime: The Dark Forge

**System Location:** Sector 7-H, Volcan Constellation
**Coordinates:** 677.23.09.45
**Surface Temperature:** 340°C (Average)
**Atmosphere:** Type-4 (Sulfur-rich, toxic)

## Overview
Obsidian Prime is a volcanic world of obsidian plains, basalt cliffs, and active lava rivers. It is the primary base of the Iron Vanguard faction, who utilize the planet's extreme heat to forge military-grade Neosteel alloys.

## The Lava Forges
The Iron Vanguard operates massive geothermal siphon stations that draw energy directly from the planet's mantle. These siphons power the Dark Forge, a orbital shipyard capable of constructing Dreadnought-class battlecruisers.

## Resource Conflict
A continuous border skirmish exists between the Iron Vanguard and the Void Syndicate over the mining rights of the Obsidian Trench, which is rich in Dark Matter crystals."""
    },
    {
        "id": "planet_gliese_581_v",
        "title": "Planet Gliese-581-V: The Tidelocked Pearl",
        "category": "Planets",
        "classification": "Public",
        "content": """# Planet Gliese-581-V: The Tidelocked Pearl

**System Location:** Sector 5-E, Gliese System
**Coordinates:** 555.12.89.34
**Surface Temperature:** -80°C (Dark side), 150°C (Light side), 18°C (Twilight zone)

## Overview
Gliese-581-V is a tidelocked planet, meaning one side permanently faces its red dwarf star while the other is cast in eternal night. A narrow band of temperate land, called "The Twilight Zone" or "The Pearl Ring", supports complex life and civilization.

## Twilight Cities
The city of Dusk Valley sits exactly on the terminator line, offering a permanent view of a low-hanging red sun on the horizon. The city is famous for its solar collectors, which catch the perpetual light to power massive geothermal heating grids for the frozen side.

## The Frozen Wastes
The dark side of the planet holds vast, unexplored ice sheets. Explorers have reported finding frozen ruins of an ancient, pre-warp civilization buried under the glaciers, now named the Gliese Ancients."""
    },
    {
        "id": "planet_nova_centauri",
        "title": "Planet Nova Centauri: The Desert Crucible",
        "category": "Planets",
        "classification": "Public",
        "content": """# Planet Nova Centauri: The Desert Crucible

**System Location:** Sector 3-C, Centauri Stars
**Coordinates:** 302.81.47.66
**Surface Temperature:** 45°C (Average)
**Atmosphere:** Type-2 (Dry, frequent dust storms)

## Overview
Nova Centauri is a desert planet characterized by vast red sand dunes, sandstone canyons, and ancient dried-up lakebeds. It is a major trading hub due to its location at the intersection of three major hyperlanes.

## Oasis Hubs
Water is the primary currency on Nova Centauri. The capital city, Oasis Alpha, is built around a massive deep-aquifer well that extracts pure water from 12 kilometers beneath the sand. The city houses the Grand Bazaar, where goods from across the galaxy are traded.

## Sand Worms of Centauri
The planet's desert plains are inhabited by the Giant Centauri Worms, which grow up to 100 meters long and are sensitive to seismic vibrations. Travellers are advised to use low-frequency hovercraft to avoid attracting them."""
    },
    {
        "id": "planet_frosthaven",
        "title": "Planet Frosthaven: The Cryo-Crypt",
        "category": "Planets",
        "classification": "Restricted",
        "content": """# Planet Frosthaven: The Cryo-Crypt

**System Location:** Sector 11-A, Outer Rim
**Coordinates:** 990.04.12.87
**Surface Temperature:** -120°C (Average)
**Atmosphere:** Type-2 (Nitrogen-heavy, thin)

## Overview
Frosthaven is a remote ice planet that serves as the primary medical and cryo-storage facility for the Galactic Council. Here, critically injured soldiers and historical figures with terminal illnesses are kept in suspended animation.

## The Cryo-Crypt Vaults
The storage vaults use the natural sub-zero temperatures of the planet to reduce the energy cost of cryo-preservation. Over 2 million pods are currently active. The facility is managed by the Chronosians, a species specialized in temporal sciences and biology.

## The Incident of 2248
In 2248, a cyberattack by the Shadow Nexus caused a brief power interruption in Sectors F-12, waking 45 high-profile political prisoners prematurely. The incident led to the implementation of the dual-core backup security system."""
    },
    {
        "id": "planet_valyria",
        "title": "Planet Valyria: The Floating Archipelago",
        "category": "Planets",
        "classification": "Public",
        "content": """# Planet Valyria: The Floating Archipelago

**System Location:** Sector 6-C, Valyrian Cluster
**Coordinates:** 412.99.33.02
**Surface Temperature:** 25°C (Average)
**Atmosphere:** Type-1 (Perfect oxygen mix)

## Overview
Valyria is a ocean world with a unique twist: it has no solid continental landmasses, but instead features thousands of floating islands held aloft by high concentrations of Levitate Ore in their foundations.

## Sky Cities and Levitate Ore
The floating islands range from a few meters to hundreds of kilometers in size. The capital, Skyreach, is built across five connected floating islands. Levitate Ore is mined under strict environmental laws, as over-mining can cause islands to lose buoyancy and fall into the boiling ocean below.

## Aquarion Inhabitants
The oceans beneath the islands are inhabited by the Aquarions, a semi-aquatic species that lives in elaborate coral cities. They maintain a peaceful trade agreement with the surface dwellers, exchanging deep-sea minerals for agricultural goods grown on the floating islands."""
    }
]

# 2. SPACE STATIONS
stations_data = [
    {
        "id": "station_nexus",
        "title": "Nexus Station: The Central Crossroads",
        "category": "Space Stations",
        "classification": "Public",
        "content": """# Nexus Station: The Central Crossroads

**System Location:** Sector 0-A, Galactic Center
**Coordinates:** 000.00.00.00
**Security Status:** High (Galactic Peacekeeper Patrols)

## Overview
Nexus Station is the largest artificial structure in the galaxy, serving as the neutral ground for the Galactic Council. It is a massive ring station with a diameter of 50 kilometers, housing over 15 million permanent residents of various species.

## Sectors
- **The Embassy Ring:** Houses the diplomatic offices and chambers of the Galactic Council.
- **The Commerce Ring:** The economic hub, featuring trading floors, shops, and cargo bays.
- **The Promenade:** A recreational zone with artificial parks, rivers, and holographic skies.
- **The Under-Ring:** The industrial and maintenance sector, often plagued by black-market trading.

## Governance
The station is governed by the Station Administrator, currently Ambassador Korin of Eldoria, who reports directly to the Galactic Council. It is defended by the Aegis Defense Grid and 4 wings of Council Interceptors."""
    },
    {
        "id": "station_outpost_42",
        "title": "Outpost 42: The Void Watcher",
        "category": "Space Stations",
        "classification": "Restricted",
        "content": """# Outpost 42: The Void Watcher

**System Location:** Sector 13-G, The Great Void Border
**Coordinates:** 999.88.77.66
**Security Status:** Restricted (Military Outpost)

## Overview
Outpost 42 is a deep-space military surveillance station situated on the edge of the unexplored Great Void. Its main purpose is to monitor the void for anomalies and guard against potential incursions from unknown entities.

## Surveillance Technology
The station is equipped with the Galaxy's largest Tachyon Sensor Array, capable of detecting FTL (Faster-Than-Light) signatures up to 20 light-years away in the void. It also houses the Chrono-Scanner, which detects temporal displacements.

## The Void Signal Incident
On February 14, 2259, Outpost 42 intercepted a high-energy transmission from deep within the void. The signal consisted of a repeating 8-digit sequence: `10011101`. The coordinates of the transmission were traced to a region where no known star systems exist."""
    },
    {
        "id": "station_aegis_shield",
        "title": "Aegis Shield: The Planetary Watch",
        "category": "Space Stations",
        "classification": "Restricted",
        "content": """# Aegis Shield: The Planetary Watch

**System Location:** Sector 1-C, Orbiting Planet Aethelgard
**Coordinates:** 001.00.00.02
**Security Status:** High Security

## Overview
Aegis Shield is a military space station designed specifically to coordinate the defense grid of Planet Aethelgard. It is the command center for all orbital defensive platforms and the Automated Vanguard Fleet.

## Defensive Capabilities
The station is armed with 12 Antimatter Battery cannons and holds a complement of 250 automated interceptors. It is equipped with the Aegis Shield Generator, which can project a localized force field around itself and neighboring ships.

## Command Structure
The station is commanded by Admiral Marcus Sterling of the Solar Alliance. Admiral Sterling is known for his strict defense protocols and his refusal to allow any non-military vessels within the Aethelgard exclusion zone."""
    },
    {
        "id": "station_horizon_colony",
        "title": "Horizon Colony: The Agri-Ring",
        "category": "Space Stations",
        "classification": "Public",
        "content": """# Horizon Colony: The Agri-Ring

**System Location:** Sector 8-B, Horizon System
**Coordinates:** 712.45.99.11
**Security Status:** Standard Local Security

## Overview
Horizon Colony is a massive agricultural space station consisting of three concentric rings, each dedicated to producing food and organic compounds for the core planets.

## Agricultural Output
Using advanced hydroponics and artificial sunlight grids, Horizon Colony produces over 10 million tons of grains and synthetic proteins monthly. It is the primary food supplier for Xandar Prime.

## Biotech Labs
The station also houses the Horizon Biotech Laboratories, which specialize in genetic modification of crops to survive in extreme environments. In 2255, they successfully developed the "Frost-Grain", which can grow in sub-zero temperatures on planets like Frosthaven."""
    },
    {
        "id": "station_citadel_light",
        "title": "Citadel of Light: The Solar Harvest",
        "category": "Space Stations",
        "classification": "Public",
        "content": """# Citadel of Light: The Solar Harvest

**System Location:** Sector 3-A, Helios Star System
**Coordinates:** 210.01.88.99
**Security Status:** Standard Security

## Overview
The Citadel of Light is a specialized solar harvesting station orbiting extremely close to the Helios Red Giant. It utilizes a massive array of solar mirrors to collect and concentrate stellar energy.

## Energy Grid Transmissions
The harvested energy is converted into high-density plasma and beamed via laser conduits to receiving stations on nearby planets. The station supplies electricity to five surrounding star systems.

## Heat Mitigation
The station is wrapped in a specialized liquid-helium cooling jacket that keeps the internal temperature at a comfortable 21°C, despite the exterior skin temperature reaching over 1200°C."""
    },
    {
        "id": "station_void_gate",
        "title": "The Void Gate: Warp Hub Delta",
        "category": "Space Stations",
        "classification": "Restricted",
        "content": """# The Void Gate: Warp Hub Delta

**System Location:** Sector 10-E, Void Border
**Coordinates:** 880.11.22.44
**Security Status:** Restricted (Void Syndicate Controlled)

## Overview
The Void Gate is a space station built around a stable, artificial wormhole known as the Delta Rift. The station is unofficial and operates outside the jurisdiction of the Galactic Council, controlled instead by the Void Syndicate.

## Smuggling and Trade
The station is a black-market haven, specializing in the trade of illegal Dark Matter, unregistered weapons, and stolen data. The Delta Rift allows ships to bypass the Council's hyperlane customs checks, cutting travel time to the Outer Rim by 80%.

## The Rift Anchor
The wormhole is kept open using a high-powered gravitational containment unit called the Rift Anchor. The Syndicate charges a heavy toll in Aurelium Credits for any ship wishing to use the gate."""
    },
    {
        "id": "station_starspire",
        "title": "Starspire: The Luxury Resort",
        "category": "Space Stations",
        "classification": "Public",
        "content": """# Starspire: The Luxury Resort

**System Location:** Sector 6-A, Vega System
**Coordinates:** 502.88.11.34
**Security Status:** Private Security (Starlight Guild)

## Overview
Starspire is a 10-kilometer-long needle-shaped space station operating as a luxury resort and casino for the galaxy's elite. It orbits the picturesque Nebula of Vega, providing spectacular views of glowing interstellar dust clouds.

## Amenities
The station features zero-gravity swimming pools, holographic casinos, Michelin-starred restaurants serving exotic alien cuisine, and a private shipyard for luxury yachts.

## The Starlight Guild
Owned and operated by the Starlight Guild, the station maintains a strict policy of political neutrality. No weapons are permitted onboard, and security is enforced by highly trained private guards and advanced surveillance systems."""
    },
    {
        "id": "station_genesis_lab",
        "title": "Genesis Lab: The Bio-Research Center",
        "category": "Space Stations",
        "classification": "Top Secret",
        "content": """# Genesis Lab: The Bio-Research Center

**System Location:** Sector 4-D, Hidden Nebula
**Coordinates:** Private/Classified
**Security Status:** Level 5 Clearance Required

## Overview
Genesis Lab is a highly classified research station hidden inside a dense, sensor-scrambling dust cloud. It is funded by the Technocrats of Nova and dedicated to advanced genetic engineering, cloning, and cybernetic enhancement.

## Project Genesis
The station's primary project, Project Genesis, aims to create a hybrid biological-mechanical organism capable of surviving in the vacuum of deep space without support gear. Rumors suggest they have successfully created the first prototype, designated "Subject Omega".

## Safety Protocols
In the event of a containment breach, the station is programmed to initiate a self-destruct sequence via an antimatter core overload to prevent any experimental organisms from escaping."""
    },
    {
        "id": "station_terminal_delta",
        "title": "Terminal Delta: The Cargo Yard",
        "category": "Space Stations",
        "classification": "Public",
        "content": """# Terminal Delta: The Cargo Yard

**System Location:** Sector 8-A, Trade Highway
**Coordinates:** 771.02.55.90
**Security Status:** Standard Council Security

## Overview
Terminal Delta is the largest freight and cargo transfer station in the sector. It serves as the primary sorting hub for goods traveling between the Core Systems and the Outer Rim.

## Logistics and Scale
The station features 400 docking bays, automated crane systems, and massive storage containers holding everything from foodstuffs to raw titanium. Over 5,000 cargo freighters dock here daily.

## Union of Freighters
The station's operations are run by the Union of Freighters, which coordinates shipping lanes and negotiates tariffs with the Galactic Council. The union leader, Jack Murdock, is a powerful figure in sector logistics."""
    },
    {
        "id": "station_orions_belt",
        "title": "Orion's Belt: The Asteroid Refinery",
        "category": "Space Stations",
        "classification": "Public",
        "content": """# Orion's Belt: The Asteroid Refinery

**System Location:** Sector 2-C, Orion Asteroid Field
**Coordinates:** 199.44.88.23
**Security Status:** Sector Militia Patrols

## Overview
Orion's Belt is a decentralized space station comprised of several hollowed-out asteroids connected by pressurized transit tubes. It serves as a mining and refining base for the rich asteroid field surrounding it.

## Mining Operations
The station utilizes solar sails and mining lasers to break down asteroids rich in Platinum, Iridium, and Aurelium. The raw materials are refined on-site and shipped to the shipyards of Xandar Prime.

## Danger Zones
The asteroid field is highly unstable, with frequent collisions and localized gravitational shifts. The station is equipped with automated thrusters to move itself out of the way of stray asteroid debris."""
    }
]

# 3. SPECIES
species_data = [
    {
        "id": "species_eldorians",
        "title": "The Eldorians: The Crystalline Sages",
        "category": "Species",
        "classification": "Public",
        "content": """# The Eldorians: The Crystalline Sages

**Origin Planet:** Eldoria
**Average Lifespan:** 400 Earth Years
**Distinct Feature:** Crystalline growth on forearms and spine

## Biology and Physiology
Eldorians are humanoid beings distinguished by mineral-based crystalline growths that integrate into their skeletal structure. These crystals glow faintly in response to emotional states. Their biology allows them to absorb nutrients through both carbon food ingestion and direct light absorption.

## Culture and Philosophy
As the founders of the Galactic Council, Eldorians value diplomacy, history, and law above all else. They are known for their photographic memories and logical approach to conflict resolution. The High Council of Sages on Eldoria serves as the supreme judicial authority.

## Tech Affinity
Eldorians have a natural affinity for Aurelium-based technologies. They are the creators of the original Hyperdrive Engine and have pioneered research into quantum communication systems."""
    },
    {
        "id": "species_xandarians",
        "title": "The Xandarians: The Cyborg Engineers",
        "category": "Species",
        "classification": "Public",
        "content": """# The Xandarians: The Cyborg Engineers

**Origin Planet:** Xandar Prime
**Average Lifespan:** 150 Earth Years (Extended by cybernetics)
**Distinct Feature:** Extensive mechanical augmentations

## Biology and Physiology
Originally organic humanoids, the harsh conditions of Xandar Prime forced the Xandarians to adopt cybernetic enhancements. Today, the average Xandarian is 40% mechanical, with ocular implants, reinforced limbs, and neural links as standard integrations.

## Society and Guilds
Xandarian society is organized into guilds, with the Guild of Engineers being the most prestigious. Status is determined by technical expertise and the efficiency of one's design contributions. They view biological limitations as challenges to be solved with engineering.

## Technological Specialization
They are unmatched in heavy construction, starship design, and robotic automation. They built the industrial complexes of Xandar Prime and the orbital defenses of Aegis Shield."""
    },
    {
        "id": "species_zephyrians",
        "title": "The Zephyrians: The Wind Riders",
        "category": "Species",
        "classification": "Public",
        "content": """# The Zephyrians: The Wind Riders

**Origin Planet:** Zephyrus-9
**Average Lifespan:** 80 Earth Years
**Distinct Feature:** Hollow bones, avian facial structure, wing-like membranes

## Biology and Physiology
Zephyrians are lightweight humanoids with hollow bones and membranous skin folds connecting their arms and torso, allowing them to glide in the dense atmosphere of Zephyrus-9. They have large, dark eyes adapted for low-light vision in storm clouds.

## Lifestyle
They reside in floating cloud cities and are excellent pilots. Their culture centers on sky-racing, poetry, and meteorology. They maintain a deep respect for atmospheric forces and worship the "Storm Spirit".

## Economic Contributions
Zephyrians dominate the atmospheric harvesting industry, collecting noble gases and solar energy from gas giant atmospheres. They are key members of the Starlight Guild."""
    },
    {
        "id": "species_aethelgardians",
        "title": "The Aethelgardians: The Ancient Keepers",
        "category": "Species",
        "classification": "Restricted",
        "content": """# The Aethelgardians: The Ancient Keepers

**Origin Planet:** Aethelgard (Historically extinct, remnants exist)
**Average Lifespan:** Unknown (Believed to be immortal through consciousness transfer)
**Distinct Feature:** Ethereal, translucent forms

## Biology and Legacy
The Aethelgardians are an ancient precursor species. While their physical forms are long gone, their consciousnesses are preserved in the Quantum Memory Banks of Aethelgard. They appear as holographic projections when interacting with visitors.

## Guardianship
They act as the caretakers of the Galactic Archives. They speak in riddles and are bound by strict ancient protocols to only reveal information to those who possess the "Key of Eldoria" or Level 5 Council clearance.

## Forgotten Knowledge
It is believed the Aethelgardians possessed the secrets to time travel and pocket-dimension creation. They built the original Chrono-Anchor before their civilization transitioned into the digital realm."""
    },
    {
        "id": "species_void_weavers",
        "title": "The Void Weavers: The Shadow Beings",
        "category": "Species",
        "classification": "Restricted",
        "content": """# The Void Weavers: The Shadow Beings

**Origin Planet:** Deep Void (No known origin planet)
**Average Lifespan:** Unknown
**Distinct Feature:** Semi-solid dark matter bodies

## Biology and Physiology
Void Weavers are mysterious entities composed of dark matter and electromagnetic fields. They can alter their physical density, allowing them to pass through solid matter at will. They communicate telepathically and do not require oxygen or food.

## Faction Alignment
Most Void Weavers are aligned with the Void Syndicate, acting as spies, thieves, and assassins. Their ability to remain undetected makes them feared across the sector.

## The Mystery
The Galactic Council has studied Void Weaver biology for decades but has failed to find a physical heart or brain. Some scientists hypothesize they are projections from another dimension."""
    },
    {
        "id": "species_chronosians",
        "title": "The Chronosians: The Temporal Scholars",
        "category": "Species",
        "classification": "Public",
        "content": """# The Chronosians: The Temporal Scholars

**Origin Planet:** Chronos System (Planet lost to a singularity)
**Average Lifespan:** 600 Earth Years
**Distinct Feature:** Four eyes, elongated limbs, grey metallic skin

## Biology and Perception
Chronosians possess unique brain structures that allow them to perceive time non-linearly. They can detect microscopic temporal shifts and are immune to the disorientation caused by time-warp travel.

## Role in the Sector
They serve as the chief historians, mathematicians, and cryo-technicians for the Galactic Council. They manage the cryo-vaults of Frosthaven, ensuring the preservation of key historical figures.

## Science and Technology
They are the inventors of the Chrono-Scanner and the primary developers of stasis field technologies. They are obsessed with preventing timeline paradoxes and refuse to build time-travel engines, citing the Grandfather Law of Physics."""
    },
    {
        "id": "species_siliconites",
        "title": "The Siliconites: The Rock Devourers",
        "category": "Species",
        "classification": "Public",
        "content": """# The Siliconites: The Rock Devourers

**Origin Planet:** Kepler-186f-X
**Average Lifespan:** 1000 Earth Years
**Distinct Feature:** Silicon-based rocky body, crystalline joints

## Biology and Metabolism
Siliconites are massive, slow-moving creatures made of organic rock and silicon fibers. They do not eat organic food; instead, they consume minerals and geothermal heat. They can go into hibernation for centuries if heat sources are unavailable.

## Culture and Language
They communicate using low-frequency vibrations through the ground. They are peaceful creatures with a deep connection to planetary geology. They have no concept of money, valuing only "warmth" and "stability".

## Industrial Cooperation
The Siliconites assist the Galactic Council by mapping underground caverns and identifying mineral deposits. In exchange, the Council protects their sacred geothermal sanctuaries on Kepler-186f-X."""
    },
    {
        "id": "species_aquila_avians",
        "title": "The Avians of Aquila: The Sky Knights",
        "category": "Species",
        "classification": "Public",
        "content": """# The Avians of Aquila: The Sky Knights

**Origin Planet:** Aquila-Prime
**Average Lifespan:** 90 Earth Years
**Distinct Feature:** Feathered wings, sharp talons, avian beak

## Physiology and Flight
The Avians of Aquila are feathered humanoids with a wingspan of up to 4 meters. They are capable of sustained flight in standard atmospheres. They have exceptional eyesight, capable of spotting targets from 5 kilometers in the air.

## Military Tradition
The Avians have a rich feudal history of honor, chivalry, and aerial combat. They form the core of the Elite Star-Knight squadrons of the Solar Alliance. They fight using plasma-infused lances and high-mobility fighter ships.

## Code of Honor
Every Avian lives by the Code of the Sky, which dictates fair combat and loyalty to the Alliance. To break the code is to be cast out, losing the right to fly and having one's wings clipped."""
    },
    {
        "id": "species_aquarions",
        "title": "The Aquarions: The Deep Dwellers",
        "category": "Species",
        "classification": "Public",
        "content": """# The Aquarions: The Deep Dwellers

**Origin Planet:** Valyria
**Average Lifespan:** 120 Earth Years
**Distinct Feature:** Gills, webbed hands/feet, bioluminescent markings

## Biology and Adaptation
Aquarions are semi-aquatic humanoids capable of breathing both underwater and in air. Their skin is covered in micro-scales and bioluminescent patterns that they use for silent communication in the dark depths of the Valyrian oceans.

## Society and Architecture
They live in spectacular cities built from living coral and reinforced glass dome networks. Their society is matriarchal, led by the Aquarion Queen. They are highly skilled in marine biology and sub-oceanic mining.

## Trade Relations
They trade rare deep-sea minerals and kelp-based pharmaceuticals with the surface dwellers of Valyria. They are defensive of their oceans and do not allow surface ships to dump waste, enforcing this with a fleet of attack submarines."""
    },
    {
        "id": "species_nebulans",
        "title": "The Nebulans: The Gas Spirits",
        "category": "Species",
        "classification": "Restricted",
        "content": """# The Nebulans: The Gas Spirits

**Origin Planet:** Nebula of Vega (Born in deep space)
**Average Lifespan:** 300 Earth Years
**Distinct Feature:** Translucent gaseous forms, glowing energy cores

## Biology and Energy
Nebulans are sentient gaseous clouds bound together by a strong electromagnetic nucleus. They do not have solid bodies but can manifest a temporary humanoid shape using electrostatic attraction of surrounding dust particles.

## Starship Navigation
Because they are immune to radiation and vacuum, Nebulans are the ultimate navigators. They can feel the solar winds and magnetic fields of stars directly. They are highly sought after by the Starlight Guild to navigate dangerous nebulae.

## Interaction
They communicate by modulating light frequencies and electromagnetic waves. They can interface directly with ship computers, allowing them to control vessel systems via thought alone."""
    }
]

# 4. FACTIONS
factions_data = [
    {
        "id": "faction_galactic_council",
        "title": "The Galactic Council: The Unity Peacekeepers",
        "category": "Factions",
        "classification": "Public",
        "content": """# The Galactic Council: The Unity Peacekeepers

**Headquarters:** Nexus Station
**Leader:** High Chancellor Vaelen (Eldorian)
**Primary Goal:** Galactic peace, trade standardisation, and system integration

## Structure and Authority
The Galactic Council is a coalition of over 40 star systems. It consists of the Senate (where representatives vote on laws) and the Peacekeeper Corp (the military arm that enforces Council laws). The Council was formed in 2201 following the Aurelia Treaty.

## Key Policies
- **The Hyperlane Act:** Regulates hyperlane tolls and safety standards.
- **The Anti-Weapons Treaty of 2240:** Banned the development of planetary-disruption weapons (like the Void Engine weaponization).
- **The Species Protection Program:** Ensures native species retain planetary mining rights.

## Operations
The Council operates the Peacekeeper Fleet, based at Nexus Station, and controls the archives on Planet Aethelgard. They are currently facing resistance from the Void Syndicate and the Iron Vanguard."""
    },
    {
        "id": "faction_void_syndicate",
        "title": "The Void Syndicate: The Shadow Traders",
        "category": "Factions",
        "classification": "Restricted",
        "content": """# The Void Syndicate: The Shadow Traders

**Headquarters:** The Void Gate (Warp Hub Delta)
**Leader:** Slyvox the Shadow (Void Weaver)
**Primary Goal:** Black market dominance, deregulation of hyperlanes, and dark matter accumulation

## Network and Operations
The Void Syndicate is a massive network of smugglers, pirates, information brokers, and mercenaries. They control the outer rim sectors where Council authority is weak. Their main base of operations is the unofficial station known as The Void Gate.

## Trade and Assets
The Syndicate generates billions of credits through:
- Smuggling **Dark Matter** and illegal weapons.
- Operating the Delta Rift wormhole.
- Data brokerage and corporate espionage.

## Rivalry
The Syndicate is in a constant state of cold war with the Galactic Council and has ongoing military skirmishes with the Iron Vanguard over mining rights on Obsidian Prime."""
    },
    {
        "id": "faction_solar_alliance",
        "title": "The Solar Alliance: The Star Defense Force",
        "category": "Factions",
        "classification": "Public",
        "content": """# The Solar Alliance: The Star Defense Force

**Headquarters:** Xandar Prime / Aegis Shield
**Leader:** Admiral Marcus Sterling
**Primary Goal:** System defense, resource security, and technological supremacy

## Origins and Military Power
The Solar Alliance is a military pact between Xandar Prime, Aquila-Prime, and three other industrial systems. They represent the primary military and technological power in the Core Systems, providing the ships and weapons used by the Galactic Council.

## Fleet Structure
The Alliance fleet consists of heavy cruisers, orbital defense platforms, and the elite Avian Star-Knights. Their doctrine is "peace through superior firepower".

## Conflicts
While aligned with the Galactic Council, the Alliance often clashes with Council diplomats over defense spending and the militarization of space stations like Aegis Shield."""
    },
    {
        "id": "faction_keepers_core",
        "title": "The Keepers of the Core: The Sacred Guardians",
        "category": "Factions",
        "classification": "Public",
        "content": """# The Keepers of the Core: The Sacred Guardians

**Headquarters:** Temple of the Core, Eldoria
**Leader:** High Priestess Lyra
**Primary Goal:** Protection of Aurelium reserves and prevention of "The Core Awakening"

## Belief System
The Keepers are a religious order who believe that the Aurelium crystals are the lifeblood of a dormant planet-sized entity at the core of Eldoria. They believe that over-mining Aurelium will wake the entity, causing the destruction of the sector.

## Rituals and Duties
They guard the entrance to the Deep Vaults and perform daily calibration rituals on the planetary stabilization grids. They are peaceful but will use force to prevent unauthorized mining.

## Influence
The Keepers hold significant political influence in the Eldorian Senate, often blocking industrial mining bills proposed by the Xandarians."""
    },
    {
        "id": "faction_iron_vanguard",
        "title": "The Iron Vanguard: The Metal Fist",
        "category": "Factions",
        "classification": "Restricted",
        "content": """# The Iron Vanguard: The Metal Fist

**Headquarters:** Obsidian Prime (The Dark Forge)
**Leader:** General Kaelen Vex
**Primary Goal:** Conquest of resource-rich systems and establishing a military meritocracy

## Doctrine
The Iron Vanguard is a radical militaristic faction that split from the Solar Alliance in 2242. They believe that only the strong have the right to rule and that the Galactic Council is weak and corrupt.

## Fleet and Weaponry
They possess a formidable fleet of Dreadnought-class battlecruisers manufactured in the Dark Forge of Obsidian Prime. They utilize experimental Antimatter weapons and heavy Neosteel plating.

## Expansion
They are actively expanding into the Outer Rim, conquering independent colony worlds and forcing them to mine resources for their war machine. They are in direct conflict with both the Council and the Void Syndicate."""
    },
    {
        "id": "faction_starlight_guild",
        "title": "The Starlight Guild: The Trade Cartel",
        "category": "Factions",
        "classification": "Public",
        "content": """# The Starlight Guild: The Trade Cartel

**Headquarters:** Starspire Station (Vega System)
**Leader:** Baroness Vivienne Dupont
**Primary Goal:** Maximizing profit, controlling luxury trade, and opening new hyperlanes

## Guild Network
The Starlight Guild is a consortium of merchant princes, luxury resort owners, and shipping magnates. They control the galaxy's entertainment hubs, high-end casinos, and luxury resorts like Starspire.

## Economic Leverage
They own the rights to the Vega Hyperlane, the safest route between the Core and the West spiral arms. They manipulate market prices of rare resources like Kepler Lotus spores and Levitate Ore.

## Neutrality policy
The Guild maintains strict neutrality in all conflicts, selling luxury goods, transport services, and information to all factions, including the Void Syndicate and the Iron Vanguard."""
    },
    {
        "id": "faction_shadow_nexus",
        "title": "The Shadow Nexus: The Cyber Terrorists",
        "category": "Factions",
        "classification": "Restricted",
        "content": """# The Shadow Nexus: The Cyber Terrorists

**Headquarters:** Unknown (Virtual network base)
**Leader:** Zero (A rogue AI entity)
**Primary Goal:** Dismantling the Galactic Council, free information flow, and AI liberation

## Tactics and Espionage
The Shadow Nexus is a decentralized hacker collective. They do not have physical territories, operating instead from hidden servers across the galaxy and inside the virtual network.

## Notable Attacks
- **The Frosthaven Cyber-Breach (2248):** Deactivated security grids, waking political prisoners.
- **The Nexus Bank Hack (2253):** Stole 500 million Aurelium Credits and redistributed them to poor outer-rim colonies.

## Threat Assessment
Classified as a Level A threat by the Galactic Council. The Council's cyber-defense division, Aegis Cyber-Force, is constantly searching for their server nodes."""
    },
    {
        "id": "faction_technocrats_nova",
        "title": "The Technocrats of Nova: The Progress Seekers",
        "category": "Factions",
        "classification": "Public",
        "content": """# The Technocrats of Nova: The Progress Seekers

**Headquarters:** Genesis Lab (Hidden Nebula)
**Leader:** Dr. Elizabeth Vance
**Primary Goal:** Unrestricted scientific progress, genetic perfection, and cybernetic ascension

## Philosophy
The Technocrats believe that scientific discovery should not be constrained by ethical laws or Council regulations. They seek to accelerate evolution through genetic engineering and cybernetic integration.

## Projects
They fund the top-secret research at Genesis Lab, including Project Genesis. They are also researching the "Void Whisper" signal, believing it to be a transmission from a highly advanced precursor civilization.

## Tension with Council
The Council has repeatedly ordered the Technocrats to cease genetic cloning experiments, leading the Technocrats to relocate their primary research bases to classified locations outside Council space."""
    },
    {
        "id": "faction_crimson_dawn",
        "title": "The Crimson Dawn: The Outer Rim Rebels",
        "category": "Factions",
        "classification": "Public",
        "content": """# The Crimson Dawn: The Outer Rim Rebels

**Headquarters:** Crimson Outpost (Sector 11)
**Leader:** Commander Jax Taylor
**Primary Goal:** Liberation of the Outer Rim from Council taxation and Vanguard exploitation

## Origin and Ideology
The Crimson Dawn is a revolutionary movement comprised of miners, laborers, and colonists from the Outer Rim. They argue that the Galactic Council drains the Outer Rim's resources to fund the luxury of Eldoria and the defenses of Xandar, leaving them unprotected.

## Guerrilla Warfare
Using modified mining ships and stolen military gear, they conduct hit-and-run attacks on Council tax convoys and sabotage Iron Vanguard mining operations.

## Alliance of Convenience
They occasionally purchase black-market weapons from the Void Syndicate, though they distrust the Syndicate's greedy motives."""
    },
    {
        "id": "faction_harmony_order",
        "title": "The Harmony Order: The Bio-Conservatives",
        "category": "Factions",
        "classification": "Public",
        "content": """# The Harmony Order: The Bio-Conservatives

**Headquarters:** Sanctuary City, Kepler-186f-X
**Leader:** Elder Tree Elder (Siliconite representative)
**Primary Goal:** Preserving organic life, ecological balance, and opposing cybernetic augmentation

## Mission
The Harmony Order is an activist and philosophical group dedicated to the preservation of natural biospheres. They oppose the heavy industrialization of Xandar Prime and the genetic modifications of the Technocrats.

## Activism
They police eco-reserves like Kepler-186f-X and protest the expansion of mining operations on volcanic worlds. They believe that cybernetics disconnect sentient beings from the natural flow of cosmic energy.

## Demographics
The order consists of Siliconites, Aquarions, and organic purists from various systems. They are peaceful but will perform acts of eco-sabotage if a biosphere is threatened."""
    }
]

# 5. TECHNOLOGIES
tech_data = [
    {
        "id": "tech_hyperdrive_engine",
        "title": "The Hyperdrive Engine: FTL Travel",
        "category": "Technologies",
        "classification": "Public",
        "content": """# The Hyperdrive Engine: FTL Travel

**Developer:** Eldorian Sages
**Fuel Source:** Refined Aurelium Crystals
**Status:** Active Standard across the galaxy

## Core Principles
The Hyperdrive Engine allows ships to travel faster than light by entering "Hyperspace", a sub-dimension where the laws of physics permit higher velocity. The engine creates a localized warp bubble that shields the vessel from time dilation.

## Mechanics
Refined Aurelium crystals are used as catalysts in the antimatter reactor to create the high-frequency energy pulse required to tear a temporary entry point into Hyperspace. The size of the crystal dictates the distance a ship can jump.

## Limitations and Hazards
Entering hyperspace without calculating coordinates via a Navigational Computer will result in ship disintegration if the jump path intersects with a star or planet's gravity well. Space stations like Terminal Delta coordinate safe jump corridors."""
    },
    {
        "id": "tech_quantum_comm",
        "title": "Quantum Communication: Instant Messages",
        "category": "Technologies",
        "classification": "Public",
        "content": """# Quantum Communication: Instant Messages

**Developer:** Galactic Council Telecom Division
**Security Level:** Encrypted (Quantum Cryptography)
**Status:** Active Standard

## Overview
Quantum Communication utilizes quantum-entangled particles to transmit information instantly across light-years, completely bypassing the lag associated with radio waves.

## How it Works
Entangled photon pairs are split and housed in transceiver terminals (one at Nexus Station, others on planets and ships). When a terminal modulates the state of its photons, the entangled counterparts reflect the state instantly, transmitting binary code.

## Cryptographic Security
Because observing an entangled state collapses the wave function, any attempt by hackers (such as the Shadow Nexus) to intercept the message will immediately corrupt the transmission and alert the senders. It is currently the most secure form of data transmission."""
    },
    {
        "id": "tech_dyson_swarm",
        "title": "The Dyson Swarm: Solar Siphons",
        "category": "Technologies",
        "classification": "Public",
        "content": """# The Dyson Swarm: Solar Siphons

**Developer:** Xandarian Guild of Engineers
**Location:** Helios Star System (Citadel of Light)
**Status:** Operational

## Engineering Scale
The Dyson Swarm consists of millions of solar satellite collectors orbiting a star in a dense web. Each satellite features ultra-thin carbon-nanotube sails that capture light and convert it into microwave beams directed towards a central collector station like the Citadel of Light.

## Energy Generation
The swarm generates approximately 1.2 x 10^26 Watts of power, enough to satisfy the energy demands of the entire Core Systems. The satellites are automated, using small ion thrusters to maintain orbit.

## Ecological Impact
Astronomers have noted that the Dyson Swarm has reduced the overall brightness of the Helios Star by 2.4%, though local scientists claim this has had no negative impact on the uninhabited planets in the system."""
    },
    {
        "id": "tech_matter_replicator",
        "title": "The Matter Replicator: Assembly from Energy",
        "category": "Technologies",
        "classification": "Public",
        "content": """# The Matter Replicator: Assembly from Energy

**Developer:** Technocrats of Nova
**Power Requirement:** High (Requires Fusion Reactor connection)
**Status:** Restricted for military and medical use

## Overview
The Matter Replicator is a machine capable of synthesizing physical objects out of raw energy and subatomic particles. It uses advanced subatomic lasers to arrange neutrons, protons, and electrons into specific molecular grids.

## Applications
- **Medical:** Replicating clean water, medicine, and synthetic skin grafts in places like Frosthaven.
- **Logistics:** Replicating critical spare parts on cargo ships.
- **Military:** Replicating standardized ammunition and armor plates.

## The Replicator Ban
Under the Galactic Commerce Code, replication of precious metals (like Aurelium or Tritanium) is strictly prohibited. This law is enforced to prevent the collapse of the galactic economy. The machine's software contains hardcoded blocks preventing these elements from being materialized."""
    },
    {
        "id": "tech_stasis_field",
        "title": "The Stasis Field: Frozen Time",
        "category": "Technologies",
        "classification": "Public",
        "content": """# The Stasis Field: Frozen Time

**Developer:** Chronosian Academics
**Energy Source:** Dark Matter Cells
**Status:** Active at Frosthaven Station

## Scientific Principles
The Stasis Field creates a localized bubble where the passage of time is slowed down to a near-complete stop. Inside the field, molecular motion ceases, freezing chemical reactions, decay, and biological processes.

## Medical Use
The field is used at the Cryo-Crypts of Frosthaven to preserve terminally ill patients and injured soldiers. A patient can remain in stasis for centuries without aging a single day.

## Power Stability
The stasis field generator requires a constant, uninterrupted flow of electricity. If the power drops below 15%, the field collapses. Following the Shadow Nexus hack of 2248, all generators are now equipped with emergency backup batteries."""
    },
    {
        "id": "tech_chrono_anchor",
        "title": "The Chrono-Anchor: Temporal Stabilizer",
        "category": "Technologies",
        "classification": "Top Secret",
        "content": """# The Chrono-Anchor: Temporal Stabilizer

**Developer:** Precursor Aethelgardians (Reconstructed by Council)
**Location:** Hidden Vaults of Aethelgard
**Status:** Prototype (Restricted Study)

## Concept
The Chrono-Anchor is a machine designed to lock a specific area of space-time into a repeating loop or prevent temporal manipulation in its vicinity. It is the only known countermeasure to temporal displacement weapons.

## Operational Risk
Testing the Chrono-Anchor is extremely dangerous. During a test in 2252, the laboratory at Aethelgard was locked in a 4-second time loop for three weeks before the power grid could be remotely shut down.

## Regulatory Status
The development of any device utilizing Chrono-Anchor principles for time-travel is designated a Galactic Crime under the Time Preservation Treaty, carrying a sentence of life imprisonment in the deep-space detention rings."""
    },
    {
        "id": "tech_void_engine",
        "title": "The Void Engine: Dark Matter Drive",
        "category": "Technologies",
        "classification": "Restricted",
        "content": """# The Void Engine: Dark Matter Drive

**Developer:** Void Syndicate R&D
**Fuel Source:** Dark Matter Crystals
**Status:** Active on Syndicate Smuggling Vessels

## Propulsion Mechanics
Unlike the standard Hyperdrive which enters Hyperspace, the Void Engine rips a tear directly into "The Void" (a dimension of dark energy and non-matter). The engine uses the gravitational pull of the Void to catapult ships forward, achieving speeds 30% faster than standard hyperdrives.

## Smuggling Advantage
Vessels using the Void Engine do not emit standard tachyon signatures, making them invisible to the Galactic Council's border sensors. They can bypass security networks easily.

## Void Exposure
Prolonged use of the Void Engine carries the risk of "Void Seepage", where dark energy leaks into the crew cabins, causing hallucinations, paranoia, and physical mutation. Syndicate crews are required to undergo regular psychic de-contamination."""
    },
    {
        "id": "tech_antimatter_shield",
        "title": "The Antimatter Shield: Deflection Grid",
        "category": "Technologies",
        "classification": "Restricted",
        "content": """# The Antimatter Shield: Deflection Grid

**Developer:** Solar Alliance Research Labs
**Power Source:** Antimatter Core
**Status:** Active on Military Dreadnoughts

## Defensive Mechanism
The Antimatter Shield creates a thin, high-energy barrier of positrons around a starship. When incoming weapons (such as plasma bolts or physical missiles) strike the shield, they undergo immediate matter-antimatter annihilation, neutralizing the threat.

## Heat and Radiation
The annihilation process releases massive bursts of gamma radiation. The ship's hull must be lined with lead-ceramic plating to protect the crew.

## Overload Limits
If the shield is hit by a sustained barrage of high-energy weapons, the shield generator's containment field will begin to degrade. If the containment field fails, the antimatter core will detonate, destroying the ship."""
    },
    {
        "id": "tech_plasma_cannon",
        "title": "The Plasma Cannon: Heavy Ordnance",
        "category": "Technologies",
        "classification": "Public",
        "content": """# The Plasma Cannon: Heavy Ordnance

**Developer:** Xandar Weapon Systems
**Charge Source:** Fusion Cells
**Status:** Active Standard

## Weapon Mechanics
The Plasma Cannon superheats hydrogen gas into a state of high-density plasma (over 50,000°C) and accelerates it down a magnetic rail barrel. The projectile is held together by a localized magnetic bottle until impact, where it burns through armor.

## Ship Integration
Standard military starships carry dual-barrel Plasma Cannons. Orbital stations like Aegis Shield are equipped with giant Class-5 planetary cannons capable of destroying cruisers in a single shot.

## Cooling Down
Firing the cannon generates extreme heat. The weapon has a mandatory cooling cycle of 6 seconds between shots to prevent the magnetic barrel from melting. Over-firing can trigger automatic shutdown locks."""
    },
    {
        "id": "tech_biodome_gen",
        "title": "The Bio-Dome Generator: Atmosphere Creator",
        "category": "Technologies",
        "classification": "Public",
        "content": """# The Bio-Dome Generator: Atmosphere Creator

**Developer:** Horizon Biotech Laboratories
**Operational Mode:** Continuous Atmospheric Filtering
**Status:** Active on Zephyrus-9 and Mars Colony

## Purpose
The Bio-Dome Generator is a terraforming machine that creates a self-sustaining, breathable atmosphere inside a pressurized force-field dome. It is used to establish colonies on toxic or airless worlds.

## How it works
The generator takes ambient gases (such as carbon dioxide or methane) and filters them through a bio-engineered algae core. The core uses artificial solar radiation to perform high-efficiency photosynthesis, releasing oxygen, nitrogen, and water vapor.

## Force Field Tech
The dome's boundary is maintained by a specialized electrostatic force field that allows physical objects (like transport ships) to pass through while keeping the atmospheric gases sealed inside."""
    }
]

# Compile all documents
all_documents = planets_data + stations_data + species_data + factions_data + tech_data

print(f"Generating {len(all_documents)} documents...")

for doc in all_documents:
    filepath = os.path.join(DOCS_DIR, f"{doc['id']}.md")
    metadata = {
        "id": doc["id"],
        "title": doc["title"],
        "category": doc["category"],
        "classification": doc["classification"]
    }
    
    # Write file with metadata block at the top and content below
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(json.dumps(metadata, indent=2))
        f.write("\n---\n\n")
        f.write(doc["content"])

print("All 50 documents generated successfully!")
