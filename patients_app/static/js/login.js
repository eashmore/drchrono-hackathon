function showLoadingScreen() {
  $('#loading-text').html('Loading Patient Data');
  $('#save-screen').removeClass('display-none');
}

(function() {
  $('#doctor-signin-btn').click(showLoadingScreen);
})();
