 document.addEventListener('DOMContentLoaded', () => {
   
  // If screen not too short, hide the contact form so that it doesn't
  // bleed over into the next section
  const contact_form_wrapper = document.querySelector('.contact-form-wrapper')
  const navbar = document.querySelector('.navbar')
  const landing_page_footer = document.querySelector('.landing-page-footer')
  
  if (contact_form_wrapper.offsetHeight > window.innerHeight - (navbar.offsetHeight + landing_page_footer.offsetHeight + 60)) {
    contact_form_wrapper.style.display = 'none'
  } else {
    //
  }
}) 