from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video.db'
db = SQLAlchemy(app)
ApiKeyYoutube = 'ВАШ_КЛЮЧ_API'
Googleurl = 'https://www.googleapis.com/youtube/v3/'


class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    channelid = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(512))

    def __init__(self, channelid=None, name=None):
        self.channelid = channelid
        self.name = name


class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    videoid = db.Column(db.String(250), unique=True)

    def __init__(self, videoid=None):
        self.videoid = videoid

# db.drop_all()
db.create_all()


@app.route('/', methods=['GET', 'POST'])
def channels():
    if request.method == 'POST':
        channelid = request.form['url'].split("/channel/")[-1]
        apiurl = Googleurl + 'channels?part=snippet&id=' + \
            channelid + '&key=' + ApiKeyYoutube
        j = requests.get(apiurl).json()
        name = j['items'][0]['snippet']['title']
        me = Channel(channelid, name)
        db.session.add(me)
        db.session.commit()

    return render_template("channels.html", rows=Channel.query.all())


@app.route('/channel-videos-list/<channelid>/<page>/')
def video_list(channelid, page):
    apiurl = Googleurl + 'search?part=snippet&channelId=' + channelid + \
        '&key=' + ApiKeyYoutube + '&maxResults=9&order=date&type=video'
    if page != 'first_page':  # Навигация по страничкам канала
        apiurl = apiurl + '&pageToken=' + page
    j = requests.get(apiurl).json()
    n = 0
    for i in j['items']:
        videoid = j['items'][n]['id']['videoId']
        v = Video.query.filter(Video.videoid == videoid).first()
        if v:
            j['items'][n]['viwed'] = 1
        n += 1
    channel_name = Channel.query.filter(Channel.channelid == channelid).first()
    return render_template("video_list.html", allinfo=j, namec=channel_name)


@app.route('/view-video/<channelid>/<videoid>/')
def view_video(channelid, videoid):
    channel_name = Channel.query.filter(Channel.channelid == channelid).first()
    v = Video.query.filter(Video.videoid == videoid).first()
    return render_template("view_video.html", namec=channel_name, idv=videoid,
                           v=v)


@app.route('/_viwed')
def _viwed():
    videoid = request.args.get('videoid')
    me = Video(videoid)
    db.session.add(me)
    db.session.commit()
    return ""


if __name__ == "__main__":
        # app.run()
        app.debug = True
        app.run(host='0.0.0.0')
