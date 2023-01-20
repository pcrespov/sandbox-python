---
name: 🚀 Release to production  (developers-only)
about: Creates an issue to release from staging to production
title: '🚀 Release vX.X.0'
labels: 'release'
assignees: 'pcrespov'

---

In preparation for [release](https://github.com/ITISFoundation/osparc-simcore/releases). Here an initial (incomplete) list of tasks to prepare before releasing:


- [ ] Prepare staging
- [ ] Check changelog 🚨
- [ ] Check devops ⚠️
- [ ] Test assessment: e2e-testing
- [ ] Test assessment: targeted-testing
- [ ] Test assessment: user-testing ✅
- [ ] Release summary
- [ ] Release assessment

---

# Prepare staging
<!--
- Pre-release and hotfix until stable
- Keep "motivation" as concrete as possible
- ...
-->

# Check changelog 🚨
<!--
- draft changelogs accumulated from staging
- human-readable highlights (optional)
-->


# Check devops ⚠️
<!-- review and prepare (⚠️ devops)
	- assess whether announcement necessary (e.g. logout?)
	- assess when is the most comfortable time to do release
-->

# Test assessment: e2e-testing
 <!-- Assessment carried out by batman/robin based on e2e daily tests outcome
 -->

# Test assessment: targeted-testing ✅
 <!-- Assessment carried out app-team on changelog **at least** on items marked with 🚨. Then replace with ✅ -->


# Test assessment: user-testing
 <!-- save all record zoom session  ``filesrv/osparc/DEVELOPERS/test-sessions`` and
 create an issue to follow up on them. Add issue here!
 -->


# Release summary

- what:  <!-- ```make release-prod version=MAJ.MIN.0 git_sha=SHA_OF_THE_WANTED_STAGING_RELEASE``` -->
- who: <!-- @Surfict @GitHK  -->
- when: <!-- THURSDAY Oct.20, afternoon -->


# Release assessment

<!-- How did the release go? Any incidents, problems, difficulties, unexpected issues, ... during the release process?
Notes on special warnings or configurations we should pay attention ... or in general any relevant information that helps us
mitigate the risk of failure when releasing to production
-->