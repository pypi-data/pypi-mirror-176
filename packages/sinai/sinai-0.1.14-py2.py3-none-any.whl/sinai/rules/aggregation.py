from __future__ import annotations

from datetime import datetime, timedelta

from sinai.metrics import AGGREGATION_CLASSES
from sinai.rules.base import Rule
from sinai.sources.base import MetricSource
from sinai.types import (
    AggregationMetricClass,
    AggregationMetrics,
    Evaluation,
    JDict,
    MetricClasses,
    MetricList,
    MetricSourceClass,
    MetricSourceClasses,
    MetricSourceInstance,
    MonitorInstance,
    SList,
)


class MetricAggregationRule(Rule):
    """A rule that aggregates stored metrics and produces a metric."""

    sources: MetricSourceClasses = []
    update: SList = []
    count: MetricClasses = []
    sum: MetricClasses = []
    max: MetricClasses = []
    min: MetricClasses = []
    mean: MetricClasses = []
    mode: MetricClasses = []
    median: MetricClasses = []
    last_only: bool = False
    exclude_checked: bool = False
    recent_only: bool = False

    def __init__(self, monitor: MonitorInstance, metric_source: MetricSource):
        super().__init__(monitor)
        self.metric_source = metric_source

    def evaluate(self) -> Evaluation:
        self.metrics: AggregationMetrics = []
        for agg in AGGREGATION_CLASSES:
            met_cls = getattr(self, agg)
            if met_cls:
                base_name = "+".join([cls.name for cls in met_cls])
                self._process_agg(agg, base_name)
        return self.metrics

    def _process_agg(self, aggregation_name: str, base_name: str) -> None:
        metric_instances = []
        for source_cls in self.sources:
            metric_instances.extend(
                self._get_metric_instances(source_cls, aggregation_name)
            )
        data_points = [metric.value for metric in metric_instances]
        metric_cls = self._get_aggregation_cls(aggregation_name)
        metric = metric_cls(name=f"{base_name}:{metric_cls.name}", update=self.update)
        metric.process_data_points(data_points)
        self.metrics.append(metric)

    def recent(self) -> datetime:
        """Subclass and redefine to change the definition of recent."""
        return datetime.utcnow() - timedelta(hours=4)

    def _get_aggregation_cls(self, aggregation_name: str) -> AggregationMetricClass:
        return AGGREGATION_CLASSES[aggregation_name]

    def _get_metric_instances(
        self, source_cls: MetricSourceClass, aggregation_name: str
    ) -> MetricList:
        metric_instances = []
        source: MetricSourceInstance = self.monitor.source(source_cls)  # type: ignore
        for target_class in getattr(self, aggregation_name):
            filter: JDict = {"name": target_class.name}
            if self.last_only:
                filter["monitor_id"] = self.monitor.id
            if self.exclude_checked:
                filter["checked"] = False
            if self.recent_only:
                filter["updated_at"] = {"$gt": self.recent()}
            instances = source.get(**filter)
            metric_instances.extend(instances)
        return metric_instances
