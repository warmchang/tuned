import re
import tuned.logs
from . import base

log = tuned.logs.get()

class lscpu_check(base.Function):
	"""
	Checks regexes against the output of lscpu. Accepts arguments in the
	following form: REGEX1, STR1, REGEX2, STR2, ...[, STR_FALLBACK]
	If REGEX1 matches something in the output it expands to STR1,
	if REGEX2 matches it expands to STR2. It stops on the first match,
	i.e. if REGEX1 matches, no more regexes are processed. If none
	regex matches it expands to STR_FALLBACK. If there is no fallback,
	it expands to empty string.
	"""
	def __init__(self):
		# unlimited number of arguments, min 2 arguments
		super(lscpu_check, self).__init__("lscpu_check", 0, 2)

	def execute(self, args):
		if not super(lscpu_check, self).execute(args):
			return None
		# Stdout is the 2nd result from the execute call
		_, lscpu = self._cmd.execute("lscpu")
		for i in range(0, len(args), 2):
			if i + 1 < len(args):
				if re.search(args[i], lscpu, re.MULTILINE):
					return args[i + 1]
		if len(args) % 2:
			return args[-1]
		else:
			return ""
