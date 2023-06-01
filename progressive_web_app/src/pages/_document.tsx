import { Html, Head, Main, NextScript } from 'next/document';

const Document = () => (
    <Html lang="en">
        <Head>
            <link rel="icon" href="/favicon.ico" />
            <meta name="description" content="Hawkeye" />
            <link rel="manifest" href="/manifest.json" />
        </Head>
        <body>
            <Main />
            <NextScript />
        </body>
    </Html>
);

export default Document;