import typing as t
import dataclasses as dt


@dt.dataclass(frozen=True)
class Segment:
    start: int  # segment start index (inclusive)
    end: int  # segment end index (exclusive)
    category: int  # class index

    def __post_init__(self):
        assert self.start >= 0
        assert self.end > self.start

    def iou(self, other: "Segment") -> float:
        """
        Evaluate IoU between self segment and other segment
        :param other: the other segment
        :return IoU of the two segments
        """

        # Checks if the intersection exists
        if max(self.start, other.start) <= min(self.end, other.end):
            intersection_len = min(self.end, other.end) - max(self.start, other.start)
        else:
            intersection_len = 0

        union_len = max(self.end, other.end) - min(self.start, other.start)
        return intersection_len / union_len

    def __len__(self) -> int:
        """
        Evaluate the length of this segment
        :param None
        :return length of this segment
        """
        return self.end - self.start
