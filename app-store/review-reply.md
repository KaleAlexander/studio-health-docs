# Guideline 2.1 — Information Needed (new developer account)

Apple wants **the same answers in two places**: Resolution Center **and** App Review Information → Notes. They also want a **physical iPhone** screen recording (latest iOS), starting at launch.

Fill these, then find-and-replace in the paste below:

| Token | Put this |
| --- | --- |
| `USERNAME_EMAIL` | Demo client email (same as Sign-in required) |
| `PASSWORD_OTP` | Fixed 6-digit code (same as Password; must match production `APPLE_REVIEW_OTP`) |
| `DEMO_VIDEO_URL` | Unlisted YouTube or Drive link that opens without a login |

Test on TestFlight first: email → Continue → code → Home with content.

## Record the video

Physical iPhone, latest iOS, **TestFlight build of the submitted binary**, signed out. Start recording **before** you tap the icon. 90–120 seconds. Do not actually delete the demo account.

1. Tap Studio Health (cold launch). Land on **Sign in with your email**. Pause so they can read that a coach invites you and there is no self-registration.
2. Type `USERNAME_EMAIL` → **Continue**.
3. Type the 6-digit `PASSWORD_OTP` → **Sign in**.
4. **Home** — branded studio, today’s plan.
5. **Today → Program** — tick or log one exercise.
6. **Today → Health** — open the tab. Deny Apple Health if prompted; keep going.
7. **Today → Diet** — open the tab (meal log for the coach).
8. **Calendar** — week with logged days.
9. **Videos** — play a few seconds of a studio clip.
10. **Book** — booking page.
11. Chat bubble → **Messages** — existing 1:1 thread with the coach. Do not send junk.
12. Home → **Account**. Scroll to **Delete account**. Tap it, tap **Continue**, then **Cancel** on “This cannot be undone.” Leave the account intact.
13. Stop recording. There is no paywall, IAP, or registration screen to show — that is the point.

Upload unlisted. Paste the URL into the table above.

## Connect fields

- Sign-in required: **On**
- Username / Password: the email and 6-digit code
- Notes: paste **Reply (items 1–6)** below
- Resolution Center: paste the **same** block, plus attach the video file if Connect lets you
- Contact: a phone/email you will answer

## Reply (items 1–6) — paste into Resolution Center and Notes

Keep this under Connect’s 4,000-character Notes limit. Attach the video in Resolution Center as well as linking it.

```
Hello App Review,

Thank you. Studio Health is complete and ready for customers. Answers to your six items are below and duplicated in App Review Information → Notes.

1. SCREEN RECORDING
DEMO_VIDEO_URL
Physical iPhone, latest iOS, submitted TestFlight build. Starts at launch (signed out): email → 6-digit code → Home → Today (log an exercise, Health, Diet) → Calendar → Videos → Booking → coach Messages → Account, including Delete account (cancelled so the demo login remains).

No in-app registration (coaches invite clients on the web). No IAP or paid unlocks in iOS. No public UGC feed, so no public report/block UI (see 6).

2. PURPOSE AND AUDIENCE
Studio Health is the client app for people who train with a studio already on Studio Health (fitness, pilates, personal training, similar coaching).

Problem: programs, recovery, demos, diet logs, messages, and booking are usually scattered. Value: the coach sets up the studio on the web; the client opens one branded app for today’s program, session logs, optional Apple Health recovery (steps, heart rate, sleep), studio demos, coach messages, and booking.

Public App Store companion for invited clients — not an employee-only or MDM app. Coaching tool, not a medical device; it does not diagnose or treat any condition.

https://studiohealth.ai
https://studiohealth.ai/clients
https://studiohealth.ai/privacy

3. SETUP AND ACCESS
Email + 6-digit code (not a password). The Connect Password field is that code.

Username: USERNAME_EMAIL
Password: PASSWORD_OTP
No email is sent for this reviewer account. Type the code on the second screen.

1. Launch signed out.
2. Enter USERNAME_EMAIL → Continue.
3. Enter PASSWORD_OTP → Sign in.
4. Home is a seeded demo studio (ChiForm) with program, health, diet, videos, booking, and messages.

Then: Home (Account top-right) · Today (Program / Health / Diet) · Calendar · Videos · Book · chat bubble for Messages.

HealthKit is optional (read-only). Deny it; the rest still works.

Account deletion: Home → Account → Delete account. Please do not delete this demo login unless testing that path; we will restore it.

4. EXTERNAL SERVICES
• Supabase — auth, database, file storage
• Studio Health API — login codes, account deletion, notifications
• Resend — login emails for real clients (this demo uses the fixed code)
• Stripe — studio subscriptions on the web only; no IAP in this app
• Google Gemini — program drafts on the web dashboard; iOS only shows saved programs
• Apple Health / HealthKit — optional steps, heart rate, sleep
• Expo — push notifications
• YouTube / Vimeo embed players — studio exercise demos
• Studio booking URL in an in-app browser, when enabled

5. REGIONAL DIFFERENCES
Same features and content in all regions. English UI. No geo-restricted content.

6. REGULATED INDUSTRY / THIRD-PARTY MATERIAL
Not a licensed healthcare provider. Health data is coaching context only.

Studios supply programs, messages, and videos and must have rights to that material (https://studiohealth.ai/terms). YouTube/Vimeo play via official embeds. Clients only see content from the studio that invited them. No public media marketplace.

This is a private invited coaching channel, not a public social network, so there is no public report/block UI. The studio controls who is invited. Clients can delete their account in the app.

Happy to restore the demo account or provide anything else you need.

Thank you,
Kale Hanby
Studio Health
hello@studiohealth.ai
```

## Before you hit Reply

- [ ] TestFlight login works with the exact email and code in the paste
- [ ] Video starts at launch on a physical iPhone, latest iOS
- [ ] Video shows login, main tabs, Messages, and Delete account → Cancel
- [ ] Video URL opens without a login wall
- [ ] Production API, Supabase, and the ChiForm demo studio are up
- [ ] `APPLE_REVIEW_EMAIL` / `APPLE_REVIEW_OTP` still set on production
- [ ] Same text in Resolution Center **and** Notes
- [ ] Sign-in required fields match the paste
- [ ] Privacy and support URLs load
