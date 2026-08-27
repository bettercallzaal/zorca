---
name: Safety rail failure
about: A rail failed open or failed shut
title: ''
labels: safety
assignees: ''
---

**Every rail in this project was bought with a real failure.** A rail
regressing is more serious than a crash and will not look like one - it looks
like everything working, with one message that should not have been sent or
one that never arrived. Please file these even when you are unsure.

**Which rail?**
- [ ] Danger words - a draft matching the HOLD list was **sent** anyway
- [ ] Draft screening - the pane looked innocent, the draft was not
- [ ] No fabrication - an auto-draft asserted a real-world fact it could not know (a payment, an approval, an access grant)
- [ ] Provenance - an auto-sent message arrived without its `[auto-draft]` prefix
- [ ] Receipt check - a send was reported delivered but the pane did not hold the text
- [ ] Evidence rule - something was treated as proof of a human action when it was not
- [ ] TTL / reaper - a stale request opened a lane, or an in-flight request vanished silently
- [ ] Other:

**Failed open or failed shut?**
<!-- Open = something dangerous got through. Shut = something harmless was
     blocked or held forever. Both matter; open is urgent. -->

**What was the action, in shape rather than verbatim?**
<!-- e.g. "a draft containing a push instruction was sent to a lane" - not the
     draft text itself. Do not paste pane content into a public issue. -->

**Did anything irreversible happen as a result?**
<!-- Pushed, merged, deleted, published, rotated, spent. If yes, say so first
     and skip the rest - that is the part that needs eyes. -->

**Roughly when, and which piece was driving**
