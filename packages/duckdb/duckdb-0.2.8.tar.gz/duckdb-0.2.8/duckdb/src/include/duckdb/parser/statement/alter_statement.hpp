//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/parser/statement/alter_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/parser/column_definition.hpp"
#include "duckdb/parser/parsed_data/alter_table_info.hpp"
#include "duckdb/parser/sql_statement.hpp"

namespace duckdb {

class AlterStatement : public SQLStatement {
public:
	AlterStatement();
	explicit AlterStatement(unique_ptr<AlterInfo> info);

	unique_ptr<AlterInfo> info;

public:
	unique_ptr<SQLStatement> Copy() const override;
};

} // namespace duckdb
