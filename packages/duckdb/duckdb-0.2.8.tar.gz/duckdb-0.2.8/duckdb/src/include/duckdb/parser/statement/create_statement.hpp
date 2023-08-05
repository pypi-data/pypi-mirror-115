//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/statement/create_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/parser/parsed_data/create_info.hpp"
#include "duckdb/parser/sql_statement.hpp"

namespace duckdb {

class CreateStatement : public SQLStatement {
public:
	CreateStatement();

	unique_ptr<CreateInfo> info;

public:
	unique_ptr<SQLStatement> Copy() const override;
};

} // namespace duckdb
