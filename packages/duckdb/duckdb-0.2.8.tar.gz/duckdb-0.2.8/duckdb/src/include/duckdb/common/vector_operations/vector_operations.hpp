//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/vector_operations/vector_operations.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/types/data_chunk.hpp"
#include "duckdb/common/types/vector.hpp"

#include <functional>

namespace duckdb {

// VectorOperations contains a set of operations that operate on sets of
// vectors. In general, the operators must all have the same type, otherwise an
// exception is thrown. Note that the functions underneath use restrict
// pointers, hence the data that the vectors point to (and hence the vector
// themselves) should not be equal! For example, if you call the function Add(A,
// B, A) then ASSERT_RESTRICT will be triggered. Instead call AddInPlace(A, B)
// or Add(A, B, C)
struct VectorOperations {
	//===--------------------------------------------------------------------===//
	// In-Place Operators
	//===--------------------------------------------------------------------===//
	//! A += B
	static void AddInPlace(Vector &A, int64_t B, idx_t count);

	//===--------------------------------------------------------------------===//
	// NULL Operators
	//===--------------------------------------------------------------------===//
	//! result = IS NOT NULL(A)
	static void IsNotNull(Vector &A, Vector &result, idx_t count);
	//! result = IS NULL (A)
	static void IsNull(Vector &A, Vector &result, idx_t count);
	// Returns whether or not a vector has a NULL value
	static bool HasNull(Vector &A, idx_t count);
	static bool HasNotNull(Vector &A, idx_t count);

	//===--------------------------------------------------------------------===//
	// Boolean Operations
	//===--------------------------------------------------------------------===//
	// result = A && B
	static void And(Vector &A, Vector &B, Vector &result, idx_t count);
	// result = A || B
	static void Or(Vector &A, Vector &B, Vector &result, idx_t count);
	// result = NOT(A)
	static void Not(Vector &A, Vector &result, idx_t count);

	//===--------------------------------------------------------------------===//
	// Comparison Operations
	//===--------------------------------------------------------------------===//
	// result = A == B
	static void Equals(Vector &A, Vector &B, Vector &result, idx_t count);
	// result = A != B
	static void NotEquals(Vector &A, Vector &B, Vector &result, idx_t count);
	// result = A > B
	static void GreaterThan(Vector &A, Vector &B, Vector &result, idx_t count);
	// result = A >= B
	static void GreaterThanEquals(Vector &A, Vector &B, Vector &result, idx_t count);
	// result = A < B
	static void LessThan(Vector &A, Vector &B, Vector &result, idx_t count);
	// result = A <= B
	static void LessThanEquals(Vector &A, Vector &B, Vector &result, idx_t count);

	// result = A != B with nulls being equal
	static void DistinctFrom(Vector &left, Vector &right, Vector &result, idx_t count);
	// result := A == B with nulls being equal
	static void NotDistinctFrom(Vector &left, Vector &right, Vector &result, idx_t count);
	// result := A > B with nulls being maximal
	static void DistinctGreaterThan(Vector &left, Vector &right, Vector &result, idx_t count);
	// result := A >= B with nulls being maximal
	static void DistinctGreaterThanEquals(Vector &left, Vector &right, Vector &result, idx_t count);
	// result := A < B with nulls being maximal
	static void DistinctLessThan(Vector &left, Vector &right, Vector &result, idx_t count);
	// result := A <= B with nulls being maximal
	static void DistinctLessThanEquals(Vector &left, Vector &right, Vector &result, idx_t count);

	//===--------------------------------------------------------------------===//
	// Select Comparisons
	//===--------------------------------------------------------------------===//
	static idx_t Equals(Vector &left, Vector &right, const SelectionVector *sel, idx_t count, SelectionVector *true_sel,
	                    SelectionVector *false_sel);
	static idx_t NotEquals(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                       SelectionVector *true_sel, SelectionVector *false_sel);
	static idx_t GreaterThan(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                         SelectionVector *true_sel, SelectionVector *false_sel);
	static idx_t GreaterThanEquals(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                               SelectionVector *true_sel, SelectionVector *false_sel);
	static idx_t LessThan(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                      SelectionVector *true_sel, SelectionVector *false_sel);
	static idx_t LessThanEquals(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                            SelectionVector *true_sel, SelectionVector *false_sel);

	// true := A != B with nulls being equal
	static idx_t DistinctFrom(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                          SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A == B with nulls being equal
	static idx_t NotDistinctFrom(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                             SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A > B with nulls being maximal
	static idx_t DistinctGreaterThan(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                                 SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A >= B with nulls being maximal
	static idx_t DistinctGreaterThanEquals(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                                       SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A < B with nulls being maximal
	static idx_t DistinctLessThan(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                              SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A <= B with nulls being maximal
	static idx_t DistinctLessThanEquals(Vector &left, Vector &right, const SelectionVector *sel, idx_t count,
	                                    SelectionVector *true_sel, SelectionVector *false_sel);

	//===--------------------------------------------------------------------===//
	// Nested Comparisons
	//===--------------------------------------------------------------------===//
	// true := A != B with nulls being equal, inputs selected
	static idx_t NestedNotEquals(Vector &left, Vector &right, idx_t vcount, const SelectionVector &sel, idx_t count,
	                             SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A == B with nulls being equal, inputs selected
	static idx_t NestedEquals(Vector &left, Vector &right, idx_t vcount, const SelectionVector &sel, idx_t count,
	                          SelectionVector *true_sel, SelectionVector *false_sel);

	// true := A > B with nulls being maximal, inputs selected
	static idx_t NestedGreaterThan(Vector &left, Vector &right, idx_t vcount, const SelectionVector &sel, idx_t count,
	                               SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A >= B with nulls being maximal, inputs selected
	static idx_t NestedGreaterThanEquals(Vector &left, Vector &right, idx_t vcount, const SelectionVector &sel,
	                                     idx_t count, SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A < B with nulls being maximal, inputs selected
	static idx_t NestedLessThan(Vector &left, Vector &right, idx_t vcount, const SelectionVector &sel, idx_t count,
	                            SelectionVector *true_sel, SelectionVector *false_sel);
	// true := A <= B with nulls being maximal, inputs selected
	static idx_t NestedLessThanEquals(Vector &left, Vector &right, idx_t vcount, const SelectionVector &sel,
	                                  idx_t count, SelectionVector *true_sel, SelectionVector *false_sel);

	//===--------------------------------------------------------------------===//
	// Hash functions
	//===--------------------------------------------------------------------===//
	// result = HASH(A)
	static void Hash(Vector &input, Vector &hashes, idx_t count);
	static void Hash(Vector &input, Vector &hashes, const SelectionVector &rsel, idx_t count);
	// A ^= HASH(B)
	static void CombineHash(Vector &hashes, Vector &B, idx_t count);
	static void CombineHash(Vector &hashes, Vector &B, const SelectionVector &rsel, idx_t count);

	//===--------------------------------------------------------------------===//
	// Generate functions
	//===--------------------------------------------------------------------===//
	static void GenerateSequence(Vector &result, idx_t count, int64_t start = 0, int64_t increment = 1);
	static void GenerateSequence(Vector &result, idx_t count, const SelectionVector &sel, int64_t start = 0,
	                             int64_t increment = 1);
	//===--------------------------------------------------------------------===//
	// Helpers
	//===--------------------------------------------------------------------===//
	//! Cast the data from the source type to the target type. Any elements that could not be converted are turned into
	//! NULLs. If any elements cannot be converted, returns false and fills in the error_message. If no error message is
	//! provided, an exception is thrown instead.
	static bool TryCast(Vector &source, Vector &result, idx_t count, string *error_message, bool strict = false);
	//! Cast the data from the source type to the target type. Throws an exception if the cast fails.
	static void Cast(Vector &source, Vector &result, idx_t count, bool strict = false);

	// Copy the data of <source> to the target vector
	static void Copy(const Vector &source, Vector &target, idx_t source_count, idx_t source_offset,
	                 idx_t target_offset);
	static void Copy(const Vector &source, Vector &target, const SelectionVector &sel, idx_t source_count,
	                 idx_t source_offset, idx_t target_offset);

	// Copy the data of <source> to the target location, setting null values to
	// NullValue<T>. Used to store data without separate NULL mask.
	static void WriteToStorage(Vector &source, idx_t count, data_ptr_t target);
	// Reads the data of <source> to the target vector, setting the nullmask
	// for any NullValue<T> of source. Used to go back from storage to a proper vector
	static void ReadFromStorage(data_ptr_t source, idx_t count, Vector &result);
};
} // namespace duckdb
