//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/planner/operator/logical_pragma.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/planner/logical_operator.hpp"
#include "duckdb/parser/parsed_data/pragma_info.hpp"
#include "duckdb/function/pragma_function.hpp"

namespace duckdb {

//! LogicalSimple represents a simple logical operator that only passes on the parse info
class LogicalPragma : public LogicalOperator {
public:
	LogicalPragma(PragmaFunction function_p, PragmaInfo info_p)
	    : LogicalOperator(LogicalOperatorType::LOGICAL_PRAGMA), function(move(function_p)), info(move(info_p)) {
	}

	//! The pragma function to call
	PragmaFunction function;
	//! The context of the call
	PragmaInfo info;

protected:
	void ResolveTypes() override {
		types.push_back(LogicalType::BOOLEAN);
	}
};
} // namespace duckdb
