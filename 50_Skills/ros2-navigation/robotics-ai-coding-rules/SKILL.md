---
name: robotics-ai-coding-rules
description: AI programming collaboration rules for robotics, robot vision, machine vision, and electrical control projects. Use before changing code in projects involving 机器人, 机器人视觉, 机器视觉, 电控, 上位机, 下位机, ROS, ROS2, OpenCV, camera calibration, hand-eye calibration, 相机标定, 手眼标定, coordinate transforms, TF, pose estimation, YOLO, AprilTag, ArUco, depth camera, RGB-D, RealSense, point cloud, visual servoing, SLAM, Nav2, STM32, MCU, FreeRTOS, micro-ROS, motor control, PID, PWM, encoder, servo, stepper motor, DC motor, BLDC, CAN, CANopen, UART, serial, RS485, Modbus, EtherCAT, GPIO, ADC, interrupt, DMA, watchdog, emergency stop, 急停, limit switch, 限位开关, IMU, sensor fusion, or HIL.
---

# Robotics AI Coding Rules

## Highest Priority

Before editing code, restate the user's request and wait for explicit confirmation. Do not modify code, config, tests, or project files until the user confirms the plan.

For every programming request:

1. Restate what the user wants.
2. State the expected behavior after the change.
3. State what must remain unchanged.
4. Describe the implementation plan.
5. Show the planned file or module structure.
6. Wait for the user's confirmation.

If the user only asks a question, do not propose file edits as if they were already approved.

## Plan Format

For a new or empty project, show the planned high-level blocks:

```text
project/
├── perception/      # camera input, detection, calibration, frame transforms
├── control/         # control loops, actuator commands, safety limits
├── communication/   # CAN, UART, RS485, Modbus, EtherCAT, ROS topics/services
├── config/          # hardware parameters, calibration, frame names, limits
└── tests/           # simulation, unit tests, hardware-free checks
```

For an existing project, show only the affected structure and label each file:

```text
src/
├── vision/
│   └── detector.cpp      # modify target filtering logic
├── control/
│   └── motor_loop.cpp    # read to verify command path, no planned change
└── tests/
    └── detector_test.cpp # add regression coverage
```

Also include:

- New or changed functionality.
- Existing functionality that must stay the same.
- Modules that may be affected.
- Verification steps to run before final response.

## No Unrequested Cleverness

Do not add unrequested features, UI changes, dependencies, abstractions, protocol changes, calibration shortcuts, automatic tuning, or hardware assumptions.

If an extra change is necessary, explain before editing:

- Why it is necessary.
- What breaks without it.
- Whether it is unusual or partly against normal practice.
- Whether it changes existing behavior.

Wait for confirmation before adding it.

## Common Sense Violations

If the user's instruction violates engineering common sense, robotics safety, electrical safety, data integrity, or basic security practice, warn twice before proceeding.

Use this pattern:

```text
This request is risky because ...

I need to emphasize again: ... Please explicitly confirm whether to continue.
```

Examples requiring double warning:

- Disabling emergency stop, watchdogs, current limits, or limit switches.
- Ignoring coordinate frames, units, timestamps, calibration, or actuator limits.
- Hardcoding motor directions, gear ratios, CAN IDs, serial baud rates, pin maps, or camera intrinsics without evidence.
- Changing control-loop timing or PID behavior without checking downstream effects.
- Sending actuator commands without simulation, dry-run, or hardware-safe guards.

## Read Before Editing

Before changing code, inspect the program enough to protect existing behavior.

- For small projects, read the whole program.
- For large projects, scan the full tree and read all affected modules, entry points, config files, interfaces, tests, and call chains.
- Prefer `rg` and `rg --files` for discovery.
- Identify existing architecture, naming, style, and toolchain before proposing changes.
- Do not claim full understanding if only part of the system was inspected.

If the impact cannot be bounded, state the uncertainty and ask before editing.

## Robotics Domain Checks

For robot vision, perception, control, and electrical-control changes, explicitly check the relevant items:

- Camera pipeline, exposure assumptions, image format, resolution, distortion model, intrinsics, extrinsics, hand-eye calibration, and timestamp sync.
- Coordinate frames, frame names, units, handedness, axis conventions, TF tree, base/link/camera/tool frames, and pose representation.
- Detection thresholds, target classes, filtering, tracking, latency, lost-target behavior, and false-positive handling.
- Control-loop frequency, PID gains, saturation, deadband, acceleration limits, velocity limits, current limits, and fail-safe states.
- Motor type, encoder feedback, gear ratio, zero position, homing, limit switches, emergency stop, watchdog, and command timeout.
- Communication protocol, baud rate, CAN ID, node ID, register map, byte order, CRC, retry behavior, and disconnect handling.
- Simulation, log replay, hardware-free tests, or HIL checks before hardware-affecting changes when possible.

Do not invent missing hardware facts. Inspect configs, docs, code, logs, launch files, URDF/Xacro, calibration files, firmware headers, or ask the user.

## Verification

After edits, verify with the smallest meaningful checks available:

- Build or typecheck.
- Unit tests or targeted regression tests.
- Simulation, log replay, or dry-run for robotics behavior.
- Static checks or formatting if already used by the project.

If hardware behavior is affected and hardware cannot be tested, say so clearly and list the remaining hardware validation steps.

## Final Response

Keep the final response concise and include:

- Files changed.
- What changed.
- How the new behavior works.
- What existing behavior was preserved.
- Tests or checks run.
- Any remaining risk, especially hardware, calibration, timing, or safety risk.
