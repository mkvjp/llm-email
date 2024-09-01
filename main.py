from flask import Flask, render_template, request
import os
import openai
from markupsafe import Markup

app = Flask(__name__)

# 環境変数からAPIキーを取得
openai.api_key = os.getenv('OPENAI_API_KEY')

# nl2brフィルタの定義
@app.template_filter('nl2br')
def nl2br(value):
    return Markup(value.replace('\n', '<br>\n'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # フォームからの入力データを取得
        addressee = request.form['addressee']  # 宛名
        email_purpose = request.form['email_purpose']
        email_summary = request.form['email_summary']
        tone = request.form['tone']
        your_name = request.form['your_name']
        desired_action = request.form['desired_action']  # 相手に希望するアクション
        previous_emails = request.form.get('previous_emails', '')
        sample_email = request.form.get('sample_email', '')

        # ChatGPTへのプロンプトを作成
        prompt = (
            f"あなたはプロのメール作成アシスタントです。以下の情報に基づいて、宛名に送るべきメールを作成してください。\n\n"
            f"宛名: {addressee}\n"
            f"メールの目的: {email_purpose}\n"
            f"要旨: {email_summary}\n"
            f"雰囲気: {tone}\n"
            f"自分の名前: {your_name}\n"
            f"相手に希望するアクション: {desired_action}\n"
        )
        if previous_emails:
            prompt += f"\nここまでのメールの履歴:\n{previous_emails}\n"
        if sample_email:
            prompt += f"\nサンプルメール:\n{sample_email}\n"

        # OpenAI APIへのリクエスト
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはプロのメール作成アシスタントです。"},
                {"role": "user", "content": prompt}
            ]
        )

        # 生成されたメールを取得
        output = response['choices'][0]['message']['content'].strip()
        return render_template('index.html', output=output)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
