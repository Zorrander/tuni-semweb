import QtQuick 2.9
import QtQuick.Controls 2.2
import CobotCommand 1.0
import Robot 1.0

Page {
    id: page
    width: 1200
    height: 800
    property alias button: button

    title: qsTr("Page 1")

    Command {
        id: command
    }

    Robot {
        id: robot
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
        id: planbutton
        x: 457
        y: 274
        width: 114
        height: 109
        text: "Plan"
    }

    Connections {
        target: planbutton
        onClicked: {
            print("clicked")
            command.plan(actionlist.currentText, objectlist.currentText)
        }
    }

    Button {
        id: sendbutton
        x: 457
        y: 107
        width: 114
        height: 36
        text: "Send"
    }

    Connections {
        target: sendbutton
        onClicked: {
            print("clicked")
            command.send(nlpcommand.text)
        }
    }

    Rectangle {
        id: rectangle
        x: 31
        y: 231
        width: 540
        height: 1
        color: "#000000"
    }

    Label {
        text: qsTr("Dialog")
        anchors.horizontalCenterOffset: -1
        anchors.verticalCenterOffset: -164
        anchors.centerIn: parent
    }

    ComboBox {
        id: objectlist
        x: 231
        y: 337
        model: command.actionlist
    }

    ComboBox {
        id: actionlist
        x: 231
        y: 268
        model: command.objectlist
    }

    TextArea {
        id: nlpcommand
        x: 128
        y: 110
        width: 301
        height: 29
        text: qsTr("")
        placeholderText: "NLP command"
    }
}
