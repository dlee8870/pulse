/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        page: {
          light: "#FAFAF9",
          dark: "#0E0E11",
        },
        surface: {
          light: "#FFFFFF",
          dark: "#18181C",
        },
        track: {
          light: "#EEEEEC",
          dark: "#222226",
        },
        hover: {
          light: "#F4F4F3",
          dark: "#222226",
        },
        accent: {
          light: "#4F46E5",
          dark: "#818CF8",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Consolas",
          "monospace",
        ],
      },
      letterSpacing: {
        tightish: "-0.01em",
        tightest: "-0.02em",
      },
      borderRadius: {
        card: "8px",
        container: "10px",
      },
    },
  },
  plugins: [],
};