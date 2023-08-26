from chord_extractor import clear_conversion_cache, LabelledChordSequence
from chord_extractor.extractors import Chordino
import os
from os.path import abspath, join, realpath, isfile
from timeit import default_timer
import json

sample_file_dir = abspath(join(realpath(__file__), '../data'))
out_dir = abspath(join(realpath(__file__), '../out'))
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


def _get_files_in_dir(dir_):
    return [abspath(join(dir_, f)) for f in os.listdir(dir_) if (isfile(join(dir_, f)))]


def _remove_files(dir_):
    for f in _get_files_in_dir(dir_):
        os.remove(f)


sample_files = _get_files_in_dir(sample_file_dir)


def output_file(chord_list: LabelledChordSequence):
    if chord_list.sequence is None:
        return
    base = os.path.basename(chord_list.id)
    with open(os.path.join(out_dir, os.path.splitext(base)[0]), 'w') as f:
        json.dump(chord_list, f)

# TODO: The file "tests/data/3error_not_really_a_midi.mid" has an output file anyway
def test_extract_many():
    _remove_files(out_dir)
    start = default_timer()
    c = Chordino()
    clear_conversion_cache()
    res = c.extract_many(sample_files,
                         num_extractors=2,
                         num_preprocessors=2,
                         max_files_in_cache=3,
                         callback=output_file)
    end = default_timer()
    print(end - start)
    assert len(res) == 15
    assert len([name for name in os.listdir(out_dir)]) == 14


def test_extract():
    start = default_timer()
    c = Chordino()
    for s in sample_files:
        if 'error' in s:
            continue
        conversion = c.preprocess(s)
        if conversion:
            c.extract(conversion)
            os.remove(conversion)
        else:
            c.extract(s)
    end = default_timer()
    print(end - start)
