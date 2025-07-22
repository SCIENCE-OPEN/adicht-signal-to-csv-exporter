import adi
import os
import sys
import numpy as np
import pandas as pd
import argparse

def validate_destination(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Is required a valid destination directory for .csv output file or files: {path}")
    return path

def validate_source(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"Is required a valid source directory or a single .adicht file path: {path}")
    if os.path.isfile(path) and not path.endswith(".adicht"):
        raise argparse.ArgumentTypeError(f"Is required a valid source directory or a single .adicht file path: {path}")
    return path

def parse_suffix_map(map_str):
    mapping = {}
    for item in map_str.split(","):
        suffix, ch = item.strip().split(":")
        mapping[suffix.lower()] = int(ch)
    return mapping

parser = argparse.ArgumentParser()
parser.add_argument("src_path", type=validate_source, help="Path to source directory or single .adicht file")
parser.add_argument("dest_dir_path", type=validate_destination, help="Path to destination directory for .csv output file or files")
parser.add_argument("--sep", default=",", help="Delimiter used to split specimen entries in filenames (default is comma)")
parser.add_argument("--suffix-map", default="r:0,g:2", help="Mapping of specimen suffixes to channel numbers, e.g. r:0,g:2")
args = parser.parse_args()

src_path = args.src_path
dest_dir_path = args.dest_dir_path
sep = args.sep
suffix_map = parse_suffix_map(args.suffix_map)

def is_signal_flat(signal, tolerance=0.01, flat_ratio=0.9):
    median = np.median(signal)
    lower = median - tolerance
    upper = median + tolerance
    flat_points = np.logical_and(signal >= lower, signal <= upper)
    return np.sum(flat_points) / len(signal) >= flat_ratio

def process_adicht_file(file_path_adicht, dest_dir_path):
    basename = os.path.splitext(os.path.basename(file_path_adicht))[0]
    f = adi.read_file(file_path_adicht)
    print(f"Loaded {file_path_adicht}")
    record_id = 1
    written_any = False

    parts = basename.split(sep)
    for part in parts:
        part_clean = part.strip()
        if not part_clean:
            continue

        matched = False
        for suffix, channel in suffix_map.items():
            if part_clean.lower().endswith(suffix):
                core_name = part_clean[:-len(suffix)]
                try:
                    data = f.channels[channel].get_data(record_id)
                    if not is_signal_flat(data):
                        out_path = os.path.join(dest_dir_path, core_name + ".csv")
                        pd.DataFrame(data).to_csv(out_path, header=False, index=False, sep=sep)
                        print(f"Created {out_path}")
                        written_any = True
                        matched = True
                        break
                    else:
                        print(f"Channel {channel} for {core_name} is flat.")
                except Exception as e:
                    print(f"Error accessing channel {channel} in {file_path_adicht}: {e}")
        if matched:
            continue

        # if no suffix match and only one ID in filename, try fallback
        if len(parts) == 1:
            core_name = part_clean
            print(f"No suffix match. Trying fallback for single ID: {core_name}")
            for ch in range(len(f.channels)):
                try:
                    data = f.channels[ch].get_data(record_id)
                    if not is_signal_flat(data):
                        out_path = os.path.join(dest_dir_path, core_name + ".csv")
                        pd.DataFrame(data).to_csv(out_path, header=False, index=False, sep=sep)
                        print(f"Created {out_path} (from channel {ch})")
                        written_any = True
                        break
                except Exception:
                    continue

    if not written_any:
        print(f"Skipping {basename}: no usable signal found.")

if os.path.isdir(src_path):
    src_files = [os.path.join(dirpath, f)
                 for dirpath, _, files in os.walk(src_path)
                 for f in files if f.endswith('.adicht')]

    if not src_files:
        print("No .adicht files found in the specified source directory.")
        sys.exit(0)

    for file_path_adicht in src_files:
        process_adicht_file(file_path_adicht, dest_dir_path)
else:
    process_adicht_file(src_path, dest_dir_path)
