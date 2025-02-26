from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from bot.services.database.models import Domain, User
from bot.services.database.engine import async_session


class UserORM:
    @staticmethod
    async def create_user(user: int) -> Optional[User]:
        async with async_session() as session:
            try:
                user = User(
                    user_id=user,
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)

                return user
            except IntegrityError:
                await session.rollback()

    @staticmethod
    async def get_all_user_id() -> Optional[list[int]]:
        async with async_session() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            users = result.scalars().all()

            users_list = [user.user_id for user in users]

            return users_list


class DomainORM:
    @staticmethod
    async def create_domain(domain: str) -> Optional[Domain]:
        async with async_session() as session:
            try:
                domain = Domain(
                    domain=domain,
                )

                session.add(domain)
                await session.commit()
                await session.refresh(domain)

                return domain
            except Exception as e:
                await session.rollback()

    @staticmethod
    async def get_all_domain_id() -> Optional[list[str]]:
        async with async_session() as session:
            stmt = select(Domain)
            result = await session.execute(stmt)
            domains = result.scalars().all()
            domains_list = [domain.domain for domain in domains]

            return domains_list

    @staticmethod
    async def banned_domain(domain: str) -> Optional[Domain]:
        async with async_session() as session:
            stmt = select(Domain).where(Domain.domain == domain)
            result = await session.execute(stmt)
            domain = result.scalars().first()

            if not domain:
                return

            domain.banned = True
            session.add(domain)
            await session.commit()
            await session.refresh(domain)