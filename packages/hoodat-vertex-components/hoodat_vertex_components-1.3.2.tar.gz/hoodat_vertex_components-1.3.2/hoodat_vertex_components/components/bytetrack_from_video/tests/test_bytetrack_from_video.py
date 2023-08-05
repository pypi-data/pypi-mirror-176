from unittest import mock
from kfp.v2.dsl import Artifact


@mock.patch("tools.demo_track.yolox.data.data_augment")
# @mock.patch('tools.demo_track.yolox')
def test_bytetrack_from_video():
    """Assert bytetrack_from_video calls the main function with exp and
    args
    """
    from component import bytetrack_from_video

    # with mock.patch("google.cloud.aiplatform.Artifact") as mock_video, mock.patch("google.cloud.aiplatform.Artifact") as mock_weights, mock.patch("google.cloud.aiplatform.Artifact") as mock_output_file:

    # Mock attribute and method
    # mock_video.resource_name = "mock-video-name"
    # mock_video.labels = {}
    # mock_video.list.return_value = [mock_video]

    # mock_weights.resource_name = "mock-weights-name"
    # mock_weights.labels = {}
    # mock_weights.list.return_value = [mock_weights]

    # mock_output_file.resource_name = "mock-output-file-name"
    # mock_output_file.labels = {}
    # mock_output_file.list.return_value = [mock_output_file]

    bytetrack_from_video(
        input_video=Artifact(uri="hey"),
        input_weights=Artifact(uri="hey"),
        output_file=Artifact(uri="hey"),
        device="gpu",
    )
