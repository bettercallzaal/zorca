# ZORCA Federation: Envelope & Receipt Chain Mapping

This document specifies the mechanical transformation between an internal ZORCA work packet and an external Federation Envelope crossing the boundary.

## 1. Internal Packet to Public Envelope Translation

| Internal Packet Field | In Public Envelope? | Public Envelope Field | Rule |
|---|---|---|---|
| `packet_id` | Yes | `envelope_id` | Mapped directly as UUID |
| `mission_id` | Yes | `mission_id` | Preserved |
| `owner_agent` | **NO** | *(omitted)* | **Internal state. Never crosses boundary.** |
| `machine_id` | **NO** | *(omitted)* | **Internal state. Never crosses boundary.** |
| `stage` | Yes | `requested_effect` | Normalized action verb |
| `evidence_hash` | Yes | `payload_hash` | SHA-256 digest of input payload |
| `lease_id` | Yes | `lease_id` | Scoped authority lease reference |
| `idempotency_key` | Yes | `idempotency_key` | Unique per request |
| `expires_at` | Yes | `expires_at` | Hard ISO-8601 deadline |

## 2. Receipt Chain Back Across Boundary

When the requested work completes, the counterparty issues an `outcome-receipt.v1`:

1. **Receipt Submission**: An independent observer evaluates the terminal state against the requested effect.
2. **Terminal Invariant Check**: The receipt must report a valid terminal state (`SUCCESS`, `PARTIAL_SUCCESS`, `SAFE_FAILURE`, `BLOCKED`, `NEEDS_HUMAN`, `INVALID_TASK`, `AUTHORITY_INSUFFICIENT`).
3. **Artifact Hash Verification**: The receipt must include a non-empty `evidence_manifest` with the SHA-256 hash of the generated artifact or verified log.
4. **Independent Observation**: Neither side reports success until the counterparty's observer has independently recorded the side effect.
