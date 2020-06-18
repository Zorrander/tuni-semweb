import QtQuick 2.9
import QtQuick.Controls 2.2
import Robot 1.0

Page {
    id: page
    width: 1200
    height: 800

    title: qsTr("Page 2")

    Robot {
        id: robot
    }

    Connections {
        target: save_button
        onClicked: {
            print("save_button clicked")
            robot.save(target_name_input.text)
        }
    }

    Connections {
        target: move_target_button
        onClicked: {
            print("move_target_button clicked")
            robot.move_target(target_list.currentText)
        }
    }

    Connections {
        target: open_gripper_button
        onClicked: {
            print("open_gripper_button clicked")
            robot.open_gripper()
        }
    }

    Connections {
        target: close_gripper_button
        onClicked: {
            print("close_gripper_button clicked")
            robot.close_gripper()
        }
    }

    Connections {
        target: grasp1_button
        onClicked: {
            print("close_gripper_button clicked")
            robot.grasp1()
        }
    }

    Connections {
        target: routine_button
        onClicked: {
            print("close_gripper_button clicked")
            robot.routine(command_input.text)
        }
    }

    Button {
        id: open_gripper_button
        x: 439
        y: 175
        text: qsTr("Open")
    }

    Button {
        id: close_gripper_button
        x: 570
        y: 175
        text: qsTr("Close")
    }

    Button {
        id: button3
        x: 849
        y: 407
        text: qsTr("Execute controller")
    }

    Rectangle {
        id: rectangle
        x: 374
        y: 283
        width: 452
        height: 1
        color: "#000000"
    }

    Label {
        id: label
        x: 335
        y: 151
        text: qsTr("Gripper")
    }

    Label {
        id: label1
        x: 335
        y: 312
        text: qsTr("Arm")
    }

    Button {
        id: routine_button
        x: 649
        y: 35
        text: qsTr("Send ")
    }

    Button {
        id: save_button
        x: 584
        y: 347
        width: 124
        height: 40
        text: qsTr("Save (Joints)")
    }

    ComboBox {
        id: comboBox
        x: 849
        y: 347
    }

    Button {
        id: move_target_button
        x: 584
        y: 415
        width: 124
        height: 40
        text: qsTr("Move (Targets)")
    }

    ComboBox {
        id: target_list
        x: 260
        y: 415
        width: 200
        model: robot.targetlist
        height: 40
    }

    TextField {
        id: target_name_input
        x: 260
        y: 347
        text: qsTr("")
        placeholderText: "Enter joint configuration name..."
    }

    TextField {
        id: command_input
        x: 424
        y: 35
        text: qsTr("")
        placeholderText: "Enter a command"
    }

    Button {
        id: grasp1_button
        x: 718
        y: 175
        text: qsTr("Grasp")
    }

    Label {
        id: label2
        x: 306
        y: 662
        text: qsTr("End effector")
    }

    Label {
        id: label3
        x: 306
        y: 533
        width: 58
        height: 26
        text: qsTr("Joints")
    }

    ComboBox {
        id: joints_list
        x: 306
        y: 576
        model: ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6", "joint_7"]
    }

    ComboBox {
        id: axis
        x: 306
        y: 713
        model: ["x", "y", "z"]
    }

    Slider {
        id: slider
        x: 537
        y: 576
        value: "0.5"
    }

    Slider {
        id: slider1
        x: 537
        y: 713
        value: 0.5
    }

    TextArea {
        id: joint_value_display
        x: 823
        y: 587
        text: qsTr("")
        placeholderText: "Current value"
    }

    TextArea {
        id: end_effector_pose_display
        x: 823
        y: 706
        text: qsTr("")
        placeholderText: "Current value"
    }
}
