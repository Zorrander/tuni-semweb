import QtQuick 2.9
import QtQuick.Controls 2.2
import CobotCommand 1.0

Page {
    id: page
    width: 600
    height: 400

    title: qsTr("Page 1")

    Command {
        id: command
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

    Connections {
        target: button
        onClicked: {
            print("clicked")
            command.send(textField.text)
        }
    }

    Label {
        id: label
        x: 253
        y: 24
        width: 80
        height: 23
        text: qsTr("Skill Creator")
    }

    Rectangle {
        id: rectangle
        x: 0
        y: 285
        width: 600
        height: 115
        color: "#ffffff"
        border.width: 1

        Grid {
            id: skill_grid
            x: 0
            y: 0
            width: 600
            height: 115
            spacing: 10
        }
    }
}
