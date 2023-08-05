//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/statement/pragma_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/parser/sql_statement.hpp"
#include "duckdb/parser/parsed_data/pragma_info.hpp"
#include "duckdb/parser/parsed_expression.hpp"

namespace duckdb {

class PragmaStatement : public SQLStatement {
public:
	PragmaStatement();

	unique_ptr<PragmaInfo> info;

public:
	unique_ptr<SQLStatement> Copy() const override;
};

} // namespace duckdb
