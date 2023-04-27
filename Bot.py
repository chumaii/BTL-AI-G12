import logging
# thư viện cho phép ghi lại các sự kiện quan trọng và lỗi trong ứng dụng.
import sys
# thư viện cho phép tương tác với các thông tin hệ thống.
from telegram.ext import *
#  thư viện cho phép tạo và quản lý bot trên nền tảng Telegram.
import requests
# thư viện cho phép gửi và nhận các yêu cầu HTTP.
import urllib.parse
# thư viện cho phép mã hóa và giải mã các thông tin truy vấn URL.
import spacy # 3.5.0
# thư viện cho phép xử lý ngôn ngữ tự nhiên và trích xuất các thông tin ngữ pháp.
import openai
# thư viện cho phép tạo câu trả lời tự động dựa trên các câu hỏi và thông tin đã cho.
import json
# thư viện cho phép xử lý các định dạng dữ liệu JSON.
from process import ask, append_interaction_to_chat_log
# Hàm ask() được sử dụng để đưa câu hỏi của người dùng vào một mô hình xử lý ngôn ngữ tự nhiên 
# và tạo ra câu trả lời tương ứng. Hàm append_interaction_to_chat_log() 
# được sử dụng để lưu lại thông tin về các cuộc trò chuyện giữa người dùng và bot trong một tệp log.
from News import GetNews
# Hàm GetNews() được sử dụng để lấy các tin tức mới nhất từ các nguồn tin tức khác nhau dựa trên một từ khóa được cung cấp.
from io import BytesIO
# Lớp BytesIO cho phép tạo và xử lý các đối tượng bytes trong bộ nhớ, thay vì phải tạo các tệp tạm thời trong ổ đĩa.
import numpy as np
# thư viện cho phép xử lý các phép toán số học.
import cv2
# thư viện cho phép xử lý ảnh và video.
import tensorflow as tf
# thư viện cho phép xây dựng và huấn luyện các mô hình học máy.
import en_core_web_sm
# một gói ngôn ngữ của spacy dùng để phân tích các thành phần ngữ pháp.
import telebot
# thư viện cho phép tương tác với API Telegram.
from spotipy.oauth2 import SpotifyClientCredentials
# Lớp SpotifyClientCredentials được sử dụng để xác thực ứng dụng của bạn truy cập vào API của Spotify thông qua phương thức OAuth2.
import spotipy
# thư viện cho phép tương tác với API Spotify

bot = telebot.TeleBot("6251885022:AAHeWje78zf4gzRzdvB6F5lZPolo5eGFhY8")
TOKEN = "6251885022:AAHeWje78zf4gzRzdvB6F5lZPolo5eGFhY8"
# token telegram_bot ( mỗi bạn code chức năng khác nhau nên triển khai code khác nhau)

client_credentials_manager = SpotifyClientCredentials(client_id='ba88803887d14a5a85d0a5c6532127e4', client_secret='b0d78b3a45604444a8dbb8075c5d49c5')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# sử dụng để thiết lập xác thực cho ứng dụng Spotify của bạn khi sử dụng API của Spotify.

nlp = en_core_web_sm.load()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# cho phép chúng ta sử dụng các tính năng của thư viện SpaCy để phân tích ngôn ngữ tự nhiên.


logger = logging.getLogger(__name__)
# Logger sẽ được sử dụng để ghi lại các thông tin và cảnh báo trong quá trình chạy ứng dụng.
openai_secret_key = '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'
openai.api_key = openai_secret_key
# sử dụng mã truy cập này để gửi các yêu cầu đến API của OpenAI
session = {}
# Biến này sẽ được sử dụng để lưu trữ lịch sử trò chuyện của người dùng với bot, giúp bot có thể tương tác và trả lời một cách thông minh hơn.
sys.path.append('Method/News')
# là câu lệnh để thêm đường dẫn tới thư mục chứa module liên quan tới việc lấy tin tức. 
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
x_train, x_test = x_train / 255, x_test / 255
# tải tập dữ liệu CIFAR-10 từ tf.keras.datasets.
# Dòng đầu tiên tải bộ dữ liệu và chia thành 2 phần tương ứng là tập huấn luyện và tập kiểm tra
# Dòng thứ hai chuẩn hóa các giá trị pixel của các ảnh trong tập huấn luyện và tập kiểm tra bằng cách chia cho 255
class_names = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
# xác định danh sách tên lớp cho bộ dữ liệu CIFAR-10.

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
# Đoạn code này xây dựng một mô hình mạng neuron tích chập (CNN) để phân loại ảnh trong bộ dữ liệu CIFAR-10.

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Xin chào!\n"
                                                                    "Tôi là Chatbot đa zi năng đây!\n"
                                                                    "Tôi rất sẵn lòng giúp bạn những việc sau đây:\n"
                                                                    "1./help : trợ giúp bạn mọi thứ\n"
                                                                    "2. /search_image + nội dung: Tìm kiếm hình ảnh\n"
                                                                    "3. /news: Tìm kiếm tin tức\n"
                                                                    "4. /qa: Bạn có thể hỏi đáp với tôi\n"
                                                                    "5./play_song+ tên bài hát: đưa ra file mp3 dài 29s về bài hát đó\n" 
                                                                    "6./train chức năng nhận diện ảnh khi bạn gửi vào 1 image\n"
                                                                    "Rất vui được phục vụ bạn :3")

# khi gọi hàm start thì nội dung trên sẽ được hiển thị

def qa_gpt(update, context):
    chat_log = session.get('chat_log')
    answer = ask(update.message.text[3:].strip(), chat_log)
    session['chat_log'] = append_interaction_to_chat_log(update.message.text, answer,
                                                         chat_log)
    update.message.reply_text(f"{str(answer)}")
# thông tin về lịch sử trò chuyện được lưu trữ trong một dictionary có tên là session.
# Hàm ask được sử dụng để đưa câu hỏi từ người dùng vào mô hình GPT-3 để trả lời.
# Kết quả trả về được lưu trữ trong answer và sau đó được trả lời lại cho người dùng thông qua phương thức update.message.reply_text.
# Các tin nhắn và câu trả lời được lưu trữ trong chat_log.

def search_image(update, context):
    nlp = spacy.load("en_core_web_sm")
    # Load thư viện spacy để xử lý ngôn ngữ tự nhiên.
    query = update.message.text[14:]
    # Hàm này lấy chuỗi kí tự từ vị trí thứ 14 trong tin nhắn nhận được. 
    doc = nlp(query)
    # Hàm này tạo một đối tượng từ các từ khóa tìm kiếm
    related_words = [token.text for token in doc if not token.is_stop]
    # Hàm này tạo một danh sách các từ liên quan đến từ khóa tìm kiếm.
    search_query = " ".join(related_words)
    # Hàm này tạo chuỗi truy vấn từ danh sách các từ liên quan đã được tạo.
    encoded_query = urllib.parse.quote(search_query)
    # Hàm này mã hóa chuỗi truy vấn để sử dụng trong URL tìm kiếm của Google.
    API_KEY = 'AIzaSyDZaWsrKy4LbiZaG8abJ7FezrIvCpMDETU'
    CX_ID = 'c0c7d82b59f994517'
    url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX_ID}&q={encoded_query}&hl=vi&searchType=image&ie=UTF-8'
    response = requests.get(url)
    # Hàm này sử dụng thư viện requests để gửi yêu cầu GET đến URL tìm kiếm và nhận phản hồi từ Google.
    data = response.json()
    image_url = data['items'][0]['link']
    # 2 dòng này trích xuất URL hình ảnh đầu tiên từ phản hồi JSON của Google.
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
    # Hàm này sử dụng đối tượng bot của bot Telegram để gửi hình ảnh tìm kiếm đến người dùng.
# dùng để tìm kiếm hình ảnh trên Google Images dựa trên từ khóa mà người dùng nhập vào. 


def news(update, context):
    try:
        # limit_news = int(context.args[0])  # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
        limit_news = 5
        # lấy về 5 tin
        newses = GetNews(limit_news)
        # để lấy danh sách các tin tức mới nhất.
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Mình tìm được một số tin tức sốt dẻo cho bạn đây!!!")
        for x in range(0, len(newses)):  
            message = json.loads(newses[x])
            update.message.reply_text(message['link'] + "\n" + message['description'])
        # Deserialize dữ liệu json trả về từ file News.py lúc nãy
    except (IndexError, ValueError):
        update.message.reply_text('Xin lỗi Mình không thể tìm kiếm tin tức cho bạn!!')
# Hàm news có tác dụng tìm kiếm và trả về các tin tức mới nhất. 


def train(update, context):
    update.message.reply_text("Model is being trained...")
    # bot sẽ gửi tin nhắn "Model is being trained..." đến người dùng để thông báo rằng mô hình đang được huấn luyện.
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    #  bot sử dụng phương thức compile() của mô hình để cấu hình quá trình huấn luyện
    model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))
    # Mô hình sẽ được huấn luyện trong 10 epochs. 
    model.save('cifar_classifier.model')
    # Sau khi quá trình huấn luyện kết thúc, mô hình sẽ được lưu vào file cifar_classifier.model bằng phương thức save().
    update.message.reply_text("Done! You can now send a photo!")
# hàm này dùng để train bot


def handle_photo(update, context):
    file = context.bot.get_file(update.message.photo[-1].file_id)
    f = BytesIO(file.download_as_bytearray())
    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)

    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)

    
    prediction = model.predict(np.array([img/255]))
    update.message.reply_text(f"In the image I see a {class_names[np.argmax(prediction)]}")
# Hàm handle_photo nhận vào một tấm ảnh được gửi bởi người dùng, 
# sau đó sử dụng thư viện python-telegram-bot để tải về file ảnh đó.
# hàm này sử dụng thư viện OpenCV để đọc và xử lý ảnh đó, 
# đưa về kích thước chuẩn là 32x32 pixel và chuẩn hóa các giá trị pixel về khoảng từ 0 đến 1. 
# Cuối cùng, hàm sử dụng mô hình đã được đào tạo trước đó để dự đoán đối tượng trong ảnh 
# và trả về kết quả dưới dạng một tin nhắn cho người dùng.
def play_song(update, context):
    # Lấy từ khóa tìm kiếm từ tin nhắn của người dùng
    search_query = update.message.text
    
    # Tìm kiếm bài hát trên Spotify
    results = sp.search(search_query, type='track', limit=1)
    if len(results['tracks']['items']) > 0:
        # Lấy thông tin về bài hát được tìm thấy
        track = results['tracks']['items'][0]
        
        # Lấy URL của bài hát để phát nhạc
        preview_url = track['preview_url']
        if preview_url is None:
            update.message.reply_text("Xin lỗi, bài hát không có phiên bản xem trước.")
        else:
            # Phát nhạc trên Telegram
            update.message.reply_audio(audio=preview_url)
    else:
        update.message.reply_text("Xin lỗi, không tìm thấy bài hát nào.")
# được sử dụng để phát nhạc trên Telegram thông qua Spotify API.
# nếu tìm thấy bài hát, chúng ta lấy URL của phiên bản xem trước bài hát (preview_url) để phát nhạc trên Telegram. 
# Nếu không có phiên bản xem trước bài hát, 
# chúng ta sẽ trả về một tin nhắn thông báo về việc không tìm thấy phiên bản xem trước bài hát.
 
def main():

    updater = Updater(TOKEN, use_context=True)
    # Khởi tạo một đối tượng Updater với thông tin mã thông báo bot
    # và use_context = True để sử dụng phương thức mới của API Telegram
    dp = updater.dispatcher

    # command
    
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("search_image", search_image))
    dp.add_handler(CommandHandler("qa", qa_gpt))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(CommandHandler("train", train))
    dp.add_handler(CommandHandler("play_song", play_song))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    
    # Đăng ký các trình xử lý bằng cách sử dụng các CommandHandler và MessageHandler.
    # Các CommandHandler được đăng ký để xử lý các lệnh được gửi đến bot. 
    # MessageHandler được đăng ký để xử lý các tin nhắn văn bản và hình ảnh được gửi đến bot.
    updater.start_polling()
    updater.idle()
    # Khởi động bot:
    
    

if __name__ == "__main__":
    main()