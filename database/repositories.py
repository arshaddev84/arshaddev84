from __future__ import annotations

from sqlalchemy.orm import Session

from .models import Document, User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: str) -> User | None:
        return self.session.query(User).filter(User.id == user_id).first()
    
    def create(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self.session =  session

    def get_by_id(self, doc_id: str) -> Document | None:
        return self.session.query(Document).filter(Document.id == doc_id).first()
    
    def get_by_user_id(self, user_id: str) -> list[Document]:
        return self.session.query(Document).filter(Document.user_id == user_id).all()
    
    def create(
            self,
            filename: str,
            content_type: str,
            size_bytes: str,
            file_path: str,
            user_id: str
    ) -> Document:
        doc = Document(
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            file_path=file_path,
            user_id=user_id
        )
        self.session.add(doc)
        self.session.commit()
        self.session.refresh(doc)
        return doc
    
    def mark_indexed(self, doc_id: str) -> None:
        doc = self.get_by_id(doc_id)
        if doc:
            doc.indexed = "1"
            self.session.commit()