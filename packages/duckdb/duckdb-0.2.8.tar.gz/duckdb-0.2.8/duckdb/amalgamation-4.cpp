#include "src/function/table/system/pragma_functions.cpp"

#include "src/function/table/system/pragma_storage_info.cpp"

#include "src/function/table/system/pragma_table_info.cpp"

#include "src/function/table/system_functions.cpp"

#include "src/function/table/table_scan.cpp"

#include "src/function/table/unnest.cpp"

#include "src/function/table/version/pragma_version.cpp"

#include "src/function/udf_function.cpp"

#include "src/main/appender.cpp"

#include "src/main/client_context.cpp"

#include "src/main/config.cpp"

#include "src/main/connection.cpp"

#include "src/main/database.cpp"

#include "src/main/duckdb-c.cpp"

#include "src/main/materialized_query_result.cpp"

#include "src/main/prepared_statement.cpp"

#include "src/main/prepared_statement_data.cpp"

#include "src/main/query_profiler.cpp"

#include "src/main/query_result.cpp"

#include "src/main/relation.cpp"

#include "src/main/relation/aggregate_relation.cpp"

#include "src/main/relation/create_table_relation.cpp"

#include "src/main/relation/create_view_relation.cpp"

#include "src/main/relation/delete_relation.cpp"

#include "src/main/relation/distinct_relation.cpp"

#include "src/main/relation/explain_relation.cpp"

#include "src/main/relation/filter_relation.cpp"

#include "src/main/relation/insert_relation.cpp"

#include "src/main/relation/join_relation.cpp"

#include "src/main/relation/limit_relation.cpp"

#include "src/main/relation/order_relation.cpp"

#include "src/main/relation/projection_relation.cpp"

#include "src/main/relation/query_relation.cpp"

#include "src/main/relation/read_csv_relation.cpp"

#include "src/main/relation/setop_relation.cpp"

#include "src/main/relation/subquery_relation.cpp"

#include "src/main/relation/table_function_relation.cpp"

#include "src/main/relation/table_relation.cpp"

#include "src/main/relation/update_relation.cpp"

#include "src/main/relation/value_relation.cpp"

#include "src/main/relation/view_relation.cpp"

#include "src/main/relation/write_csv_relation.cpp"

#include "src/main/stream_query_result.cpp"

#include "src/optimizer/column_lifetime_analyzer.cpp"

#include "src/optimizer/common_aggregate_optimizer.cpp"

#include "src/optimizer/cse_optimizer.cpp"

#include "src/optimizer/deliminator.cpp"

#include "src/optimizer/expression_heuristics.cpp"

#include "src/optimizer/expression_rewriter.cpp"

#include "src/optimizer/filter_combiner.cpp"

#include "src/optimizer/filter_pullup.cpp"

#include "src/optimizer/filter_pushdown.cpp"

#include "src/optimizer/in_clause_rewriter.cpp"

#include "src/optimizer/join_order/join_relation_set.cpp"

#include "src/optimizer/join_order/query_graph.cpp"

#include "src/optimizer/join_order_optimizer.cpp"

#include "src/optimizer/matcher/expression_matcher.cpp"

#include "src/optimizer/optimizer.cpp"

#include "src/optimizer/pullup/pullup_both_side.cpp"

#include "src/optimizer/pullup/pullup_filter.cpp"

#include "src/optimizer/pullup/pullup_from_left.cpp"

#include "src/optimizer/pullup/pullup_projection.cpp"

#include "src/optimizer/pullup/pullup_set_operation.cpp"

#include "src/optimizer/pushdown/pushdown_aggregate.cpp"

#include "src/optimizer/pushdown/pushdown_cross_product.cpp"

#include "src/optimizer/pushdown/pushdown_filter.cpp"

#include "src/optimizer/pushdown/pushdown_get.cpp"

#include "src/optimizer/pushdown/pushdown_inner_join.cpp"

#include "src/optimizer/pushdown/pushdown_left_join.cpp"

#include "src/optimizer/pushdown/pushdown_mark_join.cpp"

#include "src/optimizer/pushdown/pushdown_projection.cpp"

#include "src/optimizer/pushdown/pushdown_set_operation.cpp"

#include "src/optimizer/pushdown/pushdown_single_join.cpp"

#include "src/optimizer/regex_range_filter.cpp"

#include "src/optimizer/remove_unused_columns.cpp"

#include "src/optimizer/rule/arithmetic_simplification.cpp"

#include "src/optimizer/rule/case_simplification.cpp"

#include "src/optimizer/rule/comparison_simplification.cpp"

#include "src/optimizer/rule/conjunction_simplification.cpp"

#include "src/optimizer/rule/constant_folding.cpp"

#include "src/optimizer/rule/date_part_simplification.cpp"

#include "src/optimizer/rule/distributivity.cpp"

#include "src/optimizer/rule/empty_needle_removal.cpp"

#include "src/optimizer/rule/in_clause_simplification_rule.cpp"

#include "src/optimizer/rule/like_optimizations.cpp"

#include "src/optimizer/rule/move_constants.cpp"

#include "src/optimizer/statistics/expression/propagate_aggregate.cpp"

#include "src/optimizer/statistics/expression/propagate_between.cpp"

#include "src/optimizer/statistics/expression/propagate_case.cpp"

#include "src/optimizer/statistics/expression/propagate_cast.cpp"

#include "src/optimizer/statistics/expression/propagate_columnref.cpp"

#include "src/optimizer/statistics/expression/propagate_comparison.cpp"

#include "src/optimizer/statistics/expression/propagate_conjunction.cpp"

#include "src/optimizer/statistics/expression/propagate_constant.cpp"

#include "src/optimizer/statistics/expression/propagate_function.cpp"

#include "src/optimizer/statistics/expression/propagate_operator.cpp"

#include "src/optimizer/statistics/operator/propagate_aggregate.cpp"

#include "src/optimizer/statistics/operator/propagate_cross_product.cpp"

#include "src/optimizer/statistics/operator/propagate_filter.cpp"

#include "src/optimizer/statistics/operator/propagate_get.cpp"

#include "src/optimizer/statistics/operator/propagate_join.cpp"

#include "src/optimizer/statistics/operator/propagate_limit.cpp"

#include "src/optimizer/statistics/operator/propagate_order.cpp"

#include "src/optimizer/statistics/operator/propagate_projection.cpp"

#include "src/optimizer/statistics/operator/propagate_set_operation.cpp"

#include "src/optimizer/statistics/operator/propagate_window.cpp"

#include "src/optimizer/statistics_propagator.cpp"

#include "src/optimizer/topn_optimizer.cpp"

#include "src/parallel/executor.cpp"

#include "src/parallel/pipeline.cpp"

#include "src/parallel/task_scheduler.cpp"

#include "src/parallel/thread_context.cpp"

#include "src/parser/base_expression.cpp"

#include "src/parser/column_definition.cpp"

#include "src/parser/constraint.cpp"

#include "src/parser/constraints/check_constraint.cpp"

#include "src/parser/constraints/not_null_constraint.cpp"

