import typing as t
import dataclasses as dt
from mapioulib.segment import Segment


@dt.dataclass(frozen=True)
class Video:
    name: str  # Sample reference name for the video
    segments: t.List[Segment]  # Sequence of action segments in order

    def create_transcript(sequence: t.List[int]) -> t.Tuple[t.List[int], t.List[int]]:
        """
        Creates a transcript of the video framewise annotation

        :param sequence: sequence of class indices for a video
        :return transcript: sequence of segments, segment_length: length of each segments
        """
        transcript = []
        segment_length = []
        prev = 0

        idx = 0
        while idx < len(sequence):
            curr = sequence[idx]
            if curr != prev or idx == 0:  # if current class mismatch previous, add it
                transcript.append(curr)
                segment_length.append(1)
                prev = curr
            else:
                segment_length[-1] += 1
            idx += 1

        return transcript, segment_length

    @staticmethod
    def create_from_list(name: str, video_sequence: list, bg_class: int) -> "Video":
        """
        Creates a Video type of sequence of action segments

        :param name: name tag for this video
        :param video_sequence: sequence of action or background for the video
        :param bg_class: background class index to ignore them for the segment

        :return Video
        """
        transcript, segments_length = Video.create_transcript(video_sequence)

        running_length = 0
        segments = []
        for idx, tr in enumerate(transcript):
            if tr != bg_class:
                segments.append(
                    Segment(running_length, running_length + segments_length[idx], tr)
                )
            running_length += segments_length[idx]

        return Video(name, segments)

    def filter_by_category(self, category: int) -> "Video":
        """
        Filter the Video with only said category, i.e. Video with only "category" class

        :param category: class index to be filtered
        :return Video: video with only "category" class
        """
        return Video(
            self.name,
            list(filter(lambda item: item.category == category, self.segments)),
        )

    def video_visualize(self) -> None:
        pass
