/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#080b10",
        cardBg: "rgba(17, 24, 39, 0.7)",
        cardBorder: "rgba(255, 255, 255, 0.08)",
        brand: {
          purple: "#7c3aed",
          pink: "#db2777",
          cyan: "#06b6d4",
          emerald: "#059669",
        }
      },
      fontFamily: {
        sans: ["Outfit", "Inter", "sans-serif"],
      },
      boxShadow: {
        glass: "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        glow: "0 0 15px rgba(124, 58, 237, 0.5)",
      }
    },
  },
  plugins: [],
}
