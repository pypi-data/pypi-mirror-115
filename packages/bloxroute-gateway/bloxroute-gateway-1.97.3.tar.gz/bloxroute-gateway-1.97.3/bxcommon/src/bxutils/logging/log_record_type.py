from enum import Enum


class LogRecordType(Enum):
    Stats = "stats"
    BX = "bx"
    BlockInfo = "stats.blocks.events"
    BlockPropagationInfo = "stats.blocks.events.p"
    BdnPerformanceStats = "stats.bdn_performance"
    TransactionInfo = "stats.transactions.events"
    TransactionPropagationInfo = "stats.transactions.events.p"
    TransactionStats = "stats.transactions.summary"
    CloudApiPerformance = "stats.publicapi.performance"
    Throughput = "stats.throughput"
    Memory = "stats.memory"
    TransactionFeedStats = "stats.transaction.feed"
    EthOnBlockFeedStats = "stats.ethonblock.feed"
    NodeStatus = "stats.node.status"
    NodeInfo = "stats.node.info"
    NodeEvent = "stats.node.event"
    NetworkInfo = "stats.network.info"
    ConnectionState = "stats.connection_state"
    BlockCleanup = "bx.cleanup.block"
    TransactionCleanup = "bx.cleanup.transaction"
    BxMemory = "bx.memory"
    Recovery = "stats.recovery"
    TransactionHistogram = "bx.transaction.histogram"
    TransactionAudit = "stats.transaction.audit"
    TransactionAuditSummary = "stats.transaction.audit.summary"
    TransactionStatus = "transaction.status"
    TransactionTracing = "network_content.tx.tracing"
    BlockAuditSummary = "stats.block.audit.summary"
    AuditUpdates = "stats.audit.updates"
    CustomerInfo = "stats.customer.info"
    ExecutionTimerInfo = "stats.execution.timer.info"
    TaskDuration = "stats.task_duration"
    NetworkContent = "network_content.stats"
    NetworkContentTx = "network_content.tx.stats"
    NetworkContentBlock = "network_content.block.stats"
    RoutingService = "routing.service"
    ConnectionHealth = "stats.connection_health"
    PerformanceTroubleshooting = "stats.performance.responsiveness"
    MessageHandlingTroubleshooting = "stats.performance.message_handling"
    AlarmTroubleshooting = "stats.performance.alarm"
    NetworkTroubleshooting = "stats.performance.network"
    RoutingTableStats = "stats.routing"
    GarbageCollection = "stats.gc"
    ShortIdAllocation = "sid.allocation"
    Config = "config"
    QuotaNotification = "stats.quota.notification"
    QuotaFillStatus = "stats.quota.fill"
    TransactionFiltering = "transaction.filter"
    TxBlockchainStatusInfo = "stats.transaction.status"
    PrivateTransaction = "stats.private_transaction"
    PaidTransaction = "stats.transaction.paid_transaction"
    TxDetectionTimeLocation = "stats.transaction.tx_detection_time_location"
    TransactionMonitoring = "stats.transaction.monitoring"
    MEVBundleTransaction = "stats.transaction.mev_bundle"
    ProfitSharingPrivateTransaction = "stats.transaction.profit_sharing"
