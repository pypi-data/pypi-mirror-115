//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/execution/operator/helper/physical_vacuum.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/execution/physical_operator.hpp"
#include "duckdb/parser/parsed_data/load_info.hpp"

namespace duckdb {

//! PhysicalVacuum represents an etension LOAD operation
class PhysicalLoad : public PhysicalOperator {
public:
	explicit PhysicalLoad(unique_ptr<LoadInfo> info, idx_t estimated_cardinality)
	    : PhysicalOperator(PhysicalOperatorType::LOAD, {LogicalType::BOOLEAN}, estimated_cardinality),
	      info(move(info)) {
	}

	unique_ptr<LoadInfo> info;

public:
	void GetChunkInternal(ExecutionContext &context, DataChunk &chunk, PhysicalOperatorState *state) const override;
};

} // namespace duckdb
