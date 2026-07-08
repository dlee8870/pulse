/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          light: "rgba(255,255,255,0.45)",
          dark: "#18181C",
        },
        raised: {
          light: "rgba(255,255,255,0.72)",
          dark: "#222226",
        },
        track: {
          light: "rgba(255,255,255,0.65)",
          dark: "#222226",
        },
        hover: {
          light: "rgba(255,255,255,0.55)",
          dark: "#222226",
        },
        page: {
          light: "rgba(255,255,255,0.30)",
          dark: "#0E0E11",
        },
        accent: {
          light: "#5D63F9",
          dark: "#818CF8",
        },
        ink: {
          DEFAULT: "#0B0B14",
          soft: "#3C4468",
        },
        muted: {
          light: "#5B679D",
          dark: "#9C9CB8",
        },
        faint: {
          light: "#8A93BE",
          dark: "#6A6A66",
        },
      },
      backgroundImage: {
        "page-gradient-light":
          "linear-gradient(180deg, #8FA5F1 0%, #B9C4F3 45%, #DEE4F4 100%)",
        "page-gradient-dark":
          "linear-gradient(135deg, #1A1B2E 0%, #14142B 45%, #0E0E22 100%)",
      },
      fontFamily: {
        sans: [
          "Lato",
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
        card: "16px",
        container: "20px",
      },
    },
  },
  plugins: [],
};