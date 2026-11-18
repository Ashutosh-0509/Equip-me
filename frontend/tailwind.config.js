/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FFB400',
          dark: '#E5A000',
          light: '#FFF7E6',
        },
        secondary: '#1C1C1E',
        background: '#F8F9FA',
        surface: '#FFFFFF',
        'surface-subtle': '#F5F5F7',
        'surface-card': '#F5F5F5',
        'text-primary': '#1C1C1E',
        'text-secondary': '#6B7280',
        'text-muted': '#9CA3AF',
        'border-subtle': '#E5E7EB',
        status: {
          green: '#16A34A',
          'green-light': '#DCFCE7',
          warning: '#E67E22',
          'warning-light': '#FEF3C7',
          error: '#D93025',
          'error-light': '#FEE2E2',
          info: '#2563EB',
          'info-light': '#DBEAFE',
        }
      },
      fontFamily: {
        sans: ['Noto Sans', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
