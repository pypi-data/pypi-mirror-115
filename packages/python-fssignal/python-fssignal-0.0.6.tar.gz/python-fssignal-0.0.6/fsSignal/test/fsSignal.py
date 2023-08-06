# Builtin modules
import os, unittest, signal as _signal
from threading import Timer
from time import monotonic, sleep
from typing import List
# Third party modules
# Local modules
from .. import Signal, KillSignal
# Program
class SignalTest(unittest.TestCase):
	rootSignal:Signal
	@classmethod
	def setUpClass(self) -> None:
		self.rootSignal = Signal()
		return None
	def tearDown(self) -> None:
		self.rootSignal.reset()
		return None
	def killmeTimer(self) -> None:
		def suicide() -> None:
			os.kill(os.getpid(), _signal.SIGINT)
			return None
		Timer(1, suicide).start()
		return None
	def test_sleep(self) -> None:
		t = monotonic()
		self.rootSignal.sleep(2)
		self.assertGreater(monotonic()-t, 2.0)
		return None
	def test_sleepRaise(self) -> None:
		self.killmeTimer()
		with self.assertRaises(KillSignal):
			self.rootSignal.getSoftSignal().sleep(2, raiseOnKill=True)
		return None
	def test_iter(self) -> None:
		s = list(range(5))
		d:List[int] = []
		signal = self.rootSignal.getSoftSignal()
		self.killmeTimer()
		with self.assertRaises(KillSignal):
			for i in s:
				signal.sleep(0.5, raiseOnKill=True)
				d.append(i)
		return None
	def test_hardkill(self) -> None:
		self.killmeTimer()
		sleep(0.1)
		self.killmeTimer()
		sleep(0.1)
		self.killmeTimer()
		sleep(0.1)
		self.rootSignal.forceCounter = 3
		with self.assertRaises(KillSignal):
			self.rootSignal.sleep(10, raiseOnKill=True)
		self.rootSignal.forceCounter = 10
		return None
	def test_check(self) -> None:
		signal = self.rootSignal.getSoftSignal()
		signal.check()
		self.assertEqual(signal.get(), False)
		self.killmeTimer()
		signal.sleep(2, raiseOnKill=False)
		with self.assertRaises(KillSignal):
			signal.check()
		self.assertEqual(signal.get(), True)
