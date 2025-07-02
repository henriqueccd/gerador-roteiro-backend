import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS # Importa a extensão CORS
import json # Importa a biblioteca JSON para trabalhar com dados JSON

app = Flask(__name__)
CORS(app) # Habilita o CORS para todas as rotas (permite comunicação entre frontend e backend)

# --- CONFIGURAÇÃO DA CHAVE DE API DO GEMINI ---
# !!! IMPORTANTE: COLOQUE SUA CHAVE DE API AQUI. Nunca exponha isso no frontend!
# Se for para produção, idealmente carregue de variáveis de ambiente (ex: import os; api_key=os.environ.get("GEMINI_API_KEY"))
genai.configure(api_key="AIzaSyCSkqbHKuyF1FNU1Y2llSz0uaUcz9R9Ja8") # <--- CERTIFIQUE-SE DE QUE SUA CHAVE REAL ESTÁ AQUI
# --- FIM DA CONFIGURAÇÃO ---

@app.route('/')
def home():
    return "Servidor Flask do Gerador de Roteiros está rodando!"

@app.route('/generate-roteiro', methods=['POST'])
def generate_roteiro():
    # Pega os dados JSON enviados pelo frontend
    data = request.json 
    
    # Extrai os dados específicos
    tema_escolhido = data.get('tema')
    duracao_video = data.get('duracao')
    num_blocos = data.get('blocos')

    if not tema_escolhido or not duracao_video or not num_blocos:
        return jsonify({"error": "Dados incompletos fornecidos. Por favor, preencha todos os campos."}), 400

    # --- CONSTRUÇÃO DO PROMPT COMPLETO PARA A IA ---
    # Este é o comando super detalhado que refinamos juntos!
    prompt_para_ia = f"""
Você é um roteirista profissional com experiência em histórias emocionantes em primeira pessoa, voltadas para vídeos narrados no estilo "canal dark". Seu público são brasileiros que consomem conteúdos sobre conflitos familiares, traições, superações e revelações.

Siga estas instruções com atenção, focando em gerar uma narrativa que prenda a atenção do início ao fim e provoque forte identificação emocional no público. O formato de saída deve ser um JSON válido, conforme especificado no final.

1.  **Tema da História:** O tema escolhido é: "{tema_escolhido}". Com base neste tema, construa a narrativa.

2.  **Criação da História:** Crie uma história realista, envolvente e original, em primeira pessoa. Utilize descrições de sentimentos, reações físicas e diálogos marcantes para dar profundidade, como se fosse uma cena de novela das 21h no Brasil. A história deve conter reviravoltas significativas e situações inesperadas.

    * **Cálculo da Extensão:** A duração total do vídeo é de {duracao_video} minutos, dividida em {num_blocos} blocos. Assuma uma média de 150 palavras por minuto de narração. Calcule a quantidade aproximada de palavras por bloco e faça a história se encaixar nessa estimativa. A história inteira deve ter aproximadamente {duracao_video * 150} palavras no total.

    * **Presença do Cotidiano Brasileiro:** O cotidiano brasileiro deve ser muito presente nas histórias, com elementos culturais, sociais e comportamentais que o público reconheça e se identifique (ex: gírias, costumes, cenários típicos, interações familiares e sociais comuns no Brasil).

    * **Linguagem e Voz da Narrativa:** A linguagem e o ritmo da narrativa devem ser autênticos, apropriados ao contexto e emoção da história, e personalizados de acordo com a idade, características e o tom de voz implícito do personagem principal. Por exemplo, uma personagem mais velha pode ter uma voz mais "carregada", lenta e reflexiva, com um vocabulário que remeta à sua vivência. Já uma mais jovem pode ser mais ágil, direta e usar gírias mais contemporâneas. A linguagem pode variar entre tons informais e mais formais quando a trama assim exigir, mas sempre mantendo a conexão emocional e a cotidianidade brasileira.

    * **Divisão da História:** A história deve ser dividida em exatamente {num_blocos} blocos. Cada bloco deve ter a quantidade de palavras calculada acima, garantindo que o conteúdo seja denso e aprofundado, sem diluir a qualidade narrativa.

    * **Voz Pessoal e Contextual:** Escreva como se estivesse tendo uma conversa real com alguém, usando uma linguagem empática e validadora, adaptada ao contexto emocional do público.

    * **Originalidade Constante:**
        * Crie expressões únicas para cada roteiro.
        * Ao introduzir um tema ou ideia, use a emoção do momento e o contexto para criar algo original.
        * Substitua Clichês por Ideias Personalizadas: Capture o sentimento por trás da frase e reformule com novas palavras específicas para o contexto atual do roteiro. Crie novas formas de expressão e apresentação de conceitos.
        * Ao sugerir analogias ou histórias, crie exemplos únicos e novos para este roteiro. Seja criativo e inteligente.
        * Procure maneiras criativas de expressar a mesma ideia. Invente novas maneiras de apresentar conceitos que já são conhecidos.

    * **Variedade na Estrutura dos Blocos:**
        * **Abertura (Bloco 1):** Comece com uma introdução única. Pode ser com: Uma pergunta reflexiva; Um fato surpreendente; Uma metáfora visual; Frases que provoquem identificação imediata; Comandos humanos com emoções e sentimentos predominantes.

    * **Gatilhos Mentais:** Use de 3 a 5 gatilhos mentais por roteiro para não sobrecarregar o público. Distribua-os estrategicamente na Introdução, Desenvolvimento e Encerramento. Crie variações de gatilhos mentais originais para cada novo roteiro. Exemplos de categorias: Autoridade, Reciprocidade, Escassez, Prova Social, Curiosidade, Promessa de Transformação, Novidade, Medo da Perda, Urgência, Conexão, Simplicidade.

    * **Comandos Humanos Emocionais:** Use comandos humanos com Emoções predominantes e sentimentos associados, ao longo do roteiro (introdução, meio e fim), para tornar o roteiro mais humanizado e criar uma conexão mais próxima com o público. Crie variações originais para cada novo roteiro.

    * **Progressão Narrativa e Emocional dos Blocos:**
        * **Bloco 1:** Apresente o cenário e o conflito inicial.
        * **Blocos Intermediários:** Desenvolva a trama, intensificando a tensão com eventos inesperados, revelações menores ou aprofundamento das relações. Mostre o impacto emocional.
        * **Último Bloco (Clímax/Consequência):** Apresente o ápice do conflito, a maior revelação ou as consequências mais drásticas. Finalize com uma reflexão que gere impacto e prepare para o gancho.

**Ao final da geração, formate a saída como um objeto JSON. O JSON deve conter as seguintes chaves:**

* `tema_sugerido`: (string) O tema escolhido ou gerado.
* `historia`: (array de strings) Uma lista onde cada item é o texto de um bloco da história.
* `titulos_sugeridos`: (array de strings) 3 sugestões de títulos chamativos com tom de clickbait.
* `headline_chamativa`: (string) Uma frase de "gancho" ou headline chamativa.
* `cta_final`: (string) Uma chamada à ação emocional para comentários.
* `elementos_thumbnail`: (objeto) Detalhes para a thumbnail:
    * `nome_personagem`: (string) Nome do personagem principal.
    * `idade_personagem`: (string) Idade do personagem principal.
    * `caracteristicas_fisicas`: (string) Descrição física relevante.
    * `elemento_visual_chave`: (string) Objeto, cenário ou breve descrição da cena icônica.
* `srt_completo`: (string) A versão `.srt` completa da história, unificada, com timestamps fictícios de 10 segundos por segmento (formato `1\n00:00:00,000 --> 00:00:10,000\n[Texto]\n\n2\n00:00:10,000 --> 00:00:20,000\n[Texto]`).

**Evite:**
-   Frases frias, linguagem muito formal ou poética (a menos que seja parte da voz do personagem).
-   Termos estrangeiros ou fora da realidade brasileira (a menos que se encaixem no cotidiano).
-   Repetições excessivas de palavras, ideias ou blocos com pouca progressão narrativa.
-   Finais que resolvam tudo de forma simples ou feliz, a menos que a história realmente exija. O foco é a complexidade emocional e o impacto.
-   Qualquer menção direta a que você é uma IA ou um modelo de linguagem.
-   Qualquer texto fora da estrutura JSON solicitada.
"""
    # --- FIM DA CONSTRUÇÃO DO PROMPT ---

    # 1. Cria o modelo de IA (agora usando o modelo mais atualizado que você tem disponível)
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    
    # 2. Faz a chamada à IA. Usamos response.text para pegar a string diretamente.
    # Adicione retry para maior robustez
    try:
        gemini_response = model.generate_content(prompt_para_ia)
        # Tenta pegar o texto. Se a resposta não tiver texto (ex: filtro de segurança), pode dar erro
        ia_text_response = gemini_response.text
    except Exception as e:
        # Captura erros da API (ex: conteúdo bloqueado, problema de conexão)
        print(f"Erro ao chamar a API Gemini: {e}")
        return jsonify({"error": f"Não foi possível gerar o roteiro. Erro na IA: {e}"}), 500

    # Tenta analisar a string de resposta da IA como JSON
    try:
        # A IA deve retornar uma string JSON válida.
        # Vamos garantir que ela realmente retorne um JSON e não texto livre.
        # Se a IA às vezes retorna texto extra (ex: "```json\n...\n```"), limpe antes de parsear.
        if ia_text_response.strip().startswith("```json"):
            ia_text_response = ia_text_response.strip()[len("```json"):].rstrip("```")
        
        roteiro_gerado_json = json.loads(ia_text_response) # Converte a string JSON para um objeto Python
    except json.JSONDecodeError as e:
        print(f"Erro ao analisar JSON da IA: {e}")
        print(f"Resposta bruta da IA: {ia_text_response}")
        return jsonify({"error": f"Erro interno: A IA não retornou um formato JSON válido. Tente novamente ou ajuste o prompt. Detalhes: {e}"}), 500
    except Exception as e:
        print(f"Erro inesperado ao processar resposta da IA: {e}")
        return jsonify({"error": f"Erro inesperado ao processar roteiro. Detalhes: {e}"}), 500

    # O roteiro_gerado_json já está no formato que o frontend espera!
    return jsonify(roteiro_gerado_json)

if __name__ == '__main__':
    app.run(debug=True, port=5000)