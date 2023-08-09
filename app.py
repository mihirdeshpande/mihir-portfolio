from flask import Flask, render_template, request

from server_code.options.get_strategies import get_strategies
from server_code.utils.utils import get_est_now

app = Flask(__name__)


@app.route("/")
def render_home():
    return render_template('home.html')


@app.route("/options/")
def render_options():
    return render_template('options_suggestor.html')


@app.route("/options/get_strategies", methods=['GET'])
def fetch_strategies():
    budget = int(request.args.get('budget'))
    strategies = get_strategies(budget)
    if strategies:
        return render_template(
            'options_strategies_results.html',
            strategies=strategies,
            generated_at=get_est_now().strftime("%m/%d/%Y %I:%M:%S %p"))
    return render_template('options_no_results.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
