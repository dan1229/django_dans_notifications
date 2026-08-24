# TODO - Django Dan's Notifications
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

-------------------------------------------------------
## [Unreleased]
-----





-----
### 1.4.0



#### add `metadata` field to base notification model
- add a field to the base notification model that can store extra data
- e.g.,:
    - `metadata = JSONField(blank=True, null=True)`
    - this will allow users to store extra data in the notification
    - e.g.,:
        - `{"meeting_id": "1234", "meeting_time": "2024-01-01 12:00:00"}`
-
- add to serializers and api docs



#### notification models - add more fields
- how to allow user to add extras fields?



---




#### notification basic api 'recipients' field
- only taking 1 recipient as a string - is this valid?
- if so add more docs - i.e., add docstrings to apis and stuff



#### email api - post api
- create and send emails via api
    - need some way for user to set the permissions for it
        - allowall, isauth or any class


#### install the standard release workflow
- there is no `.github/workflows/detect-version.yml` here at all - releasing means opening
  the Actions tab and running `release.yml` by hand
    - the empty-body half of this is already closed (2026-08-23): `release.yml` was reading
      `body` from `github.event.head_commit.message` and `commit` from
      `github.event.pull_request.head.sha`, neither of which exists on a
      `workflow_dispatch` run, so every release shipped blank. It now extracts the version's
      section out of `CHANGELOG.md` - the same awk the standard uses - and fails on a
      missing or empty section *before* the PyPI upload rather than after. What is left
      here is the trigger, not the notes
- the standard makes the release a commit: a `release: [X.X.X]` subject on main tags the
  repo, cuts a `release/X.X.X` marker branch, and creates the release with notes read out
  of `CHANGELOG.md` at that SHA
- keep `release.yml` and wire it as the downstream dispatch so PyPI publishing still runs.
  It is `workflow_dispatch`, not `on: push: tags:`, so it will not stop firing once CI
  pushes the tag
- turn ON the version-source check using the **`setup.cfg`** variant - the version lives
  there, not in `pyproject.toml`
- tags stay bare (`1.3.1`, not `v1.3.1`) - all 32 existing tags are bare
- `docs/release.md` still describes the run-it-from-the-Actions-tab flow and has to be
  rewritten in the same change, or it contradicts the workflow the day it lands
- `/dan:release-setup` installs it




### [1.5.0] - 2026-MM-DD
- TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
