//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/join/physical_join.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_sink.hpp"
#include "duckdb/planner/operator/logical_comparison_join.hpp"

namespace duckdb {

//! PhysicalJoin represents the base class of the join operators
class PhysicalJoin : public PhysicalSink {
public:
	PhysicalJoin(LogicalOperator &op, PhysicalOperatorType type, JoinType join_type, idx_t estimated_cardinality);

	JoinType join_type;

public:
	static void ConstructSemiJoinResult(DataChunk &left, DataChunk &result, bool found_match[]);
	static void ConstructAntiJoinResult(DataChunk &left, DataChunk &result, bool found_match[]);
	static void ConstructMarkJoinResult(DataChunk &join_keys, DataChunk &left, DataChunk &result, bool found_match[],
	                                    bool has_null);
	static void ConstructLeftJoinResult(DataChunk &left, DataChunk &result, bool found_match[]);
};

} // namespace duckdb
