/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    './templates/**/*.html',
    './plantblog/extensions.py',
    './plantblog/forms.py'
  ],
  theme: {
    extend: {
      colors: {
        'main-green': '#B0C4B1',
        'pale-white': '#F6F8F2',
      },
      fontFamily: {
        myFont: ['custom', 'sans-serif'],
        noto: ['Noto-serif', 'serif']
      },
    },
    
  },
  plugins: [
    require('daisyui')
  ],
}

