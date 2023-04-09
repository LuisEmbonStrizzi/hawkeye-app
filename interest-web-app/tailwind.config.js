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
     "sm-sm": ["14px"],
      "base-sm": ["16px"],
      "lg-sm": ["20px"],
      "xl-sm": ["24px"],
      "2xl-sm": ["32px"],
      "3xl-sm": ["40px"],
      "4xl-sm": ["48px"],
      "5xl-sm": ["64px"],
    },
    fontFamily: {
      sans: ["var(--font-sans)"],
      clash: ["var(--font-clash)"],
    },
    extend: {},
  },
  plugins: [],
};