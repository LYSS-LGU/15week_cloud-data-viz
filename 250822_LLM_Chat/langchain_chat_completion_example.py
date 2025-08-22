#!/usr/bin/env python3
"""
LangChain을 활용한 Chat Completion API 실습 예제
==============================================

LangChain 프레임워크를 사용하여 OpenAI Chat Completion을 더 효율적으로 활용하는 방법

사용법:
1. 환경변수 설정: OPENAI_API_KEY
2. 필요한 패키지 설치: 
   pip install langchain-openai langchain-community python-dotenv
3. 실행: python langchain_chat_completion_example.py

작성일: 2025-08-22
"""

import os
import asyncio
import time
from typing import List
from dotenv import load_dotenv

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

# 환경변수 로드
load_dotenv()

class LangChainChatDemo:
    """LangChain을 활용한 Chat Completion 데모"""
    
    def __init__(self):
        """LangChain ChatOpenAI 초기화"""
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=500
        )
        
    def basic_langchain_chat(self) -> None:
        """기본 LangChain Chat 예제"""
        print("=" * 50)
        print("🦜 기본 LangChain Chat 예제")
        print("=" * 50)
        
        # 메시지 구성
        messages = [
            SystemMessage(content="당신은 친절한 한국어 AI 어시스턴트입니다."),
            HumanMessage(content="LangChain이 무엇인지 간단히 설명해주세요.")
        ]
        
        # 토큰 사용량 추적
        with get_openai_callback() as callback:
            response = self.llm.invoke(messages)
            
            print(f"📝 응답: {response.content}")
            print(f"💰 토큰 사용량:")
            print(f"   - 프롬프트 토큰: {callback.prompt_tokens}")
            print(f"   - 완료 토큰: {callback.completion_tokens}")
            print(f"   - 총 토큰: {callback.total_tokens}")
            print(f"   - 예상 비용: ${callback.total_cost:.6f}")

    def prompt_template_example(self) -> None:
        """프롬프트 템플릿 활용 예제"""
        print("\n" + "=" * 50)
        print("📋 프롬프트 템플릿 예제")
        print("=" * 50)
        
        # 프롬프트 템플릿 정의
        template = ChatPromptTemplate.from_messages([
            ("system", "당신은 {role}입니다. {style} 스타일로 답변해주세요."),
            ("human", "{question}")
        ])
        
        # 체인 구성
        chain = template | self.llm
        
        # 다양한 역할과 스타일로 실행
        scenarios = [
            {
                "role": "수학 선생님",
                "style": "친근하고 이해하기 쉬운",
                "question": "피타고라스 정리를 설명해주세요."
            },
            {
                "role": "요리 전문가",
                "style": "전문적이고 상세한",
                "question": "김치찌개 맛있게 끓이는 방법을 알려주세요."
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎭 시나리오 {i}: {scenario['role']}")
            
            with get_openai_callback() as callback:
                response = chain.invoke(scenario)
                print(f"응답: {response.content}")
                print(f"토큰 사용: {callback.total_tokens}")

    def conversation_memory_demo(self) -> None:
        """대화 메모리 관리 예제"""
        print("\n" + "=" * 50)
        print("💭 대화 메모리 관리 예제")
        print("=" * 50)
        
        # ConversationBufferMemory 사용
        memory = ConversationBufferMemory(return_messages=True)
        
        # 프롬프트 템플릿 (메모리 포함)
        template = ChatPromptTemplate.from_messages([
            ("system", "당신은 여행 상담사입니다. 고객의 여행 계획을 도와주세요."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 체인 구성
        chain = template | self.llm
        
        # 대화 시뮬레이션
        conversations = [
            "부산 여행을 계획하고 있어요. 2박 3일로 가려고 합니다.",
            "해운대 말고 다른 관광지도 추천해주세요.",
            "맛집도 알려주시면 좋겠어요.",
            "숙박은 어디가 좋을까요?"
        ]
        
        for i, user_input in enumerate(conversations, 1):
            print(f"\n👤 사용자 {i}: {user_input}")
            
            # 메모리에서 대화 히스토리 가져오기
            history = memory.chat_memory.messages
            
            with get_openai_callback() as callback:
                response = chain.invoke({
                    "input": user_input,
                    "history": history
                })
                
                print(f"🤖 AI: {response.content}")
                print(f"💰 토큰: {callback.total_tokens}")
                
                # 메모리에 대화 저장
                memory.chat_memory.add_user_message(user_input)
                memory.chat_memory.add_ai_message(response.content)
        
        print(f"\n📊 총 대화 히스토리 길이: {len(memory.chat_memory.messages)}")

    def window_memory_demo(self) -> None:
        """윈도우 메모리 예제"""
        print("\n" + "=" * 50)
        print("🪟 윈도우 메모리 예제")
        print("=" * 50)
        
        # 최근 4개 메시지만 유지 (2턴)
        window_memory = ConversationBufferWindowMemory(
            k=4,  # 최근 4개 메시지만 유지
            return_messages=True
        )
        
        template = ChatPromptTemplate.from_messages([
            ("system", "당신은 도움이 되는 어시스턴트입니다."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        chain = template | self.llm
        
        # 긴 대화 시뮬레이션
        long_conversations = [
            "안녕하세요! 파이썬 공부를 시작하려고 합니다.",
            "변수 선언하는 방법을 알려주세요.",
            "리스트와 튜플의 차이점은 무엇인가요?",
            "반복문은 어떻게 사용하나요?",
            "함수는 어떻게 정의하나요?",
            "처음 질문이 뭐였는지 기억하시나요?"  # 윈도우 밖의 내용
        ]
        
        for i, user_input in enumerate(long_conversations, 1):
            print(f"\n👤 [{i}] {user_input}")
            
            history = window_memory.chat_memory.messages
            print(f"📝 현재 메모리 크기: {len(history)} 메시지")
            
            response = chain.invoke({
                "input": user_input,
                "history": history
            })
            
            print(f"🤖 {response.content}")
            
            # 윈도우 메모리에 저장
            window_memory.chat_memory.add_user_message(user_input)
            window_memory.chat_memory.add_ai_message(response.content)
            
            time.sleep(1)

    async def async_batch_processing(self) -> None:
        """비동기 배치 처리 예제"""
        print("\n" + "=" * 50)
        print("⚡ 비동기 배치 처리 예제")
        print("=" * 50)
        
        # 여러 질문을 동시에 처리
        questions = [
            "파이썬의 장점 3가지를 알려주세요.",
            "머신러닝이란 무엇인가요?",
            "웹 개발에 필요한 기술스택을 추천해주세요.",
            "데이터베이스 설계 시 고려사항은?",
            "클라우드 컴퓨팅의 이점은 무엇인가요?"
        ]
        
        messages_list = []
        for question in questions:
            messages_list.append([
                SystemMessage(content="당신은 IT 전문가입니다."),
                HumanMessage(content=question)
            ])
        
        print("🚀 동기 처리 시작...")
        start_time = time.time()
        
        # 동기 처리 (순차 실행)
        sync_responses = []
        for messages in messages_list:
            response = self.llm.invoke(messages)
            sync_responses.append(response.content)
        
        sync_time = time.time() - start_time
        print(f"⏱️ 동기 처리 시간: {sync_time:.2f}초")
        
        print("\n🚀 비동기 처리 시작...")
        start_time = time.time()
        
        # 비동기 처리 (병렬 실행)
        async_responses = await self.llm.abatch(messages_list)
        
        async_time = time.time() - start_time
        print(f"⏱️ 비동기 처리 시간: {async_time:.2f}초")
        print(f"📈 성능 향상: {sync_time/async_time:.1f}배 빠름")
        
        # 결과 비교
        print(f"\n📊 처리 결과:")
        for i, (question, response) in enumerate(zip(questions, async_responses), 1):
            print(f"{i}. {question}")
            print(f"   답변: {response.content[:100]}...")
            print()

    def streaming_response_demo(self) -> None:
        """스트리밍 응답 예제"""
        print("\n" + "=" * 50)
        print("🌊 스트리밍 응답 예제")
        print("=" * 50)
        
        messages = [
            SystemMessage(content="당신은 창의적인 작가입니다."),
            HumanMessage(content="미래 도시에서 벌어지는 짧은 이야기를 들려주세요.")
        ]
        
        print("📖 실시간 스토리 생성:")
        print("-" * 30)
        
        # 스트리밍으로 응답 받기
        for chunk in self.llm.stream(messages):
            print(chunk.content, end='', flush=True)
        
        print("\n" + "-" * 30)
        print("✅ 스토리 생성 완료")

    def advanced_prompting_techniques(self) -> None:
        """고급 프롬프팅 기법 예제"""
        print("\n" + "=" * 50)
        print("🧠 고급 프롬프팅 기법 예제")
        print("=" * 50)
        
        # Chain-of-Thought 프롬프팅
        cot_template = ChatPromptTemplate.from_messages([
            ("system", "당신은 논리적 사고를 중시하는 문제 해결 전문가입니다."),
            ("human", """
다음 문제를 단계별로 차근차근 풀어보세요:

{problem}

각 단계별로 계산 과정을 명확히 보여주세요.
""")
        ])
        
        cot_chain = cot_template | self.llm
        
        problem = """
한 회사의 직원 수가 작년에 120명이었습니다.
올해 상반기에 20% 증가했고, 하반기에 15% 감소했습니다.
현재 직원 수는 몇 명인가요?
"""
        
        print("🧮 Chain-of-Thought 문제 해결:")
        with get_openai_callback() as callback:
            response = cot_chain.invoke({"problem": problem})
            print(response.content)
            print(f"\n💰 토큰 사용: {callback.total_tokens}")

    def run_all_demos(self) -> None:
        """모든 데모 실행"""
        print("🚀 LangChain Chat Completion 종합 실습 시작!")
        print("API 키 확인:", "✅ 설정됨" if os.getenv("OPENAI_API_KEY") else "❌ 없음")
        
        if not os.getenv("OPENAI_API_KEY"):
            print("\n❌ OPENAI_API_KEY 환경변수를 설정해주세요!")
            return
        
        demos = [
            ("기본 LangChain Chat", self.basic_langchain_chat),
            ("프롬프트 템플릿", self.prompt_template_example),
            ("대화 메모리 관리", self.conversation_memory_demo),
            ("윈도우 메모리", self.window_memory_demo),
            ("스트리밍 응답", self.streaming_response_demo),
            ("고급 프롬프팅 기법", self.advanced_prompting_techniques),
        ]
        
        for i, (name, demo_func) in enumerate(demos, 1):
            try:
                print(f"\n\n📌 [{i}/{len(demos)}] {name} 실행 중...")
                demo_func()
                time.sleep(2)
            except Exception as e:
                print(f"❌ {name} 실행 중 오류: {e}")
                continue
        
        # 비동기 데모는 별도 실행
        print(f"\n\n📌 [{len(demos)+1}/{len(demos)+1}] 비동기 배치 처리 실행 중...")
        try:
            asyncio.run(self.async_batch_processing())
        except Exception as e:
            print(f"❌ 비동기 배치 처리 실행 중 오류: {e}")
        
        print("\n\n🎉 모든 LangChain 데모 실행 완료!")
        print("\n💡 LangChain 활용 포인트:")
        print("   1. 프롬프트 템플릿으로 재사용성 향상")
        print("   2. 메모리 관리로 대화 맥락 유지")
        print("   3. 체인 구성으로 복잡한 워크플로우 구축")
        print("   4. 비동기 처리로 성능 최적화")
        print("   5. 콜백으로 토큰 사용량 모니터링")


def main():
    """메인 실행 함수"""
    demo = LangChainChatDemo()
    
    print("=" * 60)
    print("🦜 LangChain Chat Completion API 실습 예제")
    print("=" * 60)
    print("LangChain 프레임워크의 강력한 기능들을 실습해보세요!")
    print()
    
    while True:
        print("\n📋 실행할 데모를 선택하세요:")
        print("1. 전체 데모 실행")
        print("2. 기본 LangChain Chat")
        print("3. 프롬프트 템플릿")
        print("4. 대화 메모리 관리")
        print("5. 윈도우 메모리")
        print("6. 비동기 배치 처리")
        print("7. 스트리밍 응답")
        print("8. 고급 프롬프팅 기법")
        print("0. 종료")
        
        choice = input("\n선택 (0-8): ").strip()
        
        if choice == "0":
            print("👋 실습을 종료합니다!")
            break
        elif choice == "1":
            demo.run_all_demos()
        elif choice == "2":
            demo.basic_langchain_chat()
        elif choice == "3":
            demo.prompt_template_example()
        elif choice == "4":
            demo.conversation_memory_demo()
        elif choice == "5":
            demo.window_memory_demo()
        elif choice == "6":
            asyncio.run(demo.async_batch_processing())
        elif choice == "7":
            demo.streaming_response_demo()
        elif choice == "8":
            demo.advanced_prompting_techniques()
        else:
            print("❌ 올바른 번호를 선택해주세요!")


if __name__ == "__main__":
    main()
