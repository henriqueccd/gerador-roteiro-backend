import google.generativeai as genai
import os

# --- CONFIGURAÇÃO DA CHAVE DE API DO GEMINI ---
# É MUITO IMPORTANTE USAR A MESMA CHAVE DE API QUE ESTÁ NO SEU app.py
# Se você colocou a chave diretamente no app.py, copie ela e cole aqui.
# genai.configure(api_key="AIzaSyCSkqbHKuyF1FNU1Y2llSz0uaUcz9R9Ja8")

# Alternativamente, para segurança (e o que faremos agora para teste)
# Tente carregar a chave de uma variável de ambiente, se você a definiu.
# Ou simplesmente cole ela diretamente aqui para este teste rápido (mas NÃO em app.py para produção)
try:
    api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyCSkqbHKuyF1FNU1Y2llSz0uaUcz9R9Ja8") # Substitua pela sua chave REAL
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Erro ao configurar a API key: {e}. Verifique se sua chave está correta.")
    exit() # Sai do script se houver erro na chave

print("Tentando listar modelos disponíveis para generateContent...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  Nome do Modelo: {m.name}")
            print(f"    Descrição: {m.description}")
            print(f"    Versão da API: {m.version}")
            print(f"    Métodos Suportados: {m.supported_generation_methods}")
            print("-" * 30)
except Exception as e:
    print(f"Erro ao listar modelos: {e}")
    print("Verifique sua conexão com a internet e sua chave de API.")

print("\nLista de modelos concluída.")