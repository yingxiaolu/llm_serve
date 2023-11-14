import json
import urllib.request
import urllib.request
from icecream import ic
# from lib.utils import get_old_content,append_save_json
from flask import Flask, request, render_template
from flask_cors import CORS
from werkzeug.exceptions import abort

from flaskr.db import init_app, get_db

MAX_NEW_TOKENS=2048
MAX_LEGTH=2048*2
SQL_TABLE='lama'
# import openai

app = Flask(__name__)
CORS(app, supports_credentials=True)
app = Flask(__name__, static_url_path='/chatgpt_static')
init_app(app)

def llm_api_server(input_text,temperature):
    llama_chat_prompt='''<s>[INST] <<SYS>> 
{system_prompt} 
<</SYS>>

{user_message} [/INST]'''
    system_prompt="You're an AI assistant"
    user_message=input_text

    header = {'Content-Type': 'application/json'}

    data = {
          "system_prompt": "",
          "history": llama_chat_prompt.format(system_prompt=system_prompt,user_message=user_message),
          "n" : 1,
          "best_of": 1, 
          "presence_penalty": 1.2, 
          "frequency_penalty": 0.2, 
          "temperature": temperature, 
          "top_p" : 0.95, 
          "top_k": 50, 
          "use_beam_search": False, 
          "stop": [], 
          "ignore_eos" :False, 
          "logprobs": None,
          "max_new_tokens": MAX_NEW_TOKENS, 
          "max_length": MAX_LEGTH
    }
    request = urllib.request.Request(
        url='http://127.0.0.1:8001/generate',
        headers=header,
        data=json.dumps(data).encode('utf-8')
    )

    result = "no resp"
    try:
        response = urllib.request.urlopen(request, timeout=300)
        res = response.read().decode('utf-8')
        result = json.loads(res)
        # print(json.dumps(data, ensure_ascii=False, indent=2))
        # print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(e)

    return result

@app.route("/chatgpt", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        messages = request_data['messages']
        ic(messages)
        temperature = float(request_data['temperature'])
        ic(temperature)
        # max_tokens = request_data['max_tokens']
        # presence_penalty = float(request_data['presence_penalty'])
        # frequency_penalty = float(request_data['frequency_penalty'])

        chat_id = request_data['timestamp']

        # openai.api_key = api_key
        # openai.organization = organization_id
        db = get_db()
        cursor = db.cursor()
        # sql_script = f"INSERT INTO `chat`.`tom_list` (`chat_id`, `role`, `content`) VALUES ('{chat_id}', {repr(messages[-1]['role'])}, {repr(messages[-1]['content'])});"
        sql_script = f"INSERT INTO `chat`.`{SQL_TABLE}` (`chat_id`, `role`, `content`) VALUES ('{chat_id}', {repr(messages[-1]['role'])}, {repr(messages[-1]['content'])});"
        cursor.execute(sql_script)
        chat_user_id = db.insert_id()
        db.commit()

        try:
            res=llm_api_server(repr(messages[-1]['content']),temperature)
            ic(res)
            # if re.search(r"^\d+$", max_tokens) is not None:
            #     max_tokens = int(max_tokens)
            #     res = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo",
            #         temperature=temperature,
            #         max_tokens=max_tokens,
            #         presence_penalty=presence_penalty,
            #         frequency_penalty=frequency_penalty,
            #         messages=messages)
            # else:
            #     res = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo",
            #         temperature=temperature,
            #         presence_penalty=presence_penalty,
            #         frequency_penalty=frequency_penalty,
            #         messages=messages)
        except Exception as openError:
            message = openError.json_body['error']['message']
            abort(500, message)

        cursor.execute(
            # f"INSERT INTO `chat`.`tom_list` (`chat_id`, `role`, `content`, `token`) VALUES ('{chat_id}', {repr(res.choices[0].message['role'])}, {repr(res.choices[0].message['content'])}, {res.usage.completion_tokens});")
            f"INSERT INTO `chat`.`{SQL_TABLE}` (`chat_id`, `role`, `content`, `token`) VALUES ('{chat_id}', {repr('assistant')}, {repr(res)}, {-1});")
        cursor.execute(
            # f"UPDATE `chat`.`tom_list` SET `token` = {res.usage.prompt_tokens} WHERE (`id` = {chat_user_id});")
            f"UPDATE `chat`.`{SQL_TABLE}` SET `token` = {-1} WHERE (`id` = {chat_user_id});")
        db.commit()

        # msg = res.choices[0].message
        msg = {'content':res,'role':'assistant','finish_reason':'stop'}
        
        # return json.dumps({'message': msg, 'usage': res.usage, 'finish_reason': res.choices[0]['finish_reason']})
        return json.dumps({'message': msg, 'usage': 0, 'finish_reason': 'stop'})
    return render_template('chatbox.html')


# @app.route("/count_token", methods=('GET', 'POST'))
# def count_token():
#     request_data = json.loads(request.data)
#     input = request_data['input']

#     openai.api_key = api_key
#     openai.organization = organization_id
#     res = openai.Embedding.create(
#         model="text-embedding-ada-002",
#         input=input
#     )
#     print()
#     return json.dumps(res.usage)


@app.route("/logs", methods=('GET', 'POST'))
def logs():
    page_num = 1
    if 'page_num' in request.args:
        page_num = int(request.args['page_num'])
    page_size = 20

    db = get_db()
    cursor = db.cursor()

    # cursor.execute(f"""SELECT COUNT(id) FROM `chat`.`tom_list`;""")
    cursor.execute(f"""SELECT COUNT(id) FROM `chat`.`{SQL_TABLE}`;""")
    total_num = int(cursor.fetchone()[0])

    total_page = (total_num // page_size) + (1 if total_num % page_size > 0 else 0)

    if page_num > total_page:
        page_num = total_page

    # cursor.execute(f"SELECT * FROM `chat`.`tom_list` ORDER BY id DESC LIMIT {(page_num - 1) * page_size},{page_size};")
    cursor.execute(f"SELECT * FROM `chat`.`{SQL_TABLE}` ORDER BY id DESC LIMIT {(page_num - 1) * page_size},{page_size};")
    result = cursor.fetchall()
    return render_template('logs.html', result=result, total_page=total_page, total_num=total_num, page_num=page_num)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
