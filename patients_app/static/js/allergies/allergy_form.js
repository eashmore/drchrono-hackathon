function listenForAllergyUpdate() {
  if ($('#allergy-form').attr('method') === 'PATCH') {
    setAllergyStatus();
  }
  $('#save-allergy-btn').click(handleAllergy);
}

function setAllergyStatus() {
    allergyId = $('#allergy-form').data('allergy');
    $.ajax({
      url: '/api/allergy/' + allergyId + '/',
      type: 'GET',
      success: function(data) {
        status = data[0].fields.status;
        $('#allergy-' + status).attr('selected', true);
      }
    });
}

function handleAllergy(e) {
  $('#save-screen').removeClass('display-none');
  var $form = $('#allergy-form');
  var saveButton = e.currentTarget;
  saveButton.disabled = true;
  if ($form.attr("method") === 'PATCH') {
    e.preventDefault();
    updateAllergy($form, saveButton);
  }
}

function updateAllergy($form) {
  data = $form.serialize();
  allergyId = $form.data('allergy');
  $.ajax({
    url: '/api/allergy/' + allergyId + '/',
    type: 'PATCH',
    data: data,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    success: function() {
      $('#save-allergy-btn').prop('disabled', false);
      $('#success-save').removeClass('display-none');
      $('#save-screen').addClass('display-none');
    },
    error: function() {
      $('#save-allergy-btn').prop('disabled', false);
      $('#error-save').removeClass('display-none');
      $('#save-screen').addClass('display-none');
    }
  });
}

function setActiveNav() {
  $('#nav-allergies').addClass('active');
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
  listenForAllergyUpdate();
  setActiveNav();
})();
