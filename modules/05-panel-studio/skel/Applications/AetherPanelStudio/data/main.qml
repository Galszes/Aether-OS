import QtQuick 2.15
import QtQuick.Window 2.15
import QtGraphicalEffects 1.15
import QtQuick.Layouts 1.1
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.plasmoid 2.0

Item {
    id: main
    property var containmentInterface: null
    property var panelLayout: null
    property var islands: []
    property var previousBackground: null
    // The SVG highlights have a 10px radius and a 2px transparent inset.
    readonly property int innerRadius: 10
    readonly property int highlightInset: 2
    readonly property int contentMargin: Math.max(highlightInset, plasmoid.configuration.contentMargin)
    readonly property int layoutInset: contentMargin - highlightInset
    property bool layoutInsetApplied: false
    property var paddedContainers: []
    Plasmoid.preferredRepresentation: Plasmoid.fullRepresentation
    // Keep the representation loaded at login, even outside panel edit mode.
    // A subpixel width avoids Plasma's fallback to an icon-sized container.
    Plasmoid.status: PlasmaCore.Types.ActiveStatus
    Layout.minimumWidth: Plasmoid.editMode ? 28 : 0.01
    Layout.preferredWidth: Plasmoid.editMode ? 28 : 0.01
    Layout.maximumWidth: Plasmoid.editMode ? 28 : 0.01

    PlasmaCore.IconItem {
        anchors.fill: parent
        source: "preferences-desktop-theme"
        visible: Plasmoid.editMode
    }

    Component {
        id: backgroundComponent
        Rectangle {
            z: -1
            property color backgroundTint: plasmoid.configuration.backgroundColor
            color: Qt.rgba(backgroundTint.r,
                           backgroundTint.g,
                           backgroundTint.b,
                           plasmoid.configuration.backgroundOpacity)
            radius: Math.min(plasmoid.configuration.cornerRadius, height / 2)
            border.width: 1
            property color edgeTint: plasmoid.configuration.borderColor
            border.color: Qt.rgba(edgeTint.r, edgeTint.g, edgeTint.b, plasmoid.configuration.borderOpacity)
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: Qt.rgba(Math.min(1, backgroundTint.r + plasmoid.configuration.glassGradient * 0.4),
                                   Math.min(1, backgroundTint.g + plasmoid.configuration.glassGradient * 0.7),
                                   Math.min(1, backgroundTint.b + plasmoid.configuration.glassGradient),
                                   Math.min(1, plasmoid.configuration.backgroundOpacity + plasmoid.configuration.glassGradient))
                }
                GradientStop {
                    position: 0.5
                    color: Qt.rgba(backgroundTint.r, backgroundTint.g, backgroundTint.b,
                                   plasmoid.configuration.backgroundOpacity)
                }
                GradientStop {
                    position: 1
                    color: Qt.rgba(backgroundTint.r, backgroundTint.g, backgroundTint.b,
                                   Math.max(0, plasmoid.configuration.backgroundOpacity - plasmoid.configuration.glassGradient * 0.6))
                }
            }
            layer.enabled: true
            layer.effect: DropShadow {
                horizontalOffset: 0
                verticalOffset: plasmoid.configuration.shadowOffset
                radius: plasmoid.configuration.shadowBlur
                samples: 65
                property color shadowTint: plasmoid.configuration.shadowColor
                color: Qt.rgba(shadowTint.r, shadowTint.g, shadowTint.b, plasmoid.configuration.shadowOpacity)
                transparentBorder: true
            }
        }
    }

    property string lastBlurGeometry: ""
    property int blurRefresh: 0
    PlasmaCore.DataSource {
        id: blurCommand
        engine: "executable"
        connectedSources: []
        onNewData: disconnectSource(sourceName)
    }
    function updateBlur() {
        if (!main.Window.window || islands.length !== 2) return;
        var boxes = [];
        for (var i = 0; i < islands.length; i++) {
            var rect = islands[i];
            if (!rect.visible) continue;
            var point = rect.mapToItem(null, 0, 0);
            boxes.push([point.x, point.y, rect.width, rect.height, rect.radius]);
        }
        var geometry = JSON.stringify([main.Window.window.width, main.Window.window.height, boxes]);
        blurRefresh++;
        if (geometry === lastBlurGeometry && blurRefresh < 30) return;
        lastBlurGeometry = geometry;
        blurRefresh = 0;
        blurCommand.connectSource("/usr/bin/python3 /home/aether/Applications/AetherPanelStudio/panel_blur.py '" + geometry + "'");
    }

    function discover() {
        var item = main.parent;
        while (item) {
            if (!panelLayout && item instanceof GridLayout)
                panelLayout = item;
            if (!containmentInterface && item.toString().indexOf("ContainmentInterface") === 0)
                containmentInterface = item;
            item = item.parent;
        }
        if (containmentInterface && previousBackground === null) {
            previousBackground = containmentInterface.backgroundHints;
            containmentInterface.backgroundHints = PlasmaCore.Types.NoBackground;
        }
        if (panelLayout && islands.length === 0) {
            // Inset the complete content layout; do not shrink or paint spacers.
            // Binding keeps this correct when panel height or screen size changes.
            panelLayout.x = Qt.binding(function() {
                return main.layoutInset + (Qt.application.layoutDirection === Qt.RightToLeft ? main.panelLayout.toolBoxSize : 0);
            });
            panelLayout.y = 0;
            panelLayout.width = Qt.binding(function() {
                return Math.max(0, main.panelLayout.parent.width - main.panelLayout.toolBoxSize - 2 * main.layoutInset);
            });
            panelLayout.height = Qt.binding(function() {
                return main.panelLayout.parent.height;
            });
            layoutInsetApplied = true;
            islands = [backgroundComponent.createObject(panelLayout.parent),
                       backgroundComponent.createObject(panelLayout.parent)];
        }
    }

    function updateBackgrounds() {
        if (!panelLayout || !containmentInterface) discover();
        if (!panelLayout || islands.length !== 2) return;
        var groups = [[], []];
        for (var i = 0; i < panelLayout.children.length; i++) {
            var child = panelLayout.children[i];
            if (!child.applet || !child.visible || child.width <= 0) continue;
            var name = child.applet.pluginName;
            if (name !== "org.kde.plasma.panelspacer" &&
                name !== "org.aether.panelislands" &&
                name !== "luisbocanegra.panel.colorizer" &&
                paddedContainers.indexOf(child) === -1) {
                addVerticalPadding(child);
            }
            if (name === "org.kde.plasma.kickoff" || name === "org.kde.plasma.icontasks" ||
                name === "org.kde.plasma.taskmanager" || name === "org.kde.plasma.marginsseparator")
                groups[0].push(child);
            if (name === "org.kde.plasma.systemtray" || name === "org.kde.plasma.digitalclock" ||
                name === "org.kde.plasma.showdesktop")
                groups[1].push(child);
        }
        if (!plasmoid.configuration.splitPanel) {
            islands[0].visible = true;
            islands[0].x = 0;
            islands[0].y = 0;
            islands[0].width = panelLayout.parent.width;
            islands[0].height = panelLayout.parent.height;
            islands[1].visible = false;
            return;
        }
        for (var g = 0; g < groups.length; g++) {
            var rect = islands[g];
            rect.visible = groups[g].length > 0;
            if (!rect.visible) continue;
            var left = Infinity, right = -Infinity;
            for (var j = 0; j < groups[g].length; j++) {
                var target = groups[g][j];
                var point = target.mapToItem(panelLayout.parent, 0, 0);
                left = Math.min(left, point.x);
                right = Math.max(right, point.x + target.width);
            }
            var origin = panelLayout.mapToItem(panelLayout.parent, 0, 0);
            rect.x = Math.max(0, left - layoutInset);
            rect.y = origin.y;
            rect.width = Math.min(panelLayout.parent.width - rect.x, right + layoutInset - rect.x);
            rect.height = panelLayout.height;
        }
    }

    function addVerticalPadding(container) {
        // Plasma derives each container's minimum height from the panel height
        // minus these attached margins. Shrinking GridLayout alone overflows.
        container.Layout.topMargin = Qt.binding(function() {
            return container.getMargins("top") + main.layoutInset;
        });
        container.Layout.bottomMargin = Qt.binding(function() {
            return container.getMargins("bottom") + main.layoutInset;
        });
        paddedContainers.push(container);
    }

    Timer {
        interval: 300
        running: true
        repeat: true
        onTriggered: { main.updateBackgrounds(); main.updateBlur(); }
    }
    Component.onDestruction: {
        for (var i = 0; i < islands.length; i++) islands[i].destroy();
        for (var j = 0; j < paddedContainers.length; j++) restoreVerticalPadding(paddedContainers[j]);
        if (panelLayout && layoutInsetApplied) {
            var layout = panelLayout;
            layout.x = Qt.binding(function() {
                return Qt.application.layoutDirection === Qt.RightToLeft ? layout.toolBoxSize : 0;
            });
            layout.y = 0;
            layout.width = Qt.binding(function() { return layout.parent.width - layout.toolBoxSize; });
            layout.height = Qt.binding(function() { return layout.parent.height; });
        }
        if (containmentInterface && previousBackground !== null)
            containmentInterface.backgroundHints = previousBackground;
    }

    function restoreVerticalPadding(container) {
        if (!container) return;
        container.Layout.topMargin = Qt.binding(function() { return container.getMargins("top"); });
        container.Layout.bottomMargin = Qt.binding(function() { return container.getMargins("bottom"); });
    }
}
