import array
from distutils.command.bdist_wininst import bdist_wininst
from logging.handlers import WatchedFileHandler
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.utils import get_array_type

def read_mp3(filename):
    sound = AudioSegment.from_mp3(filename)
    # 将立体声音频与Pydub分开到单声道
    # 左耳
    left = sound.split_to_mono()[0]
    # 右耳
    right = sound.split_to_mono()[1]

    bit_depth = left.sample_width * 8
    print("byte_depth: ", left.sample_width)
    print("bit_depth: ",bit_depth)
    array_type = get_array_type(bit_depth)
    left_numeric_array = array.array(array_type, left._data)
    right_numeric_array = array.array(array_type, right._data)
    # 32768 = pow(2,15), 15 is because the bit_depth is 16
    # and the array_type is 'h' which means signed short int
    # the max = pow(2,15)-1
    # the min = 1-pow(2,15)
    # so divide by pow(2,15) to normalize the data
    left_channel = np.array(left_numeric_array) / 32768
    right_channel = np.array(right_numeric_array) / 32768
    wave_data = np.vstack([left_channel,right_channel])
    # sf.write('Test.wav', wave_data.T, 44100)
    # 在数字音频中，44,100 Hz（交替代表为44.1 kHz）是一个常见的采样频率。
    # 模拟音频通常是通过对每秒44,100次采样来记录的，然后使用这些样品在播放时重建音频信号。
    return wave_data, left_channel, right_channel

def get_profile_mp3(filename):
    sound = AudioSegment.from_mp3(filename)
    channel_count = sound.channels
    print("channel_count: ",channel_count)
    frames_per_second = sound.frame_rate
    print("frames_per_second: ",frames_per_second)
    duration_seconds = sound.duration_seconds
    print("duration_seconds: ",sound.duration_seconds)
    # print((len(sound) / 1000.0))
    raw_audio_data = sound.raw_data   #这是bytes类型的
    wav_data=sound.get_array_of_samples()   #这是array类型的数据
    # print("raw_audio_data: ",raw_audio_data)
    bytes_per_frame = sound.frame_width
    print("bytes_per_frame: ",bytes_per_frame)
    print("frame_count: ",frames_per_second*duration_seconds)

    # print(type(wav_data[0]))
    print("wav_data_array_type: ",wav_data.typecode," ",wav_data.itemsize) # int 2 bytes
    wav_data = np.array(wav_data)
    print("wav_data_shape: ",wav_data.shape)
    print("wav_data_max: ",wav_data.max())
    print("wav_data_min: ",wav_data.min())
    print()
    # #取得音频的分贝数
    # loudness = sound.dBFS
    # print(loudness)
    # #获取音频音量大小，该值通常用来计算分贝数（dB= 20×lgX）
    # loudness = sound.rms
    # print(loudness)

def change_mp3(filename):
    sound = AudioSegment.from_mp3(filename)
    # 语音切割,以毫秒为单位
    start_time=0
    end_time=2000
    part = sound[start_time:end_time]
    #调整音量大小
    louder_via_method = sound.apply_gain(+3.5) # 提高
    quieter_via_method = sound.apply_gain(-5.7) # 减小
    #调整多声道音频的左右声道音量
    #如果单声道音频调用此方法，它将先被转换为多声道
    stereo_balance_adjusted = sound.apply_gain_stereo(-6, +2)
    #左右声道平衡，按百分比增大一边，减小另一边
    # pan the sound 15% to the right
    panned_right = sound.pan(+0.15)
    # pan the sound 50% to the left
    panned_left = sound.pan(-0.50)

def save_frame(filename,start_time=0,end_time=2000):
    sound = AudioSegment.from_mp3(filename)
    # 语音切割,以毫秒为单位
    #语音文件切割
    part = sound[start_time:end_time]
    #定义切割文件名称
    data_split_filename='..//mp3_sample//save.wav'
    #保存切割文件
    part.export(data_split_filename, format="wav")

def mp3_to_wav(mp3_filename,wav_filename,frame_rate):
    '''
    调整语音文件的编码  mp3 --> wav
    :param mp3_filename: mp3文件名称
    :param wav_filename: wav文件名称
    :param frame_rate: 采样频率
    :return:
    '''
    mp3_file = AudioSegment.from_mp3(file=mp3_filename)
    mp3_file.set_frame_rate(frame_rate).export(wav_filename,format="wav")

test_path = "F:\\repos\\composer\\mp3_sample\\Whirling_In_Rags.mp3"
mp3_profile = get_profile_mp3(test_path)
data = read_mp3(test_path)

# save_frame(test_path)