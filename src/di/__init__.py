from dishka import make_async_container, AsyncContainer

from src.di.persistence.db import DBProvider
from src.di.repositories import RepoProvider
from src.di.usecases import UseCaseProvider


def get_async_container() -> AsyncContainer:

        db_provider = DBProvider()

        repository_provider = RepoProvider()
        use_case_provider = UseCaseProvider()

        return make_async_container(
                db_provider,
                repository_provider,
                use_case_provider,
        )