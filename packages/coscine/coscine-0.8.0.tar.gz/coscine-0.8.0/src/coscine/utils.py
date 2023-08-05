###############################################################################
# Coscine Python SDK
# Copyright (c) 2018-2022 RWTH Aachen University
# Licensed under the terms of the MIT License
###############################################################################
# Coscine, short for Collaborative Scientific Integration Environment is
# a platform for research data management (RDM).
# For more information on Coscine visit https://www.coscine.de/.
#
# Please note that this python module is open source software primarily
# developed and maintained by the scientific community. It is not
# an official service that RWTH Aachen provides support for.
###############################################################################

###############################################################################
# File description
###############################################################################

"""
This file contains utility classes and functions, sometimes taken from another
source like StackOverflow. Credit is given where it is due.
"""

###############################################################################
# Dependencies
###############################################################################

from typing import Union, List, Callable, Optional
import sys
from tqdm.auto import tqdm

###############################################################################
# Classes / Functions / Scripts
###############################################################################

def in_cli_mode() -> bool:
	"""
	Returns true if we are running in a command line interface.
	"""
	return sys.stdout is not None and sys.stderr.isatty()

###############################################################################

def is_subset(x: dict, y: dict) -> bool:
	"""
	Check whether dict x is a subset of dict y
	"""
	return x.items() <= y.items()

###############################################################################
# HumanBytes class
###############################################################################
# Source: https://stackoverflow.com/questions/12523586/
# 		  python-format-size-application-converting-b-to-kb-mb-gb-tb
# by Mitch McMabers (https://stackoverflow.com/users/8874388/mitch-mcmabers)
# Licensed under the Public Domain
###############################################################################

class HumanBytes:
	METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB",
									"PB", "EB", "ZB", "YB"]
	BINARY_LABELS: List[str] = ["B", "KiB", "MiB", "GiB",
						"TiB", "PiB", "EiB", "ZiB", "YiB"]
	# PREDEFINED FOR SPEED:
	PRECISION_OFFSETS: List[float] = [0.5, 0.05, 0.005, 0.0005]
	PRECISION_FORMATS: List[str] = ["{}{:.0f} {}", "{}{:.1f} {}",
									"{}{:.2f} {}", "{}{:.3f} {}"]

	@staticmethod
	def format(
		num: Union[int, float],
		metric: bool = False,
		precision: int = 1
	) -> str:
		"""
		Human-readable formatting of bytes, using binary (powers of 1024)
		or metric (powers of 1000) representation.
		"""

		if not isinstance(num, (int, float)):
			raise TypeError("num must be an int or float")
		if not isinstance(metric, bool):
			raise TypeError("metric must be a bool")
		if not (
			isinstance(precision, int) and precision >= 0 and precision <= 3
		):
			raise ValueError("precision must be an int (range 0-3)")

		unit_labels = (HumanBytes.METRIC_LABELS if metric
							else HumanBytes.BINARY_LABELS)
		last_label = unit_labels[-1]
		unit_step = 1000 if metric else 1024
		unit_step_thresh = unit_step - HumanBytes.PRECISION_OFFSETS[precision]

		is_negative = num < 0
		# Faster than ternary assignment
		# or always running abs():
		if is_negative:
			num = abs(num)

		for unit in unit_labels:
			# VERY IMPORTANT:
			# Only accepts the CURRENT unit if we're BELOW the threshold where
			# float rounding behavior would place us into the NEXT unit: F.ex.
			# when rounding a float to 1 decimal, any number ">= 1023.95" will
			# be rounded to "1024.0". Obviously we don't want ugly output such
			# as "1024.0 KiB", since the proper term for that is "1.0 MiB".
			if num < unit_step_thresh:
				break
			# We only shrink the number if we HAVEN'T reached the last unit.
			# NOTE: These looped divisions accumulate floating point rounding
			# errors, but each new division pushes the rounding errors further
			# and further down in the decimals, so it doesn't matter at all.
			if unit != last_label:
				num /= unit_step

		return HumanBytes.PRECISION_FORMATS[precision].format(
			"-" if is_negative else "", num, unit
		)

###############################################################################

class ProgressBar:
	"""
	The ProgressBar class is a simple wrapper around tqdm
	progress bars. It is used in download/upload methods and provides the
	benefit of remembering state information and printing only when in
	verbose mode.

	Attributes
	----------
	enabled : bool
		Enable/Disable Progress Bar (if disabled it doesn't show up)
	bar : tqdm.tqdm
		tqdm Progress Bar instance.
	filesize : int
		Filesize in bytes.
	count : int
		Number of bytes read.
	callback : Callable[[int], None] or None
		Callback function to call on update.
	"""

	enabled: bool
	progress_bar: tqdm
	filesize: int
	count: int
	callback: Optional[Callable[[int], None]]

###############################################################################

	def __init__(self, enabled: bool, filesize: int, key: str,
			callback: Optional[Callable[[int], None]] = None) -> None:
		"""
		Initializes a state-aware tqdm ProgressBar.

		Parameters
		-----------
		enabled : bool
			Enable / Disable progress bar
		filesize : int
			Size of the file object in bytes
		key : str
			key/filename of the file object
		callback : function(chunksize: int)
			Callback function to call after each update
		"""

		self.enabled = enabled
		self.callback = callback
		self.filesize = filesize
		self.count = 0
		if self.enabled:
			self.progress_bar = tqdm(total=filesize, unit="B", unit_scale=True,
										desc=key, ascii=True, maxinterval=1)

###############################################################################

	def update(self, chunksize: int) -> None:
		"""
		Updates the progress bar with respect to the consumed chunksize.
		If a callafter function has been provided to the Constructor, it is
		called during the update.
		"""

		self.count += chunksize
		if self.enabled:
			self.progress_bar.update(chunksize)
			if self.count >= self.filesize:
				self.progress_bar.refresh()
		if self.callback:
			self.callback(chunksize)

###############################################################################
