from flask import Flask, render_template, request, make_response
from io import StringIO
import parse_user_input as input_parser
import scrape_channel, scrape_playlist
import pandas as pd
app = Flask(__name__)

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    return render_template('index.html')

@app.route('/getPlaylistStats', methods=['POST'])
def getPlaylistStats():

    req_body = request.get_json()
    url = req_body['url']
    query = req_body['query']
    fullUrl = f'{url}?{query}'
    x = input_parser.main(fullUrl)
    scraped_data = None
    if x[1] == 0:
        # uploads_id = scrape_channel.get_uploads_id(x[0])
        # scraped_data = scrape_playlist.main(uploads_id)
        pass
    else:
        scraped_data = scrape_playlist.main(x[0])

    df = pd.DataFrame(scraped_data, columns=['Episode', 
                                             'Published', 
                                             'Views',
                                             'Likes',
                                             'Comments',
                                             'ID',
                                             'Time (sec)',
                                             'URL'])
    
    # Save CSV to in-memory string buffer
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Send as a file
    response = make_response(csv_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response

@app.route('/getChannelStats', methods=['POST'])
def getChannelStats():

    req_body = request.get_json()
    url = req_body['url']
    query = req_body['query']
    fullUrl = f'{url+query}'
    
    from urllib import request as req   #avoid same name with flask's request
    from bs4 import BeautifulSoup

    re = req.urlopen(fullUrl)
    re = re.read().decode('utf-8')
    soup = BeautifulSoup(re, "html.parser")
    raw_channel_url = soup.find('meta', property='og:url')['content']
    channel_id = raw_channel_url.replace('https://www.youtube.com/channel/', '')
    channel_upload_id = scrape_channel.get_uploads_id(channel_id=channel_id)
    scraped_data = scrape_playlist.main(channel_upload_id)
    df = pd.DataFrame(scraped_data, columns=['Episode', 
                                             'Published', 
                                             'Views',
                                             'Likes',
                                             'Comments',
                                             'ID',
                                             'Time (sec)',
                                             'URL'])
    
    # Save CSV to in-memory string buffer
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Send as a file
    response = make_response(csv_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response


if __name__ == '__main__':
    app.run(debug=True)