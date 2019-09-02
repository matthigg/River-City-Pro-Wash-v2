document.addEventListener('DOMContentLoaded', () => {
  
  // Show 'FREE Quote' button
  if (window.innerWidth < 768) {
    document.querySelector('.nav-free-quote').style.display = 'block'
  }

  // Hide contact form if screen is too small so that it doesn't
  // bleed into the next section
  // const contact_form = document.querySelector('.contact-form-wrapper')
  // const navbar = document.querySelector('.navbar')
  // const landing_page_footer = document.querySelector('.landing-page-footer')
  // if (contact_form.offsetHeight > window.innerHeight - (navbar.offsetHeight + landing_page_footer.offsetHeight + 60)) {
  //   contact_form.style.display = "none"
  // } 
})