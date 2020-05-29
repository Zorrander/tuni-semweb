import QtQuick 2.9
import QtQuick.Controls 2.2
import CobotCommand 1.0

Page {
    id: page
    width: 600
    height: 400
    property alias button: button

    title: qsTr("Page 1")

    Command {
        id: command
    }

    Label {
        text: qsTr("Send commands")
        anchors.verticalCenterOffset: 61
        anchors.horizontalCenterOffset: -220
        anchors.centerIn: parent
    }

    Text {
        id: text1
        x: 168
        y: 286
        text: qsTr("Action:")
        font.pixelSize: 12
    }

    Text {
        id: text2
        x: 165
        y: 356
        text: qsTr("Targets:")
        font.pixelSize: 12
    }

    Button {
        id: button
        x: 457
        y: 274
        width: 114
        height: 109
        text: "Send"
    }

    Connections {
        target: button
        onClicked: {
            print("clicked")
            command.send(action_box.text, target_box.text)
        }
    }

    TextField {
        id: action_box
        text: command.action
        placeholderText: qsTr("Action")
        onTextChanged: command.action = text
        x: 220
        y: 274
    }

    TextField {
        id: target_box
        x: 220
        y: 343
        text: command.targets
        onTextChanged: command.targets = text
        placeholderText: qsTr("Targets")
    }

    Rectangle {
        id: rectangle
        x: 31
        y: 231
        width: 540
        height: 1
        color: "#000000"
    }

    TextField {
        id: dialog_box
        x: 31
        y: 63
        width: 535
        height: 130
    }

    Label {
        text: qsTr("Dialog")
        anchors.horizontalCenterOffset: -1
        anchors.verticalCenterOffset: -164
        anchors.centerIn: parent
    }
}
