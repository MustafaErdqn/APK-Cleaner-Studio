# dev.6 startup-call and high-refresh regression pass — 2026-09-02

## Implemented scope

- Original-free candidate inspection traces Activity lifecycle helper calls across DEX files. Activity inheritance, not a fixed class-name list, determines eligibility.
- Root signatures currently supported: static void helper accepting one Context or Activity argument, receiving the lifecycle's `this` register or a direct move-object alias. Lifecycle entries: onCreate(Bundle), onCreate(Bundle, PersistableBundle), onResume().
- Known direct and deferred framework message paths are evidence, not proof that code was added later. Candidates are unchecked by default and require an explicit impact acknowledgment. Only selected initiating invokes are replaced with same-length NOPs; superclass calls and entire methods are preserved.
- Compact analysis badges: 28 px container / 20 px vector.
- Progress uses elapsed time on every animation frame rather than a 24 ms frame gate. Interrupted list transitions are measured at their visible position before cancellation. Idle/background suspension is retained.

## Verification

- 127 Python tests passed: engine/API regressions, real assembled multidex fixtures, arbitrary Activity names, lifecycle signatures, deferred callback tracing, exact-byte root patches, unchanged DEX length and valid checksums, stale-target rejection, scan ownership/locking and isolated split rescan directories.
- 13 JavaScript tests passed: rendered UI, 60/90/120/144 Hz simulated frame intervals, rapid list interruption ordering, modal cancellation/reopen, reduced motion and idle scheduling.
- Browser fixture at 390×844 and 1440×1000: automatic candidate fetch without original upload; candidate unchecked initially; apply blocked without acknowledgment; selected candidate retained on reopening; rescan; light/dark rendering. Screenshots inspected, no horizontal overflow observed.
- Installed-app fixture: successive selections leave one action row. Badge dimensions verified from computed styles. Browser error/warning log was empty.
- Preview toolbar overlays the mobile footer in test screenshots only; footer actions were exercised with Enter. Toolbar is not present in release assets.
- Android release build passed; APK v2/v3 signatures verified. Full Python suite confirms shipped Android sources match current sources.
- Windows release launched successfully: local HTTP and HTTPS, fully ready toolchain, exact shared UI source equality. Termux ZIP CRC/source equality and exclusion of runtime data passed.

## Limits and delivery

This pass does not claim measured 120 FPS on physical hardware, universal third-party APK coverage, provenance proof, or resolution of encrypted/reflective flows. Browser message candidates are fixtures; DEX tracing/patching uses separately assembled real DEX fixtures.

All three standard dev.6 files in `outputs` are current for this pass. Unlike the preceding desktop QA pass, the standard Windows filename was no longer locked and was updated successfully. `Windows-guncel.exe` was also refreshed with the same executable, so prior links do not point to a stale build.

## Pawxy and popup regression pass — 2026-09-03

- The general scanner now covers Activity, Fragment and Application lifecycle entries (`onCreate`, `onResume`, `onStart`, `onPostResume`, `onPostCreate`, `onActivityCreated` and `onViewCreated`) rather than matching launcher class names. Object-typed wrapper arguments retain concrete callback types across moves, casts, branches and DEX boundaries; ignored non-void helpers can be candidate roots while consumed return values remain excluded.
- A read-only scan of user-supplied `Pawxy v1.12.1.apk` found eight review candidates. The two missed `Browser$J.onResume` roots were selected in an isolated temporary copy: both roots disappeared, six unrelated candidates remained, the original APK hash was unchanged, and only ten non-header DEX bytes changed. This proves root-level patch isolation, not that every candidate was injected or that the modified app runs correctly on a physical device.
- Installed-app rows now use keyed DOM reconciliation. Existing image elements and unchanged data-URI sources survive filtering, reopening and repeated native callbacks; the prior icon fade-in animation is absent.
- Missing startup-impact acknowledgment is shown both inline inside the still-open dialog and in an ARIA live toast above all modal layers. The checkbox receives focus and an invalid state; no selection is applied until acknowledgment.

## Stability and focused results regression pass — 2026-09-05

This section supersedes the older toast-layer and artifact-delivery notes above.

- Shared toasts are below modal layers again (computed z-index 90 versus 510). Missing impact acknowledgment produces only the inline warning, without a duplicate toast.
- Startup results prioritize cross-namespace helper calls before the actual superclass lifecycle call. Other results remain available in a collapsed section. No candidate is automatically selected. This heuristic is not proof that a call was added to the original app.
- The user-supplied MYT APK previously exceeded the eager method-index limit. The scanner now resolves methods through a bounded per-class cache. The isolated real-APK regression found seven candidates, with exactly the two `MainActivity.onResume` helper calls (`ads.facebook` and `adstst.Start`) prioritized. Removing those two roots changed ten non-header DEX bytes, preserved DEX size/checksums and all five other candidates, and left the source APK unchanged. The APK was not installed or executed.
- Android guards callbacks after Activity destruction or renderer replacement, bounds native background concurrency, releases connection/bitmap resources on failure, and serializes old/new engine service operations. WebView renderer termination now presents a manual recovery screen instead of an automatic reload loop. Installed icons prefer launcher/alias assets and render their enabled drawable state.
- 137 Python tests and 20 JavaScript tests passed. Some Android lifecycle/icon tests are source guards, not instrumentation tests.
- Browser fixture QA: desktop light theme at 1280×720 and mobile dark theme at 390×844; two priority results, one collapsed other result, no initial selection, no horizontal modal overflow, inline acknowledgment error without toast, and successful selection after acknowledgment. The fixture toolbar is not shipped. These checks do not measure physical-device FPS.
- Android release build, signature and alignment verification passed. Windows package smoke test started the local HTTP/HTTPS engine with its toolchain ready in an isolated data directory (about 1.91 seconds). Termux ZIP/source audit passed (35 entries, no runtime-data leakage). All three standard dev.6 output filenames were updated.
- Full Android `lintRelease` is NOT clean: one `QUERY_ALL_PACKAGES` policy error and 22 warnings remain. The broad package-query permission supports the installed-app picker and requires distribution-policy review; it was not removed or suppressed merely to pass lint. Warnings include existing locale, JavaScript-WebView, backup configuration and icon/resource issues, plus untranslated native recovery strings. The successful release build is not a claim that full lint passed.
- The rare app exit and Domino icon rendering were not reproduced on physical hardware. Recovery handling and icon fallback changes are defensive fixes, not confirmation that every reported device-specific failure is resolved. No claim of universal dialog detection or provenance verification is made.

## Follow-up: Domino’s density, scrolling and halo — 2026-09-05

- User supplied Domino’s v8.0.2 (`tr.com.dominos`). Read-only AAPT inspection traced `res/BW.xml` adaptive icon to `res/Qr1.xml`: a 192×192 nodpi foreground PNG inset by a fixed 18dp on every side, over a red 108dp vector background. At density 3, the former 72px bounds yield a 108px adaptive layer minus 108px total horizontal padding: zero foreground width. `verify_dominos_icon.py` records the resource checks and geometry at six densities, with the input hash unchanged. This is geometry analysis, NOT an Android rendering test.
- Renderer now lays out drawable bounds at their intrinsic size and scales the canvas into the same 72×72 output bitmap; launcher/alias preference and bitmap recycling remain. No package-name special case or replacement logo was introduced. The layout reasoning follows Android's [adaptive layer bounds](https://developer.android.com/reference/android/graphics/drawable/AdaptiveIconDrawable.html) and [fixed inset dimensions](https://developer.android.com/reference/android/graphics/drawable/InsetDrawable.html).
- A single cancellable delayed reveal replaces independent `scrollIntoView` timers. Pointer, touch, wheel and keyboard interaction cancel a pending reveal or interrupt its smooth scroll. Reveals affect only the installed-app list, not ancestors. Modern CSS containment bypasses the old blocking modal touchmove listener; the listener remains only for engines without CSS overscroll support. Body scroll locking is unchanged.
- The first halo restoration was superseded twice. The subsequent one-shot teal orbit was incorrect: it reproduced a hand-drawn annotation in the recording. On September 6, inspection of `manager/web/theme.css` inside the retained v0.6.1 Termux archive recovered the actual `ring-breathe` definition: a 2.2-second infinite ease-in-out shadow, 0–12px spread, 0–9% green opacity. The original keyframes and progress-ring animation declaration are now restored directly; neither replacement pseudo-element remains.
- Earlier browser fixture checks covered desktop 1280×720 and mobile 390×844, light/dark appearance, the initial halo (not the later orbit), background/popup pause, no horizontal list overflow, consecutive wheel scrolls advancing list from 457.6 to 889.6 and onward to rows 19–24 while body remained locked. Console errors/warnings were empty. Wheel tests do not reproduce a physical Android finger gesture or measure device FPS.
- Regression suite now includes 138 Python tests and 25 JavaScript tests, including cancellation across repeated gestures, stale reveal replacement, visible/detached rows, legacy touch fallback and halo CSS guards. Android source checks are not instrumentation tests. No connected Android device was available (`adb devices` empty).
- Android release compile/signature/alignment verification passed. Windows HTTP/HTTPS/toolchain smoke test and Termux source/CRC audit passed in isolated test data. Full Android lint findings described in the preceding section are still open; this pass does not claim a lint-clean or guaranteed bug-free stable release.
- The September 5 orbit attempt rebuilt Android and Termux only; Windows still contained the earlier halo. All three require regeneration from the corrected September 6 source. New validation results are recorded below after completion.

## September 6: verified original animation and rebuilt distributions

- Read-only archive comparison confirmed the restored `ring-breathe` keyframes exactly match the retained v0.6.1 source; duration, easing and repeat count also match. The previous documentation's one-shot orbit claim was incorrect and has been corrected above.
- In the local browser fixture at 390×844, light and dark themes showed the expanding translucent green shadow, `ring-breathe`, 2.2s, infinite, with no pseudo-element and no text transform. Background and covering-popup checks both returned `paused`. The final embedded fixture console had no warnings/errors. The earlier desktop fixture emitted a JSON error from its missing mock POST endpoint; this is not evidence of an error in the packaged server. No physical-device FPS claim is made.
- All 138 Python and 25 JavaScript tests passed after the correction. Android release build and signature verification passed. Android package/source equality checks passed as part of the Python suite.
- Windows was rebuilt successfully, and its running HTTP/HTTPS server served UI files matching the current source. Startup smoke check took 1.37s in the isolated test environment; all embedded tools reported ready and the test process shut down cleanly. Termux ZIP source/CRC checks passed (35 entries; no runtime files leaked).
- All three dev.6 outputs now contain the corrected shared UI. Earlier full-lint and physical-device limitations remain as documented; this review covers the recent changes, not every possible device/runtime scenario.
