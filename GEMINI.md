# Gemini 컨텍스트: BizTone Converter

## 프로젝트 개요

"BizTone Converter" 프로젝트는 일상적인 언어를 전문적인 비즈니스 커뮤니케이션으로 변환하는 데 도움을 주기 위해 설계된 웹 기반 애플리케이션입니다. 이 애플리케이션은 정적 프런트엔드를 제공하고 언어 변환을 위한 API를 제공하는 Python/Flask 백엔드로 구축되었습니다. 핵심 로직은 Groq AI API를 활용하여 상사(`upward`), 동료(`lateral`), 외부 고객(`external`)과 같은 다양한 대상에 맞춰 메시지 톤을 조정합니다.

프런트엔드는 바닐라 HTML, JavaScript로 구성되었으며, Tailwind CSS로 스타일링되어 사용자가 텍스트를 입력하고, 변환된 결과를 확인하고, 클립보드에 복사할 수 있는 깔끔하고 반응성이 뛰어난 2분할 인터페이스를 제공합니다.

### 주요 기술
- **백엔드**: Python, Flask, Flask-CORS, Gunicorn
- **프런트엔드**: HTML, JavaScript (ES6+), Tailwind CSS
- **AI**: Groq AI API (`moonshotai/kimi-k2-instruct-0905` 모델)
- **환경**: Python `venv`를 사용한 종속성 관리, `.env` 파일을 사용한 비밀 관리

### 아키텍처
이 프로젝트는 간단한 클라이언트-서버 모델을 따릅니다:
1. Flask 백엔드는 `frontend/index.html` 및 해당 정적 자산(`js/script.js`)을 제공합니다.
2. 프런트엔드는 사용자 입력을 캡처하고 `/api/convert` 엔드포인트로 비동기 `POST` 요청을 보냅니다.
3. 백엔드는 요청을 수신하고, 상세하고 페르소나별 프롬프트를 구성하며, Groq AI API를 호출합니다.
4. AI의 응답은 프런트엔드로 다시 전송되며, 프런트엔드는 사용자에게 결과를 표시합니다.

## 빌드 및 실행

### 1. 설정
- `.venv` 디렉토리에 Python 가상 환경이 있어야 합니다.
- 프로젝트 루트에 `.env` 파일을 생성하고 Groq API 키를 추가합니다:
  ```
  GROQ_API_KEY="YOUR_API_KEY_HERE"
  ```

### 2. 애플리케이션 실행
애플리케이션은 프런트엔드와 백엔드 API를 모두 제공하는 단일 Flask 서버로 구성됩니다.

1. **가상 환경 활성화:**
    ```shell
    # Windows
    .\.venv\Scripts\activate
    ```

2. **종속성 설치:**
    ```shell
    pip install -r backend/requirements.txt
    ```

3. **Flask 개발 서버 시작:**
    ```shell
    python backend/app.py
    ```
    애플리케이션은 `http://127.0.0.1:5000`에서 사용할 수 있습니다.

## 개발 컨벤션

- **API 엔드포인트**: 기본 API 엔드포인트는 `POST /api/convert`입니다. 이 엔드포인트는 `keywords` (변환할 텍스트) 및 `persona` (`upward`, `lateral`, `external`)가 포함된 JSON 페이로드를 예상합니다.
- **프런트엔드 로직**: 모든 클라이언트 측 로직은 `frontend/js/script.js`에 포함되어 있습니다. DOM 조작, 사용자 이벤트 및 `fetch` 함수를 사용하여 백엔드 API를 호출합니다.
- **백엔드 로직**: 주요 애플리케이션 로직은 `backend/app.py`에 있습니다. 여기에는 프런트엔드를 제공하는 라우트, `/api/convert` API 및 AI 모델에 대한 상세한 시스템 프롬프트가 포함됩니다.
- **스타일링**: 스타일링은 `frontend/index.html`의 Tailwind CSS 유틸리티 클래스를 통해서만 처리됩니다. 프로젝트는 Tailwind CDN을 사용하므로 CSS에 대한 빌드 단계가 필요하지 않습니다.
- **로깅**: 백엔드는 Python의 내장 `logging` 모듈을 사용하여 요청, 성공적인 변환 및 오류를 콘솔에 로깅합니다.