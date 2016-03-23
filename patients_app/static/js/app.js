function listenForProblemUpdate() {
  setProblemStatus();
  $('#save-problem-btn').click(handleProblem);
}

function setProblemStatus() {
    problemId = $('#problem-form').data('problem');
    $.ajax({
      url: '/api/problem/' + problemId + '/',
      type: 'GET',
      success: function(data) {
        status = data[0].fields.status;
        $('#problem-' + status).attr('selected', true);
      }
    });
}

function handleProblem(e) {
  e.preventDefault();
  var saveButton = e.currentTarget;
  saveButton.disabled = true;
  var $form = $('#problem-form');
  if ($form.attr("method") === 'PATCH') {
    updateProblem($form, saveButton);
  } else {
    createProblem($form, saveButton);
  }
}

function updateProblem($form, button) {
  data = $form.serialize();
  problemId = $form.data('problem');
  $.ajax({
    url: '/api/problem/' + problemId + '/',
    type: 'PATCH',
    data: data,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    success: function() {
      button.disabled = false;
    }
  });
}

function createProblem($form, button) {
  data = $form.serialize();
  $.ajax({
    url: '/api/problems/',
    type: 'POST',
    data: data,
    header: {"X-CSRFToken": getCookie('csrftoken')},
    // success: function() {
    //   saveButton.disabled = false;
    // }
  });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                                cookie.substring(name.length + 1)
                              );
                break;
            }
        }
    }
    return cookieValue;
}

(function() {
  listenForProblemUpdate();
})();
