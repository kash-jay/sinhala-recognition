/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sinhala': ['Noto Sans Sinhala', 'sans-serif'], 
      },
      boxShadow: {
        'inner-shadow': 'inset 0 10px 10px -10px rgba(0 0 0 / 0.5)',
      },
      backgroundImage: {
        'black-white-gradient': 'linear-gradient(to bottom, #222831 50%, #EEEEEE 50%)',
      },
    },
  },
  plugins: [],
}

