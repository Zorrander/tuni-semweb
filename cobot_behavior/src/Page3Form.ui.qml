import QtQuick 2.9
import QtQuick.Controls 2.2
import CobotKnowledge 1.0

Page {
    id: page
    width: 800
    height: 600

    title: qsTr("Skill Creator")

    Knowledge {
        id: knowledge
    }

    Connections {
        target: button
        onClicked: {
            print("clicked")
            knowledge.export_ontology(name_file.text)
        }
    }

    Label {
        id: label
        x: 316
        y: 37
        width: 169
        height: 23
        text: qsTr("Skill Creator")
        font.pointSize: 14
        horizontalAlignment: Text.AlignHCenter
    }

    TextField {
        id: name_file
        x: 233
        y: 517
        text: knowledge.filename
        placeholderText: "Enter a file name"
    }

    Button {
        id: button
        x: 450
        y: 500
        width: 144
        height: 73
        text: qsTr("Export")
    }

    Label {
        id: label1
        x: 44
        y: 123
        text: qsTr("Create complex task")
        font.family: "Ubuntu"
        font.pointSize: 12
    }

    TextField {
        id: textField1
        x: 44
        y: 163
        placeholderText: "Task name"
    }

    RoundButton {
        id: roundButton
        x: 86
        y: 231
        width: 66
        height: 69
        text: "+"
    }

    Row {
        id: row
        x: 292
        y: 163
        width: 279
        height: 287

        Label {
            id: label3
            text: qsTr("No method defined yet")
            horizontalAlignment: Text.AlignHCenter
            width: parent.width
            color: "#8f8f9f"
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.8999999761581421}
}
##^##*/

