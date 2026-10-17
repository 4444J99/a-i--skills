# Domain Ontology — Voodoo (Vodou / Vodun / Vodoun)

**Stratum:** 1 (Ontology)
**Domain:** Voodoo / Vodou (Haitian) / Vodun (West African) — schema validator
**Created:** 2026-04-25
**Status:** Schema-stable; outlier validator

## Question

What is the domain made of?

## Boundary statement (positioned first because of ethical floor)

This ontology is for the **scholar-practitioner-respectful study** of Vodou / Vodun. It is NOT a guide to practice. The schema's existence here is to validate DIWS as generative across radically dissimilar domains — not to extract or trivialize a living religion.

## Entities

| Canonical name | Variants | Definition | Boundary case |
|---|---|---|---|
| Lwa | loa, lwa-yo (Haitian Creole plural) | Spiritual entities in the Vodou pantheon | Lwa are NOT gods in monotheistic-comparison sense; not analogous to Greek pantheon |
| Houngan | priest (male) | Male Vodou priest | Distinct from mambo (female priest); both are clergy |
| Mambo | priestess (female) | Female Vodou priestess | Distinct from houngan; coequal authority |
| Hounfour | temple, peristyle | Vodou temple / ceremonial space | Distinct from "church" — different liturgical structure |
| Service | rite, ceremony | A specific ceremonial event for specific lwa | Distinct from "Mass" — Service IS the liturgy |
| Possession | mounting, divine inhabitation | Lwa inhabits practitioner during ritual | Distinct from "spirit possession" Western framing — context-bound religious phenomenon |
| Vèvè | sacred symbol, ritual diagram | Geometric symbol for specific lwa | Functional in ritual (NOT decorative) |
| Initiation | kanzo, lave-tèt | Formal entry into Vodou priesthood | Multiple stages exist; lifelong commitment |
| Asson | ritual rattle | Sacred instrument used by initiated houngan/mambo | Symbol of initiation; not an instrument anyone holds |
| Practitioner-scholar | scholar-practitioner | Person who is both academic researcher AND initiated practitioner | Crucial role for ethical study; non-practitioner scholar has different access |

## Relations

| Relation | Source → Target | Semantics | Cardinality |
|---|---|---|---|
| serves | Houngan/Mambo → Lwa | Priest serves specific lwa via specific service | N:M |
| identifies | Vèvè → Lwa | Symbol denotes specific lwa | 1:1 |
| performs | Service → Ceremony-of-lwa | Ritual event for specific spirit | N:M |
| inhabits | Lwa → Practitioner (during possession) | Spiritual phenomenon during specific rituals | 1:1 momentary |
| transmits | Initiated-practitioner → Initiate | Passing of priesthood through ceremony | 1:N over career |

## Primitives

- **Lwa** — atomic unit of the pantheon
- **Service** — atomic unit of ritual
- **Vèvè** — atomic unit of symbolic vocabulary
- **Initiation level** — atomic unit of religious authority

## Canonical vocabulary

- **Vodou** (capitalized — Haitian; preferred over "Voodoo" in scholarly contexts)
- **Vodun** (capitalized — West African origin; broader)
- **Houngan / Mambo** (capitalized as titles)
- **Lwa** (capitalized; Haitian Creole)
- **Hounfour** (capitalized; ceremonial space)
- **Vèvè** (with grave accent; specific spelling matters)

## Boundary cases — what's NOT this domain

- **Pop-culture "voodoo"** (zombie movies, voodoo dolls, Harlequin Hollywood) — adjacent extractive-stereotype domain; NOT this domain
- **New Orleans Voodoo as commercial-tourism** — adjacent; some legitimate practice exists; much is performance
- **Generic syncretic spiritualism** — adjacent; not Vodou specifically
- **Brazilian Candomblé / Cuban Santería** — adjacent African-diaspora religions with overlapping pantheons; distinct traditions
- **Wicca / contemporary witchcraft** — adjacent; entirely separate religious development

## Authoritative sources

- *Mama Lola: A Vodou Priestess in Brooklyn* (Karen McCarthy Brown) — foundational ethnography
- *The Spirits and the Law: Vodou and Power in Haiti* (Kate Ramsey) — historical / legal scholarship
- *Sacred Arts of Haitian Vodou* (Donald Cosentino, ed.) — visual/material culture canon
- *The Drum and the Hoe* (Harold Courlander) — early ethnography, period-bounded
- *Tell My Horse* (Zora Neale Hurston) — primary source ethnography 1937 (with caveats)
- Houngan-scholar primary sources where available (e.g., Houngan Aboudja's writings)

## Validation gate

A fresh agent reading this file alone can answer "what is X in this Vodou domain?" with the explicit understanding that this is **scholar-respectful study**, not practitioner instruction.

## Anti-extraction note

This stratum exists to demonstrate that DIWS can describe an ethically-sensitive domain *with appropriate respect built in*. The substrate skill's value is precisely that it makes the ethical floor explicit rather than implicit. See `domain-contribution-charter.md` for the heavy Stratum 8 work that follows.

## Changelog

- 2026-04-25 — initial fill (outlier validator for DIWS schema; respectful design-only)
