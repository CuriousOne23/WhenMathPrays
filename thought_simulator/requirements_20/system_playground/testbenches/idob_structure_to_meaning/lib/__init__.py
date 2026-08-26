"""Shared helpers for the IdOB learning bench."""

from .hash_toy import toy_structural_key
from .packet import empty_packet, print_packet
from .schema_load import bench_root, load_yaml
from .vector6 import NAMES, add_scaled, clip_unit, delta_l2, fmt, from_mapping, zeros
