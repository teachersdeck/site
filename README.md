# suite
TeachersDeck Suite
# TeachersDeck — v0.9.7

TeachersDeck, a classroom-management app, built plain HTML/CSS/JS so it can run
either as a normal web page or as a Chrome new-tab extension with no rewrite.

The current version number lives in several places, kept in sync by hand:
`js/app.js` (`const APP_VERSION = '...'`, shown at the bottom of the Settings
drawer), `manifest.json` (`"version"`, used by Chrome), this file's title, and
`manual.html` (its header and footer). Bump them together and add a line under
**Version history** below whenever you ship a change. Then run
`python3 tools/release.py` — it checks that every place agrees, refreshes
`RELEASES.md`, and writes the build as `teachersdeck-v<version>.zip`. Every
shipped zip carries its version in its name.

## Version history
- **v0.9.7** — **Actual bug fix**, found from a screenshot of the Theme drawer:
  "Upload a school / company logo" was still visible even though it correctly
  carries `hidden` in `index.html` and `ENTERPRISE_FEATURES` is `false`.
  Cause: `.upload-row{ display:flex; ... }` in `css/style.css` is an author
  rule, and author rules always beat the browser's built-in `[hidden]`
  styling regardless of specificity — so `.upload-row` was rendering despite
  the `hidden` attribute. Every *other* hideable piece in this file
  (`.drawer[hidden]`, `.edge-dock[hidden]`, `.pro-modal-backdrop[hidden]`,
  etc.) already has its own explicit `[hidden]{ display:none; }` override for
  exactly this reason — `.upload-row` was just missing its copy of that
  pattern. Added `.upload-row[hidden]{ display:none; }`; no JS or markup
  changes needed, and the flip-`ENTERPRISE_FEATURES`-to-re-enable path noted
  in `js/app.js` still works the same way once this fix is in.
- **v0.9.6** — Verified the school/company logo upload is fully enterprise-gated
  (asked to confirm it "won't appear unless flagged for enterprise use"): it
  already was — `ENTERPRISE_FEATURES = false` in `js/app.js` plus a static
  `hidden` attribute on the upload row in `index.html`, so it's inert
  regardless of Pro status. What wasn't consistent: the Pro upgrade modal's
  feature list (`plan_pro_f4`) and several spots in `manual.html`/`README.md`
  still advertised the logo as something a Pro purchase unlocks. Fixed all of
  those so Pro's description, the manual, and the README's overview sections
  now match what's actually gated — logo is enterprise-only, not Pro.
- **v0.9.5** — **Release-time obfuscation, and export watermarking tied to license keys.**
  `tools/release.py --obfuscate` now shells out to `npx terser` then
  `npx javascript-obfuscator` on `js/app.js`, `js/cloud.js`, and
  `js/lesson-template.js` and packs the result as a second
  `teachersdeck-v<version>-obfuscated.zip`, for the **standalone web-page**
  channel only — the Chrome Web Store's Developer Program Policies prohibit
  obfuscated code in submitted extensions, so keep uploading the plain zip
  there regardless. Separately, every Pro-only export that produces a file a
  teacher could pass along — right now, the Lesson Planner's Word download —
  now carries a 6-character token in the file's own metadata (Word's
  Keywords field, never in the visible plan), derived from the license key
  and device that made it (`exportWatermarkToken`/`watermarkHash` in
  `js/app.js`). It's not copy protection, just traceability: paste a token
  found in a leaked file into `admin/license-admin.html`'s new "Trace a
  watermark" panel and it's matched back to the key + device by recomputing
  the same hash over every loaded license, entirely in the browser.
- **v0.9.4** — **Real, server-bound Pro licensing, and a distributable license admin panel.**
  Licensing moves from a pure client-side checksum to a small Cloud
  Functions backend (new `license-backend/` folder — source only, needs
  deploying into `trifecta-firebase-backend`, see its README) that binds
  each key to one device: the first device to activate a key claims it,
  and a second, different device trying the same key is rejected. The
  app re-checks its license with the server once a day
  (`recheckLicenseIfNeeded` in `js/app.js`) so a Voided key gets
  deactivated without the teacher doing anything, and falls back
  gracefully offline for up to 7 days before failing closed. Also
  swapped `isPro()`/`PRO_WIDGET_IDS` back from the testing-mode
  everything-unlocked override to the real Free/Pro split (25 widgets +
  background/logo/drawer customization behind Pro) — this is the actual
  live gate now, not a placeholder. `admin/license-admin.html` (issue
  keys with a name/email/amount/method attached, list every key's
  status, void one) now lives inside the project, with its sidebar
  restructured as a dropdown-selectable set of sections (one section,
  "Licensing," today — built so a future admin section can be added
  without restructuring the layout). `tools/generate-key-batch.js` and
  `tools/seed-licenses.js` let you pre-mint a batch of keys offline and
  load them into Firestore once the backend is deployed; the first
  batch of 20 (unassigned, format `TDPRO-XXXX-XXXX-XXXX`) shipped
  alongside this release as `TeachersDeck-Pro-License-Keys.docx`.
- **v0.9.3** — **Fix for "I switched Google accounts and the class codes
  disappeared."** Cloud Class remembers which class is linked
  (`state.cloudClassId`) per browser profile, independent of which Google
  account is signed in — by design, so re-opening the app as the *same*
  teacher doesn't lose the link. But switching to a *different* Google
  account left it pointed at a class that account doesn't own; Firestore
  correctly rejected the read, and the widget just showed a blank codes
  panel instead of explaining why. It now detects that (a class it can't
  read under the current account) and falls back to the create/pick-a-class
  screen with a toast explaining what happened, instead of going blank.
  Two separate, unrelated things worth knowing if you hit this while
  testing: (1) StudentDeck's "join with class code" needs the **student**
  code specifically — the parent code (also shown here) will be rejected;
  (2) a class created under one Google account is only ever usable by that
  same account signing back in, by design — there's no "wrong account, let
  me in anyway" override, since ownership is exactly what
  `firestore.rules` checks.
- **v0.9.2** — **Fix for the "student shows up twice" report:** the actual
  duplicate-creation logic lives in the `joinClassAsStudent` Cloud Function
  (in the separate trifecta-firebase-backend package, not in this zip) — by
  design, StudentDeck's "🚪 Join with class code" always creates a **new**
  `students/` record, while "🔑 I have a PIN" resumes an existing one. A
  student who re-joins with the class code instead of their PIN — easy to
  do, since nothing warned them — legitimately ends up with two records
  under the same name. Two things landed here to address it: (1) the Cloud
  Class roster now flags any two students sharing a name with a ⚠️
  "possible duplicate" badge, and gives the teacher a 🗑️ button to remove a
  stray record on the spot (`TDCloud.removeStudent()`, a direct Firestore
  delete — needs a `students/{id}` delete rule scoped to the class owner in
  firestore.rules if one isn't there yet); (2) StudentDeck's join tab (see
  its own changelog) now tells a student to use their PIN instead if
  they've joined before, to stop new duplicates from happening. The
  Cloud Function itself is unchanged — send over trifecta-firebase-backend
  if you'd like the join flow itself to detect/reuse a matching name
  automatically.
- **v0.9.1** — **Combines v0.9.0's Assignments widget with v0.8.5's emoji
  polish pass** (merged from two parallel updates — nothing else changed
  beyond the two below).
- **v0.9.0** — **Assignments widget, and the Calendar is now canonical.**
  New Assignments widget: create/edit/delete assignments (title, subject, due
  date/time, points, instructions). Saving one auto-mirrors a linked event
  into the Calendar widget (📘 badge) so a due date only has to be set once —
  the Calendar is now the one place all dates in the deck show up, including
  assignment due dates. `cloud.js` gained `syncHomework()` (same one-way,
  diff-and-batch pattern as `syncCalendar()`), pushing assignments to
  `classes/{id}/homework` whenever a linked Cloud Class is active — this is
  what StudentDeck's Homework To-Do widget and ParentDeck's new Homework
  widget read from. Requires `classes/{id}/homework/*` to be covered by the
  same ownership/read rules as `calendarEvents/*` in firestore.rules.
- **v0.8.5** — **Visual polish pass:** every widget in the dock now has an
  emoji alongside its name (📅 Calendar, 🏆 Scoreboard, ☁️ Cloud Class, and
  so on for all 30+ widgets), and the Cloud Class panel's own labels,
  buttons, and empty states got the same treatment (🔑 sign in, 🎁 rewards,
  ⭐ points, 🗑️ delete, etc.). Purely cosmetic — no behavior changed.
- **v0.8.4** — **Name Picker is back, and Cloud Class can feed it names.**
  Name Picker (random-call-on-a-student) was accidentally left out of the
  widget registry since v0.5.0 despite its code still being in the app —
  it's now a real widget again (dock/drawer placement is automatic on
  first load, like any newly-added widget). It draws from the same
  per-class-pill "Class list" as Attendance, Group Maker and Hall Pass
  (Settings → Class list), unchanged. Cloud Class's roster panel now has a
  "↻ Copy names to Class list" button: one click copies every cloud-joined
  student's display name into that local Class list (case-insensitive
  de-duped, additive only — never removes a name you typed in by hand that
  hasn't joined the cloud class yet), so students who join with the class
  code show up in Name Picker/Attendance/Group Maker/Hall Pass without
  retyping the roster. One-way (cloud → local) since local names are plain
  strings with no cloud account behind them.
- **v0.8.3** — **Cloud Class: demerit points and quick-pick reasons.** The
  roster's plain "reason" text box now sits behind a "Quick reason…"
  dropdown grouped into 🙂 **Merit** (Participation +1, Helping a classmate
  +2, Kindness +2, Great work +5) and 🙁 **Demerit** (Late −1, Talking −1,
  Not listening −1, Not participating −1, Fighting −5). Picking one awards
  that exact point value (positive or negative) to the student immediately
  — no separate +5/−5 click needed. "✏️ Custom reason…" reveals the old free-
  text box, which still works with the +5/−5 buttons exactly as before.
  Demerits use the same `awardPoints` Cloud Function as merits (it already
  accepted any signed integer); this only changes the TeachersDeck UI, not
  the backend. The preset list is `MERIT_REASONS`/`DEMERIT_REASONS` near
  `renderCloudClass` in `js/app.js` — add, remove, or re-point entries there
  (each needs a `cc_reason_<key>` string in `STRINGS` for its label).
- **v0.8.2** — `js/firebase-config.js` now carries a live project config
  (project `teachersdeck-b5720`). This file isn't a secret — a Firebase
  web `apiKey` only identifies which project to talk to; it's Firestore
  security rules and Cloud Functions' own auth checks (both already
  deployed as of the backend's v1.1.1) that actually gate access, the same
  as any Firebase web app. No code changes.
- **v0.8.1** — **Bug fix found during a cross-app dataflow audit:** the very
  first "Sign in with Google" in a session was calling `ensureUserProfile`
  (which sets the `role: 'teacher'` custom claim server-side) but never
  refreshing the client's cached ID token afterwards — so the next call
  that needed that claim (e.g. "Create a cloud class") could fail with
  `permission-denied` until the token happened to refresh on its own (up to
  ~an hour). `js/cloud.js`'s `signIn()` now force-refreshes the token right
  after `ensureUserProfile` resolves, before returning. Same bug, same fix,
  in ParentDeck's `js/data.js`.
- **v0.8.0** — **Cloud Class: real Firebase sync with StudentDeck & ParentDeck.**
  New "Cloud Class" widget (`js/cloud.js`, entirely optional — see
  `js/firebase-config.js`): Google sign-in, create/pick a class, show and
  regenerate the student/parent join codes, a live roster with per-student
  +5/−5 point buttons (backed by the `awardPoints` Cloud Function), a
  rewards-catalog editor, and a ranking-visibility setting. The local
  Calendar widget now mirrors its events up to the class's cloud calendar
  automatically whenever they change (`saveState()` → `TDCloud.syncCalendar`)
  — that's what lets StudentDeck and ParentDeck see a teacher's calendar.
  Fully additive: with no Firebase project configured, the widget just shows
  a setup message and every other widget behaves exactly as in v0.7.2. See
  the trifecta-firebase-backend package for what's on the other end of this.
- **v0.7.2** — **Versioned release zips and a release log.** No change to the
  app itself. From this version on every build is a zip named
  `teachersdeck-v<version>.zip` (it still unzips to a folder called
  `teachersdeck/`), and each version is tracked in `RELEASES.md`.
  - **`tools/release.py`** (Python 3, standard library only) is the one step
    that produces a release: it reads the version from `js/app.js`,
    `manifest.json`, this README's title and both spots in `manual.html`, stops
    if any disagree, checks this history has an entry for that version at the
    top, refreshes `RELEASES.md`, and builds the zip (`--check` only verifies;
    `--date`, `--out`, `--force` are there for the odd case). It refuses to
    overwrite a zip of the same version unless told to, so a version number
    keeps meaning one exact set of files.
  - **`RELEASES.md`** is a table of every version in this history with its
    release date and zip file name, plus a one-line summary taken from the
    entry below. Versions before this one show dashes for date and zip —
    they shipped before the log existed and nobody recorded them.
  - The old note here said the version lived in two places; the manual added
    two more, and the checker now knows about all of them.
  - **Why a version bump with no app change:** the new zip contains files the
    old one didn't (`tools/`, `RELEASES.md`), and a version number has to
    identify one exact build.
- **v0.7.1** — **Fixed: a widget's minimise and close buttons could be
  unreachable.** Reported on the Lesson Planner; it could hit any widget, but
  the Planner is the biggest (330×610) so it overlaps the others most.
  - **Root cause — a regression from v0.6.9's drag fix.** That release stopped
    re-appending a panel to the DOM to bring it forward and used a z-index
    counter instead, but only panels that had been *clicked* got a z-index. A
    freshly opened widget had none, so it opened **underneath** any panel that
    had already been clicked — and where it overlapped one, clicks on its
    title-bar buttons landed on the panel above. Reproduced in Chromium:
    Calendar clicked (z 12), Planner opened over it → close/minimise
    unreachable (`elementFromPoint` returned the Calendar).
  - `openWidget()` now calls `bringToFront()` on the new panel, so a newly
    opened widget is on top, as it was before v0.6.9.
  - `bringToFront()` no longer bumps the counter when the panel is already the
    front-most one — clicking into a form (the Planner has many fields) used to
    inflate `topZ` on every click.
  - Note this is ordinary stacking, not a bug: a panel that is genuinely
    covered by another still can't be clicked through — click any visible part
    of it to bring it forward first. Stack order isn't saved across reloads
    (open order applies), same as before.
  - Verified in Chromium with real mouse clicks: five overlapping widgets,
    minimise/restore/close on the Planner, reopening it lands on top, z-index
    doesn't climb under repeated clicks, and dragging, resizing and the
    Planner's Word/Docs/calendar flows all still pass.
- **v0.7.0** — **Lesson Planner widget** (Pro; the 31st widget). Fill in a
  lesson once, then open your Universal Lesson Planner document in Word or
  Google Docs and put the lesson on the calendar.
  - **Fields**: topic, date, start time, length (min), calendar reminder,
    teacher, subject, grade/class (prefilled once from the open class's name),
    plus two collapsible sections — objectives + materials, and minutes for
    each of the template's five phases (with a running total). The draft lives
    in `state.lessonPlanner`, so it is per class like everything else, and
    autosaves as you type.
  - **Open in Word** builds a filled copy of the user's template and
    downloads it (`Lesson Plan - <topic> - <date>.docx`). **A web page cannot
    launch desktop Word**, so the file lands in Downloads to be opened from
    there — that is the honest ceiling for a page with no backend.
    `lpFillDocXml()` patches `word/document.xml` of the embedded template by
    matching its exact placeholder text: the six `Label: ______` header lines,
    the two `[Click here to type objectives/materials...]` paragraphs (one
    paragraph per typed line), and the five `____ min` cells. Blank fields keep
    their underscores/placeholders so they can still be handwritten. Formatting
    is the template's own, so the result paginates identically to the blank.
  - **Open in Google Docs** copies the same plan to the clipboard as an HTML
    table layout (`text/html` + `text/plain`, with a legacy `execCommand`
    fallback) and opens `docs.google.com/document/create?title=…`; the teacher
    pastes with Ctrl/Cmd+V. If the clipboard is refused the toast says so and
    points at Word-then-upload-to-Drive. Pushing a file straight into someone's
    Drive would need a Google sign-in (OAuth client ID) this app doesn't have —
    the obvious upgrade if it's ever wanted.
  - **Save to calendar** writes a Calendar-widget event (`lesson:true`): title
    `Lesson: <topic> — <class>` (clipped to the calendar's 60-char limit), date,
    time (all-day if no start time), length, reminder, and a notes summary.
    The event id is kept in the draft, so saving again **updates** that event
    rather than duplicating; the status line under the buttons shows where it
    sits and turns amber when the form has drifted from what's saved. A topic
    is required for the calendar (never for opening the document). "Also save to
    the calendar" (default on) makes both Open buttons do it too.
  - **New lesson** clears topic/content/pacing/date but keeps teacher, subject,
    class, start time, length and reminder.
  - **Calendar changes** this needed: events may carry an optional `duration`
    (minutes) that `buildGoogleCalUrl()` now uses instead of a fixed hour; the
    Calendar widget listens for a `td:calendar-changed` document event and
    redraws when another widget adds events (skipped while its edit form is
    open); and **a latent bug fixed** — event title/notes were interpolated
    unescaped into the edit form's markup, so text like `</textarea>` in a note
    broke it (now `escHtml()`).
  - **Toasts** now wrap in a `max-width:min(440px,92vw)` column; the old
    shrink-to-fit made long messages a narrow half-screen strip.
  - **New files**: `js/lesson-template.js` (the template as base64, so it works
    when `index.html` is opened from a folder — a `fetch()` there would be
    blocked, the same limit the Games widget has) and `js/jszip.min.js`
    (JSZip 3.10.2, dual MIT/GPL-3.0 — used under MIT; the licence header is
    intact in the file). To swap the template: replace the .docx, regenerate
    the base64, and if the placeholder wording changed update `lpFillDocXml()`.
  - **Registered as Pro**, added to the commented-out intended-split list above
    `PRO_WIDGET_IDS` (now 26 widgets) — like the others it is unlocked while
    testing mode is on and must be re-locked before any sale. New widgets land
    in the app tray (dock placement `hidden`); assign one in Settings → Dock
    buttons.
  - **Verified** in headless Chromium: generated .docx passes the OOXML schema
    validator against the original, renders in LibreOffice identical to the
    template with values filled, and special characters (`& < > $& $1`) come out
    intact and well-formed; the same build works from `file://`; clipboard
    holds HTML + plain text and the Docs tab opens on the titled create URL;
    calendar save/update/no-duplicate/stale-status/live-refresh, Google Calendar
    link length, per-class isolation, persistence across reload, Vietnamese
    labels, zero console errors. **Not verified**: how the live Google Docs
    editor renders the pasted tables (needs a signed-in Google session), and
    opening the file in desktop Word itself (LibreOffice stood in).
- **v0.6.9** — **Fixed widget dragging.** Reported symptom: a panel moves a
  pixel or two and then stops. Reproduced in headless Chromium — with a real
  mouse drag the panel didn't move *at all*.
  - **Root cause**: `makeDraggable()`'s `pointerdown` handler called
    `wall.appendChild(el)` to bring the panel to the front. `el` is already in
    `wall`, so that removes and re-inserts the node — and per the Pointer
    Events spec, re-inserting the element that holds the pointer capture
    releases the capture and fires `pointercancel`, which ran the drag's own
    `end()` on the first move. Whatever pixels landed before that arrived were
    the "moves a little bit".
  - Panels are now brought forward with a **z-index counter** (`topZ` /
    `bringToFront()`) — no DOM move, so nothing disturbs the capture. Clicking
    anywhere on a panel also raises it.
  - The **whole title bar** drags, not just the 20px grip (the grip stays as
    the visual affordance); the minimise/close buttons are excluded so they
    still click. `.widget-head` got `cursor:grab` / `:active` grabbing and
    `touch-action:none`.
  - Drag and resize now share **one window-level gesture tracker** (`gesture`,
    `startGesture/moveGesture/endGesture`) rather than per-widget `pointermove`
    listeners, so a lost capture can't strand a drag and closing a widget can't
    leave handlers behind. `blur` ends a gesture too.
  - Positions are read from `offsetLeft/offsetTop` (wall-relative, the same
    frame the saved `left/top` are written in) instead of
    `getBoundingClientRect()`, which was viewport-relative.
  - Panels are **clamped to the wall**: never past the top or left edge, and
    always at least ~150×44px on screen at the right/bottom, so a panel shoved
    off the edge can still be grabbed by its grip and dragged back.
  - The **resize corner** was nearly invisible at 14px/0.35 opacity — now 18px,
    0.4 opacity, full opacity on hover, `touch-action:none`.
  - Verified in Chromium: drag by grip / title / bar, resize, values persisted
    to `state.layout` and surviving reload, clamping and recovery from
    off-screen, z-order stacking with two panels, minimise/close still
    clickable, body inputs still usable, touch-pointer drag, and no leftover
    handlers after repeated open/close — zero console errors.
- **v0.6.8** — Added `manual.html`, a teacher-facing instruction manual that
  ships in the project root next to this README. Self-contained single HTML
  file (no build step, no external assets beyond the same Google Fonts link
  the app uses, and it degrades to system fonts offline), styled with the
  app's own palette and using the real widget icons pulled from `ICONS` in
  `js/app.js`. Covers: the three install routes (double-click, Chrome
  "Load unpacked" new-tab extension, local web server) and what each one
  costs you, a tour of the docks/tray/panels, classes, theme + layout +
  language settings, all 30 widgets one by one (what it's for, how to drive
  it, and its real limits — mic needs a secure context, YouTube opens in a
  tab, currency rates are fixed not live, built-in games need http(s)),
  Free vs Pro and the licence box, where the data lives and what erases it,
  and a troubleshooting section. Two things it states plainly rather than
  papering over: this build is unlocked for testing, and the "Settings →
  Class list" editor that Attendance / Group Maker / Hall Pass point at
  doesn't exist yet (the orphaned Name Picker roster UI), so those three run
  on the shipped sample list. **Keep it in sync** with the app the same way
  as this README when widgets or settings change. Version bumped in
  `js/app.js`, `manifest.json` and the manual's own header (it reads
  `APP_VERSION` at build time from `build_manual.py`-style generation — in
  practice, just edit the two places it appears in `manual.html`).
- **v0.6.7** — **Classes.** A teacher with several classes a day can now keep one
  deck per class and switch between them from the top bar.
  - **Class pill** (`#class-pill-wrap` in the header, registered in `PILLS` as
    id `classes`) shows the class that's open; clicking it drops a menu listing
    every class plus "Manage classes…". Like the language and theme pills it can
    sit in the top pill row or be hidden, from Settings → Top bar pills
    (`pill-place-classes`).
  - **Settings → Classes** (first section, `#classes-section`): rename any class
    inline, "Open" to switch to it, × to delete it, a name box + **Create & open**
    to add one, and **Copy this class** to clone the current deck (same widgets,
    layout and theme) for a second section.
  - **What's per class:** everything in `state` — roster, which widgets are open
    and where, layout mode, dock/drawer placement, theme + background image,
    checklist, scoreboard, attendance, agenda, poll, announcements, language,
    date system. **Shared across classes** (one teacher, one browser): the
    IndexedDB media library (files, games, music, videos, sounds), the school
    logo, and the Pro license.
  - **Storage:** a new index key `td_classes_v1` = `{active, list:[{id,name}]}`.
    The existing `ww_state_v1` key is now simply class one — **anyone upgrading
    keeps their current deck untouched and finds it as their first class**.
    Classes added afterwards live in `ww_state_v1::<id>`. Background images are
    per class too (`background` for the first class, `background::<id>` after),
    via the `state.activeBgId` field that already existed.
  - **Switching reloads the page** on purpose (`switchClass()` saves the class
    you're leaving, points the index at the new one, then `location.reload()`),
    so every widget re-initialises from its own state instead of hot-swapping
    4,000 lines of live UI. Deleting the class you're in opens the next one;
    deleting any other class doesn't reload. The last remaining class can't be
    deleted. Cap of `MAX_CLASSES = 12`.
  - "Reset everything" now clears every class's state and the index, not just
    the open one.
  - **Not Pro-gated** — that's a pricing call, not a code one. To make multiple
    classes a Pro feature later, gate `addClass()` and the "Create & open" /
    "Copy this class" buttons on `isPro()`, the same way the background/logo
    uploads are.
  - Verified in Chromium (Playwright): create, rename, switch, copy, delete
    (active and non-active), last-class guard, per-class roster/theme/open-widgets
    isolation, per-class background images kept separately in IndexedDB, pill
    moved between header and pill row (menu flips side and stays on screen),
    pill hidden/shown, menu closes on outside click and Escape, labels follow the
    language switch, and state surviving a plain reload — zero console errors.
- **v0.6.6** — Background upload now always changes the background. Reported
  symptom: after v0.6.5, picking a background image showed "Couldn't save that
  image — try a smaller file…" and the background never changed. Reproduced in a
  real headless Chromium: it is **not** about file size (a fresh profile accepted
  a 36 MB PNG). The failure happens when storage is unavailable — e.g. the app
  running inside a sandboxed/embedded preview (no IndexedDB/localStorage; that
  reproduces the exact toast) — and, separately, a stale tab from an older build
  holding the DB open makes the v1→v2 upgrade hang with no message. Changes:
  - The chosen image is now painted **immediately from the picked file**, same
    single-slot loader as before (id `'background'`, `center/cover no-repeat`,
    no gallery). Saving to IndexedDB happens afterwards, best-effort, with a 6 s
    timeout. If it can't be saved the background still stays for the session and
    a new `bg_not_saved` toast says it won't survive a reload (instead of
    aborting the change).
  - `saveState()` no longer throws when localStorage is blocked, so theme presets,
    the dim toggle and everything else that calls it keep working in a sandboxed
    preview (before, the throw skipped whatever ran after it).
  - `idb.open()` releases its connection on `versionchange`, so an open tab can no
    longer block a future DB upgrade.
  - If `state.customBg` is set but the saved image can't be read, the layer falls
    back to the selected theme instead of staying blank.
  - `bg_upload_failed` (still used by the logo upload) reworded — it blamed file
    size, which was never the cause — and error toasts stay up 5 s instead of
    2.2 s. `toast(msg, ms)` takes an optional duration.
  - **Deliberately kept the IndexedDB version at 2.** Reverting to `open(..., 1)`
    would throw `VersionError` in any browser that already opened v2 and break
    every widget that uses IndexedDB (Files, Games, Music, Video, Soundboard).
  - Verified in Chromium (Playwright): fresh profile (small, 23 MB JPG, 36 MB PNG,
    persists across reload, preset switch clears it); sandboxed iframe (image
    applies, "won't be remembered" toast, dim/preset still work); stale v1 tab
    holding the DB (image applies at once, toast after 6 s, works again after
    the stale tab closes).
- **v0.6.5** — Reverted v0.6.4's background gallery UI back to a single-slot
  loader (upload replaces the one custom background again, no "Your
  backgrounds" swatch grid, no per-image remove button). Removed
  `buildCustomBgGrid()`/`genBgId()`, the `#theme-custom-bgs` grid and
  `.swatch-wrap`/`.swatch-remove` CSS, and the now-unused `your_backgrounds`/
  `remove_bg`/`bg_removed` i18n keys. **Kept** the actual v0.6.4 bug fix,
  since reverting that would silently reintroduce the original problem:
  `idb.open()` is still on DB version 2 (not back to the hardcoded 1 that
  caused uploads to fail forever for anyone whose local DB predated the
  `images` store), and both upload handlers still try/catch and show
  `bg_upload_failed` on a real failure instead of doing nothing. A saved
  state from v0.6.4 (which had a `customBgList` array) is migrated on load —
  whichever background was last active becomes the one single background
  again, and the list field is dropped. Verified with a headless jsdom +
  fake-indexeddb smoke test across three starting states (fresh install,
  pre-v0.6.4 legacy, v0.6.4 gallery state): upload correctly overwrites
  rather than appending in all three, with zero thrown errors.
- **v0.6.4** — Fixed background-image upload and added a background gallery:
  - **Root-cause fix**: `idb.open()` hardcoded `indexedDB.open('TeachersDeck', 1)` even as
    object stores (`images`, `games`, `music`, `videos`, `sounds`) were added over several
    versions. `onupgradeneeded` only fires when the requested version is *higher* than
    whatever's already on disk, so a browser profile whose "TeachersDeck" DB was first
    created before a given store existed would silently be missing it forever — any
    `idb.put()`/`idb.get()` against that store then rejects, and since the old upload
    handlers didn't catch that rejection, nothing visibly happened. Bumped the DB version
    to 2, which forces the (already idempotent, `contains()`-guarded) store-creation logic
    to run once for everyone. Also added an explicit rejection when `indexedDB` itself is
    undefined (e.g. some sandboxed/embedded browsing contexts), and `req.onblocked`/`req.onerror`
    now reject with a real error instead of the raw event.
  - **Visible failure instead of silent failure**: both the background and logo upload
    handlers now wrap `idb.put()` in try/catch and show a `bg_upload_failed` toast on
    failure (with a hint to try a different browser/window if testing from an embedded
    preview), instead of just doing nothing.
  - **Background gallery**: uploading a background no longer overwrites the previous one.
    Each upload gets its own id (`genBgId()`) and is appended to `state.customBgList`;
    the theme drawer now shows a "Your backgrounds" swatch grid (`#theme-custom-bgs`,
    built by `buildCustomBgGrid()`) below the upload row so any previously uploaded image
    can be clicked back into use, each with a small × to remove it. Removing the active
    one falls back to the next saved custom background, or to the preset swatches if none
    are left. Existing single-background users (old `state.customBg === true` shape) are
    migrated automatically — their one image becomes the first gallery entry, nothing is
    lost.
  - Verified with a headless jsdom + fake-indexeddb smoke test: fresh-install upload,
    legacy single-background migration, a second upload alongside the first, and removal
    — all run with zero thrown errors. As always, that's not a substitute for clicking
    through it in a real browser.
- **v0.6.3** — Extended v0.5.0's testing-mode unlock to cover Pro features
  outside the widget list. `PRO_WIDGET_IDS` being emptied only unlocks
  widgets gated through `isProWidget()`; it does nothing for the three
  Pro features gated directly on `isPro()` — custom background photo,
  custom school logo, and left/right drawer customization. `isPro()` is
  now temporarily forced to `true`, so those are unlocked too, with the
  real check commented directly above it, same as the existing
  `PRO_WIDGET_IDS` pattern. **Full list of what's unlocked for testing and
  needs re-locking before shipping:**
  - 25 Pro widgets: Traffic Light, Dice, Checklist, Scoreboard, Poll, Noise
    Meter, Music Player, Video Player, Soundboard, Games (the original 10),
    plus Wave 1's 15 — Attendance Tracker, Group Maker, Exit Ticket, Agenda
    Board, QR Code Generator, Days-Until Countdown, Hall Pass Tracker,
    Reading Timer & Log, Text-to-Speech Reader, Unit Converter,
    Announcements Board, Instructions Display, Conversation Starter Cards,
    Idiom of the Day, Grammar Quick-Reference.
  - 3 license-gated features: custom background photo, custom school logo,
    left/right drawer customization.
  - To re-lock everything before a real release: swap `PRO_WIDGET_IDS`
    back to its commented full list (in the comment block just above its
    declaration), and swap `isPro()` back to its commented real
    implementation (checking `state.license.pro`) directly above it.
- **v0.6.2** — Moved the app-tray line onto the dock itself: `#app-tray-tab`
  and `#dock` are now both inside a single `.dock-wrap` container, with the
  tab as a flush flex child sitting directly on the dock's top edge
  (`margin-bottom:-1px` so the borders merge) instead of a separately
  fixed-positioned element with a gap above the dock. Centering and the
  bottom offset moved from `.dock` to `.dock-wrap`; `.dock` itself is no
  longer `position:fixed`. The hover-collapsible slide-down animation is
  unaffected — it's a transform on `.dock` alone, so the tab stays put
  exactly where it was while the dock tucks away beneath it.
- **v0.6.1** — Two fixes/tweaks to v0.6.0's layout modes and app tray:
  - **Side dock cap enforced.** `ensureDockPlacement()`'s first-run migration
    used to split every non-bottom widget 50/50 into the left/right drawers
    with no regard for `DOCK_CAPS` (5 each) — with 30 widgets registered,
    that meant 10+ widgets could land in a single 5-slot drawer. It now fills
    the bottom dock to its own cap first, then alternates into left/right up
    to their 5-widget caps, sending any further overflow to `'hidden'`
    (still reachable via the app tray). `widgetsFor()` also now defensively
    slices to `DOCK_CAPS[loc]` at render time, so anyone whose saved state
    already had more than 5 in a side drawer sees it corrected immediately
    without needing to reset anything.
  - **App tray tab redesign.** The up-arrow above the bottom dock is now a
    plain horizontal line (`.app-tray-tab-line`), matching the drag-handle
    bar used to close the tray sheet itself, instead of a chevron that
    flipped on open/close.
- **v0.6.0** — Layout modes + app tray:
  - **App tray**: a small arrow tab now sits just above the bottom dock.
    Tapping it slides up an Android-style bottom sheet listing *every*
    widget (`#app-tray-grid`, built by `buildAppTray()`), regardless of its
    dock placement — the one guaranteed way to reach a widget whose drawer
    is currently hidden. Click a tile to open/close that widget, same as any
    dock button; click the handle, click outside the sheet, or press Escape
    to close it.
  - **Layout modes** (`state.layoutMode`, `LAYOUT_MODES` in `js/app.js`): a
    new "Layout mode" picker at the top of the Settings drawer offers three
    presets:
    - *Compact* — only the bottom dock is shown (left/right drawers forced
      off); use the app tray arrow to reach everything else.
    - *Comfortable* — bottom, left and right docks are all forced on (the
      previous default multi-dock look).
    - *Custom* — hands control back to the existing per-widget "Dock
      buttons" placement list and the "Show left/right drawer" toggles,
      which are greyed out and disabled while Compact/Comfortable is active
      (a small note explains they're set by the layout mode above).
    Switching modes only changes which docks are *visible* — it never
    touches a widget's saved dock assignment (`state.dockPlacement`), so
    flipping back to Custom restores exactly what was set before.
  - Existing saves (no `layoutMode` in their state yet) migrate to *Custom*
    so nobody's current left/right drawer setup changes on upgrade; brand
    new installs default to *Comfortable*.
  - The "Show left drawer" / "Show right drawer" toggles from v0.5 and
    earlier are unchanged in behavior — they now simply only take effect in
    Custom mode.
- **v0.5.0** — Wave 1 of the widget roadmap: 15 new widgets, all registered as Pro
  (Attendance Tracker, Group Maker, Exit Ticket, Agenda Board, QR Code Generator,
  Days-Until Countdown, Hall Pass Tracker, Reading Timer & Log, Text-to-Speech
  Reader, Unit Converter, Announcements Board, Instructions Display, Conversation
  Starter Cards, Idiom of the Day, and Grammar Quick-Reference). All are
  local-only, following the existing storage/i18n/toast conventions in
  `js/app.js`.
  - **QR Code Generator** vendors `qrcode-generator` v2.0.4 by Kazuhiko Arase
    (MIT license) as `js/qrcode-lib.js`, loaded before `js/app.js` — the QR is
    built and rendered as an SVG entirely on-device, no network call.
  - **Unit Converter**'s currency mode uses a small fixed rate table
    (`UC_CURRENCY` in `js/app.js`) rather than a live feed, since this app has
    no backend — it's clearly labeled as an approximate, not-live rate and is
    meant for rough classroom estimates, not real transactions. Update the
    table by hand if the rates drift too far.
  - **Instructions Display** ships text-only steps for now — the roadmap's
    "optional image per step" is a follow-up, not included in this pass.
  - **Testing mode**: `PRO_WIDGET_IDS` is temporarily set to `[]` so every
    widget (the 10 pre-existing Pro ones and all 15 new Wave 1 widgets) is
    unlocked for trying out. The full intended list is left commented
    directly above it in `js/app.js` — swap the two lines back once Wave 1
    has been tested, to re-lock everything behind Pro.
  - Verified with a headless smoke test (jsdom): all 30 widgets — old and
    new — open, run their setup, and close without throwing, and a handful
    of interactions were exercised directly (attendance toggle, group
    shuffle, QR generation, countdown date, hall pass send/return, reading
    log entry, unit conversion, posting an announcement, adding an
    instruction step, cycling conversation cards/idioms/grammar topics, exit
    ticket tally, agenda field, TTS invocation). This is not the same as
    clicking through it by hand in a real browser — do that pass before
    relying on it in a classroom.
- **v0.4.7** — Debugged the whole app end-to-end (served the project with a
  real local web server and checked every href/src/fetch path against actual
  files — all resolved with no 404s). The Classroom Word Wheel → Scoreboard
  score hand-off (`td_scoreboard_transfer` in localStorage) was confirmed
  working correctly when the project is served as real files and the app
  tab is open. The most likely real-world cause of a "404 on click": built-in
  games (fetched from `games/games.json`) only work when TeachersDeck is
  served as actual files (a local web server or the Chrome extension) — they
  can't work from the single-file published artifact link, and a game
  uploaded standalone through the Games widget's own picker loses its
  sibling files (e.g. instructions.html) since it only carries the one
  uploaded file. Hardened against this either way: clicking a built-in
  game tile or its "?" instructions button now does a HEAD check first and
  shows a clear toast instead of silently opening a broken/blank tab.
- **v0.4.6** — Reverted all dock buttons (bottom dock, top widget dock, left
  drawer, right drawer) from the trapezoid "folder tab" shape back to
  plain rounded rectangles.
- **v0.4.5** — Games' "click to add an HTML game" control now shows the
  same "Browse" button as v0.4.4's Files/Video/Music/Soundboard change.
  Only the Calendar's .ics import still uses the older text+"+" style.
- **v0.4.4** — Files, Video Player, Music Player, and Soundboard's "click to
  add a file" controls now show a real "Browse" button (icon + label,
  app-styled) instead of clickable placeholder text with a small "+" next
  to it — same underlying file picker, just a clearer, more obviously
  clickable control. Games and the Calendar's .ics import still use the
  older text+"+" style for now.
- **v0.4.3** — Moved the **Settings** button out of the bottom dock and into
  the top pill row, pinned as the last (rightmost) pill — alongside the
  language and theme pills, but always visible and not reassignable from the
  "Top bar pills" picker (it doesn't compete for the 5-slot cap). Follows the
  bottom dock's hover-open/pinned-open behavior along with the other pills.
- **v0.4.2** — Classroom Word Wheel's "Send scores" button now actually
  works: it used to try opening a `classroom_scoreboard.html` file that was
  never part of the game's folder (a 404). It now hands its team scores
  straight to TeachersDeck's own built-in Scoreboard widget via a small
  `localStorage` handoff (same-origin, no extra file needed) — the widget
  picks it up live if it's already open, opens itself if it isn't, and
  applies it on next load if the app tab wasn't open yet when scores were
  sent. `games/README.md` documents the handoff so any future game with its
  own scoring can use the same mechanism.
- **v0.4.1** — Registered the **Classroom Word Wheel** game (dropped into
  `games/Classroom-Word-Wheel/`) in `games.json`, so it now shows up as a
  Built-in games tile — it was sitting in the folder but wasn't listed yet.
  Also wired up the `instructions` field for real: a built-in game tile now
  gets a small "?" button when it has one, opening that file in a new tab.
  `games/README.md` now documents this game as the house style to follow
  for future TeachersDeck games (visual theme, host/setup panel pattern,
  sound design, scoreboard conventions) — see "House style for TeachersDeck
  games" in there.
- **v0.4.0** — Six changes:
  1. **Video Player: delete button for saved clips.** Each clip in the "My
     files" list now has a "−" button to remove it, matching the Music
     Player's track list.
  2. **Music Player: delete button changed to a "−" sign** (was an "X"
     icon) — same functionality, clearer at a glance.
  3. **Every "click to add a file" control now has a small circular "+"
     button next to the text**, across Files, Games, Music Player, Video
     Player, Soundboard, and the Calendar's .ics import. The whole label
     still opens the file picker either way — this just makes it obvious
     at a glance that it's clickable.
  4. **Fixed the Timer's Reset button.** Reset used to clear the countdown
     display but silently kept the last duration cached, so hitting Start
     right after Reset would jump straight back into counting down from
     that old number. Reset now clears the cached duration too — Start
     does nothing until you add time again with +1m/+5m.
  5. **Stopwatch: added a Lap button.** Available while running, it
     records a split; a scrollable list shows each lap's split time and
     running total, most recent on top. Reset clears the lap list along
     with the stopwatch itself.
  6. **New `games/` folder** for dropping in ready-made HTML games plus
     whatever else they need (images, a separate script file, an
     instructions handout) — a second path into the Games widget alongside
     its own single-file upload button. See `games/README.md`; a working
     example game ships in `games/example-guess-the-number/`.
- **v0.3.1** — The IndexedDB database is now named `TeachersDeck`, finishing
  the rename that v0.2.2 deliberately left alone. **This is a one-way break:**
  anyone with data in the old `widget-wall` database (uploaded files, custom
  background/logo images) will see an empty library on this build — there's
  no migration, by request. The app also does a one-time cleanup on load that
  deletes the old `widget-wall` database if it's still sitting in the
  browser, so nothing orphaned lingers.
- **v0.3.0** — Four changes:
  1. **Fixed the language/theme pills disappearing.** The top pill drawer was
     moving the live language-toggle and theme-button elements into itself,
     then wiping its own container on every rebuild — which destroyed those
     elements outright the next time you switched language or touched a
     drawer setting, and they never came back. It now only ever moves those
     elements between containers, never destroys them.
  2. **New top widget dock.** A left-justified row of up to 5 icon-only
     widget launchers, sitting right after the "TeachersDeck" brand name in
     the header — a fourth home for widgets alongside the bottom dock and
     left/right drawers. Pick it from Settings → Dock buttons like any other
     placement.
  3. **YouTube links now open in a new browser tab** instead of playing in
     an embedded iframe, in both the Music Player's Stream tab and the Video
     Player's YouTube tab. This sidesteps YouTube's embed-referer rules
     entirely (see the retired "Error 153" note below) — a full tab always
     just works, regardless of ad-blockers or how the app is being served.
     The widget shows a small "Open in YouTube" card so you can relaunch the
     link later without retyping it.
  4. **Folder-tab styling for the bottom, left, right, and (new) top widget
     docks.** Each widget launcher is now a trapezoidal tab — flush against
     the edge it "hangs" from and tapering toward the canvas — with
     overlapping tabs and the active/hovered one popping forward, so the
     whole set reads like tabs on a folder rather than plain icon buttons.
     (The language/theme pill drawer keeps its original pill look — it's a
     toggle row, not a widget launcher.)
- **v0.2.2** — Renamed the app from Widget Wall to **TeachersDeck** everywhere
  user-facing: browser tab title, header brand mark, extension name/description
  in `manifest.json`, and this README. The `teachersdeck` folder replaces the
  old `widget-wall` folder name (update your Chrome extension's "Load unpacked"
  selection to point at the new folder). Internally, the IndexedDB database is
  still named `widget-wall` on purpose — renaming it would create a *new*,
  empty database and silently wipe every teacher's saved layout, theme, roster,
  and uploaded files. That's a one-way data migration to do carefully later,
  not something to fold into a cosmetic rename.
- **v0.2.1** — Fixed the top drawer: it was splitting pills into a
  top-left/top-right pair, and top-left sat directly over the brand mark
  in the header, which is why the language-switch pill effectively
  disappeared there. The top drawer is now a single left-justified group,
  capped at 5, anchored at the top-right so it never overlaps the brand.
- **v0.2** — Widget drawers. The bottom dock now holds up to 10 widgets;
  new left and right drawers hold up to 5 each (for scaling toward 50+
  widgets); a new top drawer holds "pill" toggles (language switch, theme
  button — room for 5 more). All three are on by default and can be
  turned off, reassigned, or set to auto-hide-and-reveal-on-hover from
  Settings → *Side & top drawers*. Settings now also shows the app version.
- **v0.1** — Core shell: dock, draggable/resizable widgets, theme drawer,
  settings drawer, first 16 widgets, EN/VI-first localization.

## Run it now (standalone web app)
Just open `index.html` in Chrome. Everything works locally — no server needed.

## Turn it into a Chrome extension (new tab override)
1. In Chrome, go to `chrome://extensions`, enable **Developer mode**.
2. Click **Load unpacked** and select this `teachersdeck` folder.
3. Open a new tab — TeachersDeck replaces Chrome's default new tab page.

The same `index.html` powers both, so anything you build in the browser
version carries straight over to the extension version — with one
exception: **Cloud Class loads the Firebase SDK from Google's CDN
(`gstatic.com`)**, which Manifest V3's default extension CSP
(`script-src 'self'`) blocks for a packed/Web-Store extension. Cloud Class
works as-is in the standalone web-app version; shipping it inside the
actual Chrome extension needs the SDK vendored locally into `js/` plus
`host_permissions` for Firestore/Auth/Cloud Functions added to
`manifest.json` — not done here. Every other widget is unaffected.

## What's included in this shell
- **Dock** at the bottom to open/close widgets, styled after the reference site.
- **Draggable, resizable widget panels** — position and size are saved per
  browser (localStorage), so the layout is remembered next time.
- **Theme drawer**: six preset backgrounds, plus upload-your-own background
  image (stored in this browser's IndexedDB — not uploaded anywhere). A
  school/company logo overlay also exists in the code but is gated behind
  `ENTERPRISE_FEATURES` (see "Free vs Pro" below) — off, and hidden from the
  UI, unless that flag is flipped on for a specific enterprise build.
- **Classes**: one deck per class (roster, widgets, layout, theme all
  separate), switched from the class pill in the top bar; managed in Settings
  → Classes.
- **Settings drawer**: editable class roster (used by Name Picker), reset
  layout, reset everything.
- **Working widgets**: Clock, Timer, Stopwatch, Traffic Light, Dice,
  Checklist, Name Picker, Files, Games.
- **Files widget**: teachers add PDFs / PowerPoint / Word / Excel files,
  stored locally in the browser (IndexedDB) and opened in a new tab. PDFs
  render with Chrome's built-in PDF viewer. Office files currently open via
  the browser's/OS's default handler — true in-page rendering (so a .pptx
  or .docx displays inline in a widget, not just downloads) is a separate
  next step; see below.
- **Games widget**: add a self-contained `.html` game file and launch it in
  a new tab. Games written in Java or Python won't run in a browser as-is —
  they'd need converting to HTML/JS (or a Python-in-browser runtime like
  Pyodide, or a Java-to-web toolchain), which is a bigger separate task.

## Widget drawers (bottom / left / right / top) + top widget dock
Built for scaling past 16 widgets toward 50+ without crowding one bar:

- **Bottom dock** — up to 10 widget launchers (unchanged from v0.1).
- **Left drawer** — up to 5 widget launchers, vertical, hugs the left edge.
- **Right drawer** — up to 5 widget launchers, vertical, hugs the right edge.
- **Top widget dock** (new in v0.3.0) — up to 5 widget launchers, icon-only,
  left-justified right after the "TeachersDeck" brand name in the header.
  Always visible (no on/off setting, unlike the drawers below) — pick it
  from **Settings → Dock buttons** like any other placement.
- **Top pill drawer** — a separate thing from the widget dock above; not for
  widgets at all, it's for "pill" toggles like the language switch and theme
  button, shown as a single left-justified row (up to 5 pills) anchored at
  the top-right, clear of the brand mark. When this drawer is turned off,
  those two pills just sit inline in the header like they did in v0.1.

All four widget launchers (bottom, left, right, top) share the same
**folder-tab look**: each button is a trapezoid, flush against the edge it
"hangs" from and tapering toward the canvas, with tabs overlapping slightly
and the active/hovered one popping forward — like tabs on a folder rather
than plain buttons. The pill drawer keeps its original pill styling, since
it's a toggle row, not a widget launcher.

Every widget lives in exactly one of bottom / left / right / top / hidden —
**Settings → Dock buttons** has a dropdown per widget to move it, and each
location enforces its cap (moving a 6th widget into a 5-slot dock is
rejected with a toast). On upgrade from a v0.1 save, the first 10 widgets
(registry order) stay on the bottom dock and the rest are split evenly
into the left/right drawers, so nothing that used to be reachable
disappears; the new top widget dock starts empty until you assign
something to it.

**Settings → Side & top drawers** controls (these govern the left/right
widget drawers and the top *pill* drawer — the new top *widget* dock has
no visibility toggle, since it's always on):
- Show left / right / top drawer — on by default; turn any of them off to
  reclaim that edge of the screen entirely.
- Open drawers on hover — off by default (drawers you've made visible just
  stay fully open, like the bottom dock always has). Turn it on and the
  bottom dock plus every visible edge drawer — pill drawer, left, and
  right — tucks away to a thin strip at its edge and slides fully into
  view when the mouse reaches that edge, collapsing again when the mouse
  leaves. (The new top widget dock sits inline in the header rather than
  floating, so it doesn't tuck away — it's always fully visible.)

## Free vs Pro

TeachersDeck now ships with a Free tier and a paid Pro tier, unlocked from
**Settings → TeachersDeck Pro** (at the top of the Settings drawer).

- **Free**: clock, timer, stopwatch, built-in calendar, lesson files.
- **Pro**: traffic light, dice, checklist, scoreboard, poll, noise meter,
  games, music & video player, soundboard, custom background photo, and
  left/right drawer customization. Edit the `PRO_WIDGET_IDS` array in
  `js/app.js` to change this split.
- **Enterprise** (separate from Pro — a build-time flag, not a purchasable
  tier): the school/company logo overlay. Off by default
  (`ENTERPRISE_FEATURES = false` near the top of `js/app.js`, upload row
  `hidden` in `index.html`); flip both to ship a custom build for a
  district/organization that wants it.

The Name Picker widget (and its "Class list" roster setting) has been
removed from this version.

There's no backend or account system — Pro is unlocked with an **offline
license key** (format `TDPRO-XXXX-XXXX-XXXX`) validated client-side, so it
works with the "no login, no setup" design of the app. That also means it's
not hardened DRM: the checksum lives in the shipped JS, so a determined user
could read `PRO_LICENSE_SALT` in `js/app.js` and mint their own key. It's
enough to stop casual free-riding, not a determined bypass. For stronger
protection, keys would need to be issued and checked by a small server
instead (e.g. a Stripe webhook calling a license API).

**To go live, fill in these placeholders near the top of `js/app.js`:**

| Constant | What to set it to |
|---|---|
| `PRO_PRICE_USD` / `PRO_PRICE_VND` | Your real Pro price |
| `HSBC_ACCOUNT_NUMBER` / `HSBC_ACCOUNT_NAME` | Your HSBC Vietnam VietQR account details (shown first, as a bank-transfer QR code via the public img.vietqr.io API) |
| `STRIPE_PAYMENT_LINK` | A Stripe Payment Link URL (dashboard.stripe.com/payment-links) — or swap in another Asian processor's checkout link (Xendit, PayerMax, 2Checkout, PayPal.me, Wise, etc.) — no backend required either way |

After a customer pays, generate them a key by running `generateLicenseKey()`
in the browser console (uses the same checksum the app validates against)
and email it to them; they paste it into Settings → TeachersDeck Pro.

## Storage model (important for a classroom tool)
Everything — layout, theme, roster, checklist, uploaded files/games/logo —
is stored **only in that browser, on that device**, using `localStorage`
and `IndexedDB`. Nothing is uploaded anywhere. That matches "teacher
uploads/stores files locally" from the brief, but also means:
- Clearing browser data wipes it.
- It doesn't sync between a teacher's classroom computer and, say, their
  laptop at home — that would need real cloud storage (Google Drive,
  OneDrive, or your own server) as a later phase.

## Soundboard widget
A grid of one-tap attention-getter sound effects — a bell, applause, a
drumroll, whatever mp3/wav clips you add. Tap a tile to play it
immediately (it stops whatever was playing and starts the new one, so
sounds don't overlap), the playing tile pulses, and there's a Stop
button plus a volume slider. Add sounds the same way as everywhere else
in this app — pick the files, they're stored in this browser only.

## Music Player & Video Player widgets
Two widgets, each with tabs for different sources.

**Music Player** — "My files" tab, "Stream" tab (YouTube/SoundCloud), "Spotify" tab.
**Video Player** — "My files" tab, "YouTube" tab.

A few things worth knowing about what's really possible here, browser security being what it is:

- **"Import my Windows Media Player / iTunes playlist" isn't something a browser can do.**
  Those playlists (.wpl, iTunes library files, etc.) just point to file paths on your
  computer, and no browser will let a web page silently reach into your file system and
  follow those paths — that's a deliberate, unavoidable security boundary. The practical
  equivalent: use "Add music files" / "Add video files" and select the actual song or
  video files you'd normally play in those apps. Once added, they're stored in this
  browser (not uploaded anywhere) and play back with playlist controls (click to play,
  auto-advances to the next track when one ends).
- **YouTube** opens in a new browser tab rather than playing inside the widget —
  paste a video or playlist link in the Stream/YouTube tab, hit Play, and it
  launches on youtube.com in its own tab. This is deliberate: embedded YouTube
  players need a real HTTP referer to work at all (see the old "Error 153"
  note below, which no longer applies), and a full new tab always just works,
  with no dependence on how the app is being served or which ad-blockers are
  installed. The card left behind in the widget has an "Open in YouTube" link
  in case the tab didn't open (e.g. a popup blocker) or you want to relaunch it later.
- **SoundCloud** (Music Player's Stream tab) also works with no setup for public
  tracks and playlists — paste the link and it embeds SoundCloud's player.
- **Spotify is the one real limitation.** Playing Spotify tracks *inside* this widget
  would need a Spotify Premium account and your own registered Spotify developer app
  (OAuth sign-in) — Spotify doesn't allow embedded playback without that, similar to
  why Google Calendar needed its own OAuth flow. What's built instead: paste your
  playlist link and "Open in Spotify" launches it in the Spotify app or web player.
  If real in-widget Spotify playback (with your own Premium account connected) is
  something you want, that's a bigger, separate piece of work — happy to scope it out
  if you'd like to go there.

### (Retired) Troubleshooting: YouTube "Error 153"
Earlier versions embedded YouTube in an iframe inside the widget, which could
fail with error 153 because YouTube's embed rules need a real HTTP referer —
something a plain double-clicked `index.html` file, some ad-blockers, or a
video with embedding disabled by its uploader could all break. Since YouTube
links now open in their own browser tab instead of an iframe, none of that
applies anymore — this note is kept only as build history.

## Poll widget
A quick show-of-hands tally tool: set a question and 2–8 options under the
gear icon, then tap an option once per vote as hands go up (or however you
want to count them). Results show as live bars with vote counts, and
"Reset votes" clears the tally for the next question while keeping the
question and options in place. There's no student-device voting here —
everything runs on this one screen — since real-time multi-device voting
would need a backend server to sync votes between devices, which this
browser-only app intentionally doesn't have.

## Noise Meter widget (microphone)
Shows a live, color-coded noise level (green/amber/red) with an
approximate decibel number, using your device's microphone.

- Click "Enable microphone" — your browser will ask for microphone
  permission the first time.
- **Important — this needs a "secure context" to work at all**: opening
  `index.html` by double-clicking the file will NOT allow microphone
  access (browsers block it for plain local files). To use this widget,
  either:
  1. Load the app as the unpacked Chrome extension (see "Turn it into a
     Chrome extension" above) — extension pages count as secure, or
  2. Serve the folder over `http://localhost` (e.g. `python3 -m http.server`
     from inside the `teachersdeck` folder, then open `http://localhost:8000`).
  If neither is set up, the widget shows a message explaining this instead
  of a broken mic prompt.
- **The reading is approximate, not a calibrated sound level meter.**
  Browsers have no way to read true, calibrated decibels (dB SPL) from a
  microphone — that needs hardware calibration a laptop or classroom
  device doesn't have. What's shown is a relative loudness reading scaled
  to look like a familiar dB range, useful for "is the class louder than
  a minute ago" feedback, not for any measurement that needs to be exact.
- The microphone turns off automatically when you close the widget.

## Date system (Gregorian / Lunar)
Settings → Date system lets you choose how dates display everywhere:
**Gregorian** (default), **Lunar**, or **Both**. This uses the
Vietnamese/Chinese lunisolar calendar (calculated astronomically, tuned
for Vietnam's UTC+7), not a stored table, so it's accurate for any year.

- **Clock widget**: shows the lunar date instead of (or alongside) the
  Gregorian date.
- **Calendar widget**: each day in the month grid gets a small lunar
  day/month number, and the selected day's heading includes the lunar
  date too. The month grid itself still navigates by Gregorian months —
  a full lunar-month view (where the grid itself is laid out by lunar
  months, with their 29/30-day lengths and leap months) is a bigger,
  separate change if that's ever wanted.
- Changing this setting updates any open Clock or Calendar widget
  immediately.

## Calendar widget
A month-view calendar with its own gear icon (top-right of the widget) for
managing events.

- **Browse**: arrows move month to month; tap a day to see its events below
  the grid; the `+` button quick-adds an event on the selected day.
- **Manage** (gear icon): add, edit, or delete any event — title, date,
  time (optional), a reminder offset, and notes. There's also a full list
  of every event with quick edit/delete/"Add to Google Calendar" actions.
- **Popup reminders**: if an event has a reminder set, a dismissable popup
  appears in the app when it's due — this works as long as the browser tab
  is open, even if the Calendar widget itself isn't. There's also an
  optional "Enable desktop notifications" button that asks the browser for
  permission to also show an OS-level notification, for when the tab is in
  the background.
- **Google Calendar, two directions**:
  - *Push a local event to Google Calendar*: the calendar icon next to any
    event in the manage list opens Google Calendar's "add event" page,
    pre-filled, in a new tab.
  - *Pull events in from Google Calendar*: real live two-way sync needs
    Google's official API and an OAuth sign-in flow, which isn't something
    a browser-only, no-backend app like this can do safely. Instead,
    export a calendar or event from Google Calendar as an **.ics file**
    (Settings menu in Google Calendar → Export) and add that file under
    the gear icon's "Import from Google Calendar" section — it's parsed
    entirely in the browser and added as local events. If a two-way,
    always-in-sync Google Calendar connection becomes a priority, that's
    a separate, larger project (it needs a backend to hold the OAuth
    credentials) — worth a dedicated conversation if you want to go there.

## Localization
The whole interface — dock labels, drawers, widget text, toasts — is
translatable. Two languages are picked as "quick" languages and shown as
a toggle pill in the top bar (default: English / Vietnamese, since that's
the primary classroom mix). Switching that toggle re-labels the entire
app instantly, without losing anything a widget is in the middle of
(a running Timer keeps counting, for example).

- **Quick switch**: the `EN` / `VI` pill top-right.
- **Change the pair**: Settings → Language → pick any two of the built-in
  languages (English, Vietnamese, Spanish, French, Chinese, Japanese,
  Korean, Tagalog) for the two quick-switch slots.
- **Add another language**: open `js/app.js`, find the `LANGS` array near
  the top and add `{ code:'xx', name:'Your Language' }`, then add an
  `xx:'...'` translation to each entry in the `STRINGS` object right
  below it. Everything else (dock, drawers, widgets) picks it up
  automatically — no other code changes needed. Untranslated keys
  silently fall back to English rather than showing blank text.
- Student names, checklist items, and file/game names are treated as the
  teacher's own data and are never auto-translated.

## Suggested next phases
1. **In-page Office/PDF viewers** — render PDFs, PPTX, DOCX, XLSX *inside*
   a widget instead of opening a new tab (pdf.js for PDF; libraries or
   Office Online embedding for PPTX/DOCX/XLSX — each has real trade-offs
   worth discussing before picking one).
2. **True Chrome extension polish** — icons, options page, packaging for
   the Chrome Web Store.
3. **Cloud sync** (optional) — Google Drive/OneDrive so a teacher's wall
   and files follow them between devices.
4. **More widgets** — whatever else comes up as you use it (attendance,
   recipes, instructions, etc. were on the reference site's dock).

## File structure
```
teachersdeck/
  index.html        the whole app shell
  manual.html       teacher-facing instruction manual (install + every widget)
  RELEASES.md       which version shipped when, and as which zip
  css/style.css      theme + layout + widget styling
  js/app.js          widget registry, drag/resize, storage, theming
  js/jszip.min.js    JSZip 3.10.2 (MIT) — builds the filled Word file for the Lesson Planner
  js/lesson-template.js   the blank lesson plan .docx, embedded as base64
  manifest.json       optional — only needed for the Chrome extension version
  games/             drop-in .html games + their assets (see games/README.md)
    README.md        how to add a game and register it
    games.json        the list of built-in games the Games widget reads
```
(`tools/`, `admin/`, and `license-backend/` are developer-only and not included in this release zip.)

### The `games/` folder
A second way to get a game into the Games widget, alongside the widget's own
upload button. The upload button only takes a single `.html` file at a
time — fine for something fully self-contained, but not for a game that
comes with its own images, a separate script file, or a handout of
instructions for students. Drop that whole folder into `games/` instead,
list it in `games/games.json`, and it shows up as a "Built-in games" tile
next to anything uploaded through the widget. Full instructions, plus a
working example, are in `games/README.md`. Like the YouTube tabs, reading
`games.json` needs the app served over `http://localhost` or loaded as the
Chrome extension — it won't work from a bare double-clicked `index.html`.
