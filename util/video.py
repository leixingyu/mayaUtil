import os
import tempfile
import ffmpeg
import subprocess

"""
Can be used through convert_video() or use it like this to connect multiple
sequences located in seperated folder hierearchy

#------ USAGE EXAMPLE ------ #
dir_a = r'C:\project1\scene1\sequence1'
dir_b = r'C:\project2\scene3\sequence3'
output_path = r'D:\test.mov'

seq_a = Sequence(dir_a)
seq_b = Sequence(dir_b)

vc = VideoConverter(seq_a.sequence, seq_b.sequence)
vc.explicitExport(output_path, '', 0, 30)
"""


class Sequence(object):
    """
    class collects file sequence information to pass into video converter.
    """

    def __init__(self, folder):
        """
        Initialization

        :param folder: str. folder containing all the images to make sequence
        """

        self._folder = folder
        self._sequence = self._as_image_sequence()

    @property
    def folder(self):
        """
        :return: str. folder containing image sequence
        """
        return self._folder

    @property
    def sequence(self):
        """
        :return: list. image sequences in the folder.
        """
        return self._sequence

    def _as_image_sequence(self):
        """
        Returns all image files within the folder as image sequence names
        Example:
            ['C:/test01/test001.jpg', 'C:/test01/test002.jpg']

        :return: list. image full path sequences
        """
        image_names = os.listdir(self._folder)
        seq_paths = [os.path.join(self._folder, name)
                          for name in image_names]

        return seq_paths


class VideoConverter(object):
    """
    Class to combine one or more image sequence(s) to video with audio.
    """

    def __init__(self, *sequences):
        self._sequences = sequences
        self._output_dir = None

    @property
    def output_dir(self):
        return self._output_dir

    def export(self, output_path, frame_rate, audio_file='', audio_start=0):
        """
        Creates a video based on image sequence(s)
        Frame can start at any number since image names are explicitly stored
        in the demuxer.

        The input file .txt content now looks like
        (note the start frame can be any number):

        file 'C:/test01/test01-00140.jpg'
        file 'C:/test01/test01-00141.jpg'
        ...
        file 'C:/test02/test02-00899.jpg'
        file 'C:/test02/test02-00900.jpg'
        """

        # create temp demuxer and dump sequence info
        temp_dir = tempfile.mkdtemp(prefix='project_')
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            dir=temp_dir,
            prefix='project_',
            suffix='.txt'
            )
        for sequence in self._sequences:
            for image in sequence:
                temp_file.write("file '{0}'\n".format(image))
        temp_file.close()

        # use ffmpeg command to convert images to audio
        convert_cmds = [
            ffmpeg.FFMPEG_BIN,
            '-f', 'concat',
            '-r', str(frame_rate),
            '-safe', '0',
            '-i', temp_file.name,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '23',
            '-r', str(frame_rate),
            '-shortest',
            '-y',
            output_path
            ]

        combine_process = subprocess.Popen(
            convert_cmds,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )
        output, error = combine_process.communicate()

        # remove temp demuxer after convertion
        os.remove(temp_file.name)
        os.rmdir(temp_dir)

        if audio_file:
            attach_audio(output_path, frame_rate, audio_file, audio_start)

        if not error:
            print(output)
            self._output_dir = output_path
        else:
            print(error)


def frame_to_timecode(frame_number, frame_rate):
    """
    Convert frames into timecode format 00:00:00.0.
    Specificaly, the last digit set is a float for seconds --> 00:00:00.0

    :param frames: int. Frame number to convert to timecode.
    :param rate: float. Frame rate to solve timecode base. 30fps or 24 fps.
    :return: str. Converted timecode output in format 00:00:00.0
    """

    remaining_frames = frame_number
    hours = remaining_frames / (frame_rate * 60 * 60)
    remaining_frames %= frame_rate * 60 * 60
    minutes = remaining_frames / (frame_rate * 60)
    remaining_frames %= frame_rate * 60
    seconds = remaining_frames / frame_rate
    timecode = '{0:02d}:{1:02d}:{2:02f}'.format(
        int(hours),
        int(minutes),
        seconds
        )
    return timecode


def attach_audio(output_path, frame_rate, audio_file, audio_start):
    """
    Used in export function to Offset audio in merged video/audio.

    :param output_path: str. output path to movie file.
    :param frame_rate: int. frame rate
    :param audio_file: str. input path to audio file
    :param audio_start: str. start time value to offset audio from video.
    :return: (str, str). subprocess stdout and stderr.
    """

    timecode = frame_to_timecode(int(audio_start), frame_rate)
    temp_mov = '{0}\\vid.mov'.format(os.path.dirname(output_path))
    offset_cmds = [
        ffmpeg.FFMPEG_BIN,
        '-i', output_path,
        '-ss', timecode,
        '-i', audio_file,
        '-vcodec', 'copy',
        '-acodec', 'copy',
        '-map', '0:0',
        '-map', '1:0',
        '-r', '30',
        '-shortest',
        '-y',
        temp_mov
        ]
    offset_process = subprocess.Popen(offset_cmds)
    output, error = offset_process.communicate()

    os.remove(output_path)
    os.rename(temp_mov, output_path)
    return output, error


def convert_video(input_path, output_path):
    """
    Combine multiple sequences (sub-folders) into one complete video
    Example:
        inputPath = [r'C:\scene1\sequence1', r'C:\scene1\sequence2']
        outputPath = r'D:\move\scene1'

    :param input_path: str. input directory full path
    :param output_path: str. output directory full path
    """

    sequences = [Sequence(path).sequence for path in input_path]
    vc = VideoConverter(*sequences)

    if os.path.isfile(output_path):
        os.remove(output_path)
    vc.export(output_path, frame_rate=30)