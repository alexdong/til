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
