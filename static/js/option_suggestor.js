var options_strategy_globals = {};


$(document).ready(function() {
  document.getElementById('generate-strategy-btn').addEventListener('click', get_strategies);
});

function get_strategies() {
  showLoadingOverlay();
  var budget = document.getElementById('user-budget').value;
  var get_strategies_url = `/options/get_strategies?budget=${budget}`;
  fetch(get_strategies_url,
       {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
      }
       )
      .then(function (response) {
          return response.text();
      }).then(function (strategies_html) {
          hideLoadingOverlay();
          display_strategies(strategies_html);
      });
}

function display_strategies(strategies_html){
  document.getElementById('starategy-results-div').innerHTML = strategies_html;
}

function showLoadingOverlay() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.style.opacity = 1;
    loadingOverlay.style.pointerEvents = 'auto';
}

// Function to hide the loading overlay
function hideLoadingOverlay() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.style.opacity = 0;
    loadingOverlay.style.pointerEvents = 'none';
}
