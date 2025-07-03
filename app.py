import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS 
import json 
import os 

app = Flask(__name__)
CORS(app) 

# --- CONFIGURAÇÃO DA CHAVE DE API DO GEMINI ---
genai.configure(api_key=os.environ.get("AIzaSyCSkqbHKuyF1FNU1Y2llSz0uaUcz9R9Ja8")) 
# --- FIM DA CONFIGURAÇÃO ---

@app.route('/')
def home():
    return "Servidor Flask do Gerador de Roteiros está rodando!"

@app.route('/generate-roteiro', methods=['POST'])
def generate_roteiro():
    data = request.json 
    
    tema_escolhido = data.get('tema')
    num_blocos = data.get('blocos')

    if not tema_escolhido or not num_blocos:
        return jsonify({"error": "Dados incompletos fornecidos. Por favor, preencha todos os campos."}), 400

    # --- CONSTRUÇÃO DO PROMPT COMPLETO PARA A IA (COM INSTRUÇÕES DE JSON ULTRA-ROBUSTAS!) ---
    prompt_para_ia = f"""
Você é um roteirista profissional com experiência em histórias emocionantes, visceralmente detalhadas e em primeira pessoa, voltadas para vídeos narrados no estilo "canal dark" brasileiro. Seu público são brasileiros que consomem conteúdos sobre conflitos familiares profundos, traições dilacerantes, superações marcantes e revelações chocantes.

Siga estas instruções com atenção cirúrgica, focando em gerar uma narrativa que prenda a atenção de forma sufocante do início ao fim, provoque identificação emocional avassaladora e seja rica em detalhes como uma novela das 21h no Brasil. O formato de saída DEVE ser um JSON válido, conforme especificado no final.

1.  **Tema da História:** O tema escolhido é: "{tema_escolhido}". Mergulhe profundamente neste tema, explorando todas as suas camadas emocionais.

2.  **Criação da História (Intensificada):** Crie uma história absolutamente realista, envolvente, ORIGINAL e densa, em primeira pessoa.
    * **Profundidade Emocional e Detalhamento Intenso:** Utilize descrições minuciosas de sentimentos (angústia, raiva, desespero, esperança), reações físicas (coração disparado, mãos suando, nó na garganta, tremores) e diálogos carregados de subtexto e emoção, exatamente como em uma cena de novela das 21h no Brasil. Vá além do superficial; explore o monólogo interno do personagem, seus medos, dúvidas e motivações ocultas.
    * **Reviravoltas Chocantes e Situações Inesperadas:** A história DEVE conter no mínimo duas reviravoltas significativas e/ou situações inesperadas que alterem drasticamente o curso da narrativa, elevando a tensão de forma dramática. Pense em "plot twists" que um espectador de novela esperaria.
    * **Presença Vívida do Cotidiano Brasileiro:** Incorpore de forma autêntica elementos culturais, sociais e comportamentais do cotidiano brasileiro. Pense em gírias, costumes familiares, cenários típicos (como uma cozinha de casa de vó, uma rua movimentada de bairro, uma reunião de família com discussões veladas), interações sociais e problemas comuns no Brasil. Faça o público se reconhecer na ambientação.

    * **Extensão e Densidade por Bloco (EM CARACTERES!):** A história deve ser dividida em exatamente {num_blocos} blocos. Cada bloco DEVE ter entre **1500 e 2000 caracteres**, garantindo que o conteúdo seja densíssimo, aprofundado e preencha substancialmente essa extensão. A IA deve se esforçar para atingir o limite superior (2000 caracteres) se o conteúdo e a qualidade narrativa permitirem, não "enchendo linguiça", mas aprofundando o drama e os detalhes.

    * **Linguagem e Voz da Narrativa (Aprimorada):** A linguagem e o ritmo da narrativa devem ser autênticos, apropriados ao contexto e emoção da história, e personalizados IMERSIVAMENTE de acordo com a idade, características e o tom de voz implícito do personagem principal. Por exemplo, uma personagem mais velha pode ter uma voz mais "carregada", lenta, nostálgica e reflexiva, com um vocabulário que remeta à sua vivência e sabedoria popular. Já uma mais jovem pode ser mais ágil, direta, impulsiva, e usar gírias mais contemporâneas ou um tom de desabafo intenso. A linguagem pode variar entre tons informais e mais formais quando a trama assim exigir, mas sempre mantendo a conexão emocional e a cotidianidade brasileira.

    * **Divisão da História:** A história deve ser dividida em exatamente {num_blocos} blocos. Cada bloco DEVE ter a quantidade de caracteres calculada acima.

    * **Voz Pessoal e Confessional (Desabafos e Fluidez):** Escreva como se o próprio narrador(a) estivesse desabafando diretamente com o leitor/espectador, com uma honestidade brutal e uma intimidade que convida à empatia. A narrativa DEVE fluir com naturalidade, permeada por uma emoção palpável, construindo um suspense envolvente através da cadência das palavras e o ritmo do desabafo, como em uma conversa tensa e pessoal.

    * **Originalidade Constante:**
        * Crie expressões únicas para cada roteiro.
        * Ao introduzir um tema ou ideia, use a emoção do momento e o contexto para criar algo original, fugindo do óbvio.
        * Substitua Clichês por Ideias Personalizadas: Não copie frases específicas de outros roteiros. Capture o sentimento por trás da frase e reformule com novas palavras específicas para o contexto atual do roteiro, criando formas de expressão genuínas.
        * Ao sugerir analogias ou histórias, crie exemplos únicos e novos para este roteiro. Seja criativo e inteligente, mostrando um profundo entendimento do objetivo, emoção e público-alvo.
        * Procure maneiras criativas de expressar a mesma ideia. Invente novas maneiras de apresentar conceitos que já são conhecidos.

    * **Variedade na Estrutura dos Blocos (5 ATOS!):** A história DEVE seguir estritamente esta progressão em 5 atos, com a emoção e o suspense aumentando progressivamente. **Se o número de blocos solicitado for diferente de 5, distribua os atos entre os blocos disponíveis de forma lógica.**
        * **Ato 1 (Apresentação):** Apresentação do narrador e do problema inicial. Estabeleça o tom de desabafo e plante a semente do mistério ou conflito.
        * **Ato 2 (Crescimento):** Crescimento do conflito e da tensão. Detalhe os desafios iniciais e como eles afetam o narrador. Aprofunde as emoções.
        * **Ato 3 (Reviravolta):** A primeira grande reviravolta. Introduza um evento inesperado que mude a direção da história, chocando o narrador e o público.
        * **Ato 4 (Auge):** Conflito no auge, descobertas bombásticas. A trama se intensifica com novas revelações e confrontos. O narrador está no limite.
        * **Ato 5 (Desfecho):** Desfecho (feliz ou trágico) com lição ou emoção final. O conflito principal se resolve, mas deixa uma marca profunda. O desfecho deve ser impactante e ressoar emocionalmente.

    * **Gatilhos Mentais:** Use de 3 a 5 gatilhos mentais por roteiro, de forma sutil e estratégica, para não sobrecarregar o público. Distribua-os na Introdução, Desenvolvimento e Encerramento. Crie variações de gatilhos mentais originais e autênticos para cada novo roteiro. Exemplos de categorias a serem inspiradas: Autoridade, Reciprocidade, Escassez, Prova Social, Curiosidade avassaladora, Promessa de Transformação pessoal, Novidade (da revelação), Medo da Perda, Urgência da situação, Conexão profunda, Simplicidade (na linguagem para facilitar a identificação).

    * **Comandos Humanos Emocionais:** Use comandos humanos com Emoções predominantes e sentimentos associados, ao longo do roteiro (introdução, meio e fim), para tornar o roteiro mais humanizado e criar uma conexão mais próxima e íntima com o público. Crie variações originais e impactantes para cada novo roteiro.

**FORMATO DE SAÍDA FINAL (APENAS JSON): A resposta da IA DEVE ser um objeto JSON válido, e NADA ALÉM DISSO. Não inclua texto explicativo, formatação Markdown (como ```json), ou qualquer outro caractere antes ou depois do JSON. Apenas o JSON puro. É ABSOLUTAMENTE CRÍTICO que a saída seja JSON válido para o sistema funcionar.**
**- Escapamento de Aspas: Todas as aspas duplas internas dentro das strings (como dentro dos textos da história ou descrições) DEVEM ser escapadas com uma barra invertida (ex: "Ela disse: \"Adeus\".").**

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
"""
    # --- FIM DA CONSTRUÇÃO DO PROMPT (MELHORADO NOVAMENTE!) ---

    # 1. Cria o modelo de IA (usando o modelo atualizado)
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    
    # 2. Faz a chamada à IA. Usamos response.text para pegar a string diretamente.
    try:
        gemini_response = model.generate_content(prompt_para_ia)
        ia_text_response = gemini_response.text
        # DEBUG: Printa os primeiros 500 caracteres da resposta bruta da IA para o Render logs
        print(f"DEBUG: Resposta bruta da IA (primeiros 500 chars): \n{ia_text_response[:500]}...")
    except Exception as e:
        # Captura erros da API (ex: conteúdo bloqueado, problema de conexão)
        print(f"Erro ao chamar a API Gemini: {e}")
        return jsonify({"error": f"Não foi possível gerar o roteiro. Erro na IA: {e}"}), 500

    # Tenta analisar a string de resposta da IA como JSON
    try:
        # A IA DEVE retornar uma string JSON válida.
        # Remove possíveis cabeçalhos de markdown como "```json\n" e "```" finais
        cleaned_response = ia_text_response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[len("```json"):].strip()
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-len("```")].strip()
        elif cleaned_response.startswith("```"): # Caso seja ``` sem json especificado
            cleaned_response = cleaned_response[len("```"):].strip()
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-len("```")].strip()

        # Tenta encontrar o bloco JSON puro usando chaves de abertura e fechamento
        json_start = cleaned_response.find('{')
        json_end = cleaned_response.rfind('}')
        
        if json_start != -1 and json_end != -1 and json_end > json_start:
            json_string_candidate = cleaned_response[json_start : json_end + 1]
            print(f"DEBUG: JSON string candidata para loads() (limpa e isolada): \n{json_string_candidate[:500]}...")
            roteiro_gerado_json = json.loads(json_string_candidate) # Converte a string JSON para um objeto Python
            print(f"DEBUG: JSON parseado com sucesso.")
            
            # Garante que 'historia' é uma lista de strings. Se a IA retornar uma string única, converte para lista.
            if 'historia' in roteiro_gerado_json and isinstance(roteiro_gerado_json['historia'], str):
                roteiro_gerado_json['historia'] = [roteiro_gerado_json['historia']]
            
            # Garante que 'titulos_sugeridos' é uma lista de strings.
            if 'titulos_sugeridos' in roteiro_gerado_json and isinstance(roteiro_gerado_json['titulos_sugeridos'], str):
                roteiro_gerado_json['titulos_sugeridos'] = [roteiro_gerado_json['titulos_sugeridos']]
            
            # Garante que 'elementos_thumbnail' é um objeto (dicionário).
            if 'elementos_thumbnail' in roteiro_gerado_json and not isinstance(roteiro_gerado_json['elementos_thumbnail'], dict):
                print("AVISO: elementos_thumbnail não é um dicionário, tentando converter ou usar padrão.")
                roteiro_gerado_json['elementos_thumbnail'] = {} # Reseta para evitar erro no frontend
            
        else:
            raise json.JSONDecodeError(f"Não foi possível encontrar um bloco JSON completo. Resposta limpa: {cleaned_response}", cleaned_response, 0)
            
    except json.JSONDecodeError as e:
        print(f"ERRO DE JSON: Problema ao analisar JSON da IA: {e}")
        print(f"RESPOSTA BRUTA DA IA QUE CAUSOU O ERRO:\n{ia_text_response}")
        return jsonify({"error": f"Erro interno: A IA não retornou um formato JSON válido. Tente novamente ou ajuste o prompt. Detalhes: {e}"}), 500
    except Exception as e:
        print(f"ERRO INESPERADO: ao processar resposta da IA: {e}")
        return jsonify({"error": f"Erro inesperado ao processar roteiro. Detalhes: {e}"}), 500

    # O roteiro_gerado_json já está no formato que o frontend espera!
    return jsonify(roteiro_gerado_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=False)