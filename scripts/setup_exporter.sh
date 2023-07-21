# create node_exporter service template
node_exporter_service=$(cat <<EOF
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=mlx
Group=mlx
Restart=always
ExecStart=/usr/local/bin/node_exporter --web.listen-address=:42517

[Install]
WantedBy=multi-user.target
EOF
)

TEMP_DIR="/tmp/Node_Exporter"

# set up user to run the exporter
groupadd --system mlx
useradd -s /sbin/nologin --system -g mlx mlx

# download, extract and move node_exporter binary to the proper directory
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.0/node_exporter-1.6.0.linux-amd64.tar.gz -O /tmp/node_exporter.tar.gz

mkdir $TEMP_DIR
tar xvf /tmp/node_exporter.tar.gz -C $TEMP_DIR/
mv $TEMP_DIR/node_exporter*/node_exporter /usr/local/bin/

# set permissions
chown mlx:mlx/usr/local/bin/node_exporter
# set up the service
echo "$node_exporter_service" > /etc/systemd/system/node_exporter.service
rm -rf $TEMP_DIR/
# enable and start the service
systemctl daemon-reload
systemctl start node_exporter
systemctl enable node_exporter
# run "systemctl status node_exporter"
# to check the status of the service