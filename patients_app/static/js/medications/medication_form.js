function listenForMedicationUpdate() {
  if ($('#medication-form').attr('method') === 'PATCH') {
    setMedicationStatus();
  }
  $('#save-meds-btn').click(handleMedication);
}

function setMedicationStatus() {
    medicationId = $('#medication-form').data('medication');
    $.ajax({
      url: '/api/medication/' + medicationId + '/',
      type: 'GET',
      success: function(data) {
        status = data[0].fields.status;
        $('#medication-' + status).attr('selected', true);
      }
    });
}

function handleMedication(e) {
  $('#save-screen').removeClass('display-none');
  var $form = $('#medication-form');
  var saveButton = e.currentTarget;
  saveButton.disabled = true;
  if ($form.attr("method") === 'PATCH') {
    e.preventDefault();
    updateMedication($form, saveButton);
  }
}

function updateMedication($form) {
  data = $form.serialize();
  data += dawJson();
  data += prnJson();
  medicationId = $form.data('medication');
  $.ajax({
    url: '/api/medication/' + medicationId + '/',
    type: 'PATCH',
    data: data,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    success: function() {
      $('#save-meds-btn').prop('disabled', false);
      $('#success-save').removeClass('display-none');
      $('#save-screen').addClass('display-none');
    },
    error: function() {
      $('#save-meds-btn').prop('disabled', false);
      $('#error-save').removeClass('display-none');
      $('#save-screen').addClass('display-none');
    }
  });
}

function dawJson() {
  var checked = $('.daw-checkbox').attr('checked');
  if (checked) {
    return '&daw=false';
  }
  return '&daw=true';
}

function prnJson(data) {
  var checked = $('.prn-checkbox').attr('checked');
  if (checked) {
    return '&prn=false';
  }
  return '&prn=true';
}

function setActiveNav() {
  $('#nav-meds').addClass('active');
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
  setActiveNav();
  listenForMedicationUpdate();
})();
