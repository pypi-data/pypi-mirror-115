namespace java thrift.test
namespace cpp thrift.test

// more tests on double constants (precision and type checks)
const double DOUBLE_ASSIGNED_TO_INT_CONSTANT_TEST = 1
const double DOUBLE_ASSIGNED_TO_NEGATIVE_INT_CONSTANT_TEST = -100
const double DOUBLE_ASSIGNED_TO_LARGEST_INT_CONSTANT_TEST = 9223372036854775807
const double DOUBLE_ASSIGNED_TO_SMALLEST_INT_CONSTANT_TEST = -9223372036854775807
const double DOUBLE_ASSIGNED_TO_DOUBLE_WITH_MANY_DECIMALS_TEST = 3.14159265359
const double DOUBLE_ASSIGNED_TO_FRACTIONAL_DOUBLE_TEST = 1000000.1
const double DOUBLE_ASSIGNED_TO_NEGATIVE_FRACTIONAL_DOUBLE_TEST = -1000000.1
const double DOUBLE_ASSIGNED_TO_LARGE_DOUBLE_TEST = 1.7e+308
const double DOUBLE_ASSIGNED_TO_LARGE_FRACTIONAL_DOUBLE_TEST = 9223372036854775816.43
const double DOUBLE_ASSIGNED_TO_SMALL_DOUBLE_TEST = -1.7e+308
const double DOUBLE_ASSIGNED_TO_NEGATIVE_BUT_LARGE_FRACTIONAL_DOUBLE_TEST = -9223372036854775816.43

const list<double> DOUBLE_LIST_TEST = [1,-100,100,9223372036854775807,-9223372036854775807,3.14159265359,1000000.1,-1000000.1,1.7e+308,-1.7e+308,9223372036854775816.43,-9223372036854775816.43]
