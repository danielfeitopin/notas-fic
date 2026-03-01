<!--
SPDX-FileCopyrightText: 2026 Daniel Feito-Pin <danielfeitopin+github@protonmail.com>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Project governance

This document describes how decisions are made in the project, who can make them, and how anyone can participate in the community.

## Goals

- Maintain a free and open source project that is open, transparent, and inclusive.
- Encourage collaboration between maintainers, contributors, and users.
- Clearly document how conflicts are resolved and how technical decisions are made.

## Roles

### Contributors

Anyone who opens issues, submits pull requests, or participates in discussions is considered a **contributor**.

Responsibilities:

- Propose improvements and fixes through issues or pull requests.
- Respect the project’s Code of Conduct.
- Participate constructively in reviews and discussions.

Rights:

- Have their contributions reviewed carefully and in good faith.
- Propose new features and changes to the roadmap.

### Maintainers

**Maintainers** are contributors with write access who are responsible for the technical direction of the project.

Responsibilities:

- Review and merge pull requests.
- Publish new releases of the project.
- Ensure compliance with the Code of Conduct.
- Keep documentation up to date (including this file).

How to become a maintainer:

- Have contributed consistently and respectfully over a reasonable period (for example, at least 3–6 months).
- Be nominated by an existing maintainer.
- Obtain rough consensus from the other maintainers (no well-founded objections).

### Leadership team

The project is coordinated by a **leadership team** (one or more lead maintainers).

Additional responsibilities:

- Help resolve conflicts.
- Lead high-level design decisions.
- Represent the project publicly (for example, at conferences or in official communications).

The leadership team is reviewed periodically (for example, once a year) and may rotate to avoid concentration of power.

## Decision making

- For small changes (bug fixes, minor documentation improvements), a maintainer can decide after at least one review.
- For significant changes (public API, licenses, core architecture), a discussion issue is opened and labeled `governance` or `design`.
- The project seeks **rough consensus**:
  - If there are no reasoned objections within an agreed period (for example, 7–14 days), the proposal is accepted.
  - If there is disagreement, the proposal is iterated on to incorporate feedback.
  - If disagreement persists, the leadership team decides and documents the decision and rationale.

All important decisions must be recorded in public issues or pull requests.

## Conflicts and Code of Conduct

The project is governed by a `CODE_OF_CONDUCT.md` published in the repository.

- Anyone can report Code of Conduct violations publicly (issue) or privately (email to the leadership team).
- The leadership team evaluates the situation, may ask the involved parties for context, and proposes proportional measures (warnings, moderation of channels, up to banning in severe cases).
- Decisions related to the Code of Conduct are documented in a way that preserves, as much as possible, the privacy of the people involved.

## Transparency

- Key decisions (license, governance model, major architecture changes) are documented in this file or in dedicated documentation sections.
- Coordination meetings, if they exist, should publish an accessible summary (for example, in a `meetings/` directory or the wiki).

## Changes to this document

- Anyone can propose changes to this `GOVERNANCE.md` via a pull request.
- Changes to this document are considered significant changes and require:
  - Review by at least two maintainers.
  - Rough consensus among active maintainers.
- The “last updated” date must be kept current.

Last updated: 2026-03-01
