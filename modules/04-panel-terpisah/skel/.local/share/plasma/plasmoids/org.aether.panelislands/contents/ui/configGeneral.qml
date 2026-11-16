import QtQuick 2.15
import QtQuick.Controls 2.15 as Controls
import QtQuick.Layouts 1.1
import org.kde.kirigami 2.10 as Kirigami

Kirigami.FormLayout {
    property alias cfg_backgroundColor: colorField.text
    property alias cfg_backgroundOpacity: opacitySlider.value
    property alias cfg_contentMargin: marginField.value

    RowLayout {
        Kirigami.FormData.label: "Background color:"
        Controls.TextField {
            id: colorField
            placeholderText: "#181818"
            validator: RegExpValidator { regExp: /^#[0-9a-fA-F]{6}$/ }
            selectByMouse: true
        }
        Rectangle {
            width: 30
            height: 30
            radius: 6
            color: colorField.acceptableInput ? colorField.text : "#181818"
            border.color: "#808080"
        }
    }
    Controls.Label {
        text: "Neutral charcoal: #181818 · Black: #000000 · Warm gray: #282420"
        wrapMode: Text.WordWrap
        Layout.maximumWidth: 440
    }
    RowLayout {
        Kirigami.FormData.label: "Background opacity:"
        Controls.Slider {
            id: opacitySlider
            from: 0
            to: 1
            stepSize: 0.05
        }
        Controls.Label { text: Math.round(opacitySlider.value * 100) + "%" }
    }
    Controls.SpinBox {
        id: marginField
        Kirigami.FormData.label: "Highlight margin (px):"
        from: 2
        to: 12
    }
    Controls.Label {
        text: "Outer radius: " + (10 + marginField.value) + " px = inner radius 10 px + margin " + marginField.value + " px."
        wrapMode: Text.WordWrap
        Layout.maximumWidth: 440
    }
    Controls.Label {
        text: "Spacers stay clear. Increase panel height if you need more room for the icons."
        wrapMode: Text.WordWrap
        Layout.maximumWidth: 440
    }
}
