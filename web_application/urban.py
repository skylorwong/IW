import flask
import data
import visualizations as vis
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
import numpy as np
import pandas as pd

app = flask.Flask(__name__, template_folder='.')
#urban_dict_data = data.get_data()
#date_df = data.get_date_df(urban_dict_data)
#date_df_all = data.get_date_df_all(urban_dict_data)
#trends_df = data.get_trends_df(urban_dict_data)
#slang = []
#for key in urban_dict_data:
  #slang.append(key)
#pca = data.run_pca(slang)
pca = None

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.route('/linguistics', methods=['GET'])
def linguistics():
    urban_dict_data = data.get_data()
    slang = []
    for key in urban_dict_data:
        slang.append(key)
    non_slang = data.get_non_slang()
    scripts, divs = vis.get_linguistics_graphs(slang, non_slang)
    html_code = flask.render_template('linguistics.html', scripts=scripts, divs=divs)
    response = flask.make_response(html_code)
    return response

@app.route('/social', methods=['GET'])
def social():
    urban_dict_data = data.get_data()
    slang = []
    for key in urban_dict_data:
        slang.append(key)
    scripts, divs, graph = vis.get_social_graphs(urban_dict_data, slang, pca)
    html_code = flask.render_template('social.html', scripts=scripts, divs=divs, graph=graph)
    response = flask.make_response(html_code)
    return response

@app.route('/sentimentemotion', methods=['GET'])
def sentimentemotion():
    urban_dict_data = data.get_data()
    scripts, divs = vis.get_sentimentemotion_graphs(urban_dict_data)
    html_code = flask.render_template('sentimentemotion.html', scripts=scripts, divs=divs)
    response = flask.make_response(html_code)
    return response

@app.route('/trends', methods=['GET'])
def trends():
    urban_dict_data = data.get_data()
    dates_df = data.get_date_df_all(urban_dict_data)
    dates2_df = data.get_date2(urban_dict_data)
    scripts, divs = vis.get_trends_graphs(dates_df, dates2_df)
    html_code = flask.render_template('trends.html', scripts=scripts, divs=divs)
    response = flask.make_response(html_code)
    return response

@app.route('/search', methods=['GET'])
def search():
    urban_dict_data = data.get_data()
    search = flask.request.args.get('search', '')
    info_bool = False
    info = ""
    scripts = {}
    divs = {}
    nearest = []
    if search != '':
        if urban_dict_data.get(search) is not None:
            info_bool = True
            info = urban_dict_data.get(search)
            scripts, divs = vis.get_search_graphs(info)
            nearest = data.get_nearest(search)
        else:
            info = f"No information for {search}."
    html_code = flask.render_template('search.html', scripts=scripts, divs=divs, search=search, info_bool=info_bool, info=info, nearest=nearest)
    response = flask.make_response(html_code)
    return response

@app.route('/sentimenttrends', methods=['GET'])
def sentimenttrends():
    urban_dict_data = data.get_data()
    df = data.get_date2(urban_dict_data)
    graph = vis.get_sentiment_trends_graphs(df)
    html_code = flask.render_template('sentimenttrends.html', graph=graph)
    response = flask.make_response(html_code)
    return response

@app.route('/emotiontrends', methods=['GET'])
def emotiontrends():
    urban_dict_data = data.get_data()
    df = data.get_date2(urban_dict_data)
    graph = vis.get_emotion_trends_graphs(df)
    html_code = flask.render_template('emotiontrends.html', graph=graph)
    response = flask.make_response(html_code)
    return response