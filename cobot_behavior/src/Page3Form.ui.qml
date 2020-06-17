import QtQuick 2.9
import QtQuick.Controls 2.2
import CobotKnowledge 1.0
import Tasks 1.0

Page {
    id: page
    width: 800
    height: 600

    title: qsTr("Skill Creator")

    Knowledge {
        id: knowledge
    }

    Tasks {
        id: tasks
    }

    Connections {
        target: button
        onClicked: {
            print("clicked")
            knowledge.export_ontology(name_file.text)
        }
    }

    Connections {
        target: listTasks
        onCurrentIndexChanged: {
            infoBox.open()
            tasks.fetch(listTasks.currentItem.myData.description)
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
        x: 336
        y: 518
        text: knowledge.filename
        placeholderText: "Enter a file name"
    }

    Button {
        id: button
        x: 573
        y: 501
        width: 178
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
        x: 403
        y: 352
        width: 66
        height: 69
        text: "+"
    }

    Row {
        id: row
        x: 296
        y: 163
        width: 279
        height: 183

        Label {
            id: label3
            text: qsTr("No method defined yet")
            horizontalAlignment: Text.AlignHCenter
            width: parent.width
            color: "#8f8f9f"
        }
    }

    Label {
        id: label2
        x: 45
        y: 233
        text: qsTr("Existing tasks")
        font.pointSize: 12
        font.family: "Ubuntu"
    }

    ListView {
        id: listTasks
        x: 45
        y: 271
        width: 199
        height: 287
        model: Tasks {
            list: tasksList
        }
        delegate: Row {
            property variant myData: model
            width: parent.width
            height: 40
            TextField {
                text: model.description
            }

            MouseArea {
                anchors.fill: parent
                onClicked: listTasks.currentIndex = index
            }
        }
    }

    Dialog {
        id: infoBox
        Text {
            id: infotest
            text: qsTr("Test")
        }
    }
}
