from transformers import pipeline
chat_history = []

def get_context():
    context = ""
    for msg in chat_history[-6:]:  # Últimas 6 mensagens
        context += f"Usuário: {msg['user']}\nBot: {msg['bot']}\n"
    return context

# Ao gerar uma resposta, inclua o histórico no contexto do modelo.
generator = pipeline(
  model="Qwen/Qwen2.5-1.5B-Instruct",
  max_new_tokens=15,
  temperature=0.1,
  truncation=True,
  device_map="auto",          # usa GPU se disponível, senão CPU
  torch_dtype="auto",          # escolhe automaticamente a precisão (fp16 se GPU)
  trust_remote_code=True,      # necessário para modelos Qwen (código personalizado no Hub)
)

while True:

  pergunta = input("Digite pergunta: ").strip()

  if pergunta == "sair":
    break
  
  chat_history.append({"user": pergunta, "bot": ""})
  pergunta_real= "Gere um texto contendo apenas o nome para um personagem de um mundo de fantasia"
  
  system_prompt = """Você deve responder APENAS com um nome curto e nada mais. Sem explicações, sem pontuação adicional."""
  user_prompt = "Gere um nome para um personagem de fantasia."
  completions = generator(f"System: {system_prompt}. User: {user_prompt}", max_new_tokens=50 )
  
  # for comp in completions:
  #   print(f"🤖 {comp['generated_text']}")
    
  print(completions)
  print(completions[0]['generated_text'])
    
  
    
    