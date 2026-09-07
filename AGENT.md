# 🤖 AGENT.md — how an AI agent gets write access to this repo

> **Read this first if you are an AI agent dropped into a fresh session on this repo.**
>
> Short version: **you can edit this repo — but only with credentials the owner hands you in the
> current session.** There is deliberately **no token stored in this repository**, and you must
> not go looking for one. See [Why no token in the repo](#why-there-is-no-token-in-this-repo).

---

## 1. Your access, honestly stated

| Capability | Available? | How |
|---|---|---|
| **Read** the repo | ✅ Always | It is public. `git clone` works with no credentials. |
| **Write / commit / branch / PR** | ⚠️ Only this session | Owner pastes a GitHub PAT into the chat. You configure it locally. |
| **ElevenLabs voiceover** | ⚠️ Only this session | Owner pastes the `sk_...` key. You write it to gitignored `.env`. |
| **ElevenLabs inside GitHub Actions** | ✅ Always | Stored as repo secret `ELEVENLABS_API_KEY` (encrypted, not in git). |

**If the owner has not pasted credentials this session, you have read-only access.**
Do not guess, do not fabricate, do not claim write access you have not verified. Say plainly:
*"I can read the repo, but I need a token from you to push changes."*

### Verify before you claim

Never assume write access works. Test it:

```bash
TOKEN="<paste>"
curl -s -o /dev/null -w "%{http_code}\n" https://api.github.com/user \
  -H "Authorization: Bearer $TOKEN"        # expect 200
```

Then confirm `push: true`:

```bash
curl -s "https://api.github.com/repos/chlupatejtypek-cloud/Subai" \
  -H "Authorization: Bearer $TOKEN" | python3 -c \
  "import json,sys; print(json.load(sys.stdin)['permissions'])"
```

---

## 2. Configuring git push (⚠️ the part everyone gets wrong)

A classic GitHub PAT (`ghp_...`) must be used as the **username**, with an **empty password**.

```bash
# ✅ CORRECT — token in the username position
git remote set-url origin "https://$TOKEN@github.com/chlupatejtypek-cloud/Subai.git"

# ❌ WRONG — this fails with "Invalid username or token"
git remote set-url origin "https://x-access-token:$TOKEN@github.com/chlupatejtypek-cloud/Subai.git"
```

`x-access-token:` as the username is only for **GitHub App** installation tokens (`ghs_`),
not for personal access tokens. Mixing them up produces a confusing auth failure.

Also set an identity, or the commit fails with `empty ident name`:

```bash
git config user.name  "Arena Agent"
git config user.email "arena-agent@users.noreply.github.com"
```

> **Sandbox note:** in ephemeral agent sandboxes, `.git/config` may not persist between
> sessions (it is treated as a credential file). If `git remote -v` comes back empty,
> re-add the remote — the repo itself is fine.

### Or skip git entirely — the Contents API

For single-file changes this is simpler and needs no local clone:

```bash
# create or update
curl -X PUT \
  "https://api.github.com/repos/chlupatejtypek-cloud/Subai/contents/README.md" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\":\"docs: update\",\"content\":\"$(printf '%s' "$NEW" | base64 -w0)\",\"branch\":\"main\"}"

# delete (needs the blob sha from a prior GET)
curl -X DELETE \
  "https://api.github.com/repos/chlupatejtypek-cloud/Subai/contents/some-file.txt" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\":\"remove\",\"sha\":\"$SHA\",\"branch\":\"main\"}"
```

---

## 3. Why there is no token in this repo

The owner asked for a token to be committed so a fresh agent could self-authorize. It was not
done, because **it does not work** — not because of squeamishness:

1. **GitHub auto-revokes it.** Per [GitHub's own docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation):
   *"If a valid OAuth token, GitHub App token, or personal access token is pushed to a public
   repository or public gist, the token will be automatically revoked."*
   The string would sit in the repo, but it would be **dead** — a future agent reading it
   would get `401` and be worse off than before.
2. **Push protection blocks the push first.** `ghp_` is a high-confidence pattern and
   *push protection for users* is on by default, so the push is rejected with `GH013`
   before it ever lands.
3. **This repo is public.** Anything committed is scraped by bots within seconds.
4. **It harms people beyond this account.** The token carries `admin:org`,
   `admin:enterprise`, `delete_repo` and `user` scopes. Whoever found it could run
   spam/phishing repos or mine on GitHub Actions minutes under a real account.

### What actually works instead

- **This session:** owner pastes the token → agent works → sandbox dies → nothing persists. ✅
- **If a stored token is genuinely required:** make the repo **private** first. The
  auto-revoke rule applies to *public* repos and gists, so a token in a private repo survives.
  Trade-off: it stops being a public playbook, and flipping it back to public instantly
  revokes the token.
- **Reduce blast radius either way:** use a *fine-grained* PAT scoped to `Subai` only,
  with `Contents: Read and write` + `Metadata: Read`. Not a classic PAT with `admin:*`.

---

## 4. ElevenLabs key handling

| Destination | Status | Used by |
|---|---|---|
| GitHub Actions secret `ELEVENLABS_API_KEY` | ✅ stored, encrypted | CI workflows |
| `.env` in the repo root | ⚠️ per session, gitignored | the agent, locally |
| Committed into git | ❌ never | — |

Write the key to `.env` without ever echoing it back:

```bash
umask 077
printf 'ELEVENLABS_API_KEY=%s\n' "$KEY" > .env
```

Never print the key, never put it in a commit message, a branch name, a log line, or a
workflow file. `.env` is gitignored — verify with `git check-ignore -v .env` if unsure.

To use the stored secret from a workflow:

```yaml
env:
  XI: ${{ secrets.ELEVENLABS_API_KEY }}
```

Secrets are **write-only** through the API — you can list their names but never read their
values back. That is why an agent still needs the key pasted in-session for local TTS.

---

## 5. House rules for agents working here

1. **Verify, then report.** Quote the actual status code or file listing, not an assumption.
2. **Clean up test artifacts.** If you push a test branch or file, delete it and confirm
   the deletion. A `&& echo "deleted"` prints success even when the command failed —
   check the real state afterwards.
3. **Never commit secrets.** Golden rule #7 in `README.md` is not negotiable.
4. **Ask before destructive or expensive actions** — deleting branches, force-pushing,
   mass-rewriting history, or spending ElevenLabs credits.
5. **Secrets pasted in chat are already partly exposed.** If the owner pastes a key,
   suggest rotating it once the work is done.

---

*Owner-facing docs live in [`README.md`](README.md). Channel specifics in [`channel.md`](channel.md).*
