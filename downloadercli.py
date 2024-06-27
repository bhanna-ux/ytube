import streamlit as st
import streamlink
import signal
import ffmpeg
from streamlink import Streamlink
import os
from datetime import datetime
import subprocess 
from subprocess import Popen,PIPE
from streamlit.components.v1 import components


st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important; # Set the width to your desired value
        }

    </style>
    """,
    unsafe_allow_html=True,
)

html ="""

<!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport" content="width=device-widt, initial-scale=1.0">

        <title>1 Hour Timer</title>

        <style>

            body {

                font-family: Arial, sans-serif;color: #1F45FC;

                display: flex;

                justify-content: left;

                align-items: center;

                height: 100vh;

                margin: 0;

                background-color: rgba(255,255,255,0);

            }

            #timer {

                font-size: 17px;

                font-weight: bold;

            }

        </style>

    </head>

    <body>

        <div id="timer">00:00:00</div>

 

        <script>

            function updateTimer() {

                const timerElement = document.getElementById('timer');

                let seconds = 0;

 

                function pad(num) {

                    return num.toString().padStart(2, '0');

                }

 

                const intervalId = setInterval(() => {

                    seconds++;

                    const hours = Math.floor(seconds / 3600);

                    const minutes = Math.floor((seconds % 3600) / 60);

                    const remainingSeconds = seconds % 60;

 

                    timerElement.textContent = `${pad(hours)}:${pad(minutes)}:${pad(remainingSeconds)}`;

 

                    if (seconds >= 3600) {

                        clearInterval(intervalId);

                    }

                }, 1000);

            }

 

            updateTimer();

        </script>

    </body>

    </html>

"""




st.subheader(":blue[YTube Live Stream Recorder]",divider='red')


url = st.sidebar.text_input(':blue[Add Live youtube URL here:]'+':red[*]')
videoname=st.sidebar.text_input(':blue[Write Name of File]'+':red[*]')
c=datetime.now()
current_time=c.strftime('%H:%M')
videoname=videoname +'@'+str(current_time)

def stream_to_url(url, quality='best'):
    # The "audio_only" quality may be invalid for some streams (check).
    session = Streamlink()
    streams = session.streams(url)
    return streams[quality].to_url()


if url :
  play_file=st.video(url)

def recordingaudio():
    stream_url = stream_to_url(url)
    fmpeg_process = (ffmpeg
.input(stream_url)
.audio
.output('C:\'+videoname+'.mp3')
.overwrite_output()
.run_async()
)
    st.write(":red[RECORDING Audio ....]",height=30)
    st.components.v1.html(html,width=100,height=20)
    def Finish():
      fmpeg_process.send_signal(signal.SIGQUIT)
      st.write(':red[Recording FINISHED ..... ]',height=30)
    st.button("Finish Recording ",on_click=Finish)


def record():
  process= subprocess.Popen( ["streamlink" , url ,
"best","-o",'C:\'+videoname+'.mp4'])
  
  #stdout=process.communicate()
  #st.text('\n'.join(stdout.decode().split('\n')))
  st.write(":red[RECORDING Video ....]",height=30)
  st.components.v1.html(html,width=100,height=20)

  def Finish():
    process.send_signal(signal.SIGQUIT)
    st.write(':red[Recording FINISHED ..... ]',height=30)
  st.button("Finish Recording ",on_click=Finish)

  
st.sidebar.button("Start Record Video  ",on_click=record) 
st.sidebar.button("Start Record Audio Only  ",on_click=recordingaudio) 
#def pause():
  #fmpeg_process.send_signal(signal.SIGSTOP)
#st.sidebar.button("Pause",on_click=pause)

#def resume():
  #fmpeg_process.send_signal(signal.SIGCONT)
#st.sidebar.button("Resume",on_click=resume)






       #if Pause:
           #fmpeg_process.send_signal(signal.SIGSTOP)
        #if resume:
            #fmpeg_process.send_signal(signal.SIGCONT)
        #if Finish:
            #fmpeg_process.send_signal(signal.SIGQUIT)
def file_selector(folder_path='/home/bassem/Desktop/videos/'):
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox(':blue[select your file from Downloads Folder]', filenames)
    #return os.path.join(folder_path, selected_filename)
    with open(folder_path +selected_filename, "rb") as file:
        d=file.read()
        btn = st.sidebar.download_button(
                label=":red[Reload Page Before ]"+":blue[ Download ]",
                data=d,
                file_name=selected_filename,
                use_container_width=True
              )
    return os.path.join(selected_filename)
filename=file_selector()
st.sidebar.write('You selected `%s`' % filename) 







#with open('/home/bassem/Desktop/videos/video.mp4', "rb") as file:
#    d=file.read()
#    btn = st.sidebar.download_button(
#            label=":blue[Download Video]",
#            data=d,
#            file_name='recording.mp4',
#            mime='video/mp4',
#            use_container_width=True
#          )


st.sidebar.link_button(":red[Go to Transcription]",
"https://vspar-ia-v-transcript-01.afp.com/editor",
 use_container_width=True)
