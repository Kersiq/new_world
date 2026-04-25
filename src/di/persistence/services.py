from dishka import Provider, provide, Scope

from src.infra.rmq.service.faststream_rmq import FastStreamRMQService
from src.application.interfaces.services.i_rmq import IRMQService


class ServiceProvider(Provider):

    fast_stream_rmq = provide(
        source=FastStreamRMQService,
        provides=IRMQService,
        scope=Scope.REQUEST
    )
