document.addEventListener('DOMContentLoaded', () => {

  // Use the height of the navbar to set the height of the navbar 
  // spacer
  const navbar_height = document.querySelector('.navbar').offsetHeight
  document.querySelector('.navbar-spacer').style.height = navbar_height + 'px'
  document.querySelector('.landing-page-row').style.height = (screen.height - navbar_height - 60) + 'px'

})