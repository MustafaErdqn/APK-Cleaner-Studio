import type { Metadata } from "next";
import packageInfo from "../package.json";
import "./globals.css";
import "./theme.css";

const themeBootScript = `(() => {
  try {
    const preference = localStorage.getItem("apk-cleaner-theme") || "system";
    const dark = preference === "dark" || (preference === "system" && matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    document.documentElement.dataset.themePreference = preference;
  } catch {}
})();`;

export const metadata: Metadata = {
  metadataBase: new URL("http://localhost:3000"),
  title: `APK Cleaner Studio ${packageInfo.version}`,
  description: "PC ve Termux için yerel APK reklam temizleme ve split paket dönüştürme yöneticisi.",
  icons: {
    icon: [{ url: "/favicon.ico" }, { url: "/favicon.png", type: "image/png", sizes: "512x512" }],
    shortcut: "/favicon.ico",
  },
  openGraph: {
    title: `APK Cleaner Studio ${packageInfo.version}`,
    description: "APK, APKS ve APKM paketlerini yerel olarak temizle ve dönüştür.",
    images: [{ url: "/og.png", width: 1680, height: 945, alt: "APK Cleaner Studio" }],
  },
  twitter: {
    card: "summary_large_image",
    title: `APK Cleaner Studio ${packageInfo.version}`,
    description: "PC ve Termux için yerel APK temizleme ve split dönüştürme yöneticisi.",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="tr" suppressHydrationWarning><head><script dangerouslySetInnerHTML={{ __html: themeBootScript }} /></head><body>{children}</body></html>;
}
