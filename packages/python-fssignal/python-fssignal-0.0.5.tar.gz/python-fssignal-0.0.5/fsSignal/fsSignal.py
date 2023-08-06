# Builtin modules
from __future__ import annotations
import traceback,  signal as _signal
from threading import Event
from time import monotonic, sleep
from typing import Callable, Dict, Any, Iterator, Iterable, Optional, Union
# Third party modules
# Local modules
# Program
Signals = _signal.Signals

class KillSignal(Exception): pass

class SignalIterator(Iterator[Any]):
	__slots__ = ("event", "it", "checkDelay", "lastCheck")
	event:Event
	it:Iterator[Any]
	checkDelay:float
	lastCheck:float
	def __init__(self, event:Event, it:Iterable[Any], checkDelay:float=1.0):
		self.event      = event
		self.it         = it.__iter__()
		self.checkDelay = checkDelay
		self.lastCheck  = monotonic()
	def __iter__(self) -> Iterator[Any]:
		return self
	def __next__(self) -> Any:
		m = monotonic()
		if m-self.lastCheck > self.checkDelay:
			self.lastCheck = m
			if self.event.is_set():
				raise KillSignal
		return self.it.__next__()

class BaseSignal:
	_force:bool
	@classmethod
	def get(self) -> bool:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._get(self._force)
		return False
	@classmethod
	def getSoft(self) -> bool:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._get(False)
		return False
	@classmethod
	def getHard(self) -> bool:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._get(True)
		return False
	@classmethod
	def check(self) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._check(self._force)
	@classmethod
	def checkSoft(self) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._check(False)
	@classmethod
	def checkHard(self) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._check(True)
	@classmethod
	def sleep(self, seconds:Union[int, float], raiseOnKill:bool=False) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._sleep(seconds, raiseOnKill, self._force)
		return sleep(seconds)
	@classmethod
	def signalSoftKill(self, *args:Any, **kwargs:Any) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._signalSoftKill(*args, **kwargs)
	@classmethod
	def signalHardKill(self, *args:Any, **kwargs:Any) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._signalHardKill(*args, **kwargs)
	@classmethod
	def iter(self, it:Iterable[Any], checkDelay:float=1.0) -> Iterable[Any]:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._iter(it, checkDelay, self._force)
		return it
	@classmethod
	def softKill(self) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._softKill()
	@classmethod
	def hardKill(self) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._hardKill()
	@classmethod
	def reset(self) -> None:
		if isinstance(Signal._handler, Signal):
			return Signal._handler._reset()
	@classmethod
	def getSoftSignal(self) -> Any:
		return SoftSignal
	@classmethod
	def getHardSignal(self) -> Any:
		return HardSignal
	@classmethod
	def isActivated(self) -> bool:
		return isinstance(Signal._handler, Signal)

class SoftSignal(BaseSignal):
	_force:bool = False

class HardSignal(BaseSignal):
	_force:bool = True

class Signal(HardSignal):
	_handler:Optional[Signal] = None
	softKillFn:Optional[Callable[..., Any]]
	hardKillFn:Optional[Callable[..., Any]]
	forceKillCounterFn:Optional[Callable[[int, int], Any]]
	counter:int
	forceCounter:int
	eSoft:Event
	eHard:Event
	def __init__(self, softKillFn:Optional[Callable[..., Any]]=None, hardKillFn:Optional[Callable[..., Any]]=None,
	forceKillCounterFn:Optional[Callable[[int, int], Any]]=None, forceCounter:int=10):
		self.softKillFn = softKillFn
		self.hardKillFn = hardKillFn
		self.forceKillCounterFn = forceKillCounterFn
		self.counter = 0
		self.forceCounter = forceCounter
		self.eSoft = Event()
		self.eHard = Event()
		Signal._handler = self
		self._activate()
	def __getstate__(self) -> Dict[str, Any]:
		return {
			"softKillFn":self.softKillFn,
			"hardKillFn":self.hardKillFn,
			"forceCounter":self.forceCounter,
			"forceKillCounterFn":self.forceKillCounterFn,
			"eSoft":self.eSoft,
			"eHard":self.eHard,
		}
	def __setstate__(self, states:Dict[str, Any]) -> None:
		self.softKillFn = states["softKillFn"]
		self.hardKillFn = states["hardKillFn"]
		self.forceCounter = states["forceCounter"]
		self.forceKillCounterFn = states["forceKillCounterFn"]
		self.eSoft = states["eSoft"]
		self.eHard = states["eHard"]
		self._activate()
	def _activate(self) -> None:
		_signal.signal(_signal.SIGINT, Signal.signalSoftKill)
		_signal.signal(_signal.SIGTERM, Signal.signalHardKill)
	def _get(self, force:bool=True) -> bool:
		if force:
			return self.eHard.is_set()
		return self.eSoft.is_set()
	def _check(self, force:bool=True) -> None:
		if (force and self.eHard.is_set()) or (not force and self.eSoft.is_set()):
			raise KillSignal
		return None
	def _sleep(self, seconds:Union[int, float], raiseOnKill:bool=False, force:bool=True) -> None:
		if (self.eHard if force else self.eSoft).wait(float(seconds)) and raiseOnKill:
			raise KillSignal
		return None
	def _iter(self, it:Iterable[Any], checkDelay:float=1.0, force:bool=True) -> Iterator[Any]:
		return SignalIterator(self.eHard if force else self.eSoft, it, checkDelay)
	def _signalSoftKill(self, *args:Any, **kwargs:Any) -> None:
		self._softKill()
		if not self.eHard.is_set():
			self.counter += 1
			if callable(self.forceKillCounterFn):
				try:
					self.forceKillCounterFn(self.counter, self.forceCounter)
				except:
					traceback.print_exc()
			if self.counter >= self.forceCounter:
				self._hardKill()
	def _signalHardKill(self, *args:Any, **kwargs:Any) -> None:
		self._softKill()
		self._hardKill()
	def _softKill(self) -> None:
		if not self.eSoft.is_set():
			self.eSoft.set()
			if callable(self.softKillFn):
				try:
					self.softKillFn()
				except:
					traceback.print_exc()
	def _hardKill(self) -> None:
		if not self.eHard.is_set():
			self.eHard.set()
			if callable(self.hardKillFn):
				try:
					self.hardKillFn()
				except:
					traceback.print_exc()
	def _reset(self) -> None:
		self.eSoft.clear()
		self.eHard.clear()
		self.counter = 0
