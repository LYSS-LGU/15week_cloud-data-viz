#!/usr/bin/env python3
"""
Chat Completion API 실습 예제
=========================

OpenAI Chat Completion API를 활용한 다양한 프롬프트 엔지니어링 기법 실습

사용법:
1. 환경변수 설정: OPENAI_API_KEY 또는 .env 파일에 API 키 설정
2. 필요한 패키지 설치: pip install openai python-dotenv
3. 실행: python chat_completion_example.py

"""

import os
import json
import time
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

# 환경변수 로드
load_dotenv()

class ChatCompletionDemo:
    """Chat Completion API 데모 클래스"""
    
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"  # 비용 효율적인 모델 사용
        
    def basic_chat_completion(self) -> None:
        """기본 Chat Completion 예제"""
        print("=" * 50)
        print("🤖 기본 Chat Completion 예제")
        print("=" * 50)
        
        messages = [
            {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
            {"role": "user", "content": "안녕하세요! 오늘 날씨가 어떤가요?"}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            
            print(f"모델: {response.model}")
            print(f"응답: {response.choices[0].message.content}")
            print(f"사용 토큰: {response.usage.total_tokens}")
            print(f"완료 이유: {response.choices[0].finish_reason}")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

    def zero_shot_prompting(self) -> None:
        """Zero-shot 프롬프팅 예제"""
        print("\n" + "=" * 50)
        print("🎯 Zero-shot 프롬프팅 예제")
        print("=" * 50)
        
        messages = [
            {"role": "system", "content": "당신은 감정 분석 전문가입니다."},
            {"role": "user", "content": """
다음 문장의 감정을 긍정, 부정, 중립 중 하나로 분류하세요.

문장: "이 제품은 쓸만하지만 가격이 너무 비싸요."

감정:"""}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,  # 일관된 결과를 위해 낮은 temperature
            max_tokens=10
        )
        
        print(f"Zero-shot 결과: {response.choices[0].message.content.strip()}")

    def few_shot_prompting(self) -> None:
        """Few-shot 프롬프팅 예제"""
        print("\n" + "=" * 50)
        print("📚 Few-shot 프롬프팅 예제")
        print("=" * 50)
        
        messages = [
            {"role": "system", "content": "당신은 감정 분석 전문가입니다."},
            {"role": "user", "content": """
다음 예시를 참고하여 문장의 감정을 분류하세요.

예시 1:
문장: "이 제품은 정말 좋아요!"
감정: 긍정

예시 2:
문장: "별로 기대에 못 미칩니다."
감정: 부정

예시 3:
문장: "그냥 평범한 제품이네요."
감정: 중립

이제 다음 문장을 분류해주세요:
문장: "이 제품은 쓸만하지만 가격이 너무 비싸요."
감정:"""}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            max_tokens=10
        )
        
        print(f"Few-shot 결과: {response.choices[0].message.content.strip()}")

    def role_prompting(self) -> None:
        """역할 지정 프롬프팅 예제"""
        print("\n" + "=" * 50)
        print("🎭 역할 지정 프롬프팅 예제")
        print("=" * 50)
        
        # 수학 선생님 역할
        messages = [
            {"role": "system", "content": """
당신은 경험이 풍부한 수학 선생님입니다. 
학생들이 이해하기 쉽도록 친근하고 단계별로 설명해주세요.
"""},
            {"role": "user", "content": "피타고라스 정리에 대해 설명해주세요."}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        print("🧑‍🏫 수학 선생님으로서의 설명:")
        print(response.choices[0].message.content)

    def chain_of_thought_prompting(self) -> None:
        """Chain-of-Thought 프롬프팅 예제"""
        print("\n" + "=" * 50)
        print("🧠 Chain-of-Thought 프롬프팅 예제")
        print("=" * 50)
        
        messages = [
            {"role": "system", "content": "당신은 논리적 사고를 중시하는 문제 해결 전문가입니다."},
            {"role": "user", "content": """
다음 문제를 단계별로 차근차근 풀어보세요:

철수는 사과 15개를 가지고 있었습니다. 
아침에 4개를 먹고, 점심에 친구에게 6개를 나누어 주었습니다.
오후에 마트에서 8개를 더 샀습니다.
저녁에 2개를 더 먹었습니다.

철수가 현재 가지고 있는 사과는 몇 개일까요?

각 단계별로 계산 과정을 보여주세요.
"""}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=400
        )
        
        print(response.choices[0].message.content)

    def output_format_control(self) -> None:
        """출력 포맷 제어 예제"""
        print("\n" + "=" * 50)
        print("📋 출력 포맷 제어 예제")
        print("=" * 50)
        
        # JSON 형식 출력 요청
        messages = [
            {"role": "system", "content": "당신은 정확한 JSON 형식으로 응답하는 어시스턴트입니다."},
            {"role": "user", "content": """
다음 정보를 JSON 형식으로 정리해주세요:

서울과 부산 두 도시의 예상 날씨 정보
- 서울: 기온 22도, 맑음
- 부산: 기온 25도, 흐림

JSON 형식으로 응답해주세요.
"""}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            max_tokens=200
        )
        
        print("📄 JSON 형식 출력:")
        try:
            # JSON 파싱 가능한지 확인
            json_str = response.choices[0].message.content.strip()
            if json_str.startswith('```json'):
                json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            parsed_json = json.loads(json_str)
            print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("원본 응답:")
            print(response.choices[0].message.content)

    def conversation_memory_demo(self) -> None:
        """대화 메모리 관리 예제"""
        print("\n" + "=" * 50)
        print("💭 대화 메모리 관리 예제")
        print("=" * 50)
        
        # 대화 히스토리를 누적하는 방식
        messages = [
            {"role": "system", "content": "당신은 여행 전문가입니다. 고객의 여행 계획을 도와주세요."}
        ]
        
        # 첫 번째 질문
        messages.append({"role": "user", "content": "부산 여행에서 꼭 가봐야 할 곳 하나만 추천해주세요."})
        
        response1 = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        
        print("👤 사용자: 부산 여행에서 꼭 가봐야 할 곳 하나만 추천해주세요.")
        print(f"🤖 AI: {response1.choices[0].message.content}")
        
        # AI 응답을 대화 히스토리에 추가
        messages.append({"role": "assistant", "content": response1.choices[0].message.content})
        
        # 두 번째 질문 (맥락 유지)
        messages.append({"role": "user", "content": "거기까지 부산역에서 어떻게 가나요?"})
        
        response2 = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        
        print("\n👤 사용자: 거기까지 부산역에서 어떻게 가나요?")
        print(f"🤖 AI: {response2.choices[0].message.content}")
        
        print(f"\n📊 총 메시지 수: {len(messages)}")

    def parameter_comparison(self) -> None:
        """매개변수 비교 예제"""
        print("\n" + "=" * 50)
        print("⚙️ 매개변수 비교 예제")
        print("=" * 50)
        
        prompt = "창의적인 단편소설 아이디어 하나를 제안해주세요."
        
        # Temperature 비교
        temperatures = [0.1, 0.7, 1.5]
        
        for temp in temperatures:
            messages = [
                {"role": "system", "content": "당신은 창의적인 작가입니다."},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=150
            )
            
            print(f"\n🌡️ Temperature {temp}:")
            print(response.choices[0].message.content)
            time.sleep(1)  # API 호출 제한 고려

    def streaming_response(self) -> None:
        """스트리밍 응답 예제"""
        print("\n" + "=" * 50)
        print("🌊 스트리밍 응답 예제")
        print("=" * 50)
        
        messages = [
            {"role": "system", "content": "당신은 도움이 되는 어시스턴트입니다."},
            {"role": "user", "content": "인공지능의 미래에 대해 간단히 설명해주세요."}
        ]
        
        print("🔄 실시간 스트리밍 응답:")
        print("-" * 30)
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end='', flush=True)
                    
            print("\n" + "-" * 30)
            print("✅ 스트리밍 완료")
            
        except Exception as e:
            print(f"❌ 스트리밍 오류: {e}")

    def token_counting_demo(self) -> None:
        """토큰 사용량 모니터링 예제"""
        print("\n" + "=" * 50)
        print("🔢 토큰 사용량 모니터링 예제")
        print("=" * 50)
        
        messages = [
            {"role": "system", "content": "당신은 효율적인 응답을 제공하는 어시스턴트입니다."},
            {"role": "user", "content": "Python에서 리스트와 튜플의 차이점을 설명해주세요."}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=200
        )
        
        usage = response.usage
        print(f"📊 토큰 사용량 분석:")
        print(f"   - 프롬프트 토큰: {usage.prompt_tokens}")
        print(f"   - 완료 토큰: {usage.completion_tokens}")
        print(f"   - 총 토큰: {usage.total_tokens}")
        
        # 대략적인 비용 계산 (gpt-4o-mini 기준)
        # 입력: $0.00015 / 1K tokens, 출력: $0.0006 / 1K tokens
        input_cost = (usage.prompt_tokens / 1000) * 0.00015
        output_cost = (usage.completion_tokens / 1000) * 0.0006
        total_cost = input_cost + output_cost
        
        print(f"💰 예상 비용: ${total_cost:.6f}")
        print(f"\n📝 응답 내용:")
        print(response.choices[0].message.content)

    def run_all_demos(self) -> None:
        """모든 데모 실행"""
        print("🚀 Chat Completion API 종합 실습 시작!")
        print("API 키 확인:", "✅ 설정됨" if os.getenv("OPENAI_API_KEY") else "❌ 없음")
        
        if not os.getenv("OPENAI_API_KEY"):
            print("\n❌ OPENAI_API_KEY 환경변수를 설정해주세요!")
            return
        
        demos = [
            ("기본 Chat Completion", self.basic_chat_completion),
            ("Zero-shot 프롬프팅", self.zero_shot_prompting),
            ("Few-shot 프롬프팅", self.few_shot_prompting),
            ("역할 지정 프롬프팅", self.role_prompting),
            ("Chain-of-Thought", self.chain_of_thought_prompting),
            ("출력 포맷 제어", self.output_format_control),
            ("대화 메모리 관리", self.conversation_memory_demo),
            ("매개변수 비교", self.parameter_comparison),
            ("스트리밍 응답", self.streaming_response),
            ("토큰 사용량 모니터링", self.token_counting_demo),
        ]
        
        for i, (name, demo_func) in enumerate(demos, 1):
            try:
                print(f"\n\n📌 [{i}/{len(demos)}] {name} 실행 중...")
                demo_func()
                time.sleep(2)  # API 호출 제한 고려
            except Exception as e:
                print(f"❌ {name} 실행 중 오류: {e}")
                continue
        
        print("\n\n🎉 모든 데모 실행 완료!")
        print("\n💡 실습 포인트:")
        print("   1. 각 프롬프트 기법의 차이점을 비교해보세요")
        print("   2. Temperature 값에 따른 응답 변화를 관찰하세요")
        print("   3. 토큰 사용량과 비용을 고려한 최적화를 생각해보세요")
        print("   4. 실제 프로젝트에 적용할 수 있는 패턴을 찾아보세요")


def main():
    """메인 실행 함수"""
    demo = ChatCompletionDemo()
    
    print("=" * 60)
    print("🤖 OpenAI Chat Completion API 실습 예제")
    print("=" * 60)
    print("다양한 프롬프트 엔지니어링 기법을 실습해보세요!")
    print()
    
    while True:
        print("\n📋 실행할 데모를 선택하세요:")
        print("1. 전체 데모 실행")
        print("2. 기본 Chat Completion")
        print("3. Zero-shot 프롬프팅")
        print("4. Few-shot 프롬프팅")
        print("5. 역할 지정 프롬프팅")
        print("6. Chain-of-Thought")
        print("7. 출력 포맷 제어")
        print("8. 대화 메모리 관리")
        print("9. 매개변수 비교")
        print("10. 스트리밍 응답")
        print("11. 토큰 사용량 모니터링")
        print("0. 종료")
        
        choice = input("\n선택 (0-11): ").strip()
        
        if choice == "0":
            print("👋 실습을 종료합니다!")
            break
        elif choice == "1":
            demo.run_all_demos()
        elif choice == "2":
            demo.basic_chat_completion()
        elif choice == "3":
            demo.zero_shot_prompting()
        elif choice == "4":
            demo.few_shot_prompting()
        elif choice == "5":
            demo.role_prompting()
        elif choice == "6":
            demo.chain_of_thought_prompting()
        elif choice == "7":
            demo.output_format_control()
        elif choice == "8":
            demo.conversation_memory_demo()
        elif choice == "9":
            demo.parameter_comparison()
        elif choice == "10":
            demo.streaming_response()
        elif choice == "11":
            demo.token_counting_demo()
        else:
            print("❌ 올바른 번호를 선택해주세요!")


if __name__ == "__main__":
    main()
