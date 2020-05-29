import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    width: 600
    height: 400

    title: qsTr("Home")

    Image {
        id: image
        x: 211
        y: 175
        width: 178
        height: 176
        fillMode: Image.PreserveAspectFit
        source: "3Y8m5XDn_400x400.jpg"
    }

    Label {
        id: label
        x: 198
        y: 80
        text: qsTr("Collaborative Robotics")
        font.pointSize: 15
    }
}
