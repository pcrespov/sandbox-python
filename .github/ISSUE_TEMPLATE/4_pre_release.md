---
name: 🚀 Pre-release to staging (developers-only)
about: Creates an issue to pre-release from master to staging deploy (includes hotfixes)
title: '🚀 Pre-release master -> staging_SPRINTNAME_VERSION (DATE)'
labels: 'release'
assignees: 'pcrespov'
---

In preparation for [pre-release](https://github.com/ITISFoundation/osparc-simcore/releases). Here an initial (incomplete) list of tasks to prepare before pre-releasing:


- [ ] Draft changelog from commits list (see [docs/releasing-workflow-instructions.md](https://github.com/ITISFoundation/osparc-simcore/blob/6cae77e5444f825f67fca65876922c8d26901fd2/docs/releasing-workflow-instructions.md))
- [ ] Check important changes 🚨
- [ ] Devops check (⚠️ devops)
- [ ] e2e testing check
- [ ] Pre-release summary
- [ ] Pre-release assessment

---

<!-- Staging is an intermediate environment between development (master) and production that allows us to test in isolation
changes in the framework. In addition, the pre-release workflow shall be used as a simulation to production that can help us to
anticipate changes and mitigate failures.

Explain what motivates this pre-release? Which important changes we might pay attention to? How should we
test them? Is there anything in particular we should monitor?

TIPs:

- Start this section with a *motivation*
- Mark commits with 🚨 to warn about possible issues. Contact PR creator to understand how to test/target
- It is preferable that pre-releases should address the outcome of a single sprint at a time. This might be done by pre-releasing to
staging just after the sprint review, and then hotfix staging all fixes to staging that have been solved during the subsequent sprint.
Mark all the commits that were cherry picked for a hotfix as [ 📌  ``staging_switzer_5``]

-->



#  Devops check (⚠️ devops)
<!-- The goal here is to analyze the PRs marked with (⚠️ devops).  We should determine and prepare necessary changes required in the environments configs.

This procedure should be taken also as an exercise in preparation for the release to production as well.
 -->


# e2e testing check
<!-- Check that e2e in master: are there any major known issues?

Keep an agenda of what has been reported on every daily
-->
- Mon. ...
- Tue.
- Wed.
- Thu.
- Fri.

TODO: create FORM to fill this and move to osparc-simcore repository!

info:
- sprint-name
- version
- git SHA
and some TODO check steps
- e2e status?
then
- auto-generates ``make release-staging name=switzer version=2 git_sha=dbcc9a645f25468ed57d227c42e8daad6ccb62d8``


- make sure master head commit has built (i.e. CI ✅ )
  - check e2e
  - manual check master deploy
  - copy sha
- make url to pre-release . USE git_sha !!
  - auto-generate changelog -> trigger
  - manual review
    - add prefixes and icons
    - mark issues to target-test e.g. 🚨
    - mark hotfixes to production  e.g. [ 📌  ``staging_switzer_5``]
  - edit with new changes
- check pre-release CI ✅
- check it deploys (all)
- run e2e & p2e  ✅
- announce in https://mattermost.speag.com/z43/channels/osparc-maintenance-announcements channel
- close case





# Pre-release summary

- what:  <!-- ```make release-staging name=switzer version=2 git_sha=dbcc9a645f25468ed57d227c42e8daad6ccb62d8``` -->
- who: <!-- @Surfict @GitHK  -->
- when: <!-- THURSDAY Oct.20, afternoon -->



# Pre-release assessment

<!-- How did the release go? Any incidents, problems, difficulties, unexpected issues, ... during the release process?
Notes on special warnings or configurations we should pay attention ... or in general any relevant information that helps us
mitigate the risk of failure when releasing to production
-->
