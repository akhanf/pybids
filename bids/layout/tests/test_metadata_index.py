import pytest
from bids.layout import BIDSLayout
from bids.layout.layout import MetadataIndex
from os.path import join, abspath, sep
from bids.tests import get_test_data_path

# Fixture uses in the rest of the tests
@pytest.fixture(scope='module')
def index():
    data_dir = join(get_test_data_path(), '7t_trt')
    layout = BIDSLayout(data_dir)
    return MetadataIndex(layout)

def test_index_inits(index):
    assert hasattr(index, 'key_index')
    assert hasattr(index, 'file_index')
    assert index.key_index
    assert index.file_index
    keys = {'EchoTime2', 'EchoTime1', 'IntendedFor', 'CogAtlasID', 'EchoTime',
            'EffectiveEchoSpacing', 'PhaseEncodingDirection', 'RepetitionTime',
             'SliceEncodingDirection', 'SliceTiming', 'TaskName', 'StartTime',
             'SamplingFrequency', 'Columns'}
    assert keys == set(index.key_index.keys())
    targ = 'sub-04/ses-1/func/sub-04_ses-1_task-rest_acq-fullbrain_run-1_bold.nii.gz'
    targ = targ.split('/')
    targ = join(get_test_data_path(), '7t_trt', *targ)
    assert targ in index.file_index
    assert index.file_index[targ]['EchoTime'] == 0.017

def test_index_search_with_no_args(index):
    with pytest.raises(ValueError) as exc:
        index.search()
    assert str(exc.value).startswith("At least one field")

def test_index_search_with_missing_keys(index):
    # Searching with invalid keys should return nothing
    assert index.search('EchoTiming', 'Echolalia', 'EchoOneNiner') == []
    assert index.search(EchoTiming='eleventy') == []

def test_index_search_with_no_matching_value(index):
    results = index.search(EchoTime=0.017)
    assert results
