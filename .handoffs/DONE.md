# DONE - zorca-bridge-design (task_a6082d860006)

Design only. Nothing built, nothing pushed.

## Deliverables

| Path | What |
|---|---|
| `docs/DESIGN-bridge.md` | The design, v3, 638 lines. Live plan is **section 12**; section 8 is marked superseded. |
| `README.md` | One row pointing at the design. |
| `.handoffs/DONE.md` | This file. |

Commits, all unpushed (`push` is gated):
`7e2da31` v1 - `efc1b98` v2 - `6a35646` GUI port finding -
`c1fa815` appendix A, both branches - `<this commit>` v3, ratified bridge.

## What v3 settles

- **q4 answered:** ZOE v2 on OpenMatter, VPS warm as fallback. This confirms
  **branch A** and closes section 11's open question.
- **q5 dissolved, not measured:** the webhook removes the Telegram-retention
  dependency entirely. Correct shape of answer for an unverified fact.
- **Transport ratified:** webhook to the VPS, queue file, Mac polls.

## Three things the coordinator should not let pass silently

**1. Stage 1 as literally specified cannot run today. Measured:**

```
$ tailscale status          -> Tailscale is stopped.
$ lsof -nP -iTCP:22 -sTCP:LISTEN  -> nothing listening on 22
```

The spec says the VPS writes the queue file *on the Mac over SSH* and that
the *Mac keeps zero inbound ports*. Those cannot both hold - an inbound ssh
is an inbound port - and today there is neither a route nor a listener.

**Fix is one word: invert the direction.** Queue file lives on the **VPS**;
the Mac **SSHes outbound** and drains it. Webhook, queue file, SSH, polling
orchestrator, sleep-safe queue - all of Zaal's design survives. Only who
dials changes, and this variant needs zero inbound ports literally and works
today with no Tailscale and no Remote Login. Section 12.1. Stage 1 is
written against it. VPS-to-Mac push stays available at the stated cost.

**2. One webhook URL per bot token.** OpenMatter and the VPS cannot both
receive `@zaoclaw_bot` updates. "Warm fallback" is therefore not passive
standby - failover needs a health check plus an explicit `setWebhook`
repoint, and a decision on who may fire it. Section 12.4.

**3. A webhook does not reduce metered cost if OpenMatter bills by container
uptime** - the container must be up to receive. Derived ~0.837 Cr/hr against
~12 Cr is under a day of runway. Measure the billing model before cutover,
not at the balance. Same section.

## Still Zaal's, not started

- Whether to accept the inverted SSH direction or pay for VPS-to-Mac push.
- Whether the newsletter-beta grant is the right budget for lane control.
- `zorca-gui2` landed on 7778 beside 7777 mid-write with an identical write
  surface. The actuator must read its port from config, and two live GUIs
  raise a double-actuator question. Not this lane's file to change.
