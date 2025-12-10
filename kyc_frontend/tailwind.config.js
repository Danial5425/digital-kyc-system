/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        hdfcBlue: "#004C8F",
        hdfcRed: "#E31837",
        hdfcLight: "#F3F6FA",
      },
    },
  },
  plugins: [],
};


