from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/bytetrack_from_video",
    output_component_file="component.yaml",
)
def bytetrack_from_video(
    input_video: Input[Artifact],
    input_weights: Input[Artifact],
    output_video: Output[Artifact],
    output_text_file_dataset: Output[Dataset],
    output_video_path: str,
    output_text_file_dataset_path: str,
    device: str = "gpu",  # Must be gpu or cpu
):
    import os
    import shutil
    from tools.demo_track import make_parser, main, get_exp

    if device == "gpu":
        arg_list = [
            "video",
            "-f",
            "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
            "-c",
            input_weights.path,
            "--path",
            input_video.path,
            "--fp16",
            "--fuse",
            "--save_result",
        ]
    elif device == "cpu":
        arg_list = [
            "video",
            "-f",
            "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
            "-c",
            input_weights.path,
            "--device",
            "cpu",
            "--path",
            input_video.path,
            "--fuse",
            "--save_result",
        ]

    if output_video_path is not None:
        if output_video_path.startswith("gs://"):
            output_video_path_gs = output_video_path
            output_video_path_local = output_video_path.replace("gs://", "/gcs/")
        elif output_video_path.startswith("/gcs/"):
            output_video_path_gs = output_video_path.replace("/gcs/", "gs://")
            output_video_path_local = output_video_path
        else:
            raise ValueError(
                "output_video_path should start with either gs:// or /gcs/"
            )
        os.makedirs(os.path.dirname(output_video_path_local), exist_ok=True)
        output_video.uri = output_video_path_gs

    if output_text_file_dataset_path is not None:
        if output_text_file_dataset_path.startswith("gs://"):
            output_text_file_dataset_path_gs = output_text_file_dataset_path
            output_text_file_dataset_path_local = output_text_file_dataset_path.replace(
                "gs://", "/gcs/"
            )
        elif output_text_file_dataset_path.startswith("/gcs/"):
            output_text_file_dataset_path_gs = output_text_file_dataset_path.replace(
                "/gcs/", "gs://"
            )
            output_text_file_dataset_path_local = output_text_file_dataset_path
        else:
            raise ValueError(
                "output_text_file_dataset_path should start with either gs:// or /gcs/"
            )
        os.makedirs(os.path.dirname(output_text_file_dataset_path_local), exist_ok=True)
        output_text_file_dataset.uri = output_text_file_dataset_path_gs

    args = make_parser().parse_args(arg_list)
    exp = get_exp(args.exp_file, args.name)
    main(exp=exp, args=args)

    source_dir = "/ByteTrack/YOLOX_outputs/yolox_x_mix_det/track_vis"
    source_video = f"{source_dir}/output.mp4"
    source_results = f"{source_dir}/results.txt"
    shutil.copyfile(source_video, output_video_path_local)
    shutil.copyfile(source_results, output_text_file_dataset_path_local)
