from drf_spectacular.utils import OpenApiExample, OpenApiParameter

STANDARD_REGISTRATION_POST_PARAMETERS = [
    OpenApiParameter(
        name="email",
        description="E-mail",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="password",
        description="Password",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="repeat_password",
        description="Repeat password",
        required=True,
        type=str,
    ),
]

STANDARD_LOGIN_POST_PARAMETERS = [
    OpenApiParameter(
        name="email",
        description="E-mail",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="password",
        description="Password",
        required=True,
        type=str,
    ),
]

REMIND_PASSWORD_POST_PARAMETERS = [
    OpenApiParameter(
        name="email",
        description="E-mail",
        required=True,
        type=str,
    ),
]

SOCIAL_AUTH_POST_PARAMETERS = [
    OpenApiParameter(
        name="token",
        description="Social authorization token",
        required=True,
        type=str,
    ),
]

CHANGE_EMAIL_POST_PARAMETERS = [
    OpenApiParameter(
        name="new_email",
        description="New user email",
        required=True,
        type=str,
    ),
]

ACCOUNT_EMAIL_CHANGED_RESPONSE = OpenApiExample(
    "email_changed",
    value={"detail": "E-mail changed successfully!"},
    response_only=True,
    status_codes=["200"],
)

ACCOUNT_EMAIL_CHANGED_FAILED_RESPONSE = OpenApiExample(
    "password_changed",
    value={
        "detail": [
            "E-mail already in use!",
            "Action not allowed for user's account type!",
        ],
        "serializer_field": ["field error details"],
    },
    response_only=True,
    status_codes=["400"],
)
