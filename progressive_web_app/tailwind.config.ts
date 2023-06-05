import { type Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        'hawkeye' : ['var(--font-hawkeye)']
      },
    },
  },
  plugins: [],
} satisfies Config;
