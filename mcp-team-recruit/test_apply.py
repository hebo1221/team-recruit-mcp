#!/usr/bin/env python3
"""
지원서 제출 테스트 (로컬)
Slack 웹훅 없이 파일 저장만 테스트
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server import Applicant, save_applicant
from pathlib import Path

def test_applicant_validation():
    """지원자 스키마 검증 테스트"""
    print("\n=== 1. 스키마 검증 테스트 ===")

    # 정상 케이스
    try:
        valid_applicant = Applicant(
            name="테스트 지원자",
            contact="test@example.com",
            category="장병",
            message="로컬 테스트용 지원서입니다.",
            ai_subscriptions="Claude Pro"
        )
        print("✅ 정상 케이스: 검증 성공")
        print(f"   {valid_applicant.dict()}")
    except Exception as e:
        print(f"❌ 정상 케이스 실패: {e}")
        return False

    # 비정상 케이스 1: 이메일 형식 오류
    try:
        invalid_contact = Applicant(
            name="테",
            contact="123",
            category="일반인"
        )
        print("❌ 연락처 검증 실패 (통과해서는 안됨)")
        return False
    except Exception as e:
        print(f"✅ 연락처 검증: 올바르게 거부됨 ({type(e).__name__})")

    return True

def test_file_storage():
    """파일 저장 테스트"""
    print("\n=== 2. 파일 저장 테스트 ===")

    # 테스트 지원자 생성
    applicant = Applicant(
        name="김정훈",
        contact="kjh@example.com",
        category="장병",
        message="도로교통 영상 인식 프로젝트 3건 경험. DeepStream 최적화에 관심 많습니다.",
        ai_subscriptions="Claude Pro, ChatGPT Plus"
    )

    # 저장
    result = save_applicant(applicant)

    if result:
        print("✅ 파일 저장 성공")

        # 파일 확인
        data_file = Path(__file__).parent / "data" / "applicants.jsonl"
        if data_file.exists():
            print(f"✅ 파일 생성 확인: {data_file}")

            # 마지막 줄 읽기
            with open(data_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    import json
                    last_entry = json.loads(lines[-1])
                    print(f"✅ 저장된 데이터:")
                    print(f"   이름: {last_entry['name']}")
                    print(f"   연락처: {last_entry['contact']}")
                    print(f"   구분: {last_entry['category']}")
                    if last_entry.get('ai_subscriptions'):
                        print(f"   AI 구독: {last_entry['ai_subscriptions']}")
                    print(f"   타임스탬프: {last_entry['timestamp']}")
                else:
                    print("⚠️  파일은 있으나 내용이 비어있음")
        else:
            print(f"❌ 파일이 생성되지 않음: {data_file}")
            return False
    else:
        print("❌ 파일 저장 실패")
        return False

    return True

def test_multiple_applications():
    """복수 지원서 저장 테스트"""
    print("\n=== 3. 복수 지원서 저장 테스트 ===")

    applicants = [
        Applicant(
            name="이영희",
            contact="yhlee@example.com",
            category="사관생도",
            message="LLM 파이프라인 구축 경험 보유",
        ),
        Applicant(
            name="박철수",
            contact="cspark@example.com",
            category="장병",
            message="MLOps 자동화 경험",
            ai_subscriptions="Claude Pro"
        ),
        Applicant(
            name="최민수",
            contact="mscho@example.com",
            category="장병",
            message="API 설계 및 대용량 트래픽 처리 경험 3년",
            ai_subscriptions="ChatGPT Plus"
        )
    ]

    success_count = 0
    for applicant in applicants:
        if save_applicant(applicant):
            success_count += 1
            print(f"✅ {applicant.name} 저장 성공")
        else:
            print(f"❌ {applicant.name} 저장 실패")

    print(f"\n총 {success_count}/{len(applicants)}명 저장 성공")

    # 전체 파일 확인
    data_file = Path(__file__).parent / "data" / "applicants.jsonl"
    with open(data_file, "r", encoding="utf-8") as f:
        total_lines = len(f.readlines())
        print(f"✅ 전체 저장된 지원서: {total_lines}건")

    return success_count == len(applicants)

if __name__ == "__main__":
    print("=" * 60)
    print("MCP 팀 리크루팅 - 지원서 제출 로컬 테스트")
    print("=" * 60)

    # 데이터 디렉토리 확인
    data_dir = Path(__file__).parent / "data"
    print(f"\n데이터 디렉토리: {data_dir}")
    if not data_dir.exists():
        print("⚠️  데이터 디렉토리가 없습니다. 자동 생성됩니다.")

    # 테스트 실행
    all_passed = True

    all_passed &= test_applicant_validation()
    all_passed &= test_file_storage()
    all_passed &= test_multiple_applications()

    # 결과 요약
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 모든 테스트 통과!")
    else:
        print("❌ 일부 테스트 실패")
    print("=" * 60)

    sys.exit(0 if all_passed else 1)
