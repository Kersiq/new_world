from dishka import make_async_container, AsyncContainer

from src.di.persistence.db import DBProvider
from src.di.persistence.services import ServiceProvider
from src.di.repositories import RepoProvider
from src.di.usecases import UseCaseProvider
from src.di.persistence.rmq import RMQProvider


def get_async_container() -> AsyncContainer:

        db_provider = DBProvider()
        rmq_provider = RMQProvider()

        repository_provider = RepoProvider()
        use_case_provider = UseCaseProvider()
        service_provider = ServiceProvider()

        return make_async_container(
                db_provider,
                repository_provider,
                use_case_provider,
                service_provider,
                rmq_provider
        )