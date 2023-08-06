import typing as t
from mapioulib.video import Video
from mapioulib.matching import Matching


def __type_check(
    ground_truth_seq: t.List[int],
    predicted_seq: t.List[int],
    bg_class: int,
    iou_thres: float,
) -> None:
    """
    Type checks all the parameters

    :param ground_truth_seq, predicted_seq, bg_class, iou_thres
    """

    assert (
        isinstance(ground_truth_seq, t.List)
        and isinstance(predicted_seq, t.List)
        and isinstance(bg_class, int)
        and isinstance(iou_thres, float)
    ), "Input type incorrect"

    assert len(predicted_seq) == len(ground_truth_seq), "Sequence lengths mismatched"

    assert len(predicted_seq) > 0, "Sequence length cannot be 0"

    assert 0.0 < iou_thres < 1.0, "IoU should be >0.0 and <1.0"

    assert all(isinstance(val, int) for val in ground_truth_seq) and all(
        isinstance(val, int) for val in predicted_seq
    ), "Sequence should be list of integers"


def mapiou(
    ground_truth_seq: t.List[int],
    predicted_seq: t.List[int],
    bg_class: int = 0,
    iou_thres: float = 0.5,
) -> t.Tuple[int, int, int]:
    """
    Evaluates a custom mAP(IoU) for GT and pred sequence of the video

    :param ground_truth_seq: Sequence of action classes as annotated
    :param predicted_seq: Sequence of action classes as predicted
    :param bg_class: background class index
    :param iou_thres: threshold of IoU to be considered

    :return (true_positive, false_positive, false_negative)
    """
    __type_check(ground_truth_seq, predicted_seq, bg_class, iou_thres)

    set_of_classes = set(ground_truth_seq) | set(predicted_seq)

    if bg_class in set_of_classes:
        set_of_classes.remove(bg_class)

    true_positive, false_positive, false_negative = 0, 0, 0
    for class_idx in set_of_classes:
        video_gt = Video.create_from_list(
            "gt", ground_truth_seq, bg_class
        ).filter_by_category(class_idx)

        video_pred = Video.create_from_list(
            "pred", predicted_seq, bg_class
        ).filter_by_category(class_idx)

        matching = Matching.calculate_matching(video_gt, video_pred)

        print(":::: Class " + str(class_idx) + " ::::")
        matching.visualize_matching()
        print("")

        (
            true_positive_,
            false_positive_,
            false_negative_,
        ) = matching.calculate_confusion_matrix(iou_thres)

        true_positive += true_positive_
        false_positive += false_positive_
        false_negative += false_negative_

    return (
        true_positive,
        false_positive,
        false_negative,
    )
