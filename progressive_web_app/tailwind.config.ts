import { type Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        'hawkeye' : ['var(--font-hawkeye)']
      },
      fontSize: {
        'h1': '48px',
        'h2': '36px',
        'h3': '24px',
        'h4': '20px',
        'lg': '18px',
        'base': '16px',
        'sm': '14px',
      },
      colors: {
        background:{
          DEFAULT: '#181B27',
          border: '#1F2331',
        },
        foreground:{
          DEFAULT: '#8A91A8',
          important: '#E2E8F5',
        },
        primary:{
          DEFAULT: '#4ECB71',
        },
        secondary: {
          foreground: '#596585',
          background: '#1C202E',
          border: '#2A3144',
        },
        tertiary: {
          background: '#202433',
          hover: '#282E3E',
          border: '#32394D',
        },
        muted: {
          foreground: '#1F2331',
          background: '#1C202E',
        }
      },
      backdropBlur: {
        DEFAULT: '16px',
      }
    },
  },
  plugins: [],
} satisfies Config;
