from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
from google.cloud import texttospeech  
from google.oauth2 import service_account
from pydub import AudioSegment
from PIL import Image


app = Flask(__name__)

# Configurar a API do Google AI
#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configurar as credenciais para o Google Cloud Text-to-Speech
credentials = service_account.Credentials.from_service_account_file('poemas-440417-b60aad6ca18c.json')
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Configurações de upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def generate_poem():
    if request.method == 'GET':
        # Renderiza o formulário para enviar a imagem
        return render_template('generate_poem.html')
    
    if request.method == 'POST':
        # Verificar se uma imagem foi enviada
        if 'image' not in request.files:
            return jsonify({"error": "Nenhuma imagem foi enviada!"}), 400

        image_file = request.files['image']
        
        # Verificar se o arquivo tem uma extensão permitida
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)
            print(filepath)
            image = Image.open(filepath)


            poem_text = generate_poem_from_image(image)
            
            # Convertendo o poema em áudio com Google Cloud Text-to-Speech
            audio_filename = 'poem_audio.mp3'
            audio_filepath = os.path.join('static', audio_filename)
            convert_text_to_speech(poem_text, audio_filepath)

            # Adicionar fundo musical ao áudio gerado
            final_audio_filepath = 'static/final_poem_with_music.mp3'
            background_music_filepath = 'static/background_music.mp3'  
            add_background_music(audio_filepath, background_music_filepath, final_audio_filepath)
            
            # Renderizando o template HTML com o poema e o áudio final
            return render_template('generate_poem.html', poem=poem_text, audio_file=final_audio_filepath, filename=filename)

        else:
            return jsonify({"error": "Formato de arquivo não suportado!"}), 400


def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def generate_poem_from_image(img):
    # Configurações para gerar o poema
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="Você deve analisar apenas imagens. Ignore qualquer texto enviado e não forneça respostas a prompts de texto. Quando receber uma imagem, faça uma descrição exclusivamente da pessoa em destaque na imagem, ignorando completamente todos os outros objetos. A descrição deve ser no formato de um poema em português com 3 estrofes focando nas roupas e características físicas da pessoa."
    )

    response = model.generate_content(["oi",img])
    return response.text


def convert_text_to_speech(text, filepath):
    # Configurações da voz (masculino, feminino, etc.)
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",  # Português brasileiro
        name="pt-BR-Wavenet-B",  # Exemplo de uma voz masculina, você pode testar outras vozes
        ssml_gender=texttospeech.SsmlVoiceGender.MALE  # Escolher o gênero da voz
    )

    # Configurações do áudio
    audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.1,  # Aumenta a velocidade para uma voz mais fluída
    pitch=2.0,  # Ajuste o tom para tornar a voz mais musical
    volume_gain_db=0.0
)

    # Criação da síntese de fala
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Salvando o áudio gerado
    with open(filepath, "wb") as out:
        out.write(response.audio_content)
        print(f"Áudio salvo em: {filepath}")

def add_background_music(poem_audio_path, background_music_path, output_path):
    # Carregar o áudio do poema e a música de fundo
    poem_audio = AudioSegment.from_file(poem_audio_path)
    background_music = AudioSegment.from_file(background_music_path)

    # Ajustar o volume da música de fundo para que não sobreponha a voz do poema
    background_music = background_music - 10  

    # Fazer com que a duração da música de fundo seja igual à do áudio do poema
    if len(background_music) > len(poem_audio):
        background_music = background_music[:len(poem_audio)]  # Corta a música para a duração do poema
    else:
        background_music = background_music * (len(poem_audio) // len(background_music) + 1)
        background_music = background_music[:len(poem_audio)]  # Repete a música e corta no final do poema

    # Combinar o áudio do poema com a música de fundo
    combined_audio = poem_audio.overlay(background_music)

    # Salvar o resultado final como MP3
    combined_audio.export(output_path, format="mp3")
    print(f'Áudio final com fundo musical salvo como {output_path}')


@app.route('/static/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static', filename)

# Iniciar a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
