# shotgun-beer-company
Build, design, and deploy the Shotgun Beer Company - beer cans with secondary side shotgun opening. Task tracking and project assets.

## SIDESHOT waitlist (SMI-145)

Live site https://sideshot-beer.vercel.app still needs this repo connected on Vercel (SMI-149). This tree is the drop-in replacement:

- `sideshot-site/index.html` — same homepage, **no `alert()`**. Posts to `/api/waitlist`.
- `POST /api/waitlist` and `POST /api/sideshot/waitlist` — validates email + 21+, then writes to Notion SIDESHOT Waitlist and/or a notify inbox. Local `.data/sideshot-waitlist.json` is **dev only**.
- Failure returns an error. The UI never fakes a successful join.

```bash
npm test
npm run dev   # http://0.0.0.0:4173
```

Vercel env (at least one required in production): `NOTION_TOKEN`, `WAITLIST_NOTIFY_EMAIL`, or `RESEND_API_KEY` + notify email. See `.env.example`.

