# ABB_EGM_PYTHON - WINDOWS OS
This is my understanding and learnings on how to implement EGM in ABB robots using python as communication endpoint (Sensor/Server).\
This can be used to implement real time operations on a robot and has limitless capabilities - all thanks to Abb EGM.\
The purpose of this repository is to provide detailed start to end instruction on how to implement egm. Your welcome\


STEPS ARE AS GIVEN BELOW:

1) Install google protocol buffers :\
   1 - Download latest windows release from assets section in [here](https://github.com/protocolbuffers/protobuf/releases). (look for this ->  protoc-3.17.3-win64.zip) or the latest one\
   2 - Go to the extracted path and search for bin folder. Add this path to your system variable. (eg: C:\Protobuf\bin)\
   3 - Also download protobuf-python-3.18.0.tar.gz from the same link and search for setup.py\ 
   3 - Run setup.py in cmd -> This will get you installed the Protobuf compiler\
   4 - Now do 'pip install google' and 'pip install protobuf'\
   5 - Congrats!! you have succesfully installed protobuffer compilers\
   
2) Compile a proto file\
   1 - You will have a proto file from abb - ["egm.proto"](https://github.com/ros-industrial/abb_libegm/blob/master/proto/egm.proto). We have to compile this into our preffered programming language ie, Python in this case.\
   2 - To do that, use cmd to run the following command -> "protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/egm.proto" dont forget to provide destination target and source of your egm.proto file. If that is missed, current directory will be used as source and destination.\
   3 - Now check the destination folder. you'll get the python compiled file ["egm_pb2.py"](https://github.com/bestin-07/ABB_EGM_PYTHON/blob/main/Python/egm_pb2.py)\
   4 - Congrats!! Your not far away now! 
