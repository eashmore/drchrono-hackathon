function showLoadingScreen() {
  $('#loading-text').html('Sending');
  $('#save-screen').removeClass('display-none');
}

(function() {
  $('#nav-message').addClass('active');
  $('#message-btn').click(showLoadingScreen);
})();
