# App Store assets

Upload-ready files for App Store Connect (and a Play graphic if Android follows).

## Upload these

| File | Where it goes |
| --- | --- |
| `icon-1024.png` | App Store Connect → App Information → App Icon. Already 1024×1024, no alpha, no rounded corners. |
| `screenshots/UPLOAD-iphone-6.9/*.jpg` | **Default iPhone slot (6.9").** 1320×2868. Use these first. |
| `screenshots/UPLOAD-iphone-6.5/*.jpg` | Only the 6.5" slot (1284×2778), if Connect still shows one |
| `logo-horizontal-dark.png` | Marketing site, press, email. Not an App Store Connect field. |
| `logo-horizontal-light.png` | Same, for cream / white backgrounds. |
| `play-feature-graphic-1024x500.png` | Google Play only, if you ship Android. |

The framed **6.5"** set is **1284×2778**, RGB PNG, no alpha. That matches the slot Connect is currently validating (`1242×2688` / `1284×2778`). Use `iphone-6.5/`, not `iphone-6.9/`, unless a 6.9" slot is also shown.

Do not add captions again in Connect — they are already on the images.

## Still required before submit

1. **Full-resolution recapture.** The four device shots in `source/` came through chat at 473×1024. They are sharp enough to layout, not sharp enough for the store. On the phone, open Photos → the originals → Share the files (not a screenshot of this chat) into `source/` as:

   - `01-home.jpg`
   - `02-today.jpg`
   - `03-calendar.jpg`
   - `04-messages.jpg`

   Then from this folder:

   ```sh
   python3 compose_screenshots.py
   ```

   Prefer a TestFlight / production build, not Expo Go.

2. **iPad 13" screenshots.** `ios.supportsTablet` is true, so Connect will block submit without them. Capture the same four screens on an iPad (or the 13" simulator) at one of Apple’s [listed sizes](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/). Do not stretch the iPhone frames.

3. **Optional extra shots** if those features stay on for review: Health / recovery, Videos, Booking.

## Captions on the framed set

1. Home — Your studio. Today’s plan.
2. Today — Log the work as you go.
3. Calendar — The week at a glance.
4. Messages — Message your coach anytime.

`screenshots/iphone-6.5-raw/` and `iphone-6.9-raw/` are full-bleed upscales of the same captures. Do not upload those until the sources are native resolution.

## Notes on the current captures

- Demo studio is **ChiForm**, client greeting **HI APPLE**. Fine for review; recapture if you want a different studio on the listing.
- Home shows **Sign out** in the header. Recapture without it if you can hide that control.
- Messages is a short thread. A couple more bubbles would fill the white space.
- Glance at Home on a real device before you lock the listing. If “Good morning” / “Keep going” / “3 of 6” are missing spaces, that will show on the store.
