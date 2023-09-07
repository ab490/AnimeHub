from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
anime = pickle.load(open('anime.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home_ui():
    return render_template('home.html',anime_name = list(popular_df['Name'].values),
                           genre=list(popular_df['Genres'].values),
                           image=list(popular_df['Image URL'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

def indx_anime(anime):
    i=0
    while (i<len(pt.index)):
        if anime.lower() in pt.index[i].lower():
            return i
        else:
            i+=1

@app.route('/recommend_anime',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = indx_anime(user_input)
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:8]

    data = []

    matched = []
    df_matched = anime[anime['Name'] == pt.index[index]]
    matched.extend(list(df_matched.drop_duplicates('Name')['Name'].values))
    matched.extend(list(df_matched.drop_duplicates('Name')['Genres'].values))
    matched.extend(list(df_matched.drop_duplicates('Name')['Image URL'].values))

    data.append(matched)

    for i in similar_items:
        item = []
        temp_df = anime[anime['Name'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Name')['Name'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Genres'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Image URL'].values))

        data.append(item)

    if (len(data) != 0):
        print(data)
    else:
        print("anime not available")

    return render_template('recommend.html',data = data)

@app.route('/contact')
def contact_ui():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)