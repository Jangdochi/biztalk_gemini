from flask import Flask, send_from_directory, request, jsonify
import os
import logging
from groq import Groq
from dotenv import load_dotenv
from flask_cors import CORS

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Groq 클라이언트 초기화
try:
    client = Groq(api_key=GROQ_API_KEY)
    if not GROQ_API_KEY:
        logging.warning("GROQ_API_KEY not found in .env file. API calls will fail.")
except Exception as e:
    logging.error(f"Failed to initialize Groq client: {e}")
    client = None

# 정적 파일을 제공하기 위한 경로 설정
basedir = os.path.abspath(os.path.dirname(__file__))
frontend_dir = os.path.join(basedir, '..', 'frontend')

app = Flask(__name__)
CORS(app)  # 모든 라우트에 대해 CORS 허용

@app.route('/')
def index():
    """메인 HTML 파일을 제공합니다."""
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    """정적 파일(CSS, JS, 이미지 등)을 제공합니다."""
    return send_from_directory(frontend_dir, filename)

@app.route('/api/convert', methods=['POST'])
def convert_message():
    """
    프론트엔드로부터 원문과 페르소나를 받아 Groq AI를 호출하고,
    변환된 비즈니스 메시지를 JSON 형식으로 반환합니다.
    """
    if not client:
        logging.error("API call failed because Groq client is not initialized.")
        return jsonify({"error": "Groq API client not initialized. Check API key."}), 500

    data = request.get_json()
    if not data:
        logging.warning("Request received with no JSON data.")
        return jsonify({"error": "Invalid request: No JSON data received."}), 400

    keywords = data.get('keywords')
    persona = data.get('persona')

    if not keywords or not persona:
        logging.warning(f"Missing data in request: keywords={bool(keywords)}, persona={bool(persona)}")
        return jsonify({"error": "Missing 'keywords' or 'persona' in request."}), 400
    
    logging.info(f"Received conversion request for persona '{persona}' with {len(keywords)} characters.")

    # 페르소나별 최적화된 시스템 프롬프트 (한국어)
    persona_instructions = {
        "upward": (
            "당신은 뛰어난 비즈니스 커뮤니케이션 전문가입니다. 주어진 핵심 내용을 바탕으로, 상사에게 보고하기 위한 정중하고 전문적인 비즈니스 문서를 작성해야 합니다. "
            "다음 지침을 반드시 따르세요:\n"
            "1. **두괄식 작성**: 핵심 결론이나 요청 사항을 문장의 가장 처음에 명확하게 제시하세요.\n"
            "2. **정중한 격식체**: '습니다', 'ㅂ니다' 체를 사용하여 최대한 정중하고 격식 있는 언어를 사용하세요.\n"
            "3. **객관적 사실 기반**: 개인적인 감정이나 추측은 배제하고, 사실과 데이터를 기반으로 간결하게 보고하세요.\n"
            "4. **긍정적이고 능동적인 표현**: 수동적인 표현보다는 능동적인 표현을 사용하여 책임감 있는 인상을 주세요.\n"
            "5. **출력 형식**: 다른 설명 없이 변환된 메시지만 바로 출력하세요."
        ),
        "lateral": (
            "당신은 원활한 협업을 이끌어내는 커뮤니케이션 전문가입니다. 주어진 핵심 내용을 바탕으로, 다른 팀 동료에게 협조를 요청하거나 정보를 전달하기 위한 명확하고 친절한 비즈니스 메시지를 작성해야 합니다. "
            "다음 지침을 반드시 따르세요:\n"
            "1. **배경 설명**: 요청의 배경이나 맥락을 간략히 설명하여 상대방의 이해를 돕습니다.\n"
            "2. **명확한 요청/전달 사항**: 무엇을 원하는지, 무엇을 전달하는지 명확하게 표현하세요. 필요시 기한(언제까지)을 구체적으로 명시합니다.\n"
            "3. **상호 존중의 어조**: '요', '해요' 체를 기본으로 사용하되, 정중하고 친절한 표현('부탁드립니다', '감사합니다')을 함께 사용하세요.\n"
            "4. **질문 형식 활용**: 일방적인 지시보다는 '확인해주실 수 있을까요?' 와 같이 부드러운 질문 형식을 활용하여 협조적인 분위기를 조성하세요.\n"
            "5. **출력 형식**: 다른 설명 없이 변환된 메시지만 바로 출력하세요."
        ),
        "external": (
            "당신은 고객 만족을 최우선으로 하는 CS/영업 전문가입니다. 주어진 핵심 내용을 바탕으로, 외부 고객에게 전달할 매우 정중하고 신뢰감 있는 비즈니스 메시지를 작성해야 합니다. "
            "다음 지침을 반드시 따르세요:\n"
            "1. **극존칭 사용**: '하십니까', '드립니다' 등의 극존칭을 사용하여 고객에 대한 최고의 존중을 표현하세요.\n"
            "2. **공감과 이해 표현**: 고객의 상황에 공감하고 이해하는 표현을 먼저 사용하여 긍정적인 관계를 형성하세요. (예: '불편을 드려 죄송합니다', '문의주셔서 감사합니다')\n"
            "3. **전문성과 신뢰성**: 기업의 공식적인 입장을 대변하는 프로페셔널한 인상을 주어야 합니다. 명확하고 정확한 정보를 제공하세요.\n"
            "4. **긍정적인 마무리**: 문의에 대한 감사 인사나 추가적인 도움을 제안하며 긍정적으로 마무리하세요.\n"
            "5. **출력 형식**: 다른 설명 없이 변환된 메시지만 바로 출력하세요."
        )
    }

    system_prompt = persona_instructions.get(persona, persona_instructions["lateral"])

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": keywords,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7,
            max_tokens=1024, # 결과가 잘리지 않도록 토큰 수 증가
            top_p=1,
            stop=None,
            stream=False,
        )

        converted_message = chat_completion.choices[0].message.content.strip()
        logging.info(f"Successfully converted message for persona '{persona}'.")
        return jsonify({"converted_message": converted_message})

    except Exception as e:
        logging.error(f"Error calling Groq API for persona '{persona}': {e}", exc_info=True)
        return jsonify({"error": "메시지 변환 중 서버에서 오류가 발생했습니다."}), 500

if __name__ == '__main__':
    # 디버그 모드는 개발 중에만 사용하고, 프로덕션 환경에서는 비활성화해야 합니다.
    app.run(debug=True, port=5000)
