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
            command.send(textField.text)
        }
    }

    TextField {
        id: textField
        text: command.action
        placeholderText: qsTr("Action")
        onTextChanged: command.action = text
        x: 220
        y: 274
    }

    TextField {
        id: textField1
        x: 220
        y: 343
        text: "#command.action#"
        placeholderText: qsTr("Action")
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
        id: textField2
        x: 31
        y: 63
        width: 535
        height: 130
        text: command.action
        placeholderText: qsTr("Action")
    }

    Label {
        text: qsTr("Dialog")
        anchors.horizontalCenterOffset: -1
        anchors.verticalCenterOffset: -164
        anchors.centerIn: parent
    }
}
