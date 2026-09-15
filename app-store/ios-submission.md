# iOS App Store submission

Playbook for the client app in `studio-health-mobile` (`app.studiohealth.mobile`).

Apple reviewers install a fresh copy. They need a login that works without access to an email inbox. After login, the session already persists on device (`persistSession` in the mobile Supabase client). Do not ship a pre-logged-in binary.

## Status before you start

| Item | Current state |
| --- | --- |
| Bundle ID | `app.studiohealth.mobile` |
| Display name | Studio Health |
| Version | `1.0.0` in `app.json` |
| Login | Email + 6-digit OTP. Coaches invite clients. Clients cannot self-register. |
| HealthKit | Reads steps, heart rate, sleep. Does not write. |
| Tablet | `ios.supportsTablet` is `true`, so iPad screenshots are required |
| Export compliance | `ITSAppUsesNonExemptEncryption` is `false` in `app.json` |
| Purchases in the app | None. Studio billing is Stripe on the web (multiplatform / reader-style access) |
| Review OTP bypass | Built. Set `APPLE_REVIEW_EMAIL` and `APPLE_REVIEW_OTP` on the studio-health API. |

## 1. Reviewer account

Create a dedicated **production** client on a demo studio, then give Apple a **fixed 6-digit code** for that email only. Reviewers cannot open `apple-review@…` mail.

### Demo studio

In the live owner dashboard:

1. Create a studio named **Studio Health Demo**.
2. Turn on every feature you want reviewed: program, health tracking, diet, video library, booking, messaging.
3. Brand it so screenshots look like a real studio, not empty defaults.

### Demo client

1. Invite a client such as `apple-review@yourdomain.com`. Do not use a personal inbox.
2. Fill the account so every tab has content:
   - A current program with several exercises and demo videos
   - A few logged sessions on Today / Calendar
   - Diet entries if diet is on
   - Library clips on Videos
   - At least one bookable slot
   - A short coach message if chat is visible
3. Keep this studio, the API, and Supabase **up** for the whole review window.

### Fixed OTP

The App Store Connect form has Username and Password. This app does not use a password. Treat the OTP as the password, and only for this email.

The bypass lives on the studio-health API (`/api/auth/otp` and `/api/auth/otp/verify`). It is off until both env vars are set:

```
APPLE_REVIEW_EMAIL=apple-review@yourdomain.com
APPLE_REVIEW_OTP=246810
```

Set them on the **production studio-health web API**, not in Expo / EAS.

The reviewer types the email and code in the iOS app. The app then POSTs to `EXPO_PUBLIC_API_URL` (`/api/auth/otp` and `/api/auth/otp/verify`). That Next.js server is what reads `APPLE_REVIEW_EMAIL` and `APPLE_REVIEW_OTP`. Expo env vars never reach this check. Putting the OTP in EAS as `EXPO_PUBLIC_*` would also bake it into the binary.

The only Expo setting that matters for this flow is `EXPO_PUBLIC_API_URL` pointing at that production API.

- The email must already be an invited client with a seeded demo studio
- The OTP must be exactly 6 digits (the app’s code field only accepts 6)
- Every other user still gets a real email OTP
- The review email does not receive a login email; the reviewer types the documented code

Redeploy after setting the vars. Confirm on a TestFlight build: email → Continue → `246810` → Home.

### App Review Information

In App Store Connect → the iOS version → App Review Information:

| Field | Value |
| --- | --- |
| Sign-in required | On |
| Username | The demo client email |
| Password | The fixed OTP, e.g. `246810` |
| Notes | Paste the template in [listing-copy.md](listing-copy.md#app-review-notes) |
| Contact | A phone/email you will answer during review |

Say in the notes that Health data comes from Apple Health if granted, and that the rest of the app works if the reviewer denies Health access.

## 2. Legal pages

Apple opens the privacy and support URLs. They must be public `https` and match the product.

Update `studio-health-marketing` before submit. Privacy and terms still say clients sign in with a **mobile number**. The app uses **email codes**.

Publish:

| URL | Use |
| --- | --- |
| `https://your-marketing-domain/privacy` | App Store privacy policy URL (required) |
| `https://your-marketing-domain/terms` | Link from privacy / support |
| Support URL | Required. A live contact or help page, not a 404 |
| Marketing URL | Optional. The marketing homepage |

Guideline 5.1.1(v) (in-app account deletion) applies when the **app lets users create accounts**. This client app does not; coaches invite people. Still say on the privacy page how a client asks their studio (or Studio Health) to remove their data.

## 3. Listing collateral

Paste-ready copy lives in [listing-copy.md](listing-copy.md).

### Icon

Export a **1024×1024 PNG** from `studio-health-mobile/assets/images/icon.png`.

- No transparency / alpha
- No rounded corners (Apple applies the mask)
- No text that will clip at small sizes

### Screenshots

1–10 images, JPEG or PNG, no alpha.

Because the app supports iPhone and iPad, upload both:

| Device | Required sizes (portrait) |
| --- | --- |
| iPhone 6.9" (upload first; Apple scales down) | `1320×2868`, `1290×2796`, or `1260×2736` |
| iPad 13" | See [Apple’s screenshot specs](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) |

Capture from a **production / TestFlight build**, not Expo Go, logged into the demo account so screens are full.

Suggested set (same shots on iPhone and iPad):

1. Home
2. Today — program
3. Today — health / recovery
4. Calendar
5. Videos
6. Booking (if it stays on for review)

App Preview video (15–30s, up to 3) is optional.

### Privacy nutrition labels

Declare what this app and its SDKs collect. Confirm against the live binary and third parties (Supabase, Expo push / updates, HealthKit).

Suggested starting point for Studio Health:

| Data | Linked to user | Used for tracking | Typical purpose |
| --- | --- | --- | --- |
| Email address | Yes | No | App functionality (login) |
| Name | Yes | No | App functionality |
| User ID | Yes | No | App functionality |
| Health (steps, heart rate, sleep via HealthKit) | Yes | No | App functionality; shared with the coach |
| Fitness / workout logs | Yes | No | App functionality; shared with the coach |
| Other user content (messages) | Yes | No | App functionality |
| Device ID / push token | Yes | No | App functionality (notifications) |

HealthKit purpose strings are already in `app.json`. Do not claim the app diagnoses, treats, or monitors disease.

### Age rating

Complete the App Store Connect questionnaire. Health and fitness coaching content is fine if you do not present the app as a medical device.

### Categories and billing

- Primary category: **Health & Fitness**
- There is no In-App Purchase in the client app. Studio subscriptions are on the web. If review asks, this is a companion / multiplatform service (guideline 3.1.3(b)), not a paid iOS unlock.

Sign in with Apple is not required: login is first-party email OTP, not Facebook / Google / similar.

## 4. Build and submit

1. Paid [Apple Developer Program](https://developer.apple.com/programs/) membership.
2. App Store Connect → New App → bundle ID `app.studiohealth.mobile`.
3. Fill listing, privacy URL, age rating, nutrition labels, review notes, and demo credentials.
4. Production EAS build, then upload:

```sh
cd studio-health-mobile
eas build --platform ios --profile production
eas submit --platform ios
```

5. Wait for processing (often 10–15 minutes). The build appears in TestFlight.
6. Install that TestFlight build yourself. Sign in with the demo email and fixed code. Tap every tab. Confirm nothing is empty and Health denial still leaves a usable app.
7. Submit that build for App Review.

Keep the API, Supabase, and demo studio up until Apple replies. A down backend looks like a broken app.

## Rejection risks for this app

1. OTP the reviewer cannot receive (no fixed code / no notes explaining the OTP-as-password flow).
2. Empty demo studio (guideline 2.1 / 4.2 minimum functionality).
3. Privacy or terms that still mention SMS / mobile-number login.
4. HealthKit with no working fallback when permission is denied.
5. Placeholder support or privacy URLs.
6. Screenshots from a logged-out or empty account.

## After approval

- Use TestFlight for later builds before each store release.
- Keep the demo account active and seeded; you will need it for every update that requires review.
- Promotional text (170 characters) can change without a new binary. Screenshots and description need a new version.
