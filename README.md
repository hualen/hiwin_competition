=====================================================================
Terminal指令
=====================================================================
進docker資料夾
cd ub2204_ws/ubuntu20.04_docker/22.04_ros2_cuda11_cudnn/ros2/docker/

執行docker

docker start ub2204_ros2_cuda ub2204_ros2_cuda
#./run.sh
=====================================================================
doceker內指令
=====================================================================
進workspace
cd hiwin_ws/

source指令 (開新視窗都要source，不然手臂程式讀不到hiwin_interface)
. install/setup.bash 

=====================================================================
三點校正指令
=====================================================================
連線手臂server
ros2 run hiwin_libmodbus hiwinlibmodbus_server

ros2 launch hiwin_example bag_three_points_calibration.launch.py

ros2 run hiwin_example three_points_calibration_example --ros-args --params-file ~/work/hiwin_ws/install/hiwin_example/share/hiwin_example/config/bag_cali_pose.yaml


=====================================================================
手臂相關指令
=====================================================================
比賽程式
python3 src/competition/competition2.py

取料測試與調整
python3 src/competition/competition_test.py

回家程式
python3 src/competition/home.py

紀錄當前點位程式
python3 src/competition/nowposition.py
