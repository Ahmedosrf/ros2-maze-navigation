# مشروع ROS 2 للملاحة في المتاهة باستخدام TurtleBot3

يهدف هذا المشروع إلى استكشاف قدرات الملاحة الذاتية للروبوتات في بيئات المتاهة، وذلك باستخدام إطار عمل ROS 2 (Robot Operating System 2) وروبوت TurtleBot3 Burger في محاكاة Gazebo.

## نظرة عامة على المشروع

يقوم هذا المشروع بتطبيق خوارزمية **حقل الجهد (Potential Field Method)** لتمكين روبوت TurtleBot3 من التنقل في متاهة افتراضية. تعتمد الخوارزمية على توليد قوى جاذبة نحو الهدف وقوى تنافرية بعيداً عن العوائق، مما يسمح للروبوت بالتحرك بسلاسة وتجنب الاصطدامات للوصول إلى النقطة المحددة.

## الميزات الرئيسية

*   **تكامل ROS 2 Jazzy و Gazebo Harmonic:** استخدام أحدث إصدارات ROS 2 ومحاكي Gazebo لتوفير بيئة محاكاة قوية وواقعية.
*   **محاكاة TurtleBot3 Burger:** دمج روبوت TurtleBot3 Burger في بيئة Gazebo، مع إعداد كامل لنموذج الروبوت ومستشعراته.
*   **جسر `ros_gz_bridge`:** استخدام الجسر لربط البيانات بين ROS 2 و Gazebo، بما في ذلك بيانات LiDAR (`/scan`)، بيانات تحديد المواقع (`/odom`)، أوامر السرعة (`/cmd_vel`)، وساعة المحاكاة (`/clock`).
*   **خوارزمية حقل الجهد:** تطبيق فعال لخوارزمية حقل الجهد للملاحة المحلية وتجنب العوائق.
*   **معالجة بيانات LiDAR:** تصفية قراءات LiDAR غير الصالحة (مثل `0.0`، `inf`، و `nan`) لضمان دقة حسابات القوى التنافرية.
*   **تحديد الهدف والتوقف:** قدرة الروبوت على تحديد الهدف والتوقف بدقة ضمن مسافة تحمل محددة (0.20 متر).

## مكونات المستودع

يحتوي هذا المستودع على حزمة `maze_navigation` المخصصة، والتي تتضمن:

*   `launch/maze_sim.launch.py`: ملف إطلاق (launch file) يقوم بتهيئة بيئة المحاكاة، وإطلاق روبوت TurtleBot3، وتفعيل جسر `ros_gz_bridge`، وتشغيل عقدة الملاحة.
*   `maze_navigation/potential_field_planner.py`: عقدة ROS 2 التي تحتوي على تطبيق خوارزمية حقل الجهد، وتتولى معالجة بيانات المستشعرات، وحساب القوى، وإصدار أوامر السرعة.
*   `worlds/simple_maze.world`: ملف وصف العالم الخاص بالمتاهة البسيطة المستخدمة في المحاكاة.

## المتطلبات الأساسية

تم اختبار هذا المشروع على الأنظمة التالية:

*   Ubuntu 24.04 (أو WSL Ubuntu 24.04)
*   ROS 2 Jazzy
*   Gazebo Harmonic

يجب أن تكون لديك بيئة ROS 2 Jazzy و Gazebo Sim مثبتة مسبقاً.

## التبعيات المطلوبة

قم بتثبيت حزم ROS و Gazebo الضرورية باستخدام الأوامر التالية:

```bash
sudo apt update
sudo apt install -y \
  ros-jazzy-ros-gz \
  ros-jazzy-dynamixel-sdk
```

## دليل البدء السريع

لإعداد وتشغيل المشروع بسرعة، اتبع الخطوات التالية:

1.  **إنشاء مساحة عمل ROS 2:**
    ```bash
    mkdir -p ~/ros2_project_ws/src
    cd ~/ros2_project_ws/src
    ```

2.  **استنساخ هذا المستودع:**
    ```bash
    git clone https://github.com/Ahmedosrf/ros2-maze-navigation.git maze_navigation
    ```

3.  **استنساخ مستودعات TurtleBot3 المطلوبة:**
    ```bash
    git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
    git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
    git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
    ```

4.  **تثبيت تبعيات مساحة العمل:**
    ```bash
    cd ~/ros2_project_ws
    source /opt/ros/jazzy/setup.bash
    rosdep install --from-paths src --ignore-src -r -y
    ```

5.  **بناء مساحة العمل:**
    ```bash
    colcon build --symlink-install
    ```

6.  **تفعيل مساحة العمل وتحديد نموذج TurtleBot3:**
    ```bash
    source install/setup.bash
    export TURTLEBOT3_MODEL=burger
    ```

7.  **تشغيل المشروع:**
    ```bash
    ros2 launch maze_navigation maze_sim.launch.py
    ```

سيؤدي هذا الأمر إلى إطلاق Gazebo مع عالم المتاهة البسيط، وروبوت TurtleBot3 Burger، وجسر `ros_gz_bridge`، وعقدة `potential_field_planner`.

## تخصيص معلمات الإطلاق

يمكنك تعديل عالم المحاكاة، نقطة الانطلاق، ونقطة الهدف عن طريق تمرير المعلمات إلى ملف الإطلاق:

```bash
ros2 launch maze_navigation maze_sim.launch.py \
  world:=simple_maze.world \
  spawn_x:=0.5 \
  spawn_y:=0.5 \
  goal_x:=9.0 \
  goal_y:=9.0
```

**أمثلة:**

*   **تغيير الهدف:**
    ```bash
    ros2 launch maze_navigation maze_sim.launch.py goal_x:=8.0 goal_y:=8.5
    ```

*   **تغيير نقطة الانطلاق:**
    ```bash
    ros2 launch maze_navigation maze_sim.launch.py spawn_x:=1.0 spawn_y:=1.0 goal_x:=9.0 goal_y:=9.0
    ```

## استكشاف الأخطاء وإصلاحها

*   **`ros_gz_bridge` أو `ros_gz_sim` غير موجود:**
    ```bash
    sudo apt install ros-jazzy-ros-gz
    ```

*   **`dynamixel_sdk` مفقود أثناء البناء:**
    ```bash
    sudo apt install ros-jazzy-dynamixel-sdk
    ```

*   **Gazebo يعمل ولكن الروبوت لا يتحرك:**
    تأكد من أن مساحة العمل تم بناؤها بنجاح، وأنك قمت بتفعيل ملفات `setup.bash`، وأن متغير البيئة `TURTLEBOT3_MODEL` مضبوط على `burger`، وأن عقدة المخطط (planner node) والجسر يعملان بشكل صحيح.

*   **ملف إطلاق جديد غير موجود بعد الإضافة:**
    أعد بناء وتفعيل مساحة العمل:
    ```bash
    cd ~/ros2_project_ws
    source /opt/ros/jazzy/setup.bash
    colcon build --packages-select maze_navigation --symlink-install
    source ~/ros2_project_ws/install/setup.bash
    ```

## تحسينات مستقبلية محتملة

*   تطوير طرق أكثر قوة للهروب من النهايات الصغرى المحلية في المتاهات المعقدة.
*   تحسين أدوات التصور والتصحيح.
*   معايرة إضافية لتخطيطات متاهة مختلفة.
*   تضمين أدوات تقييم وتسجيل أكثر شمولاً.

## شكر وتقدير

يستند هذا العمل إلى الهيكل الأساسي المقدم في مقرر **DSAI 4304: Robot Simulation** من قبل **الدكتور مروان راضي**. لقد وفر هذا الهيكل الأساس الأولي لبنية الحزمة وإعداد المشروع، بينما تم استكمال تكامل إطلاق ROS 2، وجسر Gazebo، وإعداد TurtleBot3، ومنطق الملاحة بحقل الجهد، والاختبار في هذا التنفيذ.
