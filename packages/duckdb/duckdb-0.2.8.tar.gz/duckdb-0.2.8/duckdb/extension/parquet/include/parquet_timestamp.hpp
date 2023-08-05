//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parquet_timestamp.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb.hpp"

namespace duckdb {

struct Int96 {
	uint32_t value[3];
};

int64_t ImpalaTimestampToNanoseconds(const Int96 &impala_timestamp);
timestamp_t ImpalaTimestampToTimestamp(const Int96 &raw_ts);
Int96 TimestampToImpalaTimestamp(timestamp_t &ts);
timestamp_t ParquetTimestampMicrosToTimestamp(const int64_t &raw_ts);
timestamp_t ParquetTimestampMsToTimestamp(const int64_t &raw_ts);
date_t ParquetIntToDate(const int32_t &raw_date);

} // namespace duckdb
