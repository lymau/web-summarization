from flask import Blueprint, render_template, request, flash, jsonify
from .summarization import summarize, calculate_rouge
import json


# Routing
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        text = request.form.get('source')

        if len(text) < 1:
            flash('Text is too short!', category='error')
        else:
            result = summarize(text)
            summary = result['summary']
            len_text = result['len_text']
            len_summary = result['len_summary']
            rouge = calculate_rouge(text, summary)

            flash('Text has been summarized', category='success')
            return render_template('home.html', summary=summary, text=text, len_text=len_text, len_summary=len_summary,  rouge=rouge)

    return render_template('home.html')


@views.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
