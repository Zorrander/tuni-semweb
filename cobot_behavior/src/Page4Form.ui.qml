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
        text: qsTr("Testing benchmark")
        anchors.verticalCenterOffset: -162
        anchors.horizontalCenterOffset: 0
        anchors.centerIn: parent
    }

    Text {
        id: text2
        x: 130
        y: 355
        text: qsTr("Camera")
        font.pixelSize: 12
    }

    Button {
        id: button
        x: 250
        y: 342
        text: "Record"
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
        x: 378
        y: 342
    }

    RoundButton {
        id: roundButton
        x: 62
        y: 342
        text: ""
        autoExclusive: false
    }

    Column {
        id: column
        x: 62
        y: 66
        width: 516
        height: 232
        padding: 5
        spacing: 2

        Label {
            id: label
            text: qsTr("Label")
        }
    }
}

/*##^##
Designer {
    D{i:8;anchors_width:516;anchors_x:62;anchors_y:66}
}
##^##*/
