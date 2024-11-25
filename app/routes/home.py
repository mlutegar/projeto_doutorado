import os
from flask import Blueprint, render_template, request
from src.util.nome_file import process_files

home_bp = Blueprint('home', __name__, url_prefix='/')

ZIP_DIR = 'data'

@home_bp.route('/', methods=['GET'])
def home():
    all_files = [f for f in os.listdir(ZIP_DIR) if f.endswith('.xlsx')]
    filter_date = request.args.get('date')

    filtered_files = [file for file in all_files if filter_date in file.split('_')[1]] if filter_date else all_files
    processed_files = process_files(filtered_files)

    return render_template('home.html', processed_files=processed_files)
