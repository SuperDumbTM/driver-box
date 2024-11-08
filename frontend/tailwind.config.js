/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      // palette: https://colorhunt.co/palette/dff2ebb9e5e87ab2d34a628a
      colors: {
        'apple-green': {
          DEFAULT: '#DFF2EB',
          50: '#FFFFFF',
          100: '#FFFFFF',
          200: '#FFFFFF',
          300: '#FFFFFF',
          400: '#FCFEFD',
          500: '#DFF2EB',
          600: '#B7E2D2',
          700: '#8FD2B9',
          800: '#67C1A0',
          900: '#46AB86',
          950: '#3D9776'
        },
        'powder-blue': {
          DEFAULT: '#B9E5E8',
          50: '#FFFFFF',
          100: '#FFFFFF',
          200: '#FFFFFF',
          300: '#F6FCFC',
          400: '#D8F0F2',
          500: '#B9E5E8',
          600: '#8FD5DA',
          700: '#65C6CC',
          800: '#3EB3BB',
          900: '#308B91',
          950: '#29777C'
        },
        'half-baked': {
          DEFAULT: '#7AB2D3',
          50: '#FFFFFF',
          100: '#F5F9FC',
          200: '#D6E7F1',
          300: '#B7D5E7',
          400: '#99C4DD',
          500: '#7AB2D3',
          600: '#509AC5',
          700: '#377DA6',
          800: '#295D7C',
          900: '#1B3D52',
          950: '#142E3D'
        },
        'kashmir-blue': {
          DEFAULT: '#4A628A',
          50: '#B5C1D7',
          100: '#A7B7D0',
          200: '#8DA1C2',
          300: '#728BB3',
          400: '#5875A5',
          500: '#4A628A',
          600: '#364865',
          700: '#232E41',
          800: '#0F141C',
          900: '#000000',
          950: '#000000'
        }
      }
    }
  },
  plugins: []
}
