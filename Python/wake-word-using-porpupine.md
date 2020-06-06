Use `` to add on-device wake word detection.
https://github.com/Picovoice/porcupine

  brew install portaudio
  pip install pyaudio
  pip install pvporcupine

The following function wraps up the simplest way to detect 
wake word "bumblebee".


  import pyaudio
  import struct
  import pvporcupine


  def _wait_for_hotword(keyword="bumblebee"):
      proc = pvporcupine.create(keywords=[keyword])
      pa = pyaudio.PyAudio()
      audio_stream = pa.open(
          rate=proc.sample_rate,
          channels=1,
          format=pyaudio.paInt16,
          input=True,
          frames_per_buffer=proc.frame_length)
      while True:
          pcm = audio_stream.read(proc.frame_length)
          pcm = struct.unpack_from("h" * proc.frame_length, pcm)
          result = proc.process(pcm)
          if result:
              break

