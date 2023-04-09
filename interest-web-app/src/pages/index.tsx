import Image from 'next/image'
import { serverSideTranslations } from "next-i18next/serverSideTranslations";
import type { GetStaticProps} from 'next'
import { useTranslation } from "next-i18next";
import Head from 'next/head';

type Props = {};

export default function Home() {

  const { t } = useTranslation("common");

  return (
    <>
      <Head>
        <title>Hawkeye Project</title>
      </Head>
      <main>
        <h1 className="font-clash text-3xl-sm">{t("title")}</h1>
        <p className="font-sans text-base-sm">{t("subtitle")}</p>
      </main>
    </>
  );
};

export const getStaticProps: GetStaticProps<Props> = async ({
  locale,
}) => ({
  props: {
    ...(await serverSideTranslations(locale ?? "en", ["common"])),
  },
});
