import '../styles/globals.css';
import { AppProps } from 'next/app';
//import Layout from 'dirección x' <-- componente
//import { appWithTranslation } from "next-i18next";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Component {...pageProps} />
    </>
  )
}
