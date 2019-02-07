# conftest.py
# 
# from pathlib import Path
# from types import SimpleNamespace
# from unittest import mock
# 
# import pytest
# 
# from my_idea_pool import db, create_app
# 
# 
# HERE = Path(__file__).resolve().parent
# TESTDATA_FILE = HERE / "fixturedata.sql"
# 
# 
# def pytest_namespace():
#     return {
#         # defined in fixturedata.sql
#         "test_user": SimpleNamespace(
#                             id=42, 
#                             email="test@example.com", 
#                             password="P4ssw0rd!"
#         ),
#         "other_owner_idea_id": 17,
#     }
# 
# 
# @pytest.fixture
# def app(tmpdir):
#     """Configured Flask app for testing"""
#     app = create_app(
#         {
#             "TESTING": True,
#             "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmpdir}/testdatabase.db",
#         }
#     )
# 
#     with app.app_context():
#         db.create_all()
#         if TESTDATA_FILE.exists():
#             for stmt in TESTDATA_FILE.read_text(encoding="utf8").split(";"):
#                 if stmt.strip():
#                     db.engine.execute(stmt)
# 
#     yield app
# 
# 
# @pytest.fixture
# def app_context(app):
#     """Provide an active app context"""
#     with app.app_context():
#         yield app
# 
# 
# @pytest.fixture
# def client(app):
#     """Flask test client, for web request testing"""
#     return app.test_client()
# 
# 
# @pytest.fixture
# def user(app):
#     """REST-ful client with valid authorization token"""
#     response = app.post(
#         "/access-tokens",
#         json={"email": pytest.test_user.email, 
#               "password": pytest.test_user.password},
#     )
#     token = response.json["jwt"]
#     app.environ_base["HTTP_X_ACCESS_TOKEN"] = token
# 
#     return app
