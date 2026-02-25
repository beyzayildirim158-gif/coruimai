/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        /* Corium.ai Brand Colors */
        background: '#FFFFFF',
        surface: '#F8F9FA',
        primary: {
          DEFAULT: '#FF4D00',
          50: '#FFF5F0',
          100: '#FFE6DB',
          200: '#FFCDB8',
          300: '#FFB494',
          400: '#FF9B71',
          500: '#FF824D',
          600: '#FF4D00',
          700: '#CC3D00',
          800: '#992E00',
          900: '#661F00',
        },
        trust: {
          DEFAULT: '#007BFF',
          light: '#E6F2FF',
        },
        warning: {
          DEFAULT: '#D00000',
          light: '#FFE6E6',
        },
        text: {
          primary: '#0A0A0A',
          secondary: '#1A1A1A',
          muted: '#6B7280',
        },
      },
      fontFamily: {
        sans: ['Space Grotesk', 'Sora', 'system-ui', 'sans-serif'],
        display: ['Space Grotesk', 'Sora', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gradient': 'gradient 8s ease infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      backgroundSize: {
        '200%': '200% 200%',
      },
    },
  },
  plugins: [],
};
