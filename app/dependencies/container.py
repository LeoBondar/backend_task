from dependency_injector import containers, providers

from app.infrastructure.db import Database, SessionContext
from app.repositories.uow import IUnitOfWork, UnitOfWork
from app.settings import Settings
from app.use_cases.close_request import CloseRequestUseCase
from app.use_cases.create_operator import CreateOperatorUseCase
from app.use_cases.create_request import CreateRequestUseCase
from app.use_cases.create_source import CreateSourceUseCase
from app.use_cases.set_operator_weight import SetOperatorWeightUseCase
from app.use_cases.update_operator import UpdateOperatorUseCase
from app.views.get_leads import GetLeadsView
from app.views.get_operators import GetOperatorsView
from app.views.get_requests import GetRequestsView
from app.views.get_source_detail import GetSourceDetailView
from app.views.get_sources import GetSourcesView


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.api", __name__])
    settings = providers.Singleton(Settings)
    database: providers.Singleton[Database] = providers.Singleton(Database, settings=settings.provided.database)
    session_context = providers.Factory(SessionContext)

    unit_of_work: providers.ContextLocalSingleton[IUnitOfWork] = providers.ContextLocalSingleton(
        UnitOfWork, session_context=session_context, database=database
    )

    create_operator_use_case = providers.Factory(CreateOperatorUseCase, uow=unit_of_work)
    update_operator_use_case = providers.Factory(UpdateOperatorUseCase, uow=unit_of_work)
    create_source_use_case = providers.Factory(CreateSourceUseCase, uow=unit_of_work)
    set_operator_weight_use_case = providers.Factory(SetOperatorWeightUseCase, uow=unit_of_work)
    create_request_use_case = providers.Factory(CreateRequestUseCase, uow=unit_of_work)
    close_request_use_case = providers.Factory(CloseRequestUseCase, uow=unit_of_work)

    get_operators_view = providers.Factory(GetOperatorsView, uow=unit_of_work)
    get_sources_view = providers.Factory(GetSourcesView, uow=unit_of_work)
    get_source_detail_view = providers.Factory(GetSourceDetailView, uow=unit_of_work)
    get_requests_view = providers.Factory(GetRequestsView, uow=unit_of_work)
    get_leads_view = providers.Factory(GetLeadsView, uow=unit_of_work)
