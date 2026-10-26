# Claude skill bundle

skills/ contains the 3 default-on skills that every session lists: closeout, skill-catalog, voice-enforcement. skills-catalog/ contains complete copies of the other 165 catalog skills, indexed in CATALOG.md and loaded on demand through the skill-catalog skill. Membership and its admission rule are authored under default_on in config/runtime-catalog.json. Plugin packages remain intact under ../../plugins in the release root so their shared resources, agents, and source descriptors remain available.

Install and update using scripts/skills_install.py from the repository root.
