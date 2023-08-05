from unittest import mock
from kfp.v2.dsl import Artifact


@mock.patch("ffmpeg.concat")
def test_stitch_videos(ffmpeg_concat_patch):
    """Assert bytetrack_from_video calls the main function with exp and
    args
    """
    from component import stitch_videos

    class DummyArtifact:
        path = "hey.mp4"

    stitch_videos(input_videos=Artifact(uri="sample"), output_video=DummyArtifact())
