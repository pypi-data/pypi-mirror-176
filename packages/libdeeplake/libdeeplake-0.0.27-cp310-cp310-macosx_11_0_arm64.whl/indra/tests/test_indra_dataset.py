import deeplake
from indra import api
import numpy as np
import pytest
from .utils import tmp_datasets_dir

def test_png_chunk_bug(tmp_datasets_dir):
    ds = deeplake.dataset(tmp_datasets_dir / "png_chunk_issue", overwrite=True)
    ds.create_tensor("image", htype="image", chunk_compression="png")
    ds.image.append(np.random.randint(0, 255, (200, 200, 4), np.uint8))
    ids = api.dataset(str(tmp_datasets_dir / "png_chunk_issue"))
    assert np.all(ids.tensors[0][0] == ds.image[0].numpy())