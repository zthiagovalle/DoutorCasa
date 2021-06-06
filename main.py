import requests
import json
import os

class DoutorCasaBot:
  def __init__(self):
    token = 'coloque aqui o seu token'
    self.url_base = f'https://api.telegram.org/bot{token}/'

  # Iniciar o bot
  def Iniciar(self):
    update_id = None
    while True:
      atualizacao = self.obterMensagens(update_id)
      mensagens = atualizacao['result']
      if mensagens:
        for mensagem in mensagens:
          update_id = mensagem['update_id']
          chat_id = mensagem['message']['from']['id']
          primeiraMensagem = mensagem['message']['message_id'] == 1
          resposta = self.criarResposta(mensagem, primeiraMensagem)
          self.responderUsuario(resposta,chat_id)

  def obterMensagens(self, update_id):
    requisicao = f'{self.url_base}getUpdates?timeout=100'
    if update_id:
      requisicao = f'{requisicao}&offset={update_id + 1}'
    resultado = requests.get(requisicao)
    return json.loads(resultado.content)

  def criarResposta(self, mensagem, primeiraMensagem):
    mensagem = mensagem['message']['text']
    if(primeiraMensagem == True):
      return f'''Olá eu sou o Doutor Casa{os.linesep}
        Como você está se sentindo hoje?{os.linesep}
          1 - Ótimo 😀{os.linesep}
          2 - Bem{os.linesep}
          3 - Regular{os.linesep}
          4 - Mal 🤧{os.linesep}
        digite um dos números acima: '''
    else:
      return 'Salve Jorge'

  def responderUsuario(self, reposta, chat_id):
    linkDeEnvio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={reposta}'
    requests.get(linkDeEnvio)

bot = DoutorCasaBot()
bot.Iniciar()