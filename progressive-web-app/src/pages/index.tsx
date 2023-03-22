import Head from 'next/head'

export default function Home() {
  return (
    <>
      <Head>
        <title>My analysis</title>
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <meta name="description" content="Search among your analyzed videos whether they are matches or training sessions." lang='en' />
        <meta name="description" content="Busca entre tus videos analizados ya sean partidos o entrenamientos." lang='es' />
      </Head>
      <div>Hawkeye PWA</div>
    </>
  );
}
