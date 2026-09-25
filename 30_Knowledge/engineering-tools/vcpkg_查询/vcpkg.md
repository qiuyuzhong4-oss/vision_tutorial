cmake -B build
-- Running vcpkg install
Fetching registry information from https://github.com/microsoft/vcpkg (HEAD)...
A suitable version of cmake was not found (required v4.4.0).
Downloading https://github.com/Kitware/CMake/releases/download/v4.4.0/cmake-4.4.0-linux-x86_64.tar.gz -> cmake-4.4.0-linux-x86_64.tar.gz
Successfully downloaded cmake-4.4.0-linux-x86_64.tar.gz
Extracting cmake...
Detecting compiler hash for triplet x64-linux...
Compiler found: /usr/bin/c++
The following packages will be built and installed:
    fmt:x64-linux@12.2.0#1 -- git+https://github.com/microsoft/vcpkg@7ca0b8c0026883daf28a0db75f6b4964bae2979a
  * vcpkg-cmake:x64-linux@2024-04-23 -- git+https://github.com/microsoft/vcpkg@e74aa1e8f93278a8e71372f1fa08c3df420eb840
  * vcpkg-cmake-config:x64-linux@2026-07-21 -- git+https://github.com/microsoft/vcpkg@51befcb03097f8d19c1c59f9ec3625e69d85322a
Additional packages (*) will be modified to complete this operation.
Restored 0 package(s) from /home/liantian/.cache/vcpkg/archives in 8.06 us. Use --debug to see more details.
Installing 1/3 vcpkg-cmake-config:x64-linux@2026-07-21...
vcpkg-cmake-config:x64-linux@2026-07-21 package ABI: 60e739ffcfe7456176ee5ce94b8d59293fb6c95edfcfb92365d1b2f7e3e57a75
Building vcpkg-cmake-config:x64-linux@2026-07-21...
/home/liantian/.cache/vcpkg/registries/git-trees/51befcb03097f8d19c1c59f9ec3625e69d85322a: info: installing from git registry git+https://github.com/microsoft/vcpkg@51befcb03097f8d19c1c59f9ec3625e69d85322a
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake-config_x64-linux/share/vcpkg-cmake-config/vcpkg_cmake_config_fixup.cmake
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake-config_x64-linux/share/vcpkg-cmake-config/vcpkg-port-config.cmake
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake-config_x64-linux/share/vcpkg-cmake-config/copyright
-- Skipping post-build validation due to VCPKG_POLICY_EMPTY_PACKAGE
Starting submission of vcpkg-cmake-config:x64-linux@2026-07-21 to 1 binary cache(s) in the background
Elapsed time to handle vcpkg-cmake-config:x64-linux: 12.5 ms
Installing 2/3 vcpkg-cmake:x64-linux@2024-04-23...
vcpkg-cmake:x64-linux@2024-04-23 package ABI: a44e1a169a18d9be512c6eb5c5dfeebf092fc20795dc7fe6a0230b365cb69064
Building vcpkg-cmake:x64-linux@2024-04-23...
/home/liantian/.cache/vcpkg/registries/git-trees/e74aa1e8f93278a8e71372f1fa08c3df420eb840: info: installing from git registry git+https://github.com/microsoft/vcpkg@e74aa1e8f93278a8e71372f1fa08c3df420eb840
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake_x64-linux/share/vcpkg-cmake/vcpkg_cmake_configure.cmake
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake_x64-linux/share/vcpkg-cmake/vcpkg_cmake_build.cmake
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake_x64-linux/share/vcpkg-cmake/vcpkg_cmake_install.cmake
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake_x64-linux/share/vcpkg-cmake/vcpkg-port-config.cmake
-- Installing: /home/liantian/vcpkg/packages/vcpkg-cmake_x64-linux/share/vcpkg-cmake/copyright
-- Performing post-build validation
Starting submission of vcpkg-cmake:x64-linux@2024-04-23 to 1 binary cache(s) in the background
Elapsed time to handle vcpkg-cmake:x64-linux: 12.5 ms
Completed submission of vcpkg-cmake-config:x64-linux@2026-07-21 to 1 binary cache(s) in 3.19 ms
Installing 3/3 fmt:x64-linux@12.2.0#1...
fmt:x64-linux@12.2.0#1 package ABI: f0d9fef89be84c82bfd9e6ccb14eb7c0493ad6e84e8881434e45ca60d176c89e
Building fmt:x64-linux@12.2.0#1...
/home/liantian/.cache/vcpkg/registries/git-trees/7ca0b8c0026883daf28a0db75f6b4964bae2979a: info: installing from git registry git+https://github.com/microsoft/vcpkg@7ca0b8c0026883daf28a0db75f6b4964bae2979a
Downloading https://github.com/fmtlib/fmt/commit/588b3a0f8f6a8bcf2a959cae882d5b2703e86737.patch?full_index=1 -> fmt-backport-4813.patch
Successfully downloaded fmt-backport-4813.patch
Downloading https://github.com/fmtlib/fmt/archive/12.2.0.tar.gz -> fmtlib-fmt-12.2.0.tar.gz
Successfully downloaded fmtlib-fmt-12.2.0.tar.gz
-- Extracting source /home/liantian/vcpkg/downloads/fmtlib-fmt-12.2.0.tar.gz
-- Applying patch /home/liantian/vcpkg/downloads/fmt-backport-4813.patch
-- Using source at /home/liantian/vcpkg/buildtrees/fmt/src/12.2.0-d352ede310.clean
-- Configuring x64-linux
-- Building x64-linux-dbg
-- Building x64-linux-rel
-- Fixing pkgconfig file: /home/liantian/vcpkg/packages/fmt_x64-linux/lib/pkgconfig/fmt.pc
-- Fixing pkgconfig file: /home/liantian/vcpkg/packages/fmt_x64-linux/debug/lib/pkgconfig/fmt.pc
-- Installing: /home/liantian/vcpkg/packages/fmt_x64-linux/share/fmt/usage
-- Installing: /home/liantian/vcpkg/packages/fmt_x64-linux/share/fmt/copyright
Downloading https://github.com/NixOS/patchelf/releases/download/0.19.0/patchelf-0.19.0-x86_64.tar.gz -> patchelf-0.19.0-x86_64.tar.gz
Successfully downloaded patchelf-0.19.0-x86_64.tar.gz
-- Performing post-build validation
Starting submission of fmt:x64-linux@12.2.0#1 to 1 binary cache(s) in the background
Elapsed time to handle fmt:x64-linux: 9.8 s
Installed contents are licensed to you by owners. Microsoft is not responsible for, nor does it grant any licenses to, third-party packages.
Packages installed in this vcpkg installation declare the following licenses:
MIT
The package fmt provides CMake targets:

    find_package(fmt CONFIG REQUIRED)
    target_link_libraries(main PRIVATE fmt::fmt)

    # Or use the header-only version
    find_package(fmt CONFIG REQUIRED)
    target_link_libraries(main PRIVATE fmt::fmt-header-only)

Completed submission of vcpkg-cmake:x64-linux@2024-04-23 to 1 binary cache(s) in 2.62 ms
Waiting for 1 remaining binary cache submissions...
Completed submission of fmt:x64-linux@12.2.0#1 to 1 binary cache(s) in 60.4 ms (1/1)
All requested installations completed successfully in: 9.9 s
-- Running vcpkg install - done
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- --------------------CMAKE_BUILD_TYPE: Release--------------------
-- Found OpenCV: /usr (found version "4.5.4") 
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE  
-- Found nlohmann_json: /usr/lib/cmake/nlohmann_json/nlohmann_jsonConfig.cmake (found version "3.10.5") 
-- Found Python3: /usr/bin/python3 (found version "3.10.12") found components: Interpreter 
-- Found rosidl_generator_c: 3.1.9 (/opt/ros/humble/share/rosidl_generator_c/cmake)
-- Found rosidl_adapter: 3.1.9 (/opt/ros/humble/share/rosidl_adapter/cmake)
-- Found rosidl_generator_cpp: 3.1.9 (/opt/ros/humble/share/rosidl_generator_cpp/cmake)
-- Using all available rosidl_typesupport_c: rosidl_typesupport_fastrtps_c;rosidl_typesupport_introspection_c
-- Using all available rosidl_typesupport_cpp: rosidl_typesupport_fastrtps_cpp;rosidl_typesupport_introspection_cpp
-- Found rmw_implementation_cmake: 6.1.3 (/opt/ros/humble/share/rmw_implementation_cmake/cmake)
-- Found rmw_fastrtps_cpp: 6.2.10 (/opt/ros/humble/share/rmw_fastrtps_cpp/cmake)
-- Found OpenSSL: /usr/lib/x86_64-linux-gnu/libcrypto.so (found version "3.0.2")  
-- Found FastRTPS: /opt/ros/humble/include  
-- Using RMW implementation 'rmw_fastrtps_cpp' as default
CMake Warning at io/CMakeLists.txt:49 (message):
  ROS2 not found, skipping ROS2 specific code.


-- Found required Ceres dependency: Eigen version 3.4.0 in /usr/include/eigen3
-- Found required Ceres dependency: glog
-- Found required Ceres dependency: gflags
-- Found Ceres version: 2.0.0 installed in: /usr with components: [EigenSparse, SparseLinearAlgebraLibrary, LAPACK, SuiteSparse, CXSparse, SchurSpecializations, Multithreading]
-- Found rosidl_generator_c: 3.1.9 (/opt/ros/humble/share/rosidl_generator_c/cmake)
-- Found rosidl_adapter: 3.1.9 (/opt/ros/humble/share/rosidl_adapter/cmake)
-- Found rosidl_generator_cpp: 3.1.9 (/opt/ros/humble/share/rosidl_generator_cpp/cmake)
-- Using all available rosidl_typesupport_c: rosidl_typesupport_fastrtps_c;rosidl_typesupport_introspection_c
-- Using all available rosidl_typesupport_cpp: rosidl_typesupport_fastrtps_cpp;rosidl_typesupport_introspection_cpp
-- Found rmw_implementation_cmake: 6.1.3 (/opt/ros/humble/share/rmw_implementation_cmake/cmake)
-- Found rmw_fastrtps_cpp: 6.2.10 (/opt/ros/humble/share/rmw_fastrtps_cpp/cmake)
-- Using RMW implementation 'rmw_fastrtps_cpp' as default
-- ROS2 environment not found, skipping ROS2-related code.
-- Configuring done
-- Generating done
-- Build files have been written to: /home/liantian/projects/sp_vision_25/build
liantian@bing:~/projects/sp_vision_25$ make -C build/ -j4
make: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[1]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
[  1%] Building CXX object io/serial/CMakeFiles/serial.dir/src/serial.cc.o
[  2%] Building CXX object tasks/omniperception/CMakeFiles/omniperception.dir/decider.cpp.o
[  4%] Building CXX object tasks/auto_aim/planner/tinympc/CMakeFiles/tinympcstatic.dir/admm.cpp.o
[  4%] Building CXX object tools/CMakeFiles/tools.dir/exiter.cpp.o
[  5%] Building CXX object tools/CMakeFiles/tools.dir/extended_kalman_filter.cpp.o
[  6%] Building CXX object io/serial/CMakeFiles/serial.dir/src/impl/unix.cc.o
/home/liantian/projects/sp_vision_25/tasks/auto_aim/planner/tinympc/admm.cpp: In function ‘tinyVector project_soc(tinyVector, float)’:
/home/liantian/projects/sp_vision_25/tasks/auto_aim/planner/tinympc/admm.cpp:40:42: warning: ‘Eigen::placeholders::last’ is deprecated [-Wdeprecated-declarations]
   40 |     tinytype u0 = s(Eigen::placeholders::last) * mu;
      |                                          ^~~~
In file included from /usr/include/eigen3/Eigen/Core:265,
                 from /usr/include/eigen3/Eigen/Dense:1,
                 from /usr/include/eigen3/Eigen/Eigen:1,
                 from /home/liantian/projects/sp_vision_25/tasks/auto_aim/planner/tinympc/types.hpp:3,
                 from /home/liantian/projects/sp_vision_25/tasks/auto_aim/planner/tinympc/admm.hpp:3,
                 from /home/liantian/projects/sp_vision_25/tasks/auto_aim/planner/tinympc/admm.cpp:3:
/usr/include/eigen3/Eigen/src/Core/util/IndexedViewHelper.h:180:40: note: declared here
  180 |   EIGEN_DEPRECATED static const last_t last = Eigen::last;   // PLEASE use Eigen::last   instead of Eigen::placeholders::last
      |                                        ^~~~
[  7%] Building CXX object io/serial/CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o
[  8%] Linking CXX static library libserial.a
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
[  8%] Built target serial
[  9%] Building CXX object tools/CMakeFiles/tools.dir/ransac_sine_fitter.cpp.o
[ 10%] Building CXX object tasks/auto_aim/planner/tinympc/CMakeFiles/tinympcstatic.dir/tiny_api.cpp.o
[ 11%] Building CXX object tasks/omniperception/CMakeFiles/omniperception.dir/perceptron.cpp.o
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
[ 12%] Building CXX object io/CMakeFiles/io.dir/hikrobot/hikrobot.cpp.o
[ 12%] Building CXX object tasks/auto_aim/planner/tinympc/CMakeFiles/tinympcstatic.dir/codegen.cpp.o
[ 13%] Building CXX object tasks/auto_aim/planner/tinympc/CMakeFiles/tinympcstatic.dir/rho_benchmark.cpp.o
[ 14%] Linking CXX static library libtinympcstatic.a
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
[ 14%] Built target tinympcstatic
[ 15%] Building CXX object io/CMakeFiles/io.dir/mindvision/mindvision.cpp.o
[ 16%] Building CXX object io/CMakeFiles/io.dir/usbcamera/usbcamera.cpp.o
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
[ 16%] Built target omniperception
[ 17%] Building CXX object io/CMakeFiles/io.dir/camera.cpp.o
[ 18%] Building CXX object tools/CMakeFiles/tools.dir/img_tools.cpp.o
[ 18%] Building CXX object tools/CMakeFiles/tools.dir/math_tools.cpp.o
[ 19%] Building CXX object tools/CMakeFiles/tools.dir/plotter.cpp.o
[ 20%] Building CXX object io/CMakeFiles/io.dir/cboard.cpp.o
[ 20%] Building CXX object io/CMakeFiles/io.dir/dm_imu/dm_imu.cpp.o
[ 21%] Building CXX object io/CMakeFiles/io.dir/gimbal/gimbal.cpp.o
[ 22%] Building CXX object tools/CMakeFiles/tools.dir/trajectory.cpp.o
[ 23%] Building CXX object tools/CMakeFiles/tools.dir/recorder.cpp.o
[ 24%] Building CXX object tools/CMakeFiles/tools.dir/logger.cpp.o
[ 25%] Building CXX object tools/CMakeFiles/tools.dir/pid.cpp.o
[ 26%] Linking CXX static library libio.a
[ 27%] Building CXX object tools/CMakeFiles/tools.dir/crc.cpp.o
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
[ 27%] Built target io
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
[ 28%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/armor.cpp.o
[ 28%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/classifier.cpp.o
[ 29%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/detector.cpp.o
[ 30%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/solver.cpp.o
[ 31%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/aimer.cpp.o
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
[ 31%] Built target tools
[ 32%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/target.cpp.o
[ 33%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/tracker.cpp.o
[ 33%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/voter.cpp.o
[ 34%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/shooter.cpp.o
[ 35%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/yolo.cpp.o
[ 36%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/yolos/yolov5.cpp.o
[ 37%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/yolos/yolov8.cpp.o
[ 38%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/yolos/yolo11.cpp.o
[ 39%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/multithread/commandgener.cpp.o
[ 39%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/multithread/mt_detector.cpp.o
[ 40%] Building CXX object tasks/auto_aim/CMakeFiles/auto_aim.dir/planner/planner.cpp.o
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
[ 41%] Building CXX object CMakeFiles/capture.dir/calibration/capture.cpp.o
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[2]: 进入目录“/home/liantian/projects/sp_vision_25/build”
[ 42%] Building CXX object CMakeFiles/calibrate_camera.dir/calibration/calibrate_camera.cpp.o
In file included from /usr/include/spdlog/spdlog.h:12,
                 from /home/liantian/projects/sp_vision_25/tools/logger.hpp:4,
                 from /home/liantian/projects/sp_vision_25/io/socketcan.hpp:16,
                 from /home/liantian/projects/sp_vision_25/io/cboard.hpp:12,
                 from /home/liantian/projects/sp_vision_25/calibration/capture.cpp:8:
/usr/include/spdlog/common.h:127:111: error: ‘basic_runtime’ is not a member of ‘fmt’
  127 |           std::is_convertible<T, fmt::basic_string_view<Char>>::value || std::is_same<remove_cvref_t<T>, fmt::basic_runtime<Char>>::value>
      |                                                                                                               ^~~~~~~~~~~~~
/usr/include/spdlog/common.h:127:125: error: template argument 2 is invalid
  127 |           std::is_convertible<T, fmt::basic_string_view<Char>>::value || std::is_same<remove_cvref_t<T>, fmt::basic_runtime<Char>>::value>
      |                                                                                                                             ^~~~
/usr/include/spdlog/common.h:127:138: error: expected ‘{’ before ‘>’ token
  127 |           std::is_convertible<T, fmt::basic_string_view<Char>>::value || std::is_same<remove_cvref_t<T>, fmt::basic_runtime<Char>>::value>
      |                                                                                                                                          ^
/home/liantian/projects/sp_vision_25/calibration/calibrate_camera.cpp: In function ‘void load(const string&, const string&, cv::Size&, std::vector<std::vector<cv::Point3_<float> > >&, std::vector<std::vector<cv::Point_<float> > >&)’:
/home/liantian/projects/sp_vision_25/calibration/calibrate_camera.cpp:39:26: error: ‘format’ is not a member of ‘fmt’; did you mean ‘cv::format’?
   39 |     auto img_path = fmt::format("{}/{}.jpg", input_folder, i);
      |                          ^~~~~~
In file included from /usr/include/opencv4/opencv2/core.hpp:3305,
                 from /usr/include/opencv4/opencv2/opencv.hpp:52,
                 from /home/liantian/projects/sp_vision_25/calibration/calibrate_camera.cpp:5:
/usr/include/opencv4/opencv2/core/operations.hpp:435:16: note: ‘cv::format’ declared here
  435 | Ptr<Formatted> format(InputArray mtx, Formatter::FormatType fmt)
      |                ^~~~~~
/home/liantian/projects/sp_vision_25/calibration/calibrate_camera.cpp: In function ‘void print_yaml(const cv::Mat&, const cv::Mat&, double)’:
/home/liantian/projects/sp_vision_25/calibration/calibrate_camera.cpp:76:32: error: ‘format’ is not a member of ‘fmt’; did you mean ‘cv::format’?
   76 |   result << YAML::Comment(fmt::format("重投影误差: {:.4f}px", error));
      |                                ^~~~~~
In file included from /usr/include/opencv4/opencv2/core.hpp:3305,
                 from /usr/include/opencv4/opencv2/opencv.hpp:52,
                 from /home/liantian/projects/sp_vision_25/calibration/calibrate_camera.cpp:5:
/usr/include/opencv4/opencv2/core/operations.hpp:435:16: note: ‘cv::format’ declared here
  435 | Ptr<Formatted> format(InputArray mtx, Formatter::FormatType fmt)
      |                ^~~~~~
/usr/include/spdlog/common.h: In instantiation of ‘struct spdlog::is_convertible_to_any_format_string<const char* const&>’:
/usr/include/spdlog/logger.h:106:96:   required by substitution of ‘template<class T, typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> > void spdlog::logger::log(spdlog::source_loc, spdlog::level::level_enum, const T&) [with T = const char*; typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> = <missing>]’
/usr/include/spdlog/logger.h:164:12:   required from ‘void spdlog::logger::warn(fmt::v12::format_string<T ...>, Args&& ...) [with Args = {const char*}; fmt::v12::format_string<T ...> = fmt::v12::fstring<const char*>]’
/home/liantian/projects/sp_vision_25/io/socketcan.hpp:116:32:   required from here
/usr/include/spdlog/common.h:137:123: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char* const&, char>’ used in nested name specifier
  137 | struct is_convertible_to_any_format_string : std::integral_constant<bool, is_convertible_to_basic_format_string<T, char>::value ||
      |                                                                                                                           ^~~~~
/usr/include/spdlog/common.h:138:130: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char* const&, wchar_t>’ used in nested name specifier
  138 |                                                                               is_convertible_to_basic_format_string<T, wchar_t>::value>
      |                                                                                                                                  ^~~~~
/usr/include/spdlog/common.h: In instantiation of ‘struct spdlog::is_convertible_to_any_format_string<const char (&)[22]>’:
/usr/include/spdlog/logger.h:106:96:   required by substitution of ‘template<class T, typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> > void spdlog::logger::log(spdlog::source_loc, spdlog::level::level_enum, const T&) [with T = char [22]; typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> = <missing>]’
/usr/include/spdlog/logger.h:95:12:   required from ‘void spdlog::logger::log(spdlog::level::level_enum, const T&) [with T = char [22]]’
/usr/include/spdlog/logger.h:244:12:   required from ‘void spdlog::logger::info(const T&) [with T = char [22]]’
/home/liantian/projects/sp_vision_25/io/socketcan.hpp:58:26:   required from here
/usr/include/spdlog/common.h:137:123: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[22], char>’ used in nested name specifier
  137 | struct is_convertible_to_any_format_string : std::integral_constant<bool, is_convertible_to_basic_format_string<T, char>::value ||
      |                                                                                                                           ^~~~~
/usr/include/spdlog/common.h:138:130: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[22], wchar_t>’ used in nested name specifier
  138 |                                                                               is_convertible_to_basic_format_string<T, wchar_t>::value>
      |                                                                                                                                  ^~~~~
/usr/include/spdlog/common.h: In instantiation of ‘struct spdlog::is_convertible_to_any_format_string<const char (&)[18]>’:
/usr/include/spdlog/logger.h:106:96:   required by substitution of ‘template<class T, typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> > void spdlog::logger::log(spdlog::source_loc, spdlog::level::level_enum, const T&) [with T = char [18]; typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> = <missing>]’
/usr/include/spdlog/logger.h:95:12:   required from ‘void spdlog::logger::log(spdlog::level::level_enum, const T&) [with T = char [18]]’
/usr/include/spdlog/logger.h:244:12:   required from ‘void spdlog::logger::info(const T&) [with T = char [18]]’
/home/liantian/projects/sp_vision_25/io/socketcan.hpp:123:26:   required from here
/usr/include/spdlog/common.h:137:123: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[18], char>’ used in nested name specifier
  137 | struct is_convertible_to_any_format_string : std::integral_constant<bool, is_convertible_to_basic_format_string<T, char>::value ||
      |                                                                                                                           ^~~~~
/usr/include/spdlog/common.h:138:130: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[18], wchar_t>’ used in nested name specifier
  138 |                                                                               is_convertible_to_basic_format_string<T, wchar_t>::value>
      |                                                                                                                                  ^~~~~
/usr/include/spdlog/common.h: In instantiation of ‘struct spdlog::is_convertible_to_any_format_string<const char (&)[34]>’:
/usr/include/spdlog/logger.h:106:96:   required by substitution of ‘template<class T, typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> > void spdlog::logger::log(spdlog::source_loc, spdlog::level::level_enum, const T&) [with T = char [34]; typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> = <missing>]’
/usr/include/spdlog/logger.h:95:12:   required from ‘void spdlog::logger::log(spdlog::level::level_enum, const T&) [with T = char [34]]’
/usr/include/spdlog/logger.h:244:12:   required from ‘void spdlog::logger::info(const T&) [with T = char [34]]’
/home/liantian/projects/sp_vision_25/calibration/capture.cpp:86:24:   required from here
/usr/include/spdlog/common.h:137:123: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[34], char>’ used in nested name specifier
  137 | struct is_convertible_to_any_format_string : std::integral_constant<bool, is_convertible_to_basic_format_string<T, char>::value ||
      |                                                                                                                           ^~~~~
/usr/include/spdlog/common.h:138:130: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[34], wchar_t>’ used in nested name specifier
  138 |                                                                               is_convertible_to_basic_format_string<T, wchar_t>::value>
      |                                                                                                                                  ^~~~~
/usr/include/spdlog/common.h: In instantiation of ‘struct spdlog::is_convertible_to_any_format_string<const char (&)[35]>’:
/usr/include/spdlog/logger.h:106:96:   required by substitution of ‘template<class T, typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> > void spdlog::logger::log(spdlog::source_loc, spdlog::level::level_enum, const T&) [with T = char [35]; typename std::enable_if<(! spdlog::is_convertible_to_any_format_string<const T&>::value), int>::type <anonymous> = <missing>]’
/usr/include/spdlog/logger.h:95:12:   required from ‘void spdlog::logger::log(spdlog::level::level_enum, const T&) [with T = char [35]]’
/usr/include/spdlog/logger.h:250:12:   required from ‘void spdlog::logger::warn(const T&) [with T = char [35]]’
/home/liantian/projects/sp_vision_25/calibration/capture.cpp:90:24:   required from here
/usr/include/spdlog/common.h:137:123: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[35], char>’ used in nested name specifier
  137 | struct is_convertible_to_any_format_string : std::integral_constant<bool, is_convertible_to_basic_format_string<T, char>::value ||
      |                                                                                                                           ^~~~~
/usr/include/spdlog/common.h:138:130: error: incomplete type ‘spdlog::is_convertible_to_basic_format_string<const char (&)[35], wchar_t>’ used in nested name specifier
  138 |                                                                               is_convertible_to_basic_format_string<T, wchar_t>::value>
      |                                                                                                                                  ^~~~~
make[2]: *** [CMakeFiles/calibrate_camera.dir/build.make:76：CMakeFiles/calibrate_camera.dir/calibration/calibrate_camera.cpp.o] 错误 1
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[1]: *** [CMakeFiles/Makefile2:576：CMakeFiles/calibrate_camera.dir/all] 错误 2
make[1]: *** 正在等待未完成的任务....
make[2]: *** [CMakeFiles/capture.dir/build.make:76：CMakeFiles/capture.dir/calibration/capture.cpp.o] 错误 1
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make[1]: *** [CMakeFiles/Makefile2:550：CMakeFiles/capture.dir/all] 错误 2
make[2]: 离开目录“/home/liantian/projects/sp_vision_25/build”
[ 42%] Built target auto_aim
make[1]: 离开目录“/home/liantian/projects/sp_vision_25/build”
make: *** [Makefile:101：all] 错误 2
make: 离开目录“/home/liantian/projects/sp_vision_25/build”
liantian@bing:~/projects/sp_vision_25$ 
