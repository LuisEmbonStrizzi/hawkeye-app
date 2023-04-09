import '@/styles/globals.css'
import localFont from "next/font/local";
import type { AppProps } from 'next/app'
import { appWithTranslation } from 'next-i18next'

const sans = localFont({
  src: "../../public/fonts/sans.ttf",
  variable: "--font-sans",
});

const clash = localFont({
  src: "../../public/fonts/clash.ttf",
  variable: "--font-clash",
});

function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <style jsx global>{`
        :root {
          --font-sans: ${sans.style.fontFamily};
          --font-clash: ${clash.style.fontFamily};
        }
      `}</style>
      <Component {...pageProps} />
    </>
  );
}

export default appWithTranslation(App);
