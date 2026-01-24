from enum import Enum
from dataclasses import dataclass
from typing import Optional


class UserType(Enum):
    """사용자 유형 열거형"""
    STANDARD = "standard_user"
    LOCKED_OUT = "locked_out_user"
    PROBLEM = "problem_user"
    PERFORMANCE_GLITCH = "performance_glitch_user"
    ERROR = "error_user"
    VISUAL = "visual_user"


@dataclass
class User:
    """사용자 데이터 클래스"""
    username: str
    password: str
    user_type: UserType
    description: str
    can_login: bool = True
    expected_error: Optional[str] = None


class Users:
    """테스트 사용자 데이터"""

    PASSWORD = "secret_sauce"

    # 사용자 정의
    STANDARD = User(
        username="standard_user",
        password=PASSWORD,
        user_type=UserType.STANDARD,
        description="정상 로그인이 가능한 표준 사용자",
        can_login=True
    )

    LOCKED_OUT = User(
        username="locked_out_user",
        password=PASSWORD,
        user_type=UserType.LOCKED_OUT,
        description="잠긴 계정 - 로그인 불가",
        can_login=False,
        expected_error="Epic sadface: Sorry, this user has been locked out."
    )

    PROBLEM = User(
        username="problem_user",
        password=PASSWORD,
        user_type=UserType.PROBLEM,
        description="문제가 있는 사용자 - 이미지가 깨지는 등의 버그 발생",
        can_login=True
    )

    PERFORMANCE_GLITCH = User(
        username="performance_glitch_user",
        password=PASSWORD,
        user_type=UserType.PERFORMANCE_GLITCH,
        description="성능 문제가 있는 사용자 - 응답이 느림",
        can_login=True
    )

    ERROR = User(
        username="error_user",
        password=PASSWORD,
        user_type=UserType.ERROR,
        description="에러가 발생하는 사용자 - 특정 기능에서 에러 발생",
        can_login=True
    )

    VISUAL = User(
        username="visual_user",
        password=PASSWORD,
        user_type=UserType.VISUAL,
        description="비주얼 버그가 있는 사용자 - UI가 깨짐",
        can_login=True
    )

    @classmethod
    def get_all_users(cls):
        """모든 사용자 목록 반환"""
        return [
            cls.STANDARD,
            cls.LOCKED_OUT,
            cls.PROBLEM,
            cls.PERFORMANCE_GLITCH,
            cls.ERROR,
            cls.VISUAL
        ]

    @classmethod
    def get_valid_users(cls):
        """로그인 가능한 사용자 목록 반환"""
        return [user for user in cls.get_all_users() if user.can_login]

    @classmethod
    def get_invalid_users(cls):
        """로그인 불가능한 사용자 목록 반환"""
        return [user for user in cls.get_all_users() if not user.can_login]
