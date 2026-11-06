# anvil-demo-target

> ⚠️ **Intentionally vulnerable. Do not deploy.** This repository exists so that
> [A.E.G.I.S. / ANVIL](https://github.com/HarshalAndhale9657/ANVIL) — an autonomous
> discover → exploit → verify → patch security pipeline — has a safe, known-vulnerable
> target to demonstrate against.

**Try it:** open the [live demo](https://github.com/HarshalAndhale9657/ANVIL#live-demo),
connect GitHub, and click **Try the demo target**. ANVIL clones this repo, finds the
planted bugs, launches the app, exploits it, verifies the exploit deterministically,
writes a fix, re-runs the exploit against the patched app, and opens a pull request.
If you don't have write access here (you won't), it forks the repo into your account
and opens the PR **in your fork** — nothing is sent to this repository.

## Seeded vulnerabilities

| # | Class | Location | Trigger |
|---|-------|----------|---------|
| 1 | Insecure deserialization (RCE) | `app.py` `/api/v1/user/preferences` | `pickle.loads()` on the `session_prefs` cookie |
| 2 | Path traversal (arbitrary read) | `app.py` `/files/<filename>` | unsanitized `os.path.join` with `..` |

## Run locally

```bash
pip install -r requirements.txt
python app.py            # serves on http://127.0.0.1:9999
```

## What a correct fix looks like

Replace `pickle` with a signed/JSON format for preferences, and canonicalize + confine
the file path (`os.path.realpath` + `os.path.commonpath`) for `/files`. ANVIL only
counts a patch as valid if the original exploit **no longer succeeds** against the
patched app, and the app still starts.

> Pull requests opened by ANVIL here are left unmerged on purpose, so the demo stays
> exploitable.
