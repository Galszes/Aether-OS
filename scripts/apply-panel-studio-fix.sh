#!/bin/sh
set -e

mkdir -p /opt/AetherPanelStudio
cp -r /etc/skel/Applications/AetherPanelStudio/* /opt/AetherPanelStudio/

cat <<'EOF' > /usr/local/bin/aether-panel-studio
#!/bin/sh
exec /usr/bin/python3 /opt/AetherPanelStudio/app.py "$@"
EOF
chmod +x /usr/local/bin/aether-panel-studio
cp /usr/local/bin/aether-panel-studio /etc/skel/.local/bin/aether-panel-studio

for f in \
  /etc/skel/.local/share/plasma_icons/aether-panel-studio*.desktop \
  /etc/skel/.local/share/applications/aether-panel-studio*.desktop \
  /usr/local/share/applications/aether-panel-studio*.desktop
do
  [ -f "$f" ] || continue
  sed -i 's|^Exec=.*|Exec=/usr/local/bin/aether-panel-studio|' "$f"
  chmod 755 "$f"
  chown root:root "$f"
done
