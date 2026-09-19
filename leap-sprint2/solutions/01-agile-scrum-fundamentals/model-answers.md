# Module 01 Lab — Model Answers (Instructor Reference)

## Readiness assessment

| Item | Ready? | Reason |
|---|---|---|
| PS-101 View recent transactions | Ready | Clear value, has acceptance criteria, small and testable |
| PS-102 Make the app better | Not ready | Fails Valuable (not a specific value) and Testable, no way to know when it's "done" |
| PS-103 Export transactions to CSV | Ready | Clear value, has acceptance criteria including a scale requirement |
| PS-104 Biometric login | Not ready | Fails Testable and Estimable, missing acceptance criteria (which biometric methods, fallback behaviour, error states) |
| PS-105 Rebuild the entire app | Not ready | Fails Small, this is an epic or initiative, not a sprint-sized story |
| PS-106 Set a spending alert | Ready | Clear value, has acceptance criteria, appropriately scoped |
| PS-107 Dark mode | Not ready | Fails Testable, missing acceptance criteria (which screens, does it follow system setting, is there a manual toggle) |
| PS-108 Freeze a lost or stolen card | Ready | Clear value, has acceptance criteria, includes a measurable requirement (5 seconds) |
| PS-109 Improve performance | Not ready | Fails Valuable and Testable in its current form, "faster" isn't measurable without a target |
| PS-110 Multi-currency support | Not ready | Fails Small and Independent, explicitly depends on undecided market scope and legal review, this is an epic |

## Example acceptance criteria for PS-104 (Biometric login)

- User can enable biometric login from Settings, off by default
- If biometric authentication is available on the device, the login screen offers it as an
  alternative to password entry
- If biometric authentication fails three times, the user is returned to standard password
  login
- If the device has no biometric hardware, the option is hidden entirely, not shown disabled

## Example acceptance criteria for PS-107 (Dark mode)

- App offers a Light / Dark / System Default setting under Settings > Appearance
- When set to System Default, the app follows the device's current light/dark setting
- All screens (not just the home screen) respect the selected mode
- Text contrast in dark mode meets the same accessibility contrast ratio as light mode

## The outlier

**PS-105 (Rebuild the entire app)** is the clearest example: it's a multi-month technical
initiative written in story format, but has no acceptance criteria because none would make
sense at this size, "done" for a full rewrite isn't a single sprint's work. Treating it as an
ordinary backlog item would either get it perpetually deprioritised against smaller, clearer
stories, or it would get pulled into a sprint and blow the sprint goal entirely. It needs to be
broken down into an epic with its own smaller, INVEST-compliant stories before it belongs in
sprint planning at all.

**PS-110 (Multi-currency support)** is a secondary example worth discussing if a team finds it:
it names its own unresolved dependencies (market scope, legal review) inside the story
description itself, a strong signal it isn't independent or small enough yet.
