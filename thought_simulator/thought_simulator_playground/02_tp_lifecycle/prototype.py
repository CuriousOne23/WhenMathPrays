"""ThoughtPoint lifecycle macro module.

Pure importable module used by harness.py for deterministic verification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Iterable
import uuid

import numpy as np


DETERMINISTIC_NAMESPACE = uuid.UUID("d2d76ea9-3388-4b66-8a9f-0f66eb57fbb3")


def _stable_float_tuple(values: Iterable[float]) -> tuple[str, ...]:
	return tuple(f"{float(v):.12f}" for v in values)


def _deterministic_tp_id(parts: Iterable[str]) -> str:
	key = "|".join(parts)
	digest = sha256(key.encode("utf-8")).hexdigest()
	return str(uuid.uuid5(DETERMINISTIC_NAMESPACE, digest))


@dataclass(slots=True)
class EntropyComponents:
	"""Entropy decomposition used by ThoughtPoint state."""

	h_rep: float
	h_pred: float
	h_struct: float
	alpha: float = 1.0
	beta: float = 1.0
	gamma: float = 1.0

	def __post_init__(self) -> None:
		self.h_rep = max(0.0, float(self.h_rep))
		self.h_pred = max(0.0, float(self.h_pred))
		self.h_struct = max(0.0, float(self.h_struct))

	@property
	def total(self) -> float:
		return self.alpha * self.h_rep + self.beta * self.h_pred + self.gamma * self.h_struct

	def apply_delta(self, d_rep: float = 0.0, d_pred: float = 0.0, d_struct: float = 0.0) -> None:
		self.h_rep = max(0.0, self.h_rep + d_rep)
		self.h_pred = max(0.0, self.h_pred + d_pred)
		self.h_struct = max(0.0, self.h_struct + d_struct)

	def copy(self) -> EntropyComponents:
		return EntropyComponents(
			h_rep=self.h_rep,
			h_pred=self.h_pred,
			h_struct=self.h_struct,
			alpha=self.alpha,
			beta=self.beta,
			gamma=self.gamma,
		)

	def as_dict(self) -> dict[str, float]:
		return {
			"h_rep": self.h_rep,
			"h_pred": self.h_pred,
			"h_struct": self.h_struct,
			"alpha": self.alpha,
			"beta": self.beta,
			"gamma": self.gamma,
			"total": self.total,
		}


@dataclass(slots=True)
class HistoryEntry:
	tick: int
	action: str
	basin_id: str
	entropy_total: float
	state_counter: int
	tags: tuple[str, ...]
	note: str = ""

	def as_dict(self) -> dict[str, object]:
		return {
			"tick": self.tick,
			"action": self.action,
			"basin_id": self.basin_id,
			"entropy_total": self.entropy_total,
			"state_counter": self.state_counter,
			"tags": list(self.tags),
			"note": self.note,
		}


@dataclass(slots=True)
class ProvenanceTree:
	created_from: str = "seed"
	parent_ids: list[str] = field(default_factory=list)
	split_children: list[str] = field(default_factory=list)
	merge_sources: list[str] = field(default_factory=list)

	def as_dict(self) -> dict[str, object]:
		return {
			"created_from": self.created_from,
			"parent_ids": list(self.parent_ids),
			"split_children": list(self.split_children),
			"merge_sources": list(self.merge_sources),
		}


@dataclass(slots=True)
class ThoughtPoint:
	tp_id: str
	current_basin_id: str
	entropy: EntropyComponents
	embedding: np.ndarray
	created_at_tick: int
	energy: float = 1.0
	deterministic_mode: bool = True
	state_counter: int = 0
	last_updated_tick: int = 0
	tags: set[str] = field(default_factory=set)
	history: list[HistoryEntry] = field(default_factory=list)
	provenance: ProvenanceTree = field(default_factory=ProvenanceTree)

	def __post_init__(self) -> None:
		self.last_updated_tick = self.created_at_tick
		self.embedding = np.asarray(self.embedding, dtype=float)
		self._bump_state(tick=self.created_at_tick, action="created", note=self.provenance.created_from)

	@classmethod
	def new(
		cls,
		basin_id: str,
		entropy: EntropyComponents,
		embedding: Iterable[float],
		created_at_tick: int,
		energy: float = 1.0,
		deterministic_mode: bool = True,
		deterministic_nonce: int = 0,
		tp_id: str | None = None,
	) -> ThoughtPoint:
		embedding_arr = np.asarray(list(embedding), dtype=float)
		if tp_id is None:
			if deterministic_mode:
				tp_id = _deterministic_tp_id(
					[
						basin_id,
						str(created_at_tick),
						f"{energy:.12f}",
						str(deterministic_nonce),
						*_stable_float_tuple(embedding_arr.tolist()),
						*_stable_float_tuple(
							[
								entropy.h_rep,
								entropy.h_pred,
								entropy.h_struct,
								entropy.alpha,
								entropy.beta,
								entropy.gamma,
							]
						),
					]
				)
			else:
				tp_id = str(uuid.uuid4())
		return cls(
			tp_id=tp_id,
			current_basin_id=basin_id,
			entropy=entropy.copy(),
			embedding=embedding_arr,
			created_at_tick=created_at_tick,
			energy=energy,
			deterministic_mode=deterministic_mode,
		)

	def move_to_basin(self, basin_id: str, tick: int, note: str = "") -> None:
		if basin_id == self.current_basin_id:
			return
		self.current_basin_id = basin_id
		self._bump_state(tick=tick, action="move", note=note)

	def update_entropy(self, tick: int, d_rep: float = 0.0, d_pred: float = 0.0, d_struct: float = 0.0) -> None:
		if d_rep == 0.0 and d_pred == 0.0 and d_struct == 0.0:
			return
		self.entropy.apply_delta(d_rep=d_rep, d_pred=d_pred, d_struct=d_struct)
		self._bump_state(tick=tick, action="entropy_update")

	def add_tag(self, tag: str, tick: int) -> None:
		if tag in self.tags:
			return
		self.tags.add(tag)
		self._bump_state(tick=tick, action="tag_add", note=tag)

	def remove_tag(self, tag: str, tick: int) -> None:
		if tag not in self.tags:
			return
		self.tags.remove(tag)
		self._bump_state(tick=tick, action="tag_remove", note=tag)

	def split(self, tick: int, child_count: int = 2) -> list[ThoughtPoint]:
		if child_count < 2:
			raise ValueError("child_count must be >= 2")
		children: list[ThoughtPoint] = []
		for idx in range(child_count):
			child_id = (
				_deterministic_tp_id(["split", self.tp_id, str(tick), str(idx), str(child_count)])
				if self.deterministic_mode
				else None
			)
			child = ThoughtPoint.new(
				basin_id=self.current_basin_id,
				entropy=self.entropy,
				embedding=self.embedding,
				created_at_tick=tick,
				energy=self.energy / child_count,
				deterministic_mode=self.deterministic_mode,
				deterministic_nonce=idx,
				tp_id=child_id,
			)
			child.provenance = ProvenanceTree(created_from="split", parent_ids=[self.tp_id])
			child.add_tag(f"split_child_{idx}", tick=tick)
			children.append(child)

		self.provenance.split_children.extend([c.tp_id for c in children])
		self._bump_state(tick=tick, action="split", note=f"children={child_count}")
		return children

	@classmethod
	def merge(
		cls,
		sources: list[ThoughtPoint],
		tick: int,
		basin_id: str | None = None,
		deterministic_mode: bool = True,
	) -> ThoughtPoint:
		if not sources:
			raise ValueError("sources cannot be empty")
		dim = sources[0].embedding.shape
		if any(tp.embedding.shape != dim for tp in sources):
			raise ValueError("all source embeddings must have the same shape")

		merged_basin = basin_id or sources[0].current_basin_id
		merged_entropy = EntropyComponents(
			h_rep=float(np.mean([tp.entropy.h_rep for tp in sources])),
			h_pred=float(np.mean([tp.entropy.h_pred for tp in sources])),
			h_struct=float(np.mean([tp.entropy.h_struct for tp in sources])),
			alpha=sources[0].entropy.alpha,
			beta=sources[0].entropy.beta,
			gamma=sources[0].entropy.gamma,
		)
		merged_embedding = np.mean(np.stack([tp.embedding for tp in sources]), axis=0)
		merged_energy = float(np.sum([tp.energy for tp in sources]))

		source_ids = sorted(tp.tp_id for tp in sources)
		merged_id = (
			_deterministic_tp_id(["merge", str(tick), merged_basin, *source_ids])
			if deterministic_mode
			else None
		)

		merged = cls.new(
			basin_id=merged_basin,
			entropy=merged_entropy,
			embedding=merged_embedding,
			created_at_tick=tick,
			energy=merged_energy,
			deterministic_mode=deterministic_mode,
			tp_id=merged_id,
		)
		merged.provenance = ProvenanceTree(created_from="merge", merge_sources=source_ids)
		merged.add_tag("merged", tick=tick)
		return merged

	def _bump_state(self, tick: int, action: str, note: str = "") -> None:
		self.state_counter += 1
		self.last_updated_tick = tick
		self.history.append(
			HistoryEntry(
				tick=tick,
				action=action,
				basin_id=self.current_basin_id,
				entropy_total=self.entropy.total,
				state_counter=self.state_counter,
				tags=tuple(sorted(self.tags)),
				note=note,
			)
		)

	def to_dict(self) -> dict[str, object]:
		return {
			"tp_id": self.tp_id,
			"current_basin_id": self.current_basin_id,
			"entropy": self.entropy.as_dict(),
			"embedding": self.embedding.tolist(),
			"created_at_tick": self.created_at_tick,
			"energy": self.energy,
			"deterministic_mode": self.deterministic_mode,
			"state_counter": self.state_counter,
			"last_updated_tick": self.last_updated_tick,
			"tags": sorted(self.tags),
			"provenance": self.provenance.as_dict(),
			"history": [entry.as_dict() for entry in self.history],
		}

	def __repr__(self) -> str:
		return (
			"ThoughtPoint("
			f"tp_id={self.tp_id}, "
			f"basin={self.current_basin_id}, "
			f"state_counter={self.state_counter}, "
			f"H_total={self.entropy.total:.3f}, "
			f"energy={self.energy:.3f}, "
			f"tags={sorted(self.tags)}"
			")"
		)


__all__ = [
	"EntropyComponents",
	"HistoryEntry",
	"ProvenanceTree",
	"ThoughtPoint",
]
