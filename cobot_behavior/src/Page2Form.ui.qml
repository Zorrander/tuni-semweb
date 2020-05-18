import QtQuick 2.9
import QtCanvas3D 1.1
import QtQuick.Controls 2.2

import "interaction.js" as GLCode

Item {
    id: mainview
    width: 1280
    height: 768
    visible: true

    Canvas3D {
        id: canvas3d
        anchors.fill: parent

        onInitializeGL: {
            GLCode.initializeGL(canvas3d)
        }

        onPaintGL: {
            GLCode.paintGL(canvas3d)
        }

        onResizeGL: {
            GLCode.resizeGL(canvas3d)
        }
    }
}
