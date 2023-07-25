var options_strategy_globals = {};


$(document).ready(function() {
  document.getElementById('generate-strategy-btn').addEventListener('click', get_strategies);
});

function get_strategies() {
  fetch('/options/get_strategies/')
      .then(function (response) {
          return response.text();
      }).then(function (strategies_html) {
          display_strategies(strategies_html); 
      });
}

function display_strategies(strategies_html){
  document.getElementById('starategy-results-div').innerHTML = strategies_html;
}


