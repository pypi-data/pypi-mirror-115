import typing as t
from mapioulib.video import Video
import dataclasses as dt
from scipy.optimize import linear_sum_assignment


@dt.dataclass(frozen=True)
class Matching:
    gt_sequence: "Video"
    pred_sequence: "Video"
    matches: t.List[t.Tuple[int, t.Any]]

    @staticmethod
    def calculate_matching(gt_sequence: "Video", pred_sequence: "Video") -> "Matching":
        """
        Calculates the matching between GT sequence and Pred sequence of a video

        :param gt_sequence: Sequence of action segments in Ground Truth
        :param pred_sequence: Sequence of action segments in Prediction

        :return Matching: the best fit match between each segments of GT and Pred
        """

        gt_len = len(gt_sequence.segments)
        pred_len = len(pred_sequence.segments)

        if gt_len == 0 and pred_len > 0:
            return Matching(
                gt_sequence,
                pred_sequence,
                [(None, idx) for idx in range(pred_len)],
            )

        if pred_len == 0 and gt_len > 0:
            return Matching(
                gt_sequence, pred_sequence, [(idx, None) for idx in range(gt_len)]
            )

        if pred_len == 0 and gt_len == 0:
            return Matching(gt_sequence, pred_sequence, [])

        matrix = [[0 for _ in range(pred_len)] for _ in range(gt_len)]

        for i in range(0, gt_len):
            for j in range(0, pred_len):
                matrix[i][j] = -gt_sequence.segments[i].iou(pred_sequence.segments[j])

        # Hungarian Matching Algorithm
        gt_seg_idx, pred_seg_idx = linear_sum_assignment(matrix)

        pred_seg_covered_idx = []
        tmp_matches = [None] * gt_len
        for i, idx in enumerate(gt_seg_idx):
            if (
                gt_sequence.segments[idx].iou(pred_sequence.segments[pred_seg_idx[i]])
                == 0
            ):
                tmp_matches[idx] = None
            else:
                tmp_matches[idx] = pred_seg_idx[i]
                pred_seg_covered_idx.append(pred_seg_idx[i])

        pred_seg_remaining_idx = list(
            set(list(range(pred_len))) - set(pred_seg_covered_idx)
        )

        return Matching(
            gt_sequence,
            pred_sequence,
            [(i, pred) for i, pred in enumerate(tmp_matches)]
            + [(None, pred_rem_idx) for pred_rem_idx in pred_seg_remaining_idx],
        )

    def visualize_matching(self) -> None:
        """
        Prints the mapping of each segments in GT and Pred sequence of a video
        """
        for match in self.matches:
            if not match[0] is None and not match[1] is None:
                print(
                    "Segment "
                    + str(match[0])
                    + " of ground truth has been matched to predicted segment "
                    + str(match[1])
                )
            elif match[0] is None:
                print(
                    "None of the ground truth segments has been matched to predicted segment "
                    + str(match[1])
                )
            elif match[1] is None:
                print(
                    "None of the predicted segments has been matched to ground truth segment "
                    + str(match[0])
                )

    def calculate_confusion_matrix(
        self, iou_thres: float = 0.5
    ) -> t.Tuple[int, int, int]:
        """
        Calculates the custom confusion matrix given an iou threshold

        :param iou_thres: threshold for the IoU (Intersection over the Union)
        :return true_positive, false_positive, false_negative
        """
        true_positive, false_positive, false_negative = 0, 0, 0

        for match in self.matches:
            if match[0] == None:
                false_positive += 1
            elif match[1] != None:
                gt_segment = self.gt_sequence.segments[match[0]]
                if gt_segment.iou(self.pred_sequence.segments[match[1]]) >= iou_thres:
                    true_positive += 1
                else:
                    false_positive += 1
            else:
                false_negative += 1

        return true_positive, false_positive, false_negative
