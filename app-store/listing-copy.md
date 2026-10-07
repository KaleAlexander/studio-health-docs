# App Store listing copy

Paste into App Store Connect. Replace the demo email and OTP before submit. This listing is for the **client** app, not the studio owner dashboard. If Apple rejected for login / a demo video, use [review-reply.md](review-reply.md) instead of only this page.

## Name and subtitle

| Field | Limit | Copy |
| --- | --- | --- |
| Name | 30 | Studio Health |
| Subtitle | 30 | Your studio in your pocket |
| Promotional text | 170 | Programs, session feedback, videos, and booking from your studio — in one app your coach already set up for you. |

Alternate subtitles if the first is taken:

- Training from your studio
- Programs from your coach

## Description

```
Studio Health is the client app for people training with a studio on Studio Health.

Your coach invites you. Sign in with the email they used, then a 6-digit code. There is nothing to buy in the app.

Once you are in, you can:

• See today’s program and log your session
• Tell your coach how hard the session felt
• Follow your calendar and diet notes
• Watch exercise demos from your studio’s library
• Book sessions when your studio turns booking on

Your studio’s colours and name come through in the app. Studio Health is a coaching tool. It is not a medical device and does not diagnose or treat any condition.
```

## Keywords

100-character limit, comma-separated, no spaces after commas if you need the room. Do not use competitor names.

```
studio,coach,workout,program,feedback,fitness,training,client,pilates,strength
```

## What’s New (1.0)

```
First release of the Studio Health client app.
```

## Support, marketing, copyright

| Field | Value |
| --- | --- |
| Support URL | `https://studiohealth.ai/clients` |
| Marketing URL | `https://studiohealth.ai/` |
| Privacy Policy URL | `https://studiohealth.ai/privacy` |
| Copyright | `2026 Studio Health` (or the legal entity name) |
| Primary category | Health & Fitness |

## Screenshots

Framed iPhone 6.5" PNGs (1284×2778) live in [assets/screenshots/iphone-6.5](assets/screenshots/iphone-6.5). Upload those into the 6.5" slot. A 6.9" set (1320×2868) is in [assets/screenshots/iphone-6.9](assets/screenshots/iphone-6.9) if Connect also asks for it. iPad 13" (2064×2752) is in [assets/screenshots/UPLOAD-ipad-13](assets/screenshots/UPLOAD-ipad-13) — Home, Today, Calendar. Upload in this order. Captions are already on the images — do not add them again in Connect.

1. Home — Your studio. Today’s plan.
2. Today — Log the work as you go.
3. Calendar — The week at a glance.
4. Messages — Message your coach anytime. (iPhone only until you recapture Messages on iPad)

Do not put the App Store name, price, or Apple product bezels on the images.

## App Review notes

The current rejection is Guideline 2.1 Information Needed (new developer account). Paste [review-reply.md](review-reply.md) into **both** Resolution Center and App Review Information → Notes. The short version below is only for later submits once they already have this on file.

```
This app uses email + a 6-digit code, not a password.

1. Open the app.
2. Enter USERNAME_EMAIL and tap Continue.
3. On the next screen enter PASSWORD_OTP.

You will land on Home for a demo studio with a program, diet, videos, and booking already populated. After ticking an exercise on Today, the client can rate how hard the session felt (1–10) and leave a comment for their coach.

The app does not use HealthKit or read any health data from the device.

Clients cannot create accounts in this app. Coaches invite them from the web dashboard at https://studiohealth.ai. There are no in-app purchases. Studio subscriptions are billed on the web.

Account deletion is in the app: Home → Account → Delete account. That permanently removes the demo login, so recreate the reviewer client if Apple tests it.
```

Replace `USERNAME_EMAIL` and `PASSWORD_OTP` with the same values you put in the Sign-in required fields.

## Privacy nutrition (draft)

Confirm these against the live app and SDKs (Supabase, Expo) before saving in Connect.

**Data collected (linked to the user, not used for tracking):**

- Contact Info → Email Address → App Functionality
- Contact Info → Name → App Functionality
- Identifiers → User ID → App Functionality
- Health & Fitness → Fitness → App Functionality (workout logs and session effort ratings shared with the coach)
- User Content → Photos or Videos → App Functionality (meal photos, if diet is on)
- User Content → Other User Content (messages, session comments, meal notes) → App Functionality
- Identifiers → Device ID → App Functionality (push)

**Not collected / not used for tracking ads,** unless a future SDK changes that.

The app no longer links HealthKit or Health Connect. Do not tick Health & Fitness → Health. Session comments are free text, so they sit under Other User Content.

## Age rating questionnaire (expected)

Answer from the live product, not this guess. Likely:

- No unrestricted web access
- No gambling
- No medical claim to treat or diagnose
- Health and fitness information: yes, workout programs and session feedback
- No age-restricted content that would push 17+ unless you add it later
