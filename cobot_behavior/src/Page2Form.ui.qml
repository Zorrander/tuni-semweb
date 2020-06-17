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
        target: routine_button
        onClicked: {
            print("close_gripper_button clicked")
            robot.routine()
        }
    }

    Button {
        id: open_gripper_button
        x: 393
        y: 172
        text: qsTr("Open")
    }

    Button {
        id: close_gripper_button
        x: 597
        y: 172
        text: qsTr("Grasp")
    }

    Button {
        id: button3
        x: 803
        y: 404
        text: qsTr("Execute controller")
    }

    Rectangle {
        id: rectangle
        x: 328
        y: 280
        width: 452
        height: 1
        color: "#000000"
    }

    Label {
        id: label
        x: 289
        y: 122
        text: qsTr("Gripper")
    }

    Label {
        id: label1
        x: 289
        y: 309
        text: qsTr("Arm")
    }

    Button {
        id: routine_button
        x: 524
        y: 607
        text: qsTr("Routine")
    }

    Button {
        id: save_button
        x: 538
        y: 344
        width: 124
        height: 40
        text: qsTr("Save (Joints)")
    }

    ComboBox {
        id: comboBox
        x: 803
        y: 344
    }

    Button {
        id: move_target_button
        x: 538
        y: 412
        width: 124
        height: 40
        text: qsTr("Move (Targets)")
    }

    ComboBox {
        id: target_list
        x: 214
        y: 412
        width: 200
        model: robot.targetlist
        height: 40
    }

    TextField {
        id: target_name_input
        x: 214
        y: 344
        text: qsTr("")
        placeholderText: "Enter joint configuration name..."
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.6600000262260437}
}
##^##*/

