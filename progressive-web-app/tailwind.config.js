/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",

    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    colors: {
      //Blues
      "blue-1": "#090E1C",
      "blue-2": "#131826",
      "blue-3": "#171C2C",
      "blue-4": "#1E263A",

      //Greys
      "grey-1": "#707FA4",
      "grey-2": "#A0AED1",
      "grey-3": "#C4CCE0",

      //Whites
      "white-1": "#E6E6E6",
      "white-2": "#DADADA",

      //Brands
      "brand-1": "#41C683",
      "brand-2": "#4ECB71",
    },
    fontSize: {
      //Small devices (sm)
      "sm-sm": ["14px", "17.7px"],
      "base-sm": ["16px", "20.2px"],
      "lg-sm": ["20px", "25.3px"],
      "xl-sm": ["24px", "30.4px"],
      "2xl-sm": ["32px", "40.5px"],
      "3xl-sm": ["40px", "51px"],
      "4xl-sm": ["48px", "61px"],
      //Large devices (lg)
      "sm-lg": ["16px", "20.2px"],
      "base-lg": ["20px", "25.3px"],
      "lg-lg": ["24px", "30.4px"],
      "xl-lg": ["32px", "40.5px"],
      "2xl-lg": ["40px", "51px"],
      "3xl-lg": ["48px", "61px"],
      "4xl-lg": ["64px", "81px"],
    },
    fontFamily: {
      sans: ["var(--font-circularstd)"],
    },
    extend: {},
  },
  plugins: [],
};