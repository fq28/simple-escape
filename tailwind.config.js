/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{html,js,svelte,ts}", // Include all Svelte and JS files
      "./static/**/*.html", // Include static files
    ],
    theme: {
      extend: {
        extend: {
            animation: {
              shake: "shake 0.5s ease-in-out",
              particles: "particles 0.7s ease-out", // Add particles animation
            },
            keyframes: {
              shake: {
                "0%, 100%": { transform: "translateX(0)" },
                "25%": { transform: "translateX(-5px)" },
                "50%": { transform: "translateX(5px)" },
              },
              particles: {
                "0%": { opacity: "0", transform: "translateY(10px) scale(0.95)" },
                "100%": { opacity: "1", transform: "translateY(0) scale(1)" },
              },
            },
          },
        },
    },
    plugins: [
      require('@tailwindcss/forms'), // Optional Tailwind plugins
      require('tailwindcss-animate'), // Add this for animations
    ],
  };
  