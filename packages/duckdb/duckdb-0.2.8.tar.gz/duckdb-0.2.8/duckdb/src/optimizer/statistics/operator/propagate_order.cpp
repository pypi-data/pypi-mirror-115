#include "duckdb/optimizer/statistics_propagator.hpp"
#include "duckdb/planner/operator/logical_order.hpp"
#include "duckdb/storage/statistics/base_statistics.hpp"

namespace duckdb {

unique_ptr<NodeStatistics> StatisticsPropagator::PropagateStatistics(LogicalOrder &order,
                                                                     unique_ptr<LogicalOperator> *node_ptr) {
	// first propagate to the child
	node_stats = PropagateStatistics(order.children[0]);

	// then propagate to each of the order expressions
	for (idx_t i = 0; i < order.orders.size(); i++) {
		auto &expr = order.orders[i].expression;
		PropagateExpression(expr);
		if (expr->stats) {
			order.statistics.push_back(expr->stats->Copy());
		} else {
			order.statistics.push_back(nullptr);
		}
	}
	return move(node_stats);
}

} // namespace duckdb
