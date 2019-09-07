document.addEventListener('DOMContentLoaded', () => {
  
  // Show 'FREE Quote' button
  if (window.innerWidth < 768) {
    document.querySelector('.nav-free-quote').style.display = 'block'
  }

  // Modals
  //
  // When a <div> .section-1-baap-group element or any of its children (all of 
  // which are located in ourwork.html and together represent a 'before & after'
  // picture group) are clicked, search/scrounge for the appropriate data-id
  // attribute's value, which identifies that particular 'before & after' picture
  // group. This data-id value is then used to construct the before & after <img>
  // src attributes in the re-usable Bootstrap modal HTML markup located in 
  // ourwork-modals.html. 
  //
  // Additionally, this JavaScript will scrounge for the relative static img path 
  // (ie. /static/img/...) which is stored as data-src in the same HTML element 
  // as the data-id, and the data-src attribute's value, together with the data-id 
  // attribute's value is then used to construct a path to the before & after 
  // images that we're looking for.
  const baap_groups = document.querySelectorAll('.our-work-baap-group');
  baap_groups.forEach((baap_group) => {
    baap_group.addEventListener('click', (event) => {
      let element = event.target;
      if (element.dataset.category === undefined) {
        while (element.parentNode) {
          element = element.parentNode;
          if (element.dataset.category) {
            console.log(element.dataset)
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

    console.log(before_src, after_src)

    document.querySelector('.modal-baap-group-img-before').src = before_src
    document.querySelector('.modal-baap-group-img-after').src = after_src

    // const img_src_before = src + '/' + id + '-before.jpg';
    // const img_src_after = src + '/' + id + '-after.jpg';            
    // document.querySelector('.modal-baap-group-img-before').src = img_src_before;
    // document.querySelector('.modal-baap-group-img-after').src = img_src_after;
  }
})