import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    id: page
    width: 600
    height: 400

    title: qsTr("Page 2")

    Button {
        id: button
        x: 139
        y: 92
        text: qsTr("Open")
    }

    Button {
        id: button1
        x: 343
        y: 92
        text: qsTr("Grasp")
    }

    Button {
        id: button2
        x: 226
        y: 264
        width: 130
        height: 40
        text: qsTr("Move (Joints)")
    }

    Button {
        id: button3
        x: 395
        y: 324
        text: qsTr("Execute controller")
    }

    Rectangle {
        id: rectangle
        x: 74
        y: 200
        width: 452
        height: 1
        color: "#000000"
    }

    Label {
        id: label
        x: 35
        y: 42
        text: qsTr("Gripper")
    }

    Label {
        id: label1
        x: 35
        y: 229
        text: qsTr("Arm")
    }

    Button {
        id: button4
        x: 226
        y: 324
        text: qsTr("Move (Cartesian)")
    }

    Button {
        id: button5
        x: 67
        y: 264
        width: 124
        height: 40
        text: qsTr("Save (Joints)")
    }

    ComboBox {
        id: comboBox
        x: 395
        y: 264
    }

    Button {
        id: button6
        x: 67
        y: 324
        text: qsTr("Save (Cartesian)")
    }
}
