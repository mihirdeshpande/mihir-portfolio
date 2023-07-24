var options_strategy_globals = {};


$(document).ready(function() {
  document.getElementById('generate-strategy-btn').addEventListener('click', get_strategies);
});

function get_strategies() {
  fetch('/options/get_strategies/')
      .then(function (response) {
          return response.json();
      }).then(function (strategies_list) {
          display_strategies(strategies_list); 
      });
}

function display_strategies(strategies_list){
  console.log("Here are the results: ");
  console.log(strategies_list);
}


