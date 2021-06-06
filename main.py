import requests
import json

class DoutorCasaBot:
  def __init__(self):
      token = 'coloque seu token aqui'
      self.url_base = f'https://api.telegram.org/bot{token}/'
      self.risco = int(0)
      self.sequencia = int(0)

      self.msgFebre = '''
      Você tem febre?
      1 - Não
      2 - Sim, abaixo de 38º
      3 - Sim, 38º ou acima 🤒
      Digite um dos números acima: 
      '''
      self.msgTosse = '''
      Você tem tosse?
      1 - Não
      2 - Tosse seca
      3 - Sim, tosse com catarro
      Digite um dos números acima:
      '''
      
      self.msgRespiracao = '''
      Você está com dificuldades para respirar?
      1 - Não
      2 - Sim, mas não me impede de fazer tarefas simples
      3 - Sim, me impede de fazer tarefas simples 😟
      Digite um dos números acima:      
      '''

      self.msgNaoEntendi = 'Não consegui entender, digite iniciar para voltar ao começo do atendimento.'

  def Iniciar(self):
      update_id = None
      while True:
          atualizacao = self.obterNovasMensagens(update_id)
          mensagens = atualizacao["result"]
          if mensagens:
              for mensagem in mensagens:
                  print(mensagem)
                  try:
                    update_id = mensagem['update_id']
                    usuario = mensagem["message"]["from"]["first_name"]
                    chat_id = mensagem["message"]["from"]["id"]
                    primeiraMensagem = mensagem["message"]["message_id"] == 1
                    msgUsuario = str(mensagem["message"]["text"]).upper()
                    resposta = self.criarResposta(primeiraMensagem, msgUsuario, usuario)
                    self.respondeUsuario(resposta, chat_id)
                  except Exception:
                    self.respondeUsuario("Tive um problema, me desculpe.\n Envie uma nova mensagem.")

  def obterNovasMensagens(self, update_id):
    link_requisicao = f'{self.url_base}getUpdates?timeout=100'
    if update_id:
        link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
    resultado = requests.get(link_requisicao)
    return json.loads(resultado.content)
  
  def criarResposta(self, primeiraMensagem, msgUsuario, usuario):
    if(primeiraMensagem == True or msgUsuario in ('OI', 'OLÁ', 'OLA', 'HEY', 'EI',  'BOM DIA', 'BOA TARDE', 'BOA NOITE',  '/START', 'INICIAR')):
      self.sequencia += 1
      return"Olá eu sou o seu doutor preferido.\nVou fazer algumas perguntas sobre seu estado de saúde atual.\n\nComo você está se sentindo hoje?\n1 - Ótimo 😀\n2 - Regular\n3 - Mal 🤧\nDigite um dos números acima:"
      
    elif self.sequencia == 1:
      if(msgUsuario == '1' or msgUsuario in('ÓTIMO', 'OTIMO')):
        self.sequencia += 1
        return self.msgFebre        

      elif(msgUsuario == '2' or msgUsuario in('REGULAR')):
        self.sequencia += 1
        self.risco += 1
        return self.msgFebre

      elif(msgUsuario == '3' or msgUsuario in('MAL', 'PESSIMO', 'PÉSSIMO', 'HORRIVEL')):
        self.sequencia += 1
        self.risco += 2
        return self.msgFebre

      else:
        self.sequencia = 0
        self.risco = 0
        return self.msgNaoEntendi

    elif self.sequencia == 2:
      if(msgUsuario == '1' or msgUsuario in('NÃO', 'NAO', 'N')):
        self.sequencia += 1
        return self.msgTosse

      elif(msgUsuario == '2' or msgUsuario in('ABAIXO DE 38º', 'ABAIXO DE 38')):
        self.sequencia += 1
        self.risco += 1
        return self.msgTosse

      elif(msgUsuario == '3' or msgUsuario in('ACIMA', 'ACIMA DE 38º')):
        self.sequencia += 1
        self.risco += 2
        return self.msgTosse

      else:
        self.sequencia = 0
        self.risco = 0
        return self.msgNaoEntendi

    elif self.sequencia == 3:
      if(msgUsuario == '1' or msgUsuario in('NÃO', 'NAO', 'N')):
        self.sequencia += 1
        return self.msgRespiracao

      elif(msgUsuario == '2' or msgUsuario in('TOSSE SECA')):
        self.sequencia += 1
        self.risco += 1
        return self.msgRespiracao

      elif(msgUsuario == '3' or msgUsuario in('TOSSE COM CATARRO')):
        self.sequencia += 1
        self.risco += 2
        return self.msgRespiracao

      else:
        self.sequencia = 0
        self.risco = 0
        return self.msgNaoEntendi

    elif self.sequencia == 4:
      if(msgUsuario == '1' or msgUsuario in('NÃO', 'NAO', 'N')):
        self.sequencia += 1

      elif(msgUsuario == '2'):
        self.sequencia += 1
        self.risco += 1

      elif(msgUsuario == '3'):
        self.sequencia += 1
        self.risco += 2

      else:
        self.sequencia = 0
        self.risco = 0
        return self.msgNaoEntendi    
      
      if(self.risco <= 4):
        return "Baseado em suas respostas, é provável que esta situação NÃO se enquadre como caso suspeito de doença pelo coronavírus.\nNo entanto, isto não se trata de diagnóstico.\nMantenha as condutas de precaução e prevenção."
      else:
        return 'Va urgente para um hospital.'
    
    elif msgUsuario in('OBRIGADO', 'TCHAU', 'ADEUS', 'ATÉ MAIS', 'ATÉ LOGO'):
        self.sequencia = 0
        self.risco = 0
        return "Fico muito feliz em ter ajudado você, se cuide e fique bem."

    else:
      self.sequencia = 0
      self.risco = 0
      return self.msgNaoEntendi
      
  def respondeUsuario(self, resposta, chat_id):
    link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
    requests.get(link_requisicao)

bot = DoutorCasaBot()
bot.Iniciar()