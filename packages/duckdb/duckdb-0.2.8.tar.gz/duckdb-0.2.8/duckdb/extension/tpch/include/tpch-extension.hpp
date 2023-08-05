//===----------------------------------------------------------------------===//
//                         DuckDB
//
// tpch-extension.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb.hpp"

namespace duckdb {

class TPCHExtension : public Extension {
public:
	void Load(DuckDB &db) override;

	//! Gets the specified TPC-H Query number as a string
	static std::string GetQuery(int query);
	//! Returns the CSV answer of a TPC-H query
	static std::string GetAnswer(double sf, int query);
};

} // namespace duckdb
