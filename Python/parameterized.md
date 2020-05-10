

## Parameterized unit tests


    from parameterized import parameterized

    class TestMathUnitTest(unittest.TestCase):
       @parameterized.expand([
	   ("negative", -1.5, -2.0),
	   ("integer", 1, 1.0),
	   ("large fraction", 1.6, 1),
       ])
       def test_floor(self, name, input, expected):
	   assert_equal(math.floor(input), expected)


## Parameterized test case name with `name_func`

If the first parameter is a string, the string will be added to the end of the generated method name.
Or, use `name_func` to customise:

    import unittest
    from parameterized import parameterized

    def custom_name_func(testcase_func, param_num, param):
	return "%s_%s" %(
	    testcase_func.__name__,
	    parameterized.to_safe_name("_".join(str(x) for x in param.args)),
	)

    class AddTestCase(unittest.TestCase):
	@parameterized.expand([
	    (2, 3, 5),
	    (2, 3, 5),
	], name_func=custom_name_func)
	def test_add(self, a, b, expected):
	    assert_equal(a + b, expected)


    $ nosetests example.py
    test_add_1_2_3 (example.AddTestCase) ... ok
    test_add_2_3_5 (example.AddTestCase) ... ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK


## Using with @mock.patch

parameterized can be used with mock.patch, but the argument ordering can be confusing. The @mock.patch(...) decorator must come below the @parameterized(...), and the mocked parameters must come last:

    @mock.patch("os.getpid")
    class TestOS(object):
       @parameterized(...)
       @mock.patch("os.fdopen")
       @mock.patch("os.umask")
       def test_method(self, param1, param2, ..., mock_umask, mock_fdopen, mock_getpid):
	  ...


## Caveat

Pycharm's Ctrl+Shift+R will no longer work because the decorator will generate a list of tests with suffix like `_01` etc.

