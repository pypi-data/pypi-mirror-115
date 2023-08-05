#include "duckdb/parser/statement/delete_statement.hpp"
#include "duckdb/parser/transformer.hpp"
#include "duckdb/parser/tableref/crossproductref.hpp"

namespace duckdb {

unique_ptr<DeleteStatement> Transformer::TransformDelete(duckdb_libpgquery::PGNode *node) {
	auto stmt = reinterpret_cast<duckdb_libpgquery::PGDeleteStmt *>(node);
	D_ASSERT(stmt);
	auto result = make_unique<DeleteStatement>();

	result->condition = TransformExpression(stmt->whereClause, 0);
	result->table = TransformRangeVar(stmt->relation);
	if (result->table->type != TableReferenceType::BASE_TABLE) {
		throw Exception("Can only delete from base tables!");
	}
	if (stmt->usingClause) {
		for (auto n = stmt->usingClause->head; n != nullptr; n = n->next) {
			auto target = reinterpret_cast<duckdb_libpgquery::PGNode *>(n->data.ptr_value);
			auto using_entry = TransformTableRefNode(target);
			result->using_clauses.push_back(move(using_entry));
		}
	}
	return result;
}

} // namespace duckdb
