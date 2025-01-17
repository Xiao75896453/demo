from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from src.models.account import Account

from lib.exceptions import ConflictException, NotFound

USERNAME_NOT_EXISTS_REASON = "Username not exists"
USERNAME_ALREADY_EXISTS_REASON = "Username already exists"


async def create_account(account: Account, db_session: Session) -> None:
    try:
        db_session.add(account)
        db_session.flush()

    except IntegrityError:
        raise ConflictException(detail=USERNAME_ALREADY_EXISTS_REASON)


async def get_account(username: str, db_session: Session) -> Account:
    try:
        return (
            db_session.query(Account)
            .filter(Account.username == username)
            .with_for_update()
            .one()
        )
    except NoResultFound:
        raise NotFound(detail=USERNAME_NOT_EXISTS_REASON)


async def update_account(username: str, account: dict, db_session: Session):
    try:
        db_session.query(Account).filter(Account.username == username).update(account)
        db_session.flush()

    except IntegrityError:
        raise ConflictException(detail=USERNAME_ALREADY_EXISTS_REASON)
