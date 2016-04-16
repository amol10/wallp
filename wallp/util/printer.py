
from redlib.api.prnt import ColumnPrinter, Column, ColumnPrinterError, SepColumn, ProgressColumn
from ..db.app.config import Config


class PrinterError(Exception):
	pass


class Printer:
	progress_col_width = 10

	def __init__(self, verbosity=3):
		try:
			self._cp = ColumnPrinter(cols=[Column(width=30), SepColumn(), Column(min=30, fill=True)])
		except ColumnPrinterError as e:
			raise PrinterError(str(e))

		self._verbosity = Config().eget('output.verbosity', default=1)


	def printf(self, msg, data, progress=False, col_updt=False, verbosity=1):
		if verbosity > self._verbosity:
			return

		if not progress and not col_updt:
			self._cp.printf(msg, data)
		elif progress:
			progress_cp = ColumnPrinter(cols=[Column(width=12), ProgressColumn(pwidth=12), Column(width=30)], row_width=55)
			self._cp.printf(msg, progress_cp)
			cb = progress_cp.printf('?', '?', '', col_updt=True)

			pcb = cb.progress_cb
			pcp = cb.progress_cp
			cb.progress_cb = lambda p : pcb(1, p)

			def pcp2():
				pcp(1)
				progress_cp.done()
			cb.progress_cp = pcp2

			return cb
		else:
			return self._cp.printf(msg, data, col_updt=True)


printer = Printer()

