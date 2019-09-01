document.addEventListener('DOMContentLoaded', () => {

  // Minimize logo & darken navbar background when user scrolls down
  window.addEventListener('scroll', () => {
    if (window.scrollY > 0) {
      document.querySelector('.navbar').classList.add('solid-background')
      document.querySelector('.nav-logo-text').classList.add('minimized')
      document.querySelector('.nav-logo-wand-subtext').classList.add('minimized')
      document.querySelector('.nav-logo-wand-subtext-wrapper').classList.add('minimized')
    } else {
      document.querySelector('.navbar').classList.remove('solid-background')
      document.querySelector('.nav-logo-text').classList.remove('minimized')
      document.querySelector('.nav-logo-wand-subtext').classList.remove('minimized')
      document.querySelector('.nav-logo-wand-subtext-wrapper').classList.remove('minimized')
    }
  })


})