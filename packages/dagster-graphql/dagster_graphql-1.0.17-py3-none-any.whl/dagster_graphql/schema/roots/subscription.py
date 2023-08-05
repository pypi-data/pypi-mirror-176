import graphene

import dagster._check as check
from dagster._core.storage.compute_log_manager import ComputeIOType

from ...implementation.execution import (
    get_captured_log_observable,
    get_compute_log_observable,
    get_pipeline_run_observable,
)
from ..external import GrapheneLocationStateChangeSubscription, get_location_state_change_observable
from ..logs.compute_logs import GrapheneCapturedLogs, GrapheneComputeIOType, GrapheneComputeLogFile
from ..pipelines.subscription import GraphenePipelineRunLogsSubscriptionPayload
from ..util import non_null_list


class GrapheneDagitSubscription(graphene.ObjectType):
    """The root for all subscriptions to retrieve real-time data from the Dagster instance."""

    class Meta:
        name = "DagitSubscription"

    pipelineRunLogs = graphene.Field(
        graphene.NonNull(GraphenePipelineRunLogsSubscriptionPayload),
        runId=graphene.Argument(graphene.NonNull(graphene.ID)),
        cursor=graphene.Argument(
            graphene.String,
            description="A cursor retrieved from the API. Pass 'HEAD' to stream from the current event onward.",
        ),
        description="Retrieve real-time event logs after applying a filter on run id and cursor.",
    )

    computeLogs = graphene.Field(
        graphene.NonNull(GrapheneComputeLogFile),
        runId=graphene.Argument(graphene.NonNull(graphene.ID)),
        stepKey=graphene.Argument(graphene.NonNull(graphene.String)),
        ioType=graphene.Argument(graphene.NonNull(GrapheneComputeIOType)),
        cursor=graphene.Argument(graphene.String),
        description="Retrieve real-time compute logs after applying a filter on run id, step name, log type, and cursor.",
    )

    capturedLogs = graphene.Field(
        graphene.NonNull(GrapheneCapturedLogs),
        logKey=graphene.Argument(non_null_list(graphene.String)),
        cursor=graphene.Argument(graphene.String),
        description="Retrieve real-time compute logs.",
    )

    locationStateChangeEvents = graphene.Field(
        graphene.NonNull(GrapheneLocationStateChangeSubscription),
        description="Retrieve real-time events when a location in the workspace undergoes a state change.",
    )

    def resolve_pipelineRunLogs(self, graphene_info, runId, cursor=None):
        return get_pipeline_run_observable(graphene_info, runId, cursor)

    def resolve_computeLogs(self, graphene_info, runId, stepKey, ioType, cursor=None):
        check.str_param(ioType, "ioType")  # need to resolve to enum
        return get_compute_log_observable(
            graphene_info, runId, stepKey, ComputeIOType(ioType), cursor
        )

    def resolve_capturedLogs(self, graphene_info, logKey, cursor=None):
        return get_captured_log_observable(graphene_info, logKey, cursor)

    def resolve_locationStateChangeEvents(self, graphene_info):
        return get_location_state_change_observable(graphene_info)
