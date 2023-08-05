#include "duckdb/function/table/read_csv.hpp"
#include "duckdb/execution/operator/persistent/buffered_csv_reader.hpp"
#include "duckdb/function/function_set.hpp"
#include "duckdb/main/client_context.hpp"
#include "duckdb/main/database.hpp"
#include "duckdb/common/string_util.hpp"
#include "duckdb/main/config.hpp"
#include "duckdb/parser/expression/constant_expression.hpp"
#include "duckdb/parser/expression/function_expression.hpp"
#include "duckdb/parser/tableref/table_function_ref.hpp"

#include <limits>

namespace duckdb {

static unique_ptr<FunctionData> ReadCSVBind(ClientContext &context, vector<Value> &inputs,
                                            unordered_map<string, Value> &named_parameters,
                                            vector<LogicalType> &input_table_types, vector<string> &input_table_names,
                                            vector<LogicalType> &return_types, vector<string> &names) {
	auto result = make_unique<ReadCSVData>();
	auto &options = result->options;

	string file_pattern = inputs[0].str_value;

	auto &fs = FileSystem::GetFileSystem(context);
	result->files = fs.Glob(file_pattern);
	if (result->files.empty()) {
		throw IOException("No files found that match the pattern \"%s\"", file_pattern);
	}

	for (auto &kv : named_parameters) {
		if (kv.first == "auto_detect") {
			options.auto_detect = kv.second.value_.boolean;
		} else if (kv.first == "sep" || kv.first == "delim") {
			options.delimiter = kv.second.str_value;
			options.has_delimiter = true;
		} else if (kv.first == "header") {
			options.header = kv.second.value_.boolean;
			options.has_header = true;
		} else if (kv.first == "quote") {
			options.quote = kv.second.str_value;
			options.has_quote = true;
		} else if (kv.first == "escape") {
			options.escape = kv.second.str_value;
			options.has_escape = true;
		} else if (kv.first == "nullstr") {
			options.null_str = kv.second.str_value;
		} else if (kv.first == "sample_size") {
			int64_t sample_size = kv.second.GetValue<int64_t>();
			if (sample_size < 1 && sample_size != -1) {
				throw BinderException("Unsupported parameter for SAMPLE_SIZE: cannot be smaller than 1");
			}
			if (sample_size == -1) {
				options.sample_chunks = std::numeric_limits<uint64_t>::max();
				options.sample_chunk_size = STANDARD_VECTOR_SIZE;
			} else if (sample_size <= STANDARD_VECTOR_SIZE) {
				options.sample_chunk_size = sample_size;
				options.sample_chunks = 1;
			} else {
				options.sample_chunk_size = STANDARD_VECTOR_SIZE;
				options.sample_chunks = sample_size / STANDARD_VECTOR_SIZE;
			}
		} else if (kv.first == "sample_chunk_size") {
			options.sample_chunk_size = kv.second.GetValue<int64_t>();
			if (options.sample_chunk_size > STANDARD_VECTOR_SIZE) {
				throw BinderException(
				    "Unsupported parameter for SAMPLE_CHUNK_SIZE: cannot be bigger than STANDARD_VECTOR_SIZE %d",
				    STANDARD_VECTOR_SIZE);
			} else if (options.sample_chunk_size < 1) {
				throw BinderException("Unsupported parameter for SAMPLE_CHUNK_SIZE: cannot be smaller than 1");
			}
		} else if (kv.first == "sample_chunks") {
			options.sample_chunks = kv.second.GetValue<int64_t>();
			if (options.sample_chunks < 1) {
				throw BinderException("Unsupported parameter for SAMPLE_CHUNKS: cannot be smaller than 1");
			}
		} else if (kv.first == "all_varchar") {
			options.all_varchar = kv.second.value_.boolean;
		} else if (kv.first == "dateformat") {
			options.has_format[LogicalTypeId::DATE] = true;
			auto &date_format = options.date_format[LogicalTypeId::DATE];
			date_format.format_specifier = kv.second.str_value;
			string error = StrTimeFormat::ParseFormatSpecifier(date_format.format_specifier, date_format);
			if (!error.empty()) {
				throw InvalidInputException("Could not parse DATEFORMAT: %s", error.c_str());
			}
		} else if (kv.first == "timestampformat") {
			options.has_format[LogicalTypeId::TIMESTAMP] = true;
			auto &timestamp_format = options.date_format[LogicalTypeId::TIMESTAMP];
			timestamp_format.format_specifier = kv.second.str_value;
			string error = StrTimeFormat::ParseFormatSpecifier(timestamp_format.format_specifier, timestamp_format);
			if (!error.empty()) {
				throw InvalidInputException("Could not parse TIMESTAMPFORMAT: %s", error.c_str());
			}
		} else if (kv.first == "normalize_names") {
			options.normalize_names = kv.second.value_.boolean;
		} else if (kv.first == "columns") {
			auto &child_type = kv.second.type();
			if (child_type.id() != LogicalTypeId::STRUCT) {
				throw BinderException("read_csv columns requires a a struct as input");
			}
			D_ASSERT(StructType::GetChildCount(child_type) == kv.second.struct_value.size());
			for (idx_t i = 0; i < kv.second.struct_value.size(); i++) {
				auto &name = StructType::GetChildName(child_type, i);
				auto &val = kv.second.struct_value[i];
				names.push_back(name);
				if (val.type().id() != LogicalTypeId::VARCHAR) {
					throw BinderException("read_csv requires a type specification as string");
				}
				return_types.emplace_back(TransformStringToLogicalType(val.str_value.c_str()));
			}
			if (names.empty()) {
				throw BinderException("read_csv requires at least a single column as input!");
			}
		} else if (kv.first == "compression") {
			options.compression = kv.second.str_value;
		} else if (kv.first == "filename") {
			result->include_file_name = kv.second.value_.boolean;
		} else if (kv.first == "skip") {
			options.skip_rows = kv.second.GetValue<int64_t>();
		}
	}
	if (!options.auto_detect && return_types.empty()) {
		throw BinderException("read_csv requires columns to be specified. Use read_csv_auto or set read_csv(..., "
		                      "AUTO_DETECT=TRUE) to automatically guess columns.");
	}
	if (!(options.compression == "infer" || options.compression == "gzip" || options.compression == "none" ||
	      options.compression.empty())) {
		throw BinderException("read_csv currently only supports 'gzip' compression.");
	}
	if (options.auto_detect) {
		options.file_path = result->files[0];
		auto initial_reader = make_unique<BufferedCSVReader>(context, options);

		return_types.assign(initial_reader->sql_types.begin(), initial_reader->sql_types.end());
		names.assign(initial_reader->col_names.begin(), initial_reader->col_names.end());
		result->initial_reader = move(initial_reader);
	} else {
		result->sql_types = return_types;
		D_ASSERT(return_types.size() == names.size());
	}
	if (result->include_file_name) {
		return_types.push_back(LogicalType::VARCHAR);
		names.emplace_back("filename");
	}
	return move(result);
}

struct ReadCSVOperatorData : public FunctionOperatorData {
	//! The CSV reader
	unique_ptr<BufferedCSVReader> csv_reader;
	//! The index of the next file to read (i.e. current file + 1)
	idx_t file_index;
};

static unique_ptr<FunctionOperatorData> ReadCSVInit(ClientContext &context, const FunctionData *bind_data_p,
                                                    const vector<column_t> &column_ids,
                                                    TableFilterCollection *filters) {
	auto &bind_data = (ReadCSVData &)*bind_data_p;
	auto result = make_unique<ReadCSVOperatorData>();
	if (bind_data.initial_reader) {
		result->csv_reader = move(bind_data.initial_reader);
	} else {
		bind_data.options.file_path = bind_data.files[0];
		result->csv_reader = make_unique<BufferedCSVReader>(context, bind_data.options, bind_data.sql_types);
	}
	bind_data.bytes_read = 0;
	bind_data.file_size = result->csv_reader->file_size;
	result->file_index = 1;
	return move(result);
}

static unique_ptr<FunctionData> ReadCSVAutoBind(ClientContext &context, vector<Value> &inputs,
                                                unordered_map<string, Value> &named_parameters,
                                                vector<LogicalType> &input_table_types,
                                                vector<string> &input_table_names, vector<LogicalType> &return_types,
                                                vector<string> &names) {
	named_parameters["auto_detect"] = Value::BOOLEAN(true);
	return ReadCSVBind(context, inputs, named_parameters, input_table_types, input_table_names, return_types, names);
}

static void ReadCSVFunction(ClientContext &context, const FunctionData *bind_data_p,
                            FunctionOperatorData *operator_state, DataChunk *input, DataChunk &output) {
	auto &bind_data = (ReadCSVData &)*bind_data_p;
	auto &data = (ReadCSVOperatorData &)*operator_state;
	do {
		data.csv_reader->ParseCSV(output);
		bind_data.bytes_read = data.csv_reader->bytes_in_chunk;
		if (output.size() == 0 && data.file_index < bind_data.files.size()) {
			// exhausted this file, but we have more files we can read
			// open the next file and increment the counter
			bind_data.options.file_path = bind_data.files[data.file_index];
			data.csv_reader = make_unique<BufferedCSVReader>(context, bind_data.options, data.csv_reader->sql_types);
			data.file_index++;
		} else {
			break;
		}
	} while (true);
	if (bind_data.include_file_name) {
		auto &col = output.data.back();
		col.SetValue(0, Value(data.csv_reader->options.file_path));
		col.SetVectorType(VectorType::CONSTANT_VECTOR);
	}
}

static void ReadCSVAddNamedParameters(TableFunction &table_function) {
	table_function.named_parameters["sep"] = LogicalType::VARCHAR;
	table_function.named_parameters["delim"] = LogicalType::VARCHAR;
	table_function.named_parameters["quote"] = LogicalType::VARCHAR;
	table_function.named_parameters["escape"] = LogicalType::VARCHAR;
	table_function.named_parameters["nullstr"] = LogicalType::VARCHAR;
	table_function.named_parameters["columns"] = LogicalType::ANY;
	table_function.named_parameters["header"] = LogicalType::BOOLEAN;
	table_function.named_parameters["auto_detect"] = LogicalType::BOOLEAN;
	table_function.named_parameters["sample_size"] = LogicalType::BIGINT;
	table_function.named_parameters["sample_chunk_size"] = LogicalType::BIGINT;
	table_function.named_parameters["sample_chunks"] = LogicalType::BIGINT;
	table_function.named_parameters["all_varchar"] = LogicalType::BOOLEAN;
	table_function.named_parameters["dateformat"] = LogicalType::VARCHAR;
	table_function.named_parameters["timestampformat"] = LogicalType::VARCHAR;
	table_function.named_parameters["normalize_names"] = LogicalType::BOOLEAN;
	table_function.named_parameters["compression"] = LogicalType::VARCHAR;
	table_function.named_parameters["filename"] = LogicalType::BOOLEAN;
	table_function.named_parameters["skip"] = LogicalType::BIGINT;
}

int CSVReaderProgress(ClientContext &context, const FunctionData *bind_data_p) {
	auto &bind_data = (ReadCSVData &)*bind_data_p;
	if (bind_data.file_size == 0) {
		return 100;
	}
	auto percentage = bind_data.bytes_read * 100 / bind_data.file_size;
	return percentage;
}

TableFunction ReadCSVTableFunction::GetFunction() {
	TableFunction read_csv("read_csv", {LogicalType::VARCHAR}, ReadCSVFunction, ReadCSVBind, ReadCSVInit);
	read_csv.table_scan_progress = CSVReaderProgress;
	ReadCSVAddNamedParameters(read_csv);
	return read_csv;
}

void ReadCSVTableFunction::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(ReadCSVTableFunction::GetFunction());

	TableFunction read_csv_auto("read_csv_auto", {LogicalType::VARCHAR}, ReadCSVFunction, ReadCSVAutoBind, ReadCSVInit);
	read_csv_auto.table_scan_progress = CSVReaderProgress;
	ReadCSVAddNamedParameters(read_csv_auto);
	set.AddFunction(read_csv_auto);
}

unique_ptr<TableFunctionRef> ReadCSVReplacement(const string &table_name, void *data) {
	if (!StringUtil::EndsWith(table_name, ".csv") && !StringUtil::EndsWith(table_name, ".tsv") &&
	    !StringUtil::EndsWith(table_name, ".csv.gz")) {
		return nullptr;
	}
	auto table_function = make_unique<TableFunctionRef>();
	vector<unique_ptr<ParsedExpression>> children;
	children.push_back(make_unique<ConstantExpression>(Value(table_name)));
	table_function->function = make_unique<FunctionExpression>("read_csv_auto", move(children));
	return table_function;
}

void BuiltinFunctions::RegisterReadFunctions() {
	CSVCopyFunction::RegisterFunction(*this);
	ReadCSVTableFunction::RegisterFunction(*this);

	auto &config = DBConfig::GetConfig(context);
	config.replacement_scans.emplace_back(ReadCSVReplacement);
}

} // namespace duckdb
