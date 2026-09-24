# ZORCA Federation Boundary

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
