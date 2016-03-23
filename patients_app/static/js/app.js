function listenForPatientUpdate() {
  $('#update-patient-btn').click(updatePatient);
}

function updatePatient(e) {
  e.preventDefault();
  var saveButton = e.currentTarget;
  saveButton.disabled = true;
  var $form = $('#patient-update-form');
  var token = getToken($form.data('user'), $form.data('patient'));
}

function getToken(user_id, patient_id) {
  $.ajax({
    url: '/api/doctor/' + user_id + '/',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      var token = data.fields.token;
      // updateLocalPatient(token, $form);
      updateDrchornoPatient(token, patient_id);
    }
  });
}

function updateDrchornoPatient(token, patient_id) {
  $.ajax({
    // xhrFields: {
    //   withCredentials: true
    // },
    // crossSite: true,
    url: 'https://drchrono.com/api/' + patient_id + '/',
    type: 'PATCH',
    contentType: 'application/json',
    // headers: {'Authorization': 'Bearer ' + token,
    // 'Access-Control-Allow-Origin': 'https://drchrono.com/'},
    // headers: {'Access-Control-Allow-Origin': '*',
    //   'Access-Control-Allow-Methods': 'PATCH',
      // 'Content-Type': 'application/json'},
    beforeSend: function(xhr) {
      xhr.setRequestHeader('Authorization', 'Bearer ' + token);
    //   xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    //   xhr.setRequestHeader('Content-Type', 'application/json');
    //   xhr.setRequestHeader('Access-Control-Allow-Methods', 'PATCH');
    },
    success: function(data) {
      debugger;
    }
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
  // listenForPatientUpdate();
})();
