# LEAP Project


A group project run alongside the LEAP training programme. Teams design and build a
trading platform themselves, using whatever technology each week has just taught them, and
manage it as a real agile project: their own architecture, their own backlog, their own customer.

The technical brief is the business requirements spec issued at kickoff, in
[`kickoff/`](kickoff). It describes what the platform must do and says nothing about how to
build it, the architecture, the technology, the division of work into services, all of that is
for each team to propose and defend themselves.

This folder is Friday-by-Friday guidance for instructors: what a team might
usefully do with their weekly project time given what's just been taught, and what to ask them to
present back to the class. Teams can spend their project time however they judge best, this is a
sensible default, not a checklist to enforce.

## Structure

Each `<name>week-readme.md` file corresponds to one week of the programme. Files are named for
what that week teaches, not for its position in the sequence, so the table below is the single
source of truth for ordering - if the curriculum order changes again, only this table needs
updating, not the filenames. Kickoff's materials are in [`kickoff/`](kickoff), the one folder
that remains, since they're slide decks and the spec document rather than a guidance readme.

| Week | File | Taught focus | Capstone deliverable |
|---|---|---|---|
| 1 | [`kickoff/`](kickoff) | Foundations: Git, ways of working & GenAI | Kickoff day: candidate architecture, project plan, risk list |
| 2 | [`pipelinesweek-readme.md`](pipelinesweek-readme.md) | Pipelines: CI/CD deep dive, Docker multi-stage builds, IaC, OWASP, Secure Code Warrior | none, backlog and customer engagement |
| 2 | [`dataweek-readme.md`](dataweek-readme.md) | Data Systems: Postgres, SQL, modelling, NoSQL (parallel track alongside Pipelines) | Trade database schema |
| 3 | [`javaweek-readme.md`](javaweek-readme.md) | Java, OOAD, UML, SOLID, TDD | Domain engine |
| 4 | [`springweek-readme.md`](springweek-readme.md) | Spring Boot, REST, OpenAPI, MyBatis, JWT | Trade REST API |
| 5 | [`angularweek-readme.md`](angularweek-readme.md) | HTML/CSS, Angular | Trading UI |
| 6 | [`nodeweek-readme.md`](nodeweek-readme.md) | IAM/zero trust, JS/TypeScript, Node, NestJS | Auth service |
| 7 | [`pythonweek-readme.md`](pythonweek-readme.md) | Python, pandas, EDA, APIs, ETL | Analytics dashboard and ETL pipeline |
| 8 | [`kafkaweek-readme.md`](kafkaweek-readme.md) | Kafka, event-driven architecture, refactoring, DevSecOps | Event backbone |
| 9 | [`projectweek-readme.md`](projectweek-readme.md) | none, applied project week | Close the gap against the spec, optional BR-18 extension |
| 10 | [`cloudweek-readme.md`](cloudweek-readme.md) | AWS, deployment automation | Cloud deployment and final showcase |

Weeks 1 and 10 are presentation-heavy in a different way to the rest: Week 1's kickoff is
presented to a stakeholder panel, and Week 10's is the final programme showcase. The weeks in
between are internal weekly check-ins to the rest of the class.

**A note on sequencing**: this table reflects the curriculum's current order, which has changed
at least once (earlier material had Python running in week 4 and Java in week 5, for example -
the reverse of today's order). Each individual `<name>week-readme.md` file's own content -
especially references to "last week" or a specific earlier deliverable - was written against
whichever order was current at the time, and may need review against its new neighbours in this
table. See the note in each file's Context section where this matters.
