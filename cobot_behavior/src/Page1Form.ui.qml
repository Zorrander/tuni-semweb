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
        text: qsTr("Commands")
        anchors.verticalCenterOffset: -162
        anchors.horizontalCenterOffset: 0
        anchors.centerIn: parent
    }

    Text {
        id: text1
        x: 288
        y: 160
        text: qsTr("Action:")
        font.pixelSize: 12
    }

    TextInput {
        id: action_input
        x: 361
        y: 206
        width: 80
        height: 20
        cursorVisible: true
        font.pixelSize: 12
    }

    Text {
        id: text2
        x: 288
        y: 209
        text: qsTr("Targets:")
        font.pixelSize: 12
    }

    Button {
        id: button
        x: 288
        y: 259
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
        x: 349
        y: 148
    }
}
