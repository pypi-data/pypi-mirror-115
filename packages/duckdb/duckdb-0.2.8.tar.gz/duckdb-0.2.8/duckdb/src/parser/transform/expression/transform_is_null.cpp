#include "duckdb/common/exception.hpp"
#include "duckdb/parser/expression/operator_expression.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {

unique_ptr<ParsedExpression> Transformer::TransformNullTest(duckdb_libpgquery::PGNullTest *root, idx_t depth) {
	D_ASSERT(root);
	auto arg = TransformExpression(reinterpret_cast<duckdb_libpgquery::PGNode *>(root->arg), depth + 1);
	if (root->argisrow) {
		throw NotImplementedException("IS NULL argisrow");
	}
	ExpressionType expr_type = (root->nulltesttype == duckdb_libpgquery::PG_IS_NULL)
	                               ? ExpressionType::OPERATOR_IS_NULL
	                               : ExpressionType::OPERATOR_IS_NOT_NULL;

	return unique_ptr<ParsedExpression>(new OperatorExpression(expr_type, move(arg)));
}

} // namespace duckdb
