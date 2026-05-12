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
          light: "#5B5FE5",
          dark: "#818CF8",
        },
        muted: {
          light: "#6B6FB8",
          dark: "#9C9CB8",
        },
      },
      backgroundImage: {
        "page-gradient-light":
          "linear-gradient(135deg, #C8CFFF 0%, #DDE2FF 45%, #F0F2FF 100%)",
        "page-gradient-dark":
          "linear-gradient(135deg, #1A1B2E 0%, #14142B 45%, #0E0E22 100%)",
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