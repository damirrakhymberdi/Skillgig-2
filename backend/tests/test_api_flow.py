import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.migrations import run_startup_migrations
from app.models import User
from app.routers.questions import _client_name
from app.schemas.answer import AnswerCreate
from app.schemas.question import QuestionCreate, QuestionUpdate
from app.schemas.user import ExpertProfileUpdate


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def register_and_login(client: TestClient, role: str = "client"):
    suffix = uuid.uuid4().hex[:10]
    email = f"{suffix}@example.com"
    username = f"user_{suffix}"
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "Valid-test-password-123!",
            "username": username,
            "firstName": "Damir",
            "lastName": "Test",
            "role": role,
        },
    )
    assert response.status_code == 201, response.text
    assert response.json()["user"]["firstName"] == "Damir"
    assert response.json()["user"]["lastName"] == "Test"

    login = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "Valid-test-password-123!"},
    )
    assert login.status_code == 200, login.text
    return login.json()["accessToken"], response.json()["user"]["id"]


def test_health_and_public_question_list(client: TestClient):
    assert client.get("/").json() == {"status": "ok"}
    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []


def test_draft_can_be_published_by_its_owner(client: TestClient):
    owner_token, _ = register_and_login(client)
    owner_headers = {"Authorization": f"Bearer {owner_token}"}
    other_token, _ = register_and_login(client)
    other_headers = {"Authorization": f"Bearer {other_token}"}
    created = client.post(
        "/api/v1/questions/",
        headers=owner_headers,
        json={
            "title": "A draft to publish",
            "description": "This question starts private.",
            "category": "Web Development",
        },
    )
    assert created.status_code == 201, created.text
    question_id = created.json()["id"]
    assert created.json()["status"] == "draft"
    assert client.get(f"/api/v1/questions/{question_id}").status_code == 404
    assert client.post(f"/api/v1/questions/{question_id}/submit", headers=other_headers).status_code == 403

    published = client.post(f"/api/v1/questions/{question_id}/submit", headers=owner_headers)
    assert published.status_code == 200, published.text
    assert published.json()["status"] == "published"
    assert client.get(f"/api/v1/questions/{question_id}").status_code == 200
    assert client.get("/api/v1/questions/").json()["total"] == 1
    assert client.post(f"/api/v1/questions/{question_id}/submit", headers=owner_headers).status_code == 409


def test_registration_enforces_supported_password_length(client: TestClient):
    short_password = client.post(
        "/api/v1/auth/register",
        json={"email": f"{uuid.uuid4().hex}@example.test", "password": "short"},
    )
    assert short_password.status_code == 422

    overlong_utf8_password = client.post(
        "/api/v1/auth/register",
        json={
            "email": f"{uuid.uuid4().hex}@example.test",
            "password": "қ" * 37,
        },
    )
    assert overlong_utf8_password.status_code == 422

    unsupported_role = client.post(
        "/api/v1/auth/register",
        json={
            "email": f"{uuid.uuid4().hex}@example.com",
            "password": "Valid-test-password-123!",
            "role": "admin",
        },
    )
    assert unsupported_role.status_code == 422


def test_register_login_create_and_read_question(client: TestClient):
    token, user_id = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    profile = client.get("/api/v1/users/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["firstName"] == "Damir"
    assert profile.json()["email"].endswith("@example.com")

    public_profile = client.get(f"/api/v1/users/profile/{user_id}")
    assert public_profile.status_code == 200
    assert "email" not in public_profile.json()

    created = client.post(
        "/api/v1/questions/",
        headers=headers,
        json={
            "title": "How do I fix a Vue component?",
            "description": "A test question for the API flow.",
            "category": "Web Development",
            "status": "published",
        },
    )
    assert created.status_code == 201, created.text
    question_id = created.json()["id"]

    detail = client.get(f"/api/v1/questions/{question_id}")
    assert detail.status_code == 200
    assert detail.json()["title"] == "How do I fix a Vue component?"
    assert detail.json()["clientName"] == "Damir Test"
    assert "clientEmail" not in detail.json()

    search = client.get("/api/v1/questions/?search=Vue%20component")
    assert search.status_code == 200
    assert search.json()["total"] == 1
    assert search.json()["items"][0]["id"] == question_id

    draft = client.post(
        "/api/v1/questions/",
        headers=headers,
        json={
            "title": "Private draft question",
            "description": "This must not appear in public totals.",
            "category": "Web Development",
            "status": "draft",
        },
    )
    assert draft.status_code == 201, draft.text
    draft_id = draft.json()["id"]
    assert client.get(f"/api/v1/questions/{draft_id}").status_code == 404
    assert client.get(f"/api/v1/questions/{draft_id}", headers=headers).status_code == 200
    assert client.get(f"/api/v1/questions/{draft_id}/answers").status_code == 404
    assert client.get("/api/v1/questions/?status_filter=all").json()["total"] == 1
    assert client.get("/api/v1/questions/?status_filter=draft").json()["total"] == 0

    stats = client.get("/api/v1/stats")
    assert stats.status_code == 200
    assert stats.json()["totalQuestions"] == 1
    assert stats.json()["totalExperts"] == 0

    categories = client.get("/api/v1/categories")
    assert categories.status_code == 200
    web_category = next(
        category for category in categories.json()
        if category["name"] == "Web Development"
    )
    assert web_category["totalQuestions"] == 1

    self_answer = client.post(
        f"/api/v1/questions/{question_id}/answers",
        headers=headers,
        json={"answerText": "The owner should not answer this question."},
    )
    assert self_answer.status_code == 403

    expert_token, _ = register_and_login(client, role="expert")
    expert_headers = {"Authorization": f"Bearer {expert_token}"}
    assert client.get(f"/api/v1/questions/{draft_id}", headers=expert_headers).status_code == 404
    assert client.post(
        f"/api/v1/questions/{draft_id}/answers",
        headers=expert_headers,
        json={"answerText": "A draft must stay private."},
    ).status_code == 403
    answers = client.post(
        f"/api/v1/questions/{question_id}/answers",
        headers=expert_headers,
        json={"answerText": "Try checking the component state update."},
    )
    assert answers.status_code == 201, answers.text
    assert "authorEmail" not in answers.json()

    unanswered = client.post(
        "/api/v1/questions/",
        headers=headers,
        json={
            "title": "A second unanswered question",
            "description": "Used to verify answer-count ordering.",
            "category": "Web Development",
            "status": "published",
        },
    )
    assert unanswered.status_code == 201, unanswered.text
    unanswered_id = unanswered.json()["id"]

    most_answered = client.get(
        "/api/v1/questions/?sort_by=most-answered&status_filter=all"
    )
    least_answered = client.get(
        "/api/v1/questions/?sort_by=least-answered&status_filter=all"
    )
    assert most_answered.json()["items"][0]["id"] == question_id
    assert least_answered.json()["items"][0]["id"] == unanswered_id
    most_answered_order = most_answered.json()["items"]
    paged = client.get(
        "/api/v1/questions/?sort_by=most-answered&status_filter=all&limit=1&offset=1"
    )
    assert paged.json()["total"] == 2
    assert len(paged.json()["items"]) == 1
    assert paged.json()["items"][0]["id"] == most_answered_order[1]["id"]

    public_answers = client.get(f"/api/v1/questions/{question_id}/answers")
    assert public_answers.status_code == 200
    assert "authorEmail" not in public_answers.json()[0]


def test_production_rejects_weak_secret():
    from app.core.config import Settings

    with pytest.raises(ValueError, match="APP_SECRET_KEY"):
        Settings(
            environment="production",
            secret_key="change-me-super-secret-key",
            _env_file=None,
        )

    settings = Settings(
        environment="production",
        secret_key="a-unique-production-key-with-more-than-32-characters",
        _env_file=None,
    )
    assert settings.environment == "production"


def test_startup_migration_adds_missing_code_columns_idempotently():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE questions (id TEXT PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE answers (id TEXT PRIMARY KEY)"))

    run_startup_migrations(engine)
    run_startup_migrations(engine)

    with engine.connect() as connection:
        question_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(questions)"))
        }
        answer_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(answers)"))
        }
    assert "code_example" in question_columns
    assert "code_example" in answer_columns
    engine.dispose()


def test_public_name_fallback_does_not_expose_email():
    user = User(
        id="anonymous-name-user",
        email="private@example.test",
        role="client",
    )
    assert _client_name(user) == "Пайдаланушы"


def test_user_submitted_links_only_allow_http_or_https():
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        QuestionCreate(
            title="Unsafe link test",
            description="Testing URL validation.",
            category="Web Development",
            code_link="javascript:alert(1)",
        )
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        QuestionUpdate(links=["data:text/html,<script>alert(1)</script>"])
    with pytest.raises(ValueError):
        QuestionCreate(
            title="Invalid status test",
            description="Only open or draft statuses can be created.",
            category="Web Development",
            status="resolved",
        )
    with pytest.raises(ValueError):
        QuestionUpdate(status="resolved")
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        AnswerCreate(answer_text="See this", links=["javascript:alert(1)"])
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        ExpertProfileUpdate(github_url="//attacker.example/profile")

    assert QuestionCreate(
        title="Safe link test",
        description="This is a safe link.",
        category="Web Development",
        code_link="https://github.com/example/project",
    ).code_link == "https://github.com/example/project"


def test_chat_messages_require_question_participants(client: TestClient):
    client_token, client_id = register_and_login(client)
    expert_token, expert_id = register_and_login(client, role="expert")
    outsider_token, _ = register_and_login(client)
    client_headers = {"Authorization": f"Bearer {client_token}"}
    expert_headers = {"Authorization": f"Bearer {expert_token}"}
    outsider_headers = {"Authorization": f"Bearer {outsider_token}"}

    created_question = client.post(
        "/api/v1/questions/",
        headers=client_headers,
        json={
            "title": "Question with a private chat",
            "description": "Only the asker and answer author may chat.",
            "category": "Web Development",
            "status": "published",
        },
    )
    assert created_question.status_code == 201, created_question.text

    non_expert_answer = client.post(
        f"/api/v1/questions/{created_question.json()['id']}/answers",
        headers=outsider_headers,
        json={"answerText": "A client account should not answer as an expert."},
    )
    assert non_expert_answer.status_code == 403
    question_id = created_question.json()["id"]

    answer = client.post(
        f"/api/v1/questions/{question_id}/answers",
        headers=expert_headers,
        json={"answerText": "I can help with that."},
    )
    assert answer.status_code == 201, answer.text

    owner_chat_url = (
        f"/api/v1/chat/questions/{question_id}/messages?partner_id={expert_id}"
    )
    sent = client.post(
        owner_chat_url,
        headers=client_headers,
        json={"text": "Thanks for your answer."},
    )
    assert sent.status_code == 201, sent.text
    assert sent.json()["senderId"] == client_id
    assert sent.json()["recipientId"] == expert_id

    expert_chat_url = (
        f"/api/v1/chat/questions/{question_id}/messages?partner_id={client_id}"
    )
    received = client.get(expert_chat_url, headers=expert_headers)
    assert received.status_code == 200
    assert [item["text"] for item in received.json()] == [
        "Thanks for your answer."
    ]

    forbidden = client.get(owner_chat_url, headers=outsider_headers)
    assert forbidden.status_code == 403

    deleted = client.delete(
        f"/api/v1/questions/{question_id}", headers=client_headers
    )
    assert deleted.status_code == 204
    assert client.get(expert_chat_url, headers=expert_headers).status_code == 404


def test_accepting_another_answer_replaces_the_previous_acceptance(client: TestClient):
    owner_token, _ = register_and_login(client)
    first_expert_token, first_expert_id = register_and_login(client, role="expert")
    second_expert_token, second_expert_id = register_and_login(client, role="expert")
    outsider_token, _ = register_and_login(client)

    owner_headers = {"Authorization": f"Bearer {owner_token}"}
    first_expert_headers = {"Authorization": f"Bearer {first_expert_token}"}
    second_expert_headers = {"Authorization": f"Bearer {second_expert_token}"}
    outsider_headers = {"Authorization": f"Bearer {outsider_token}"}

    question_response = client.post(
        "/api/v1/questions/",
        headers=owner_headers,
        json={
            "title": "Choose one accepted answer",
            "description": "A question for acceptance replacement coverage.",
            "category": "Web Development",
            "status": "published",
        },
    )
    assert question_response.status_code == 201, question_response.text
    question_id = question_response.json()["id"]

    first_answer = client.post(
        f"/api/v1/questions/{question_id}/answers",
        headers=first_expert_headers,
        json={"answerText": "First proposed solution."},
    )
    second_answer = client.post(
        f"/api/v1/questions/{question_id}/answers",
        headers=second_expert_headers,
        json={"answerText": "Second proposed solution."},
    )
    assert first_answer.status_code == 201, first_answer.text
    assert second_answer.status_code == 201, second_answer.text

    verify_url = (
        f"/api/v1/questions/{question_id}/answers/"
        f"{first_answer.json()['id']}/verify"
    )
    denied = client.post(
        verify_url,
        headers=outsider_headers,
        json={"isCorrect": True},
    )
    assert denied.status_code == 403

    accepted_first = client.post(
        verify_url,
        headers=owner_headers,
        json={"isCorrect": True},
    )
    assert accepted_first.status_code == 200, accepted_first.text

    second_verify_url = (
        f"/api/v1/questions/{question_id}/answers/"
        f"{second_answer.json()['id']}/verify"
    )
    accepted_second = client.post(
        second_verify_url,
        headers=owner_headers,
        json={"isCorrect": True},
    )
    assert accepted_second.status_code == 200, accepted_second.text

    answers = client.get(f"/api/v1/questions/{question_id}/answers")
    assert answers.status_code == 200
    by_author = {item["authorId"]: item for item in answers.json()}
    assert by_author[first_expert_id]["isAccepted"] is False
    assert by_author[first_expert_id]["authorProfile"]["resolvedQuestions"] == 0
    assert by_author[second_expert_id]["isAccepted"] is True
    assert by_author[second_expert_id]["authorProfile"]["resolvedQuestions"] == 1

    question = client.get(f"/api/v1/questions/{question_id}").json()
    assert question["status"] == "resolved"
    assert question["acceptedAnswerId"] == second_answer.json()["id"]
    assert client.get("/api/v1/stats").json()["successRate"] == 100.0

    unaccepted_second = client.post(
        second_verify_url,
        headers=owner_headers,
        json={"isCorrect": False},
    )
    assert unaccepted_second.status_code == 200, unaccepted_second.text
    question = client.get(f"/api/v1/questions/{question_id}").json()
    assert question["status"] == "published"
    assert question["acceptedAnswerId"] is None
    assert client.get("/api/v1/stats").json()["successRate"] == 0.0


def test_expert_profile_is_required_to_answer_and_can_be_created_later(
    client: TestClient,
):
    owner_token, _ = register_and_login(client)
    owner_headers = {"Authorization": f"Bearer {owner_token}"}
    question_response = client.post(
        "/api/v1/questions/",
        headers=owner_headers,
        json={
            "title": "Question for expert profile access",
            "description": "An expert needs a profile before answering.",
            "category": "Web Development",
            "status": "published",
        },
    )
    assert question_response.status_code == 201, question_response.text
    question_id = question_response.json()["id"]

    suffix = uuid.uuid4().hex[:10]
    email = f"expert_{suffix}@example.com"
    username = f"expert_{suffix}"
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "Valid-test-password-123!",
            "username": username,
            "role": "expert",
        },
    )
    assert registration.status_code == 201, registration.text
    login = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "Valid-test-password-123!"},
    )
    assert login.status_code == 200, login.text
    expert_headers = {"Authorization": f"Bearer {login.json()['accessToken']}"}

    no_profile_answer = client.post(
        f"/api/v1/questions/{question_id}/answers",
        headers=expert_headers,
        json={"answerText": "This should require an expert profile."},
    )
    assert no_profile_answer.status_code == 403

    profile = client.put(
        "/api/v1/users/me/profile",
        headers=expert_headers,
        json={
            "fullName": "Profiled Expert",
            "primaryRole": "Backend Developer",
            "skills": ["FastAPI", "PostgreSQL"],
        },
    )
    assert profile.status_code == 200, profile.text

    answer = client.post(
        f"/api/v1/questions/{question_id}/answers",
        headers=expert_headers,
        json={"answerText": "This answer is allowed after profile setup."},
    )
    assert answer.status_code == 201, answer.text
    assert answer.json()["authorProfile"]["primaryRole"] == "Backend Developer"
