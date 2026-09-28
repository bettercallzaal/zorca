# ZORCA Federation Boundary

> **STATUS: DRAFT SPEC, NOT LIVE, NOT YET THE ZAO'S IDENTITY.** Merged on 2026-09-27 as a draft, by Zaal's ruling ("Merge as a draft spec"). Nothing in this directory is read, served, signed or sent by any code. Before any of it is switched on:
> 1. **The signing key.** `capability-card.json` names an Ed25519 public key (`kid: zao-fed-key-2026`) as The ZAO's federation identity. Nobody on the ZAO side has confirmed who generated it or holds the private half. Generate and hold the key on the ZAO side, or confirm its provenance, before anything is signed with it.
> 2. **The contract.** `docs/REPO-LAYOUT.md` says no envelope is specified until the partner's public federation contract and receipt format have been read. Confirm which published contract these schemas match, with a link, before treating them as the real one.
> 3. **The payout address.** `recipient_address` is the zero address, a placeholder.
> The federation canary comes after the foundation is clean.

This directory defines the public federation contract between external systems (such as DreamNet) and The ZAO's internal orchestration layer (ZORCA / Orca).

## The Core Rule

> **Normalize at the boundary, preserve each system's internal ontology behind it.**

- A partner asks *"who can perform capability X"* and never learns which internal agent, tmux pane, machine, or script executes it.
- **Owner-agent and machine do NOT cross the boundary.**
- The payload hash crosses; the internal working trees and private configs do not.
- **Completion Criterion:** Neither side can report success unless the other side can independently observe the intended state change. No internal repo access in either direction.

## Boundary Structure

| Path | Purpose |
|---|---|
| `capability-card.json` | Public declaration of civilization identity, supported protocols, public keys, advertised capabilities, proof rules, and payment rails. |
| `envelope.md` | Mapping specification from internal work packet to public envelope and receipt chain back. |
| `schemas/outcome-receipt.v1.schema.json` | Strict JSON schema for independent verification receipts (exit codes, SHA-256 evidence digests). |
| `schemas/authority-lease.v1.schema.json` | Bounded authority lease schema (`subject/office + resource + action + effect + expiry`). |
| `schemas/capability-card.v1.schema.json` | Schema validator for capability cards. |
| `schemas/dreamloop-manifest.v1.schema.json` | Engine-agnostic portable action manifest for the 59 skills. |
