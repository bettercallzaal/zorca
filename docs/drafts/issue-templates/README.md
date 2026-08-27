# Issue templates - DRAFT, not placed

Drafted 2026-08-27. **Content only.** These are not live: GitHub reads issue
templates from `.github/ISSUE_TEMPLATE/`, and this repo has no `.github/`
directory at all.

**Placement is Zaal's call and is deliberately not made here.** Moving these
into `.github/ISSUE_TEMPLATE/` is what turns them on, for a public repo, in
the issue composer every visitor sees. That is a publishing decision, not a
file move, so it is left to him. Nothing here changes repo behaviour where it
sits.

To place them, as-is:

```
mkdir -p .github/ISSUE_TEMPLATE
git mv docs/drafts/issue-templates/*.md .github/ISSUE_TEMPLATE/
rm .github/ISSUE_TEMPLATE/README.md   # this file does not belong there
```

`config.yml` sets `blank_issues_enabled` and is the one file that changes
behaviour beyond offering a form - review it before placing.

## The three, and why these three

| File | For |
|---|---|
| `bug_report.md` | Something in `orca-board`, `zorca-actuator`, the GUI or `repo-cleanup` did the wrong thing. |
| `safety_rail.md` | **The one that matters most here.** A rail failed open or failed shut: a dangerous draft was sent, a harmless one was held forever, an auto-draft asserted something it could not know, or a lane was reported briefed when it was not. ZORCA's rails were each bought with a real failure; a rail regressing is more serious than a crash, and it will not look like a crash. |
| `feature_request.md` | Everything else. |

## One deliberate omission

None of these asks for logs, config or pane text to be pasted in. `orca-board`
transcribes real pane content, and `zorca-actuator` config carries a queue
host and path. On a public repo an issue body is world-readable forever, so
each template asks for the **shape** of what happened and offers a private
route for anything else. A template that invites a log paste is a template
that will eventually collect a hostname or a token.

This is a generic hygiene choice and does **not** depend on the open
disclosure question in `../../DESIGN-bridge.md` section 14 / open question 7.
Nothing here restates or resolves that field.
