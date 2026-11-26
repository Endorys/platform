import h5py
import numpy as np
from pathlib import Path


def inspect_uff_structure(uff_filepath: str | Path) -> list[str]:
    """Lists all internal HDF5 dataset and group paths inside a .uff file."""
    paths: list[str] = []
    with h5py.File(uff_filepath, "r") as f:
        f.visit(paths.append)
    return paths


def load_uff_channel_data(
    uff_filepath: str | Path,
    dataset_path: str = "/channel_data/data",
    default_fs_hz: float = 40e6,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """
    Loads RF channel data from standard HDF5 Ultrasound File Format (.uff) files
    for compatibility with international clinical and phantom benchmarks (Zenodo/USTB).

    Returns:
        time_us (np.ndarray): 1D time axis in microseconds.
        rf_data (np.ndarray): 2D/3D raw RF waveform array.
        metadata (dict): Extracted acquisition attributes (sampling_frequency, sound_speed).
    """
    with h5py.File(uff_filepath, "r") as f:
        if dataset_path not in f:
            available = inspect_uff_structure(uff_filepath)
            raise KeyError(
                f"Dataset '{dataset_path}' not found in {uff_filepath}. "
                f"Available HDF5 paths: {available[:15]}"
            )

        rf_data = np.asarray(f[dataset_path], dtype=np.float64)
        group = f["/channel_data"] if "/channel_data" in f else f[dataset_path].parent

        fs_hz = float(group.attrs.get("sampling_frequency", default_fs_hz))
        sound_speed = float(group.attrs.get("sound_speed", 1540.0))

    n_samples = rf_data.shape
    time_us = (np.arange(n_samples, dtype=np.float64) / fs_hz) * 1e6

    metadata = {
        "source_file": str(uff_filepath),
        "dataset_path": dataset_path,
        "sampling_frequency_hz": fs_hz,
        "sound_speed_mps": sound_speed,
        "shape": rf_data.shape,
    }
    return time_us, rf_data, metadata
