(() => {
  try {
    const query = new URLSearchParams(location.search);
    const preference = localStorage.getItem("apk-cleaner-theme") || "system";
    const embedded = query.get("embedded") === "android";
    const nativeTheme = query.get("nativeTheme");
    const systemDark = embedded && nativeTheme
      ? nativeTheme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    const dark = preference === "dark" || (preference === "system" && systemDark);
    const secure = location.protocol === "https:";
    if (secure) sessionStorage.setItem("apk-cleaner-trusted-https", "1");
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    document.documentElement.dataset.themePreference = preference;
    document.documentElement.dataset.secure = secure ? "true" : "false";
    document.documentElement.dataset.embedded = embedded ? "android" : "web";
    document.documentElement.style.colorScheme = dark ? "dark" : "light";
  } catch {}
  setTimeout(() => {
    document.documentElement.classList.remove("ui-boot");
    document.documentElement.classList.add("ui-ready");
  }, 800);
})();

(() => {
  if (location.protocol !== "http:" || document.documentElement.dataset.embedded === "android") return;
  let probing = false;
  const tryTrustedHttps = async () => {
    if (probing || location.protocol !== "http:") return;
    probing = true;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 2200);
    try {
      const secureUrl = `https://${location.host}/api/status?tls_probe=1`;
      const response = await fetch(secureUrl, { cache: "no-store", mode: "cors", signal: controller.signal });
      if (response.ok) {
        sessionStorage.setItem("apk-cleaner-trusted-https", "1");
        location.replace(`https://${location.host}${location.pathname}${location.search}${location.hash}`);
      }
    } catch {} finally {
      clearTimeout(timer);
      probing = false;
    }
  };
  tryTrustedHttps();
  addEventListener("focus", tryTrustedHttps);
  addEventListener("pageshow", tryTrustedHttps);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) tryTrustedHttps(); });
})();
