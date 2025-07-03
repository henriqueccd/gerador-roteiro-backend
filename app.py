import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS # Importa a extensão CORS
import json # Importa a biblioteca JSON para trabalhar com dados JSON
import os # Importa a biblioteca OS para acessar variáveis de ambiente

app = Flask(__name__)
CORS(app) # Habilita o CORS para todas as rotas (permite comunicação entre frontend e backend)

# --- CONFIGURAÇÃO DA CHAVE DE API DO GEMINI ---
# !!! IMPORTANTE: COLOQUE SUA CHAVE DE API AQUI. Nunca exponha isso no frontend!
# Se for para produção, idealmente carregue de variáveis de ambiente (ex: import os; api_key=os.environ.get("GEMINI_API_KEY"))
genai.configure(api_key=os.environ.get("GEMINI_API_KEY")) # Lendo da variável de ambiente (como configurado no Render)
# Se você ainda está testando localmente sem variável de ambiente no Windows, pode usar:
# genai.configure(api_key="SUA_CHAVE_DE_API_AQUI")
# Certifique-se de que a chave está entre aspas duplas!
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
    # duracao_video foi removido, pois agora focamos em palavras por bloco
    num_blocos = data.get('blocos')

    if not tema_escolhido or not num_blocos: # 'duracao_video' foi removido desta verificação
        return jsonify({"error": "Dados incompletos fornecidos. Por favor, preencha todos os campos."}), 400

    # --- CONSTRUÇÃO DO PROMPT COMPLETO PARA A IA (MELHORADO NOVAMENTE!) ---
    prompt_para_ia = f"""
Você é um roteirista profissional com experiência em histórias emocionantes, visceralmente detalhadas e em primeira pessoa, voltadas para vídeos narrados no estilo "canal dark" brasileiro. Seu público são brasileiros que consomem conteúdos sobre conflitos familiares profundos, traições dilacerantes, superações marcantes e revelações chocantes.

Siga estas instruções com atenção cirúrgica, focando em gerar uma narrativa que prenda a atenção de forma sufocante do início ao fim, provoque identificação emocional avassaladora e seja rica em detalhes como uma novela das 21h no Brasil. O formato de saída deve ser um JSON válido, conforme especificado no final.

1.  **Tema da História:** O tema escolhido é: "{tema_escolhido}". Mergulhe profundamente neste tema, explorando todas as suas camadas emocionais.

2.  **Criação da História (Intensificada):** Crie uma história absolutamente realista, envolvente, ORIGINAL e densa, em primeira pessoa.
    * **Profundidade Emocional e Detalhamento Intenso:** Utilize descrições minuciosas de sentimentos (angústia, raiva, desespero, esperança), reações físicas (coração disparado, mãos suando, nó na garganta, tremores) e diálogos carregados de subtexto e emoção, exatamente como em uma cena de novela das 21h no Brasil. Vá além do superficial; explore o monólogo interno do personagem, seus medos, dúvidas e motivações ocultas.
    * **Reviravoltas Chocantes e Situações Inesperadas:** A história DEVE conter no mínimo duas reviravoltas significativas e/ou situações inesperadas que alterem drasticamente o curso da narrativa, elevando a tensão de forma dramática. Pense em "plot twists" que um espectador de novela esperaria.
    * **Presença Vívida do Cotidiano Brasileiro:** Incorpore de forma autêntica elementos culturais, sociais e comportamentais do cotidiano brasileiro. Pense em gírias, costumes familiares, cenários típicos (como uma cozinha de casa de vó, uma rua movimentada de bairro, uma reunião de família com discussões veladas), interações sociais e problemas comuns no Brasil. Faça o público se reconhecer na ambientação.

    * **Extensão e Densidade por Bloco:** A história deve ser dividida em exatamente {num_blocos} blocos. Cada bloco deve ter entre **1500 e 2000 palavras**, garantindo que o conteúdo seja denso, aprofundado e preencha substancialmente essa extensão, sem diluir a qualidade narrativa. A IA deve se esforçar para atingir o limite superior (2000 palavras) se o conteúdo permitir, mas mantendo a qualidade.

    * **Linguagem e Voz da Narrativa (Aprimorada):** A linguagem e o ritmo da narrativa devem ser autênticos, apropriados ao contexto e emoção da história, e personalizados IMERSIVAMENTE de acordo com a idade, características e o tom de voz implícito do personagem principal. Por exemplo, uma personagem mais velha pode ter uma voz mais "carregada", lenta, nostálgica e reflexiva, com um vocabulário que remeta à sua vivência e sabedoria popular. Já uma mais jovem pode ser mais ágil, direta, impulsiva, e usar gírias mais contemporâneas ou um tom de desabafo intenso. A linguagem pode variar entre tons informais e mais formais quando a trama assim exigir, mas sempre mantendo a conexão emocional e a cotidianidade brasileira.

    * **Divisão da História:** A história deve ser dividida em exatamente {num_blocos} blocos. Cada bloco deve ter a quantidade de palavras calculada acima, garantindo que o conteúdo seja denso e aprofundado, sem diluir a qualidade narrativa.

    * **Voz Pessoal e Contextual:** Escreva como se o personagem estivesse desabafando e contando sua história mais íntima e chocante a um amigo, com uma linguagem empática e validadora, adaptada ao contexto emocional do público.

    * **Originalidade Constante:**
        * Crie expressões únicas para cada roteiro.
        * Ao introduzir um tema ou ideia, use a emoção do momento e o contexto para criar algo original, fugindo do óbvio.
        * Substitua Clichês por Ideias Personalizadas: Não copie frases específicas de outros roteiros. Capture o sentimento por trás da frase e reformule com novas palavras específicas para o contexto atual do roteiro, criando formas de expressão genuínas.
        * Ao sugerir analogias ou histórias, crie exemplos únicos e novos para este roteiro. Seja criativo e inteligente, mostrando um profundo entendimento do objetivo, emoção e público-alvo.
        * Procure maneiras criativas de expressar a mesma ideia. Invente novas maneiras de apresentar conceitos que já são conhecidos.

    * **Variedade na Estrutura dos Blocos:**
        * **Abertura (Bloco 1):** Comece com uma introdução única e imediatamente impactante. Pode ser com: Uma pergunta reflexiva e dilacerante; Um fato surpreendente que mude a percepção; Uma metáfora visual que evoke um sentimento forte; Frases que provoquem identificação imediata e profunda; Comandos humanos que mergulhem na psique do público.

    * **Gatilhos Mentais:** Use de 3 a 5 gatilhos mentais por roteiro, de forma sutil e estratégica, para não sobrecarregar o público. Distribua-os na Introdução, Desenvolvimento e Encerramento. Crie variações de gatilhos mentais originais e autênticos para cada novo roteiro. Exemplos de categorias a serem inspiradas: Autoridade, Reciprocidade, Escassez, Prova Social, Curiosidade avassaladora, Promessa de Transformação pessoal, Novidade (da revelação), Medo da Perda, Urgência da situação, Conexão profunda, Simplicidade (na linguagem para facilitar a identificação).

    * **Comandos Humanos Emocionais:** Use comandos humanos com Emoções predominantes e sentimentos associados, ao longo do roteiro (introdução, meio e fim), para tornar o roteiro mais humanizado e criar uma conexão mais próxima e íntima com o público. Crie variações originais e impactantes para cada novo roteiro.

    * **Progressão Narrativa e Emocional dos Blocos:**
        * **Bloco 1:** Apresente o cenário e o conflito inicial de forma a criar uma curiosidade imediata e conectar o público ao protagonista.
        * **Blocos Intermediários:** Desenvolva a trama, intensificando drasticamente a tensão com eventos inesperados e revelações menores que aprofundam o drama. Mostre o impacto emocional avassalador dos acontecimentos.
        * **Último Bloco (Clímax/Consequência):** Apresente o ápice do conflito, a maior revelação ou as consequências mais drásticas e chocantes. Finalize com uma reflexão profunda ou um desfecho que, mesmo não sendo um final feliz, traga um fechamento para a narrativa principal, mas que deixe um gancho para a CTA.

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
-   Frases frias, linguagem muito formal ou poética (a menos que seja parte da voz do personagem e traga impacto).
-   Termos estrangeiros ou fora da realidade brasileira (a menos que se encaixem perfeitamente no cotidiano).
-   Repetições excessivas de palavras, ideias ou blocos com pouca progressão narrativa.
-   Finais que resolvam tudo de forma simples ou feliz, a menos que a história realmente exija. O foco é a complexidade emocional e o impacto duradouro.
-   Qualquer menção direta a que você é uma IA ou um modelo de linguagem.
-   Qualquer texto fora da estrutura JSON solicitada.
"""
    # --- FIM DA CONSTRUÇÃO DO PROMPT (MELHORADO!) ---

    # 1. Cria o modelo de IA (agora usando o modelo mais atualizado que você tem disponível)
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    
    # 2. Faz a chamada à IA. Usamos response.text para pegar a string diretamente.
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
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=False)