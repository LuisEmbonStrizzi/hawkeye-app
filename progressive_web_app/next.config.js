// eslint-disable-next-line @typescript-eslint/no-var-requires
const withPWA = require("next-pwa")({
  dest: "public",
  register: true,
  skipWaiting: true,
  /* 
    Deshabilitar la PWA en desarrollo pero habilitarla en producción. Para evitar sobrecarga en la consola.
  */

  disable: process.env.NODE_ENV === "development",
  // register: true,
  // scope: '/app',
  // sw: 'service-worker.js',
  //...
});

module.exports = withPWA({
  reactStrictMode: true,
  i18n: {
    locales: ["en"],
    defaultLocale: "en",
  },
  images: {
    domains: ["storage.googleapis.com", "storage.cloud.google.com"],
  },
  output: "standalone",
});
