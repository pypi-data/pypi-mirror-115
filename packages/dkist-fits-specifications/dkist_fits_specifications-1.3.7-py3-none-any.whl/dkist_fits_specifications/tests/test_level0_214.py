from dkist_fits_specifications.spec214.level0 import spec214_122_key_map, load_level0_spec214


def test_key_map():
    key_map = spec214_122_key_map()
    assert key_map['LINEWAV'] == 'WAVELNTH'


def test_level0_spec():
    spec = load_level0_spec214()
    assert 'WAVELNTH' in spec['fits']
    assert spec['dataset']['LINEWAV']['rename'] == 'WAVELNTH'

