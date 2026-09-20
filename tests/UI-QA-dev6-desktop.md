# dev.6 desktop refinement — 2026-09-01

## Changes verified

- Shared Android/Windows/Termux HTML hierarchy, compact 15-person supporter grid and separate ʙʏᴛᴇᴄʜɴᴏ acknowledgement.
- Minimal control press response; fine-pointer desktop uses integer translation rather than text scaling.
- Desktop modal fades retain scroll lock and stable scrollbar space; mobile retains its established modal transition.
- Start and download labels stay centered with symmetric space for the right-hand arrow, including dynamic start labels.

## Browser checks

- Real local engine on an isolated test data directory: upload this project's APK, analyze, optimize, view completion/report/download link, reopen history with “Tekrar işle”. All completed; no browser error/warning logs.
- Local UI fixture: light/dark themes, three profiles, no-ad disabled profiles, optional actions, split/ABI selection, message and report dialogs, confirmation cancellation, result actions and supporter section.
- Viewports: 1440×900 desktop, 900×720 narrow desktop, 390×844 embedded Android layout. No horizontal overflow in inspected narrow layouts; all 15 supporter names retained.
- Installed-app fixture: expand/collapse inline actions and search among 100 sample entries. Native share/install were not invoked.
- Measured desktop body width before/after modal lock remained 1424.8 px. Finite dialog samples recorded zero body/dialog width change and no dialog transform. One 650 ms sample had 40 frames / 17 ms maximum interval; another 38 frames / 18.7 ms. These are local measurements, not a cross-device FPS guarantee.
- Mobile start button computed centered alignment, 44 px equal horizontal padding and an absolutely positioned arrow. Screenshot inspected.

## Automated checks

- 115 Python tests passed.
- 11 Node tests passed, including desktop/mobile modal keyframes, cancellation, reduced motion, idle scheduling and shared source wiring.
- Release Android build and signature verification passed.
- New Windows build passed local HTTP/HTTPS startup, toolchain readiness and shared UI source equality checks. Termux archive passed source equality and runtime-file exclusion checks.

No physical Android device or device-wide battery benchmark was available for this pass. Tests do not establish compatibility with every third-party APK or every browser/GPU.

## Windows delivery

The previous `outputs/APK-Cleaner-Studio-v0.6.2-dev.6-Windows.exe` was locked by an already running instance and was not terminated. The audited current build was delivered as `outputs/APK-Cleaner-Studio-v0.6.2-dev.6-Windows-guncel.exe` (SHA-256 `6D298EC4E01F0CCB99BD93A1160EBA259BF6FF30FD42C501A6B386393E4C6C50`), identical to the newly built `dist` executable. The default-output audit initially rejected the old executable as stale; rerunning against the new `dist` executable passed. Do not distribute the older locked filename as this revision.
