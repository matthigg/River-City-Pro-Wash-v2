document.addEventListener('DOMContentLoaded', () => {

  // Minimize logo & darken navbar background when user scrolls down
  window.addEventListener('scroll', () => {
    if (window.scrollY > 0 && window.innerWidth >= 768) {
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

  // User clicked 'Call Now' button -- call phone number
  document.querySelector('.nav-call-now-button').addEventListener('click', () => {
    gtag('event', 'click_call_button', {
      'event_category': 'engagement',
      'event_label': 'User clicked the call button to make a phone call',
      'value': '50',
      'event_callback': function() {
        window.open('tel:+1-804-239-6085', '_self')
      },
    });
  })

  // User clicked 'FREE Quote' button -- go to contact page
  document.querySelector('.nav-free-quote-button').addEventListener('click', (event) => {
    gtag('event', 'click_free_quote_button', {
      'event_category': 'engagement',
      'event_label': 'User clicked the free quote button to go to the Contact Us page',
      'value': '0',
      'event_callback': function() {
        window.open(window.location.origin + event.target.dataset.url, '_self')
      },
    });
  })

})