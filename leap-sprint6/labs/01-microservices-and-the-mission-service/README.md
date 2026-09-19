# Module 1 Lab — Microservices & the Mission Service

## Objectives

By the end of this lab you will have:

- Discussed microservice principles, benefits, and trade-offs against a monolith
- Sketched, informally, how the Sprint 5 Order Processing & Settlement Engine could become a
  service boundary

## Setup

- Your Sprint 5 mission build (Modules 7-13), for reference
- `../../shared/mission-brief.md` (this sprint's brief)
- `worksheet-template.md` from this lab
- A partner

## Task

This is a **15-minute whiteboard exercise, not a formal design.** Don't aim for a finished
architecture diagram — aim for enough of a sketch to motivate the rest of the sprint.

In pairs, working from your Sprint 5 `OrderProcessingEngine` and this sprint's mission brief,
answer:

1. **What comes in over the wire?** What does an incoming HTTP request need to contain for the
   service to process one order? (Hint: compare to what `IncomingOrder` held in Sprint 5.)

2. **What goes out?** What should the service's response look like — for an accepted order? For
   a rejected one?

3. **What does the service need to talk to, that Sprint 5 didn't?** (Hint: look at the mission
   brief's "Changes" section.)

4. **What stays entirely internal, never exposed over the boundary?** Which Sprint 5 classes
   should nobody outside this service ever need to know exist?

## Deliverable

A filled-in `worksheet-template.md` — sketches, bullet points, or a rough diagram are all fine.
Keep it; Module 4 will turn this into a real REST API design.

## Acceptance criteria

There's no automated check for this module — the artefact is the worksheet itself. A strong
worksheet:

- Names specific fields an incoming order needs (not just "the order data")
- Distinguishes an accepted-order response from a rejected-order response
- Identifies at least two things Sprint 5 didn't need that Sprint 6 does (persistence, auth)
- Names at least one Sprint 5 class that should stay entirely internal
