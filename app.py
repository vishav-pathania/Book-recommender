from flask import Flask,render_template,request
import pickle
import numpy as np
import random

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', book_name=list(popular_df['Book-Title'].values), 
                                    author=list(popular_df['Book-Author'].values), 
                                    publisher=list(popular_df['Publisher'].values),
                                    image=list(popular_df['Image-URL-M'].values), 
                                    votes=list(popular_df['num_ratings'].values), 
                                    rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get("user_input")
    # index fetch
    indices = np.where(pt.index == user_input)[0]
    if len(indices) == 0:
        # Return random books if no similar books are found
        random_indices = np.random.choice(len(pt), size=10, replace=False)
        data = []
        for idx in random_indices:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[idx]].drop_duplicates(subset=['Book-Title'])
            item.extend(list(temp_df['Book-Title'].values))
            item.extend(list(temp_df['Book-Author'].values))
            item.extend(list(temp_df['Image-URL-M'].values))
            data.append(item)
        
        print(data)
        return render_template('recommend.html',data=data)

    # if len(indices) == 0:
    #     return []  # Return empty list if book_name is not found in pt.index
    
    index = indices[0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:11]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates(subset=['Book-Title'])
        item.extend(list(temp_df['Book-Title'].values))
        item.extend(list(temp_df['Book-Author'].values))
        item.extend(list(temp_df['Image-URL-M'].values))
        
        data.append(item)

    print(data)
    
    
    return render_template('recommend.html',data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Implement your logic to handle the form submission here

    return 'Message sent successfully'  # You can replace this with a redirect or render_template

if __name__ == '__main__':
    app.run(debug=True)



