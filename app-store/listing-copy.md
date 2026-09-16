# App Store listing copy

Paste into App Store Connect. Replace `your-marketing-domain` and the demo email before submit. This listing is for the **client** app, not the studio owner dashboard.

## Name and subtitle

| Field | Limit | Copy |
| --- | --- | --- |
| Name | 30 | Studio Health |
| Subtitle | 30 | Your studio in your pocket |
| Promotional text | 170 | Programs, recovery, videos, and booking from your studio — in one app your coach already set up for you. |

Alternate subtitles if the first is taken:

- Training from your studio
- Programs from your coach

## Description

```
Studio Health is the client app for people training with a studio on Studio Health.

Your coach invites you. Sign in with the email they used, then a 6-digit code. There is nothing to buy in the app.

Once you are in, you can:

• See today’s program and log your session
• Check steps, heart rate, and sleep when your studio uses Apple Health
• Follow your calendar and diet notes
• Watch exercise demos from your studio’s library
• Book sessions when your studio turns booking on

Your studio’s colours and name come through in the app. Studio Health is a coaching tool. It is not a medical device and does not diagnose or treat any condition.
```

## Keywords

100-character limit, comma-separated, no spaces after commas if you need the room. Do not use competitor names.

```
studio,coach,workout,program,recovery,health,fitness,training,client,pilates
```

## What’s New (1.0)

```
First release of the Studio Health client app.
```

## Support, marketing, copyright

| Field | Value |
| --- | --- |
| Support URL | `https://your-marketing-domain/clients` |
| Marketing URL | `https://your-marketing-domain/` |
| Privacy Policy URL | `https://your-marketing-domain/privacy` |
| Copyright | `2026 Studio Health` (or the legal entity name) |
| Primary category | Health & Fitness |

## Screenshots

Framed iPhone 6.5" PNGs (1284×2778) live in [assets/screenshots/iphone-6.5](assets/screenshots/iphone-6.5). Upload those into the 6.5" slot. A 6.9" set (1320×2868) is in [assets/screenshots/iphone-6.9](assets/screenshots/iphone-6.9) if Connect also asks for it. Upload in this order. Captions are already on the images — do not add them again in Connect.

1. Home — Your studio. Today’s plan.
2. Today — Log the work as you go.
3. Calendar — The week at a glance.
4. Messages — Message your coach anytime.

See [assets/README.md](assets/README.md) before upload: replace the chat-compressed sources with full-res Photos/TestFlight captures, then recapture the same four screens on iPad 13".

Do not put the App Store name, price, or Apple product bezels on the images.

## App Review notes

```
This app uses email + a 6-digit code, not a password.

1. Open the app.
2. Enter USERNAME_EMAIL and tap Continue.
3. On the next screen enter PASSWORD_OTP.

You will land on Home for a demo studio with a program, health, diet, videos, and booking already populated.

Health data comes from Apple Health if you grant permission. Deny Health access if you prefer; the rest of the app still works.

Clients cannot create accounts in this app. Coaches invite them from the web dashboard at the marketing / studio site. There are no in-app purchases. Studio subscriptions are billed on the web.

Account deletion is in the app: Home → Account → Delete account. That permanently removes the demo login, so recreate the reviewer client if Apple tests it.
```

Replace `USERNAME_EMAIL` and `PASSWORD_OTP` with the same values you put in the Sign-in required fields.

## Privacy nutrition (draft)

Confirm these against the live app and SDKs (Supabase, Expo, HealthKit) before saving in Connect.

**Data collected (linked to the user, not used for tracking):**

- Contact Info → Email Address → App Functionality
- Contact Info → Name → App Functionality
- Identifiers → User ID → App Functionality
- Health & Fitness → Health → App Functionality (HealthKit; shared with the client’s coach)
- Health & Fitness → Fitness → App Functionality
- User Content → Other User Content (messages, logs) → App Functionality
- Identifiers → Device ID → App Functionality (push)

**Not collected / not used for tracking ads,** unless a future SDK changes that.

## Age rating questionnaire (expected)

Answer from the live product, not this guess. Likely:

- No unrestricted web access
- No gambling
- No medical claim to treat or diagnose
- Health and fitness information: yes, coaching / recovery context
- No age-restricted content that would push 17+ unless you add it later
