import { Html, Head, Main, NextScript } from "next/document";
//Esto va en el head de la página de bienvenida y la de promoción por fuera de la PWA:
//<meta name="description" content="An app for all tennis players where through artificial intelligence you can analyze your matches and training sessions, use our hawk eye, obtain statistics and improve your skills and game." lang="en"/>
//<meta name="description" content="Una aplicación para todos los tenistas donde a traves de inteligencia artificial podrás analizar tus partidos y entrenamientos, usar nuestro ojo de halcón, obtener estadísticas y mejorar tus habilidades y juego." lang="es"/>


export default function Document() {
  
  return (
    <Html lang="en">
      <Head>
        <meta charSet="utf-8" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta
          name="viewport"
          content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"
        />
        <link rel="manifest" href="/manifest.json" />
        <link rel="icon" href="favicon.ico" type="image/x-icon" />
        <link rel="apple-touch-icon" href="/apple-icon.png"/>
        <meta name="theme-color" content="#317EFB" />
        <meta name="author" content="Ariel Alzogaray Flores, Ary Bacher, Luis Embon Strizzi, Alan Yeger, Guido Zylbersztein"/>
        <meta name="keywords" content="tennis, tenis, AI, IA, entrenamiento de tenis, tennis coaching, tennis training, tennis video analysis, tennis statistics, estadísticas de tenis, ai in tennis, hawkeye, hawk eye, hawk-eye, ojo de halcón, app, aplicación, website, sitio web" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}