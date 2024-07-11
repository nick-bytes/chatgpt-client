from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv
import logging


# Set up your app environment 
app = Flask(__name__, template_folder='templates')
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')



# Set up root root_logger 
root_logger = logging.getLogger(__name__)
root_logger.setLevel(logging.DEBUG)

# Set up formatter for logs 
file_handler_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s  ')
console_handler_log_formatter = logging.Formatter('%(message)s ')

# Set up file handler object for logging events to file
file_handler = logging.FileHandler('chatgpt_conversation_history.log', mode='w')
file_handler.setFormatter(file_handler_log_formatter)

# Set up console handler object for writing event logs to console in real time (i.e. streams events to stderr)
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_handler_log_formatter)

# Add the file and console handlers 
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)




@app.route('/')
def render_index_html():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def render_chat_with_chatgpt():
    user_input = request.form['text']
    root_logger.removeHandler(console_handler)
    root_logger.info(f':: Me (SDW):   {user_input}' )
    root_logger.addHandler(console_handler)
    chatgpt_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input,
        temperature=0.3,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )
    root_logger.info(f':: ChatGPT: {chatgpt_response["choices"][0]["text"]}  ')
    root_logger.debug('--------------------------------------------------')
    return chatgpt_response["choices"][0]["text"]

if __name__ == '__main__':
    app.run(debug=True)
