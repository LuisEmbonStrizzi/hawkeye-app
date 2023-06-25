import { type Session } from "next-auth";
import { SessionProvider } from "next-auth/react";
import { type AppType } from "next/app";
import { api } from "~/utils/api";
import "~/styles/globals.css";
import { Plus_Jakarta_Sans } from "@next/font/google";
import { Toaster } from "react-hot-toast";

const sans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-hawkeye",
});

const MyApp: AppType<{ session: Session | null }> = ({
  Component,
  pageProps: { session, ...pageProps },
}) => {
  return (
    <SessionProvider session={session}>
      <div className={`${sans.variable} font-hawkeye`}>
        <Component {...pageProps} />
        <Toaster
          position="top-center"
          toastOptions={{
            error: {
              icon: (
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M9.9956 14C10.2069 14 10.3854 13.9285 10.5312 13.7856C10.6771 13.6427 10.75 13.4656 10.75 13.2544C10.75 13.0431 10.6785 12.8646 10.5356 12.7188C10.3927 12.5729 10.2156 12.5 10.0044 12.5C9.79313 12.5 9.61458 12.5715 9.46875 12.7144C9.32292 12.8573 9.25 13.0344 9.25 13.2456C9.25 13.4569 9.32145 13.6354 9.46435 13.7812C9.60727 13.9271 9.78435 14 9.9956 14ZM9.25 11H10.75V6H9.25V11ZM10.0058 18C8.9047 18 7.86806 17.7917 6.89583 17.375C5.92361 16.9583 5.07292 16.3854 4.34375 15.6562C3.61458 14.9271 3.04167 14.0767 2.625 13.105C2.20833 12.1334 2 11.0952 2 9.99046C2 8.88571 2.20833 7.85069 2.625 6.88542C3.04167 5.92014 3.61458 5.07292 4.34375 4.34375C5.07292 3.61458 5.92332 3.04167 6.89496 2.625C7.86661 2.20833 8.90481 2 10.0095 2C11.1143 2 12.1493 2.20833 13.1146 2.625C14.0799 3.04167 14.9271 3.61458 15.6562 4.34375C16.3854 5.07292 16.9583 5.92169 17.375 6.89008C17.7917 7.85849 18 8.89321 18 9.99425C18 11.0953 17.7917 12.1319 17.375 13.1042C16.9583 14.0764 16.3854 14.9271 15.6562 15.6562C14.9271 16.3854 14.0783 16.9583 13.1099 17.375C12.1415 17.7917 11.1068 18 10.0058 18ZM10 16.5C11.8056 16.5 13.3403 15.8681 14.6042 14.6042C15.8681 13.3403 16.5 11.8056 16.5 10C16.5 8.19444 15.8681 6.65972 14.6042 5.39583C13.3403 4.13194 11.8056 3.5 10 3.5C8.19444 3.5 6.65972 4.13194 5.39583 5.39583C4.13194 6.65972 3.5 8.19444 3.5 10C3.5 11.8056 4.13194 13.3403 5.39583 14.6042C6.65972 15.8681 8.19444 16.5 10 16.5Z"
                    className="fill-other-error"
                  />
                </svg>
              ),
            },
            style: {
              border: "1px solid #32394D",
              padding: "10px",
              background: "rgba(32, 36, 51, 0.75)",
              color: "#E2E8F5",
              borderRadius: "6px",
              fontSize: "14px",
              backdropFilter: "blur(8px)",
              width: "fit-content",
            },
          }}
        />
      </div>
    </SessionProvider>
  );
};

export default api.withTRPC(MyApp);
