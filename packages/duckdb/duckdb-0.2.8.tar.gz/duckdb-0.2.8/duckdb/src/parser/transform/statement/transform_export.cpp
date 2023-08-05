#include "duckdb/parser/statement/export_statement.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {

unique_ptr<ExportStatement> Transformer::TransformExport(duckdb_libpgquery::PGNode *node) {
	auto stmt = reinterpret_cast<duckdb_libpgquery::PGExportStmt *>(node);
	auto info = make_unique<CopyInfo>();
	info->file_path = stmt->filename;
	info->format = "csv";
	info->is_from = false;
	// handle export options
	TransformCopyOptions(*info, stmt->options);

	return make_unique<ExportStatement>(move(info));
}

} // namespace duckdb
