// function listenForNewProblem() {
//   $('#new-btn').click(addModel);
// }
//
// function addModel(e) {
//   e.preventDefault();
//
//   $.ajax({
//     url: '/patient/problems/new/',
//     type: 'GET',
//     contentType: 'html',
//     success: function(html) {
//       debugger;
//     }
//   })
// }
//

function setActiveNav() {
  $('#nav-problems').addClass('active');
}

(function() {
  setActiveNav();
  // listenForNewProblem();
})();
