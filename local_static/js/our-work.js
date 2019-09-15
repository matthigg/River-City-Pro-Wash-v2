// Modals
//
// Add a 'click' event listener to each 'before-and-after' group of images that
// looks for a data-category attribute and, if it finds one, grabs the before &
// after image URL's, hosted on AWS S3, and sends them to the modal template for
// display.

document.addEventListener('DOMContentLoaded', () => {

  const baap_groups = document.querySelectorAll('.our-work-baap-group');
  console.log(baap_groups)
  baap_groups.forEach((baap_group) => {
    baap_group.addEventListener('click', (event) => {
      let element = event.target;
      if (element.dataset.category === undefined) {
        while (element.parentNode) {
          element = element.parentNode;
          if (element.dataset.category) {
            assignModalBAAPImage(element.dataset.beforeSrc, element.dataset.afterSrc);
            return
          } 
        }
      } else {
        assignModalBAAPImage(element.dataset.beforeSrc, element.dataset.afterSrc);
      }
    })
  })
  function assignModalBAAPImage(before_src, after_src) {
    console.log('x')
    document.querySelector('.modal-baap-group-img-before').src = before_src
    document.querySelector('.modal-baap-group-img-after').src = after_src
  }

})
