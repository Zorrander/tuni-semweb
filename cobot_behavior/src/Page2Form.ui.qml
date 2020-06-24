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
        target: grasp1_button
        onClicked: {
            print("grasp1_button clicked")
            robot.grasp1()
        }
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
        target: load_targets_button
        onClicked: {
            print("load_targets_button clicked")
            robot.load_targets()
        }
    }

    Connections {
        onClicked: {
            print("close_gripper_button clicked")
            robot.routine(command_input.text, objectList.currentText)
        }
    }

    Button {
        id: open_gripper_button
        x: 429
        y: 176
        text: qsTr("Open")
    }

    Button {
        id: close_gripper_button
        x: 560
        y: 176
        text: qsTr("Close")
    }

    Rectangle {
        id: rectangle
        x: 374
        y: 355
        width: 452
        height: 1
        color: "#000000"
    }

    Label {
        id: label
        x: 325
        y: 152
        text: qsTr("Gripper")
    }

    Label {
        id: label1
        x: 335
        y: 384
        text: qsTr("Arm")
    }

    Button {
        id: save_button
        x: 746
        y: 432
        width: 124
        height: 40
        text: qsTr("Save (Joints)")
    }

    Button {
        id: move_target_button
        x: 746
        y: 500
        width: 124
        height: 40
        text: qsTr("Move (Targets)")
    }

    ComboBox {
        id: target_list
        x: 500
        y: 500
        width: 200
        model: robot.targetlist
        height: 40
    }

    TextField {
        id: target_name_input
        x: 500
        y: 432
        text: qsTr("")
        placeholderText: "Enter joint configuration name..."
    }

    Button {
        id: grasp1_button
        x: 708
        y: 176
        text: qsTr("Grasp")
    }

    Button {
        id: load_targets_button
        x: 352
        y: 432
        width: 124
        height: 108
        text: qsTr("Load targets")
    }


    /*

    Slider {
        id: slider
        x: 537
        y: 576
        value: 0.5
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
    }*/
}
